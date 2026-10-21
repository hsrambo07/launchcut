"""Recording and image sources. Frames come out graded (style.grade) as BGR uint8, with a half-res copy for zoomed-out shots."""
import json, subprocess
import numpy as np
import cv2


def ffprobe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    info = {"duration": float(j["format"].get("duration", 0)), "has_audio": a is not None}
    if v:
        cs = v.get("color_space", "unknown")
        # untagged HD is almost always BT.709; untagged SD is BT.601. Never let the decoder guess.
        info["matrix"] = "bt709" if cs == "bt709" or (cs in ("unknown", "", None) and int(v.get("height", 0)) >= 720) else \
                         ("bt601" if cs in ("smpte170m", "bt470bg", "unknown", "", None) else cs)
        info["range"] = "pc" if v.get("color_range") == "pc" else "tv"
    if v:
        num, den = (v.get("r_frame_rate") or "0/1").split("/")
        info.update(width=int(v["width"]), height=int(v["height"]), codec=v.get("codec_name"),
                    fps=float(num) / float(den or 1), nb_frames=int(v.get("nb_frames") or 0))
        # screen recordings drop frames when nothing moves: average rate well under nominal means VFR
        info["vfr"] = bool(info["nb_frames"] and info["duration"] and info["nb_frames"] / info["duration"] < info["fps"] * 0.97)
    return info


def grade_lut(g):
    x = np.arange(256, dtype=np.float32)
    return np.clip((x - g.get("black", 0)) * g.get("gain", 1.0) + g.get("out_black", 0), 0, 255).astype(np.uint8)


class VideoSource:
    """Streams frames forward from a start time. Requests must be non-decreasing; going back restarts the decoder."""

    def __init__(self, path, lut, fps=60):
        self.path, self.lut, self.fps = path, lut, fps
        info = ffprobe(path)
        self.w, self.h, self.duration = info["width"], info["height"], info["duration"]
        self.vf = (f"fps={fps},scale=in_color_matrix={info.get('matrix', 'bt709')}:in_range={info.get('range', 'tv')}"
                   ":flags=accurate_rnd+full_chroma_int")
        self.proc = None
        self.start = None
        self.idx = -1
        self.frame = self.half = None

    def _open(self, start):
        self.close()
        start = max(0.0, start)
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.4f}", "-i", self.path, "-vf", self.vf,   # fps: VFR to CFR; explicit matrix
               "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=self.w * self.h * 3)
        self.start, self.idx, self.frame, self.half = start, -1, None, None

    def get(self, ts):
        ts = min(max(0.0, ts), max(0.0, self.duration - 1.0 / self.fps))
        if self.proc is None or ts < self.start - 1e-6 or ts > self.start + (self.idx + 1) / self.fps + 2.0:
            self._open(ts)
        k = max(0, int(round((ts - self.start) * self.fps)))
        n = self.w * self.h * 3
        while self.idx < k:
            buf = self.proc.stdout.read(n)
            if len(buf) < n:
                break
            self.frame = cv2.LUT(np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3), self.lut)
            self.half = None
            self.idx += 1
        if self.frame is None:
            raise RuntimeError(f"{self.path}: no frame at {ts:.3f}s")
        if self.half is None:
            self.half = cv2.resize(self.frame, (self.w // 2, self.h // 2), interpolation=cv2.INTER_AREA)
        return self.frame, self.half

    def close(self):
        if self.proc:
            self.proc.kill()
            self.proc.wait()
            self.proc = None


class ImageSource:
    """A still (screenshot, slide, diagram) treated as a recording that never changes."""

    def __init__(self, path, lut):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(path)
        self.frame = cv2.LUT(img, lut)
        self.h, self.w = self.frame.shape[:2]
        self.half = cv2.resize(self.frame, (self.w // 2, self.h // 2), interpolation=cv2.INTER_AREA)
        self.duration = 1e9

    def get(self, ts):
        return self.frame, self.half

    def close(self):
        pass


IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff")


def open_source(path, lut, fps):
    if path.lower().endswith(IMAGE_EXT):
        return ImageSource(path, lut)
    return VideoSource(path, lut, fps)


def source_size(path):
    if path.lower().endswith(IMAGE_EXT):
        img = cv2.imread(path)
        return img.shape[1], img.shape[0]
    info = ffprobe(path)
    return info["width"], info["height"]
