# launchcut

Turn screen recordings (one or many) and a bit of context into a directed short video. The engine breaks recordings down, renders each shot with a designed camera, adds highlights, captions and a synthesized SFX bed, and checks the result before you post it.

```
recordings + context ──▶ probe ──▶ PLAN.md (beats, shots, pacing) ──▶ cut.yaml ──▶ stills loop ──▶ render + sfx + deliver ──▶ qa
```

- **[RULES.md](RULES.md)** is the playbook: intake variables, phases with exit gates, direction vocabulary, sound map, narration, style knobs, energy presets, pitfalls. Start here.
- **[REFERENCE.md](REFERENCE.md)** is the `cut.yaml` schema.
- **[examples/agentplay](examples/agentplay)** is a real shipped cut (AgentPlay, 14 s, quote-tweet product demo), with its plan, review log and changelog.

## What it does

| Step | Command | You get |
|---|---|---|
| Inventory | `launchcut probe recs/*.mov` | specs, VFR and audio check, timestamped contact sheets, motion spikes (clicks, panel changes) and active windows (playback) |
| Lock coordinates | `launchcut grid rec.mov 12.0 --box 0 560 1700 1340` | full-res crop with a labelled pixel grid |
| Scaffold | `launchcut new cuts/my-cut` | `cut.yaml` + `PLAN.md` from the templates |
| Review loop | `launchcut stills cuts/my-cut/cut.yaml` | chosen frames rendered in seconds + a sheet |
| Picture | `launchcut render cut.yaml [--draft]` | picture master with motion blur on camera moves |
| Sound | `launchcut sfx cut.yaml` | SFX bed generated from the cut, narration mix with ducking, cue sheet |
| Deliver | `launchcut deliver cut.yaml` | bitrate-capped H.264, loudness-normalised `<name>.mp4`, `-muted.mp4`, `-vo-only.mp4` |
| Validate | `launchcut qa cut.yaml` | gate report + strip, phone-width and thumbnail sheets |
| Everything | `launchcut all cut.yaml` | render, sfx, deliver, qa |

Shot types: `ui` (a recording with a camera), `image` (a still with the same treatment), `card` (type on the background), `end` (logo lockup, typed command, tagline). Cameras use keyframes with log zoom, `frame:` boxes, tilt, anchors, punch entries, whip exits, kicks, and a dive that hands the product's own logo to the end card. Highlights are rings and pulses placed in recording pixels. Platform presets: `twitter-16x9`, `twitter-1x1`, `vertical-9x16`, `feed-4x5`, `linkedin-16x9`, `web-16x9`.

## Setup

Requirements: `ffmpeg` and `ffprobe` on PATH, [uv](https://docs.astral.sh/uv/), Python 3.10+.

```
git clone https://github.com/hsrambo07/launchcut && cd launchcut
uv run launchcut --help            # first run installs numpy, opencv-python-headless<5, pillow, pyyaml
```

Fonts: the defaults are [Geist and Geist Mono](https://vercel.com/font) and [Inter](https://rsms.me/inter/). Install them (macOS: into `~/Library/Fonts`), or set `style.fonts` to any font file stem or path. A missing font falls back to Pillow's default with a warning. A `fonts/` folder at the repo root is also searched.

## Try the example

The example points at the original recording on the author's Desktop. Point `sources.main` in `examples/agentplay/cut.yaml` at your own recording, or use it as a reading reference.

```
uv run launchcut stills examples/agentplay/cut.yaml 0 4.6 8.2 11.6
uv run launchcut all examples/agentplay/cut.yaml
```

## Using it with Claude Code

The repo ships a skill at `.claude/skills/launchcut/SKILL.md`. Open the repo in Claude Code and run `/launchcut` with your recordings and context, for example:

> /launchcut ~/Desktop/rec1.mov ~/Desktop/rec2.mov. Quote tweet of our launch post, show the new review flow, 15 s, vertical too.

The agent follows `RULES.md` phase by phase. It writes `PLAN.md` before any rendering, reviews a stills sheet before the full render, and reports the QA gates when it hands the file over.

## Layout

```
RULES.md                  the playbook
REFERENCE.md              cut.yaml schema
launchcut/
  cli.py                  commands
  config.py               cut loading, presets, extends, validation
  probe.py                inventory, motion spikes, coordinate grids
  camera.py               keyframe cameras, punch/whip/dive, clamping
  render.py               compositor, motion blur, encode, stills
  draw.py                 type with accent markup, rings, grid, pill, SVG marks, lockups
  sfx.py                  synthesized sounds, cue generation, VO ducking
  deliver.py              platform encode and mux
  qa.py                   gates and review sheets
templates/                PLAN.md and cut.yaml to start from
examples/agentplay/       a shipped cut: cut.yaml, style.yaml, PLAN.md, logo
.claude/skills/launchcut/ the /launchcut skill
```

Recordings and renders never go into git (see `.gitignore`). Commit `cut.yaml`, `style.yaml` and `PLAN.md`, and record source paths in the plan.
