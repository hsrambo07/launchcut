"""Does cleaning a lossy 360p source before a 2x upscale help? Usage: python -I predenoise.py <workdir>"""
import sys, os, subprocess
import numpy as np, cv2
wd = sys.argv[1]; os.chdir(wd)
gt = cv2.imread("gt720.png"); lo = cv2.imread("lo_clean.png")
def luma(x): return cv2.cvtColor(x, cv2.COLOR_BGR2YCrCb)[..., 0].astype(np.float64)
def psnr(a, b): return 10 * np.log10(255 ** 2 / np.mean((luma(a) - luma(b)) ** 2))
def ff(img, vf, w, h):
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{img.shape[1]}x{img.shape[0]}", "-i", "-", "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], input=img.tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(h, w, 3)
up = lambda x: cv2.warpPerspective(x, np.float64([[2, 0, .5], [0, 2, .5], [0, 0, 1]]), (1280, 720), flags=cv2.INTER_LANCZOS4)
for crf in (24, 30):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "lo_clean.png", "-c:v", "libx264", "-crf", str(crf), "-pix_fmt", "yuv420p", "q.mp4"], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "q.mp4", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    q = np.frombuffer(raw, np.uint8).reshape(360, 640, 3).copy()
    for name, pre in [("none", lambda x: x), ("ffmpeg deblock", lambda x: ff(x, "deblock", 640, 360)),
                      ("ffmpeg spp=4", lambda x: ff(x, "spp=4", 640, 360)),
                      ("ffmpeg nlmeans s=1.5", lambda x: ff(x, "nlmeans=s=1.5:p=3:r=7", 640, 360)),
                      ("cv fastNlMeans h=3", lambda x: cv2.fastNlMeansDenoisingColored(x, None, 3, 3, 7, 21))]:
        print(f"crf {crf} | pre {name:22s} | lanczos x2 PSNR-Y {psnr(up(pre(q)), gt):.2f}")
