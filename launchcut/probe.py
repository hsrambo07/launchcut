"""Inventory a recording before planning: specs, audio level, timestamped contact sheets, a motion profile that finds the
moments where something happens, and coordinate grids for locking boxes. Output goes to probe/<recording-name>/."""
import os, re, subprocess
import numpy as np
import cv2
from .media import ffprobe


def audio_level(path):
    # volumedetect logs at info level; never add -v error here or the numbers vanish
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mean = re.search(r"mean_volume: (-?[\d.]+) dB", err)
    peak = re.search(r"max_volume: (-?[\d.]+) dB", err)
    return (float(mean.group(1)) if mean else None), (float(peak.group(1)) if peak else None)


def frames(path, fps, width, gray=False):
    info = ffprobe(path)
    h = int(round(info["height"] * width / info["width"] / 2) * 2)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={width}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "gray" if gray else "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape((-1, h, width) if gray else (-1, h, width, 3))


def label(img, text):
    cv2.putText(img, text, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(img, text, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (90, 230, 255), 1, cv2.LINE_AA)
    return img


def sheets(arr, fps, out_prefix, cols=6, per_page=48):
    paths = []
    for p0 in range(0, len(arr), per_page):
        tiles = [label(arr[i].copy(), f"{i / fps:6.2f}s") for i in range(p0, min(p0 + per_page, len(arr)))]
        while len(tiles) % cols:
            tiles.append(np.zeros_like(tiles[0]))
        tiles = [cv2.copyMakeBorder(t, 0, 3, 0, 3, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t in tiles]
        img = np.vstack([np.hstack(tiles[r:r + cols]) for r in range(0, len(tiles), cols)])
        p = f"{out_prefix}_{p0 // per_page + 1:02d}.png"
        cv2.imwrite(p, img)
        paths.append(p)
    return paths


def motion_profile(arr, fps, region=None, src_w=None):
    g = arr.astype(np.float32)
    if region and src_w:
        k = arr.shape[2] / src_w
        x0, y0, x1, y1 = [int(round(v * k)) for v in region]
        g = g[:, y0:y1, x0:x1]
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    t = (np.arange(len(d)) + 1) / fps
    return t, d


def events(t, d):
    """spikes = cuts, clicks, panel changes; windows = sustained activity such as playback or typing"""
    base = float(np.median(d)) + 1e-6
    spikes = [(float(t[i]), float(d[i])) for i in range(len(d)) if d[i] > max(0.5, base * 8) and (i == 0 or d[i] >= d[i - 1]) and (i + 1 == len(d) or d[i] >= d[i + 1])]
    active = d > max(0.12, base * 3)
    wins, s = [], None
    for i, a in enumerate(active):
        if a and s is None:
            s = i
        if (not a or i + 1 == len(active)) and s is not None:
            e = i if not a else i + 1
            if t[min(e, len(t) - 1)] - t[s] >= 0.8:
                wins.append((float(t[s]), float(t[min(e, len(t) - 1)])))
            s = None
    return spikes, wins


def plot(t, d, spikes, out, w=1600, h=300):
    img = np.full((h, w, 3), 255, np.uint8)
    top = max(float(d.max()), 1e-6)
    dur = float(t[-1]) if len(t) else 1.0
    for x in range(0, int(dur) + 1):
        X = int(x / dur * (w - 40)) + 30
        cv2.line(img, (X, 0), (X, h - 20), (225, 225, 225), 1)
        if x % 5 == 0:
            cv2.putText(img, f"{x}s", (X - 8, h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (90, 90, 90), 1, cv2.LINE_AA)
    pts = np.int32([[int(ti / dur * (w - 40)) + 30, int((h - 25) - di / top * (h - 40))] for ti, di in zip(t, d)])
    cv2.polylines(img, [pts], False, (60, 60, 60), 1, cv2.LINE_AA)
    for ts, _ in spikes:
        X = int(ts / dur * (w - 40)) + 30
        cv2.line(img, (X, 5), (X, h - 25), (40, 120, 255), 1)
    cv2.imwrite(out, img)


def probe(path, out_root="probe", region=None, sheet_fps=2.0):
    name = os.path.splitext(os.path.basename(path))[0].replace(" ", "_").replace(" ", "_")
    d = os.path.join(out_root, name)
    os.makedirs(d, exist_ok=True)
    info = ffprobe(path)
    mean, peak = audio_level(path) if info["has_audio"] else (None, None)
    arr = frames(path, sheet_fps, 400)
    sheet_paths = sheets(arr, sheet_fps, os.path.join(d, "sheet"))
    m = frames(path, 10, 320, gray=True)
    t, dd = motion_profile(m, 10, region, info["width"])
    spikes, wins = events(t, dd)
    plot(t, dd, spikes, os.path.join(d, "motion.png"))
    np.savetxt(os.path.join(d, "motion.csv"), np.stack([t, dd], 1), delimiter=",", header="t,diff", fmt="%.3f")
    rep = os.path.join(d, "inventory.md")
    with open(rep, "w") as f:
        f.write(f"# Inventory: {os.path.basename(path)}\n\n")
        f.write(f"- size {info['width']}x{info['height']}, codec {info['codec']}, nominal {info['fps']:g} fps, {info['duration']:.2f}s\n")
        f.write(f"- variable frame rate: {'yes (renderer converts with -vf fps)' if info['vfr'] else 'no'}\n")
        if info["has_audio"]:
            silent = mean is not None and mean < -60
            f.write(f"- audio: mean {mean} dB, peak {peak} dB{'  (silent: plan SFX only)' if silent else ''}\n")
        else:
            f.write("- audio: none\n")
        f.write(f"\nContact sheets ({sheet_fps:g} fps, timestamps burned in): " + ", ".join(f"`{os.path.basename(p)}`" for p in sheet_paths) + "\n")
        f.write("Motion profile: `motion.png` (orange lines are spikes), raw numbers in `motion.csv`.\n\n")
        f.write("## Spikes (clicks, panel changes, cuts)\n\n| t (s) | strength |\n|---|---|\n")
        for ts, v in spikes:
            f.write(f"| {ts:.1f} | {v:.2f} |\n")
        f.write("\n## Active windows (playback, typing, animation)\n\n| from | to |\n|---|---|\n")
        for a, b in wins:
            f.write(f"| {a:.1f} | {b:.1f} |\n")
        f.write("\nNext: look at the sheets around each spike, write the beat map in PLAN.md, then lock boxes with `launchcut grid`.\n")
    return rep, d


def grid(path, t, box=None, step=100, out=None):
    """full-resolution frame at t with a labelled grid in recording pixels, cropped to box if given"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    x0, y0, x1, y1 = box or (0, 0, img.shape[1], img.shape[0])
    c = img[y0:y1, x0:x1].copy()
    for x in range((x0 // step + 1) * step if x0 % step else x0, x1, step):
        cv2.line(c, (x - x0, 0), (x - x0, y1 - y0), (60, 60, 255), 1)
        cv2.putText(c, str(x), (x - x0 + 3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 80, 255), 1, cv2.LINE_AA)
    for y in range((y0 // (step // 2) + 1) * (step // 2) if y0 % (step // 2) else y0, y1, step // 2):
        cv2.line(c, (0, y - y0), (x1 - x0, y - y0), (255, 150, 0), 1)
        cv2.putText(c, str(y), (3, y - y0 + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 170, 60), 1, cv2.LINE_AA)
    out = out or f"grid_{t:06.2f}.png"
    cv2.imwrite(out, c)
    return out
