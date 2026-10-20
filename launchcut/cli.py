"""launchcut command line. Run `launchcut <command> -h` for options.

  new      scaffold a cut folder (cut.yaml + PLAN.md) from the templates
  probe    inventory a recording: specs, audio, contact sheets, motion spikes
  grid     full-res frame with a coordinate grid, to lock boxes and points
  transcribe  word-timed transcript + sentences, pauses, fillers, soundbites (needs --extra speech)
  stills   render chosen moments of a cut to PNGs + a sheet (fast review loop)
  render   render the picture master (add --draft for a quick pass)
  sfx      synthesize the SFX bed, mix narration if any, write the cue sheet
  deliver  platform encode + mux + muted / VO-only masters
  qa       technical gates + review sheets on the delivered file
  all      render, sfx, deliver, qa in one go
"""
import argparse, os, shutil, sys, time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _cut(path):
    from .config import Cut
    return Cut(path)


def cmd_new(a):
    os.makedirs(a.dir, exist_ok=True)
    for f in ("cut.yaml", "PLAN.md"):
        dst = os.path.join(a.dir, f)
        if os.path.exists(dst):
            print(f"skip {dst} (exists)")
            continue
        shutil.copy(os.path.join(HERE, "templates", f), dst)
        print(f"wrote {dst}")


def cmd_probe(a):
    from .probe import probe
    for p in a.recordings:
        rep, d = probe(os.path.expanduser(p), a.out, a.region, a.fps, a.transcribe)
        print(f"{p}\n  -> {rep}")


def cmd_transcribe(a):
    from .speech import transcribe
    for p in a.clips:
        p = os.path.expanduser(p)
        name = os.path.splitext(os.path.basename(p))[0].replace(" ", "_").replace("\u202f", "_")
        js, md = transcribe(p, os.path.join(a.out, name), a.model, prompt=a.prompt)
        print(f"{p}\n  -> {md}\n  -> {js}")


def cmd_grid(a):
    from .probe import grid
    print(grid(os.path.expanduser(a.recording), a.t, a.box, a.step, a.out))


def cmd_stills(a):
    from .render import Renderer
    cut = _cut(a.cut)
    times = a.times or [round(sh["start"] + f * sh["duration"], 2) for sh in cut.shots for f in (0.05, 0.5, 0.9)]
    _, sheet = Renderer(cut, draft=a.draft).stills(times, cut.out("stills"))
    print(f"sheet: {sheet}")


def cmd_render(a):
    from .render import Renderer
    cut = _cut(a.cut)
    out = cut.out(f"{cut.name}-picture{'-draft' if a.draft else ''}.mp4")
    t = time.time()
    print(f"rendering {cut.name}: {len(cut.shots)} shots, {cut.duration:.2f}s, {cut.W}x{cut.H}@{cut.fps}")
    Renderer(cut, draft=a.draft).render(out, a.t_from, a.t_to)
    print(f"wrote {out} in {time.time() - t:.0f}s")
    return cut, out


def cmd_sfx(a):
    from .render import Renderer
    from .sfx import mix
    cut = _cut(a.cut)
    outs = mix(cut, Renderer(cut, draft=True))
    for k, v in outs.items():
        print(f"{k}: {v}")
    return cut, outs


def cmd_deliver(a):
    from .deliver import deliver
    from .render import Renderer
    from .sfx import mix
    cut = _cut(a.cut)
    pic = cut.out(f"{cut.name}-picture.mp4")
    if not os.path.exists(pic):
        sys.exit(f"no picture master at {pic}; run `launchcut render` first")
    audio = mix(cut, Renderer(cut, draft=True))
    outs = deliver(cut, pic, audio)
    for k, v in outs.items():
        print(f"{k}: {v}")
    return cut, outs


def cmd_qa(a):
    from .qa import qa
    cut = _cut(a.cut)
    main = a.file or cut.out(f"{cut.name}.mp4")
    ok, rep, d = qa(cut, main)
    print(open(rep).read())
    print(f"review sheets in {d}")
    if not ok:
        sys.exit(1)


def cmd_all(a):
    a.draft, a.t_from, a.t_to = False, 0.0, None
    cmd_render(a)
    cut, outs = cmd_deliver(a)
    a.file = outs["main"]
    cmd_qa(a)


def main(argv=None):
    p = argparse.ArgumentParser(prog="launchcut", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new"); s.add_argument("dir"); s.set_defaults(fn=cmd_new)
    s = sub.add_parser("probe"); s.add_argument("recordings", nargs="+"); s.add_argument("--out", default="probe")
    s.add_argument("--region", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="measure motion only inside this box")
    s.add_argument("--fps", type=float, default=2.0, help="contact sheet rate")
    s.add_argument("--transcribe", action="store_true", help="also transcribe speech (needs --extra speech)"); s.set_defaults(fn=cmd_probe)
    s = sub.add_parser("transcribe"); s.add_argument("clips", nargs="+"); s.add_argument("--out", default="probe")
    s.add_argument("--model", default="small.en", help="faster-whisper model: tiny.en base.en small.en medium.en large-v3")
    s.add_argument("--prompt", help="names and jargon to expect, e.g. 'Entelligence, AgentPlay'"); s.set_defaults(fn=cmd_transcribe)
    s = sub.add_parser("grid"); s.add_argument("recording"); s.add_argument("t", type=float)
    s.add_argument("--box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1")); s.add_argument("--step", type=int, default=100)
    s.add_argument("--out"); s.set_defaults(fn=cmd_grid)
    s = sub.add_parser("stills"); s.add_argument("cut"); s.add_argument("times", nargs="*", type=float)
    s.add_argument("--draft", action="store_true"); s.set_defaults(fn=cmd_stills)
    s = sub.add_parser("render"); s.add_argument("cut"); s.add_argument("--draft", action="store_true")
    s.add_argument("--from", dest="t_from", type=float, default=0.0); s.add_argument("--to", dest="t_to", type=float); s.set_defaults(fn=cmd_render)
    s = sub.add_parser("sfx"); s.add_argument("cut"); s.set_defaults(fn=cmd_sfx)
    s = sub.add_parser("deliver"); s.add_argument("cut"); s.set_defaults(fn=cmd_deliver)
    s = sub.add_parser("qa"); s.add_argument("cut"); s.add_argument("--file"); s.set_defaults(fn=cmd_qa)
    s = sub.add_parser("all"); s.add_argument("cut"); s.set_defaults(fn=cmd_all)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
