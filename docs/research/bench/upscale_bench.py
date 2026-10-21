"""Benchmark 640x360 -> 1280x720 upscalers against a native ground truth. Usage: python -I upscale_bench.py <workdir> <modeldir>"""
import sys, os, subprocess, time
import numpy as np, cv2
wd, md = sys.argv[1], sys.argv[2]
gt = cv2.imread(os.path.join(wd, "gt720.png"))
lo = cv2.resize(gt, (640, 360), interpolation=cv2.INTER_AREA)
cv2.imwrite(os.path.join(wd, "lo_clean.png"), lo)
# lossy 360p like a YouTube download: x264 crf 30 yuv420p round trip
p = os.path.join(wd, "lo.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(wd, "lo_clean.png"), "-vf", "scale=out_color_matrix=bt709", "-c:v", "libx264", "-crf", "30",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", p], check=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
lossy = np.frombuffer(raw, np.uint8).reshape(360, 640, 3).copy()
cv2.imwrite(os.path.join(wd, "lo_lossy.png"), lossy)

def luma(x):
    return cv2.cvtColor(x, cv2.COLOR_BGR2YCrCb)[..., 0].astype(np.float64)

def psnr(a, b):
    m = np.mean((luma(a) - luma(b)) ** 2)
    return 10 * np.log10(255 ** 2 / m)

def ssim(a, b):
    x, y = luma(a), luma(b)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    g = lambda z: cv2.GaussianBlur(z, (11, 11), 1.5)
    mx, my = g(x), g(y)
    sx, sy, sxy = g(x * x) - mx * mx, g(y * y) - my * my, g(x * y) - mx * my
    return float(np.mean(((2 * mx * my + C1) * (2 * sxy + C2)) / ((mx * mx + my * my + C1) * (sx + sy + C2))))

def unsharp_luma(img, sigma=1.0, amount=0.5):
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    y = ycc[..., 0]
    ycc[..., 0] = y + amount * (y - cv2.GaussianBlur(y, (0, 0), sigma))
    return cv2.cvtColor(np.clip(ycc, 0, 255).astype(np.uint8), cv2.COLOR_YCrCb2BGR)

def ff(img, vf):
    h, w = img.shape[:2]
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-i", "-", "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], input=img.tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(720, 1280, 3)

srs = {}
for name in ("ESPCN", "FSRCNN", "LapSRN", "EDSR"):
    s = cv2.dnn_superres.DnnSuperResImpl_create()
    s.readModel(os.path.join(md, f"{name}_x2.pb"))
    s.setModel(name.lower(), 2)
    srs[name] = s

def warp(img, flag):  # what launchcut does: warpPerspective at s=2 with pixel-centre mapping
    M = np.float64([[2, 0, 0.5], [0, 2, 0.5], [0, 0, 1]])
    return cv2.warpPerspective(img, M, (1280, 720), flags=flag)

methods = {
    "nearest": lambda x: cv2.resize(x, (1280, 720), interpolation=cv2.INTER_NEAREST),
    "cv linear": lambda x: warp(x, cv2.INTER_LINEAR),
    "cv cubic": lambda x: warp(x, cv2.INTER_CUBIC),
    "cv lanczos4 (launchcut)": lambda x: warp(x, cv2.INTER_LANCZOS4),
    "cv lanczos4 + luma USM 1.0/0.5": lambda x: unsharp_luma(warp(x, cv2.INTER_LANCZOS4), 1.0, 0.5),
    "cv cubic + luma USM 1.0/0.6": lambda x: unsharp_luma(warp(x, cv2.INTER_CUBIC), 1.0, 0.6),
    "ff spline+full_chroma_int": lambda x: ff(x, "scale=1280:720:flags=spline+accurate_rnd+full_chroma_int"),
    "ff lanczos + cas 0.5": lambda x: ff(x, "scale=1280:720:flags=lanczos+accurate_rnd+full_chroma_int,cas=strength=0.5"),
    "ESPCN x2": lambda x: srs["ESPCN"].upsample(x),
    "FSRCNN x2": lambda x: srs["FSRCNN"].upsample(x),
    "LapSRN x2": lambda x: srs["LapSRN"].upsample(x),
    "EDSR x2": lambda x: srs["EDSR"].upsample(x),
    "FSRCNN x2 + luma USM 1.0/0.4": lambda x: unsharp_luma(srs["FSRCNN"].upsample(x), 1.0, 0.4),
}
rows, crops = [], {}
for src_name, src in (("clean", lo), ("lossy", lossy)):
    for name, fn in methods.items():
        t0 = time.time()
        out = fn(src)
        dt = (time.time() - t0) * 1000
        rows.append((src_name, name, psnr(out, gt), ssim(out, gt), dt))
        crops[(src_name, name)] = out
for r in rows:
    print(f"{r[0]:6s} | {r[1]:32s} | PSNR {r[2]:6.2f} | SSIM {r[3]:.4f} | {r[4]:7.1f} ms")
# visual sheet: a text-heavy crop at 2x display zoom
y0, y1, x0, x1 = 95, 215, 0, 280
pick = ["nearest", "cv lanczos4 (launchcut)", "cv lanczos4 + luma USM 1.0/0.5", "ff lanczos + cas 0.5", "FSRCNN x2", "EDSR x2"]
tiles = []
def lab(img, t):
    img = img.copy(); cv2.putText(img, t, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(img, t, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (90, 230, 255), 1, cv2.LINE_AA); return img
for src_name in ("clean", "lossy"):
    row = [lab(gt[y0:y1, x0:x1], "ground truth (native)")] + [lab(crops[(src_name, n)][y0:y1, x0:x1], f"{src_name}: {n}") for n in pick]
    tiles.append(row)
cols = 4
flat = [t for row in tiles for t in row]
while len(flat) % cols: flat.append(np.zeros_like(flat[0]))
sheet = np.vstack([np.hstack([cv2.copyMakeBorder(t, 0, 4, 0, 4, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t in flat[i:i + cols]]) for i in range(0, len(flat), cols)])
sheet = cv2.resize(sheet, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(wd, "upscale_sheet.png"), sheet)
