"""Platform encode and mux: bitrate capped H.264 + AAC, loudness normalised, muted and VO-only masters, optional copy out."""
import os, shutil, subprocess


def run(cmd):
    subprocess.run(cmd, check=True)


def deliver(cut, picture, audio):
    o = cut.cfg["output"]
    cap = float(o["max_mbps"])
    dl = cut.out(f"{cut.name}-picture-delivery.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", picture, "-c:v", "libx264", "-preset", "slow", "-crf", str(o["crf_delivery"]),
         "-maxrate", f"{cap}M", "-bufsize", f"{cap * 2}M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(cut.fps),
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", dl])
    lufs = float(o.get("lufs", -14))
    norm = f"loudnorm=I={lufs}:TP=-1.5:LRA=11" if o.get("normalize", True) else "anull"
    outs = {}
    main = cut.out(f"{cut.name}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", dl, "-i", audio["mix"], "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", norm,
         "-ar", "48000", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", main])
    outs["main"] = main
    muted = cut.out(f"{cut.name}-muted.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", dl, "-c", "copy", "-an", "-movflags", "+faststart", muted])
    outs["muted"] = muted
    if audio.get("vo"):
        vo = cut.out(f"{cut.name}-vo-only.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", dl, "-i", audio["vo"], "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", norm,
             "-ar", "48000", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", vo])
        outs["vo_only"] = vo
    os.remove(dl)
    if cut.deliver_to:
        os.makedirs(cut.deliver_to, exist_ok=True)
        for k, p in list(outs.items()):
            dst = os.path.join(cut.deliver_to, os.path.basename(p))
            shutil.copy2(p, dst)
            outs[k + "_copy"] = dst
    return outs
