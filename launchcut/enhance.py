"""Upscale low-res sources once, before the camera, so camera moves only ever downsample a sharp master.

Default method "sharp" is deterministic: Catmull-Rom 2x (ffmpeg bicubic B=0 C=0.5, accurate rounding, full chroma) plus a
luma-only unsharp mask (3x3, 0.7). It cannot invent glyphs and measured within 0.2 dB of every learned upscaler on
lossy 360p sources (docs/research/prior-art.md). Method "esrgan" (Real-ESRGAN animevideov3 with detail transfer) is
opt-in and guarded: a frame is only accepted if downscaling it back stays within 38 dB PSNR of the source frame,
otherwise that frame falls back to "sharp". GAN models are known to rewrite letters, hence the guard.
The cache is keyed on file, size, mtime and settings; coordinates in cut.yaml stay in original source pixels."""
import hashlib, json, os, platform, shutil, subprocess, tempfile, zipfile
import numpy as np
import cv2

CACHE = os.path.expanduser("~/.cache/launchcut")
SR_DIR = os.path.join(CACHE, "realesrgan")
RELEASE = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-{os}.zip"


def binary():
    env = os.environ.get("LAUNCHCUT_REALESRGAN")
    if env and os.path.isfile(env):
        return env
    for root, _, files in os.walk(SR_DIR):
        if "realesrgan-ncnn-vulkan" in files:
            return os.path.join(root, "realesrgan-ncnn-vulkan")
    return None


def setup():
    """download the Real-ESRGAN ncnn release for this OS into ~/.cache/launchcut/realesrgan"""
    if binary():
        return binary()
    osname = {"Darwin": "macos", "Linux": "ubuntu", "Windows": "windows"}[platform.system()]
    os.makedirs(SR_DIR, exist_ok=True)
    z = os.path.join(SR_DIR, "realesrgan.zip")
    subprocess.run(["curl", "-sL", "-o", z, RELEASE.format(os=osname)], check=True)
    with zipfile.ZipFile(z) as f:
        f.extractall(os.path.join(SR_DIR, "bin"))
    b = binary()
    os.chmod(b, 0o755)
    if platform.system() == "Darwin":
        subprocess.run(["xattr", "-d", "com.apple.quarantine", b], capture_output=True)
    return b


def cache_path(src, scale, model, sigma, method="sharp"):
    st = os.stat(src)
    key = hashlib.sha1(f"{os.path.abspath(src)}|{st.st_size}|{st.st_mtime}|{scale}|{model}|{sigma}|{method}".encode()).hexdigest()[:12]
    return os.path.join(CACHE, "enhanced", f"{os.path.splitext(os.path.basename(src))[0]}.{method}x{scale}.{key}.mkv")


SHARP_VF = "scale=iw*{s}:ih*{s}:flags=bicubic+accurate_rnd+full_chroma_int:param0=0:param1=0.5,unsharp=3:3:0.7:3:3:0"


def sharp(src, scale, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", SHARP_VF.format(s=scale), "-c:v", "ffv1", "-level", "3",
                    "-pix_fmt", "yuv444p", "-c:a", "copy", out], check=True)
    return out


def enhance(src, scale=2, model="realesr-animevideov3", sigma=1.2, out=None, log=print, method="sharp"):
    """upscale every frame of src by `scale` and return the path of the cached result"""
    out = out or cache_path(src, scale, model, sigma, method)
    if os.path.exists(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if method == "sharp":
        log(f"[enhance] Catmull-Rom x{scale} + luma unsharp: {os.path.basename(src)}")
        return sharp(src, scale, out)
    b = binary() or setup()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", src],
                                     capture_output=True, text=True, check=True).stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rate = v.get("r_frame_rate", "30/1")
    tmp = tempfile.mkdtemp(prefix="launchcut-sr-", dir=os.path.dirname(out))
    try:
        fin, fsr = os.path.join(tmp, "in"), os.path.join(tmp, "sr")
        os.makedirs(fin); os.makedirs(fsr)
        log(f"[enhance] extracting frames from {os.path.basename(src)} ({w}x{h})")
        subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vsync", "passthrough", os.path.join(fin, "%06d.png")], check=True)
        n = len(os.listdir(fin))
        log(f"[enhance] Real-ESRGAN {model} x{scale} on {n} frames")
        subprocess.run([b, "-i", fin, "-o", fsr, "-n", model, "-s", str(scale), "-f", "png"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        W, H = w * scale, h * scale
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", rate,
                                "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "ffv1", "-level", "3",
                                "-pix_fmt", "bgr0", "-c:a", "copy", out], stdin=subprocess.PIPE)
        rejected = 0
        for name in sorted(os.listdir(fin)):
            o = cv2.imread(os.path.join(fin, name)).astype(np.float32)
            sr = cv2.imread(os.path.join(fsr, name))
            sr = (cv2.resize(sr, (W, H), interpolation=cv2.INTER_AREA) if sr.shape[:2] != (H, W) else sr).astype(np.float32)
            L = cv2.resize(o, (W, H), interpolation=cv2.INTER_CUBIC)
            # detail transfer: tone from the original, edges from the model
            frame = np.clip(cv2.GaussianBlur(L, (0, 0), sigma) + (sr - cv2.GaussianBlur(sr, (0, 0), sigma)), 0, 255)
            back = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
            if cv2.PSNR(back.astype(np.uint8), o.astype(np.uint8)) < 38.0:     # the model changed what the source says
                frame = L
                rejected += 1
            enc.stdin.write(frame.astype(np.uint8).tobytes())
        log(f"[enhance] {rejected} of {n} frames failed the round-trip check and fell back to plain upscaling")
        enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError("encoding the enhanced source failed")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    log(f"[enhance] cached {out}")
    return out
