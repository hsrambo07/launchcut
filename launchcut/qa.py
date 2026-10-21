"""Technical gates on the delivered file plus review sheets for the editorial gates. Writes out/<name>-qa/report.md."""
import json, os, re, subprocess
import numpy as np
import cv2
from .render import contact_sheet


def probe_json(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def loudness(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summ)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summ)
    return (float(i.group(1)) if i else None), (float(p.group(1)) if p and p.group(1) != "-inf" else None)


def black_segments(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-vf", "blackdetect=d=0.03:pix_th=0.04", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return re.findall(r"black_start:([\d.]+)", err)


def frame_at(path, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


def qa(cut, main, muted=None):
    d = cut.out(f"{cut.name}-qa")
    os.makedirs(d, exist_ok=True)
    o = cut.cfg["output"]
    rows, ok = [], True

    def gate(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        rows.append(f"| {'PASS' if passed else 'FAIL'} | {name} | {detail} |")

    j = probe_json(main)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = v["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    dur = float(j["format"]["duration"])
    mbps = float(j["format"].get("bit_rate", 0)) / 1e6
    gate("codec", v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", f"{v['codec_name']} {v.get('pix_fmt')}")
    gate("size", [int(v["width"]), int(v["height"])] == list(o["size"]), f"{v['width']}x{v['height']} (preset {o['size'][0]}x{o['size'][1]})")
    gate("frame rate", abs(fps - cut.fps) < 0.01, f"{fps:g} fps")
    gate("duration", abs(dur - cut.duration) <= 1.5 / cut.fps, f"{dur:.3f}s (cut {cut.duration:.3f}s)")
    gate("bitrate", mbps <= float(o["max_mbps"]) * 1.15, f"{mbps:.1f} Mbps overall (cap {o['max_mbps']} video)")
    if a:
        lufs, tp = loudness(main)
        target = float(o.get("lufs", -14))
        gate("loudness", lufs is not None and abs(lufs - target) <= 1.5, f"{lufs} LUFS (target {target})")
        gate("true peak", tp is not None and tp <= -0.9, f"{tp} dBFS")
    # magnification: how many screen pixels each source pixel becomes (after any enhance). Above 3x UI text goes soft.
    from .render import Renderer
    r = Renderer(cut, draft=True)
    worst, where = 0.0, ""
    for sh in cut.shots:
        if sh["type"] not in ("ui", "image"):
            continue
        cam, u = r.cam(sh), r.upf[sh["source"]]
        for t in np.linspace(0, sh["duration"] - 1e-3, 24):
            m = cam(float(t))[2] / u
            if m > worst:
                worst, where = m, f"{sh['id']} @ {t:.1f}s"
    if worst:
        enhance_hint = "" if worst <= 3.0 else " (set `enhance: 2` on the source or frame wider)"
        rows.append(f"| {'PASS' if worst <= 3.0 else 'WARN'} | source magnification | {worst:.2f}x at {where}{enhance_hint} |")
    blacks = black_segments(main)
    gate("no black frames", cut.cfg.get("allow_dark_frames") or not blacks, f"{len(blacks)} black segments")
    f0 = frame_at(main, 0.0)
    cv2.imwrite(os.path.join(d, "thumbnail-frame0.png"), f0)
    gate("frame 0 reads as a thumbnail", f0.mean() > 18 or f0.std() > 14, f"mean luma {f0.mean():.0f}, contrast {f0.std():.0f}")

    # review sheets: a strip of the whole cut, and phone-width frames where each caption is fully on screen
    times = np.arange(0, cut.duration, 0.2)
    strip = []
    for t in times:
        p = os.path.join(d, f"strip_{t:06.2f}.png")
        cv2.imwrite(p, cv2.resize(frame_at(main, float(t)), (384, int(384 * cut.H / cut.W)), interpolation=cv2.INTER_AREA))
        strip.append(p)
    contact_sheet(strip, os.path.join(d, "strip-5fps.png"), cols=10, width=384)
    for p in strip:
        os.remove(p)
    phone, labels = [], []
    for sh in cut.shots:
        cap = sh.get("caption")
        tl = (float(cap.get("in", 0.3)) + float(cap.get("out", sh["duration"]))) / 2 if cap else sh["duration"] * 0.6
        t = sh["start"] + tl
        img = frame_at(main, t)
        w = 360 if cut.W >= cut.H else 240
        p = os.path.join(d, f"phone_{sh['id']}.png")
        cv2.imwrite(p, cv2.resize(img, (w, int(w * cut.H / cut.W)), interpolation=cv2.INTER_AREA))
        phone.append(p)
        labels.append(sh["id"])
    contact_sheet(phone, os.path.join(d, "phone-width.png"), cols=3, width=360 if cut.W >= cut.H else 240, labels=labels)
    for p in phone:
        os.remove(p)

    rep = os.path.join(d, "report.md")
    with open(rep, "w") as f:
        f.write(f"# QA: {cut.name}\n\nFile: `{main}`\n\n## Technical gates\n\n| result | gate | detail |\n|---|---|---|\n")
        f.write("\n".join(rows) + "\n\n")
        f.write("## Editorial gates (a reviewer who did not build the cut ticks these)\n\n"
                "Open `strip-5fps.png`, `phone-width.png` and `thumbnail-frame0.png`, then watch the file once muted and once with sound.\n\n"
                "- [ ] Frame 0 shows the thing we are launching and works as the post thumbnail\n"
                "- [ ] Muted, at phone width, a first-time viewer can say what each beat showed\n"
                "- [ ] Every caption names something that is on screen at that moment\n"
                "- [ ] Every highlight lands on the thing the caption names, and holds long enough to read\n"
                "- [ ] Every claim (numbers, free, open source, commands) traces to the recording, the README or the brief\n"
                "- [ ] Nothing moves without a reason; transitions stay centred\n"
                "- [ ] Every sound is tied to something visible; nothing clips; VO (if any) is untouched and clear over SFX\n"
                "- [ ] The cut fits its context (what the post or the quoted post already says is not repeated)\n"
                "- [ ] Logo, colours and type match the brand files\n")
    return ok, rep, d
