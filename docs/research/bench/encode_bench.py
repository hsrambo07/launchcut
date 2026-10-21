"""Encode-path benchmark for a 4 s hold with a 6% zoom drift, 640x360 source -> 1280x720. Usage: python -I encode_bench.py <workdir>"""
import sys, os, subprocess, re
import numpy as np, cv2
wd = sys.argv[1]
src = cv2.imread(os.path.join(wd, "lo_clean.png"))
W, H, D = 1280, 720, 4.0

def frames(fps, grain, drift=True, snap=False):
    n = int(D * fps)
    for i in range(n):
        u = i / fps / D
        s = 2.0 * (1 + 0.06 * (u if drift else 0))
        cx, cy = 320.0, 180.0
        M = np.float64([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s], [0, 0, 1]])
        img = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LANCZOS4).astype(np.float32)
        if grain == "dynamic":
            img += np.random.default_rng(i).standard_normal((H, W, 1), np.float32) * 1.5
        elif grain == "static":
            img += np.random.default_rng(0).standard_normal((H, W, 1), np.float32) * 1.5
        yield np.clip(img, 0, 255).astype(np.uint8)

def enc(path, fps, grain, args, drift=True):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          *args, path], stdin=subprocess.PIPE)
    for f in frames(fps, grain, drift):
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()

def mbps(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=bit_rate", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out) / 1e6

def score(dist, ref):
    """VMAF and PSNR-Y of dist against the lossless no-grain reference at the same fps"""
    err = subprocess.run(["ffmpeg", "-nostats", "-i", dist, "-i", ref, "-lavfi", "[0:v][1:v]libvmaf=n_threads=8", "-f", "null", "-"], capture_output=True, text=True).stderr
    v = re.search(r"VMAF score: ([\d.]+)", err)
    err2 = subprocess.run(["ffmpeg", "-nostats", "-i", dist, "-i", ref, "-lavfi", "[0:v][1:v]psnr", "-f", "null", "-"], capture_output=True, text=True).stderr
    py = re.search(r"PSNR y:([\d.]+)", err2)
    return float(v.group(1)) if v else None, float(py.group(1)) if py else None

TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
MASTER = ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-profile:v", "high", *TAG]
DELIV = lambda extra=[]: ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "18M", "-bufsize", "36M", "-pix_fmt", "yuv420p", "-profile:v", "high", *extra, *TAG]
PLATFORM = ["-c:v", "libx264", "-preset", "medium", "-b:v", "2M", "-maxrate", "2.5M", "-bufsize", "5M", "-r", "30", "-pix_fmt", "yuv420p", *TAG]

os.chdir(wd)
for fps in (60, 30):
    for dr in (True, False):
        enc(f"ref{fps}{dr}.mkv", fps, "none", ["-c:v", "ffv1", "-pix_fmt", "bgr0"], dr)
rows = []
def case(name, fps, grain, double, extra=[], drift=True):
    out = f"c_{len(rows)}.mp4"
    if double:
        enc("m.mp4", fps, grain, MASTER, drift)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "m.mp4", *DELIV(extra), out], check=True)
    else:
        enc(out, fps, grain, DELIV(extra), drift)
    plat = f"p_{len(rows)}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, *PLATFORM, plat], check=True)
    v, p = score(out, f"ref{fps}{drift}.mkv")
    pv, pp = score(plat, f"ref30{drift}.mkv")
    rows.append((name, mbps(out), v, p, pv, pp))
    print(f"{name:52s} | deliv {rows[-1][1]:5.2f} Mbps VMAF {v:5.2f} PSNR-Y {p:5.2f} | after 2 Mbps 30fps re-encode VMAF {pv:5.2f} PSNR-Y {pp:5.2f}", flush=True)

case("A launchcut today: grain 1.5 dynamic, master+delivery", 60, "dynamic", True)
case("B no grain, master+delivery", 60, "none", True)
case("C no grain, single encode", 60, "none", False)
case("D static grain 1.5, single encode", 60, "static", False)
case("E no grain, single encode, -tune animation", 60, "none", False, ["-tune", "animation"])
case("F no grain, single, aq-mode=3 deblock=-1,-1 psy-rd=1:0", 60, "none", False, ["-x264-params", "aq-mode=3:deblock=-1,-1:psy-rd=1.0,0.0"])
case("G no grain, single encode, 30 fps", 30, "none", False)
case("I no grain, single, 60 fps, NO drift (locked hold)", 60, "none", False, drift=False)
case("H grain 1.5 dynamic, single encode, 30 fps", 30, "dynamic", False)
