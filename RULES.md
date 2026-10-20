# launchcut playbook

How we turn screen recordings (one or many) and a bit of context into a directed short video: broken down, planned shot by shot, executed, and validated before anyone posts it. This file is the rulebook. The engine in this repo (`launchcut`) does the mechanical work. The judgement lives here.

Use it as a human editor, or hand it to an agent (Claude Code: `/launchcut`). Both follow the same phases and the same gates.

---

## 0. The ten rules

1. **Context decides the opening.** If the post, or the post being quoted, already tells the story, open on the product. Frame 0 is the thumbnail, so it has to be the product, crisp and still. A type hook is only for videos that stand alone.
2. **One idea per shot.** Each shot teaches exactly one thing. The caption names it, the highlight lands on it, and the camera frames it big enough to read.
3. **Land, highlight, hold.** The camera arrives, the highlight appears, and then nothing moves for at least 0.8 s. Viewers need time to read. A cut that "feels fast" usually broke this rule.
4. **Length is soft, readability is not.** A requested length ("10 seconds maybe") gives way to beats a first-time viewer can follow. When the two fight, say so and pick readability.
5. **Muted first.** Most feeds autoplay muted on a phone. Check every frame at 360 px wide. If it does not read there, it does not read.
6. **Nothing moves without meaning.** Camera moves follow attention: to the click, to the result, out for context, into the next object. No decorative drift, no orbiting, and transitions stay centred.
7. **Every sound is tied to something visible.** Whooshes on camera moves, hits on landings, pops on highlights, an error tone on failures, keys on typing. No sound without a picture.
8. **Real things only.** Real logos from the brand files, numbers that appear in the recording, claims that trace to the README or the site. Never invent a metric, a logo or a feature.
9. **Narration is sacred.** If there is a VO, its samples are never regenerated or edited. SFX duck under it, and a VO-only master ships alongside.
10. **Prove it before you post it.** Stills sheet before the full render. Technical QA and an editorial review by someone who did not build the cut. Versions are never overwritten.

---

## 1. Intake: the variables

Fill these in `PLAN.md` (template in `templates/PLAN.md`) before touching footage. Ask the requester once for anything missing, then decide sensible defaults yourself and write them down.

| Variable | What to capture | Default if nobody says |
|---|---|---|
| **Purpose** | What this video must make someone do or believe, in one sentence | "Show the product doing its main job" |
| **Context** | Where it posts and what surrounds it: quote tweet of the launch film, reply, standalone post, landing page, demo day | Standalone |
| **Already said elsewhere** | Words and claims the surrounding post or quoted video already carries; we do not repeat them | Nothing |
| **Audience** | Who watches and what they already know | Developers who have not tried it |
| **Sources** | Every recording, screenshot, logo, README, VO script or file, with paths | Required |
| **Platform preset** | `twitter-16x9`, `twitter-1x1`, `vertical-9x16`, `feed-4x5`, `linkedin-16x9`, `web-16x9` | `twitter-16x9` |
| **Length target** | Soft target in seconds | 12 to 16 s for 3 to 4 product beats |
| **Energy** | `calm`, `standard`, `hype` (see section 5) | `standard` |
| **Brand** | Palette hexes, fonts, logo files (SVG preferred), tone of voice | Repo defaults (dark, lime accent) |
| **Captions** | On or off, voice (imperative, plain), language | On, at most 5 words each |
| **Narration** | VO file or script, or none | None: captions carry it |
| **Sound** | SFX on or off, beat bed bpm or none | SFX on, 120 bpm bed |
| **End card** | Logo lockup, command or URL, tagline | Logo + install command + one-line tagline |
| **Hide** | Secrets visible in recordings (keys, emails, customer names) that must be cropped, blurred or avoided | Check anyway |
| **Deadline and reviewer** | When, and who signs off | Requester |

---

## 2. Phases, commands and exit gates

Each phase ends with a gate. Do not start the next phase until the gate passes. Write what you found into `PLAN.md` as you go, so anyone can pick the work up.

### P1. Inventory every source

```
launchcut probe recordings/*.mov
```

This writes `probe/<recording>/inventory.md` for each recording. It contains the specs, whether the frame rate is variable, the audio level, contact sheets with timestamps burned in, and a motion profile. The motion profile marks **spikes** (clicks, panel changes) and **active windows** (playback, typing, animation).

Then actually look at the frames. Open the contact sheets, and pull full-resolution stills around every spike (`launchcut grid <rec> <t>`).

**Gate:** you can list every meaningful moment with its timestamp. You know whether the audio is usable or silent. You have checked every frame you plan to use for secrets.

### P2. Beat map

Write a table in `PLAN.md`:

| # | Source @ time | What happens on screen | What the viewer learns | Keep? |
|---|---|---|---|---|

Pick 3 to 6 beats and arrange them as a story arc:

- **Reveal:** the product, whole, doing its thing.
- **Proof beats:** the specific capabilities, each with one visible cause and effect.
- **Payoff:** the moment that makes someone want it, often a failure found or a problem solved.
- **Call to action:** the end card.

**Gate:** every kept beat teaches exactly one thing, and nothing in the beat map repeats what the context already says.

### P3. Direction (the shot list)

For each beat, decide all of the following and write them into the shot list in `PLAN.md`:

- **Camera:** a shot type from section 3, with the start framing and the end framing.
- **Source timing:** where it starts, and the speed. Speed up passive playback; slow down to 1x or less at the cause and effect.
- **Overlays:** which element gets a ring or a pulse, in which colour, and when.
- **Caption:** words, the accent word, and timing.
- **Sound intent:** what is heard, and what visible thing triggers it.
- **Duration:** from the pacing budget below.

**Pacing budget** (seconds, per shot):

```
entry punch            0.3
highlights             0.4 apart each
hold after last one    >= 0.8
caption read time      0.3 per word + 0.5
exit whip              0.2 - 0.3
```

Typical results: 2.5 to 3 s for a UI beat with a caption and highlights, 3 to 3.5 s for an opening reveal, and 2.5 to 3 s for an end card. Add the shots up. If the total is far from the target, cut a beat rather than squeeze them all.

**Gate:** the durations add up and every beat fits its budget. Every caption is 5 words or fewer and names something that is visible during that shot.

### P4. Lock coordinates

```
launchcut grid "<recording>" 12.0 --box 0 560 1700 1340
```

This writes a crop of the full-resolution frame with gridlines labelled in recording pixels. Read the boxes for rings (`[x0, y0, x1, y1]`), the points for pulses, and the regions to frame. Then write them into `cut.yaml`. All coordinates in the cut are in recording pixels, so they survive any change of output size.

**Gate:** every ring box and frame box has been checked against a grid image, not guessed.

### P5. Build the cut and run the stills loop

Copy the template (`launchcut new cuts/my-cut`), then fill in `cut.yaml` (schema in `REFERENCE.md`).

```
launchcut stills cuts/my-cut/cut.yaml                   # three moments per shot
launchcut stills cuts/my-cut/cut.yaml 0 2.4 4.1 7.9     # or exactly the moments you care about
```

This renders single frames in seconds, which is far quicker than minutes for a full render. Review the sheet against the shot list:

- Is the framing right?
- Does each highlight land on the element?
- Is the caption clear of the element it names?
- Is the text readable at small size?
- Is frame 0 a good thumbnail?

Iterate here.

**Gate:** the stills sheet matches the shot list for every shot, with no collisions between captions and content.

### P6. Render, sound, deliver

```
launchcut all cuts/my-cut/cut.yaml
```

This produces:

- **The picture master:** CRF 15, motion blur on camera moves.
- **The SFX bed:** generated from the cut. Ring pops, alert tones, clicks, whips, landings, the dive, typing, and the beat bed. The cue sheet lands in `out/<name>-cues.md`.
- **The narration mix**, if a VO exists. The SFX duck under it.
- **The platform encode:** bitrate capped, loudness normalised.
- **Delivery files:** `<name>.mp4`, `<name>-muted.mp4`, and `<name>-vo-only.mp4` when there is a VO.

For a quick look at motion before the slow pass, run `launchcut render cut.yaml --draft`.

### P7. Validate

`launchcut qa` runs inside `all`. It writes `out/<name>-qa/report.md`, which has:

- **Technical gates.** It fails the run if any of these fail:
  - codec and pixel format
  - size and frame rate
  - duration against the cut
  - bitrate against the platform cap
  - loudness and true peak
  - no black frames
  - frame 0 bright enough to work as a thumbnail
- **Review sheets:**
  - `strip-5fps.png`, the whole cut at 5 fps
  - `phone-width.png`, every shot at 360 px wide with its caption on screen
  - `thumbnail-frame0.png`
- **Editorial gates:** a checklist that a reviewer who did not build the cut ticks while watching the file once muted and once with sound.

If anything fails, fix the cut and render again. Allow at most three loops. After that, escalate the open question to the requester rather than polishing in circles.

Claude Code users can run the editorial pass with an independent judge agent. Give the judge `PLAN.md`, the report and the sheets.

**Gate:** all technical gates pass and every editorial box is ticked.

### P8. Hand-off

- Masters are named `<name>.mp4`, `<name>-muted.mp4` and `<name>-vo-only.mp4`. A new round is a new name (`-v2`, `-v3`). Never overwrite a version someone has seen.
- Commit `cut.yaml`, `style.yaml` and `PLAN.md`. Recordings and renders stay out of git (see `.gitignore`), so record their paths in `PLAN.md`.
- Never work in `/tmp`. It gets cleared, and the sources of a shipped cut go with it.
- Add a line to the changelog in `PLAN.md` for each round: what changed and why. This is the record of what the requester taught you, such as "open on the product, quoted video carries the words".

---

## 3. Direction vocabulary

### Shot types

| Shot | Use it for | How in `cut.yaml` |
|---|---|---|
| **Reveal** | Opening on the whole product. Frame 0 is crisp, then a slow push into the part that matters | `enter: none`; camera keyframes from `zoom: 0.93` to a framed region |
| **Punch-in** | Landing on a panel, card or row | Default `enter: punch`; a single framed keyframe, slow drift (5 to 10 % zoom) while holding |
| **Follow the click** | Cause and effect: the cursor clicks, the camera moves to where the result appears | Keyframes: hold on the click area, move (`inOutCubic`, 0.6 to 0.7 s) to the result after the click lands |
| **Collapse or kick** | A state change (filter applied, graph collapses, build passes) | `kicks: [{at}]` plus `collapses: [at]` for the sound |
| **Pull-out** | Context before a transition, or a reminder of the whole product | Keyframe to `zoom: 0.8`; the window floats on the grid with a shadow |
| **Dive** | Hand-off into an object that becomes the next shot, usually the header logo into the end card | `exit: {type: dive, box: [...], scale}` followed by an `end` shot |
| **Text card** | Only when footage cannot say it: a hook for a standalone video, a chapter title | `type: card` with `lines` |
| **Still** | A screenshot, diagram or slide given the same camera treatment | `type: image` with an image source |
| **End card** | Logo lockup, typed install command, tagline | `type: end` |

### Transitions

- The **whip** exit (zoom accelerating into motion blur) followed by the **punch** entry (landing from a slightly wider zoom) is the default joint. It makes two clips feel like one camera. Keep them centred.
- **Dive** only into something that continues in the next shot.
- Hard cuts are fine between two holds when the energy is `calm`.

### Highlights

- **Rings:** a rounded outline with a glow around the exact UI element. Use them on chips, rows, numbers and buttons. Stagger them 0.3 to 0.4 s apart, with at most 4 per shot.
- **Pulses:** a ring plus two ripples on a point. Use them on graph nodes, dots and single icons.
- **Colour:** `accent` means "look here". `alert` is for errors and failures only. Never use alert for decoration.

### Captions

- 5 words or fewer, plain, verb-first where possible ("Find where it broke.", "Filter to what matters.").
- One accent word (`*word*`). Use `!word!` (the alert colour) only for failure words.
- They sit in the bottom band, and the band darkens the footage under them. If a caption covers the element it names, reframe the shot so the element sits higher.
- Do not caption what the context already says. Captions explain the UI. They are not the manifesto.

### Sound map

| Visible action | Sound | Engine source |
|---|---|---|
| Cut out of a shot (whip) | Rising whoosh ending on the cut | exit `whip` |
| Landing on a shot (punch) | Short low hit | enter `punch` |
| Frame 0 | Impact plus a light sparkle | `audio.open_hit` |
| Ring appears | Pop (alert ring: low error tap) | `rings` |
| Node pulses | Error tap twice, plus a soft whoosh | `pulses` |
| Cursor click | Click | `clicks` |
| State collapses | Reverse "suck" plus an impact | `collapses` |
| Data streaming, playback | Fine panned ticks | `busy` |
| Big zoom out | Falling whoosh | automatic on a fast pull-out keyframe |
| Dive into a logo | Long rising whoosh | exit `dive` |
| Logo lands | Deep impact, sparkle, chime | `end` shot |
| Command typed | Keys, one per character | `end.command` |
| Tagline | Soft high chime | `end.tagline` |
| Words land on a card | Keys | `card` shot |
| Rhythm | Kick on beats, hat on off-beats; stop it before the dive so the landing hits harder | `audio.beat` |

Anything else goes in `audio.cues` with a `why` that names what is on screen.

### Narration (VO)

1. Write the script to the beat map at about 2.5 words per second. Each beat gets one sentence.
2. Record or source the VO first, then set shot durations to its phrases. The VO leads, the picture follows.
3. Point `audio.vo` at the file. The engine leaves the samples untouched, ducks the SFX by `duck_db` (8 dB by default) under speech, and writes `<name>-vo-only.mp4` next to the full mix.
4. Captions carry key words, not the transcript, unless burned-in subtitles were asked for.

---

## 4. Style variables

Everything visual lives in `style:` and can be shared across many cuts with `extends: style.yaml`.

| Knob | Effect |
|---|---|
| `palette.bg/text/accent/alert/muted` | Every colour in the cut |
| `fonts.display/body/mono` | Captions and cards, tagline, typed command. Use file stems (`Geist-SemiBold`), paths, or `Family@Instance` for variable fonts |
| `grade.black/gain/out_black` | Lifts dark-mode UIs so they read on phones. Set `gain: 1` for an untouched recording |
| `vignette`, `grain` | Finish. Set either to 0 to turn it off |
| `grid.size/strength` | The background grid seen around a floating window |
| `window.radius/shadow` | The rounded recording edge and its drop shadow |
| `caption.size/margin/band/stagger/rise` | Caption type and motion |
| `ring.width/glow/pad/radius` | Highlight look |
| `motion_blur.enabled/max_samples/px_per_sample/shutter` | Blur on camera moves (shutter 1.0 = 360 degrees) |
| `enter`, `exit` | Default transition into and out of every shot |

---

## 5. Energy presets and variations

Set these in `style:` and the shot defaults. They are starting points, not rules.

| | calm | standard | hype |
|---|---|---|---|
| enter punch `from` / `d` | none (hard cut) | 0.5 / 0.3 | 0.4 / 0.25 |
| exit whip `k` / `d` | none | 2.0 / 0.18 | 2.6 / 0.15 |
| playback speed | 1 to 1.3x | 1.5 to 2x | 2 to 3x, ramping |
| hold after landing | 1.2 s | 0.8 s | 0.6 s |
| beat bed | none | 120 bpm | 128 to 140 bpm |
| caption stagger | 0.07 | 0.05 | 0.035 |
| motion blur shutter | 0.6 | 1.0 | 1.0 |

Variations that come up often:

- **Aspect:** change `output.preset`. Coordinates stay in recording pixels. Vertical cuts need tighter `frame:` boxes, because a 16:9 UI is small in a 9:16 frame. Prefer punch-ins over full-app shots.
- **Brand swap:** a new `style.yaml` with that brand's palette, fonts and logo SVG. Shots stay the same.
- **No captions:** delete the `caption` keys. Lean on rings and pulses, and lengthen the holds.
- **Standalone version:** add a `card` hook shot first (1.0 to 1.5 s, 5 to 7 words), and keep everything else the same.
- **Teaser:** cut down to reveal plus payoff plus end card, at 6 to 8 s.

---

## 6. Many recordings, many cuts

- **One style, many cuts.** Keep the brand in `style.yaml` and give each deliverable its own `cut.yaml` that `extends` it.
- **Many recordings in one cut.** List them all under `sources:` and point each shot at one by name. Shots from different recordings join with the same whip and punch, and they stay continuous because the camera language is shared.
- **Many cuts in one go:**
  1. Probe every recording first: `launchcut probe recs/*.mov`.
  2. Write every beat map before directing any of them. This catches overlap between cuts early.
  3. Review all the stills sheets together.
  4. Then render. Renders are independent processes, so run them in parallel, one per cut.
- **Context only, no recording.** Build the cut from `card` and `image` shots. Screenshots, diagrams and the brand logo get the same camera, rings and sound.

---

## 7. Pitfalls we already paid for

- **Screen recordings are variable frame rate.** The engine always decodes through `-vf fps=<fps>`. Do not bypass it, or timings drift.
- **`ffmpeg -v error` hides `volumedetect`.** Measure audio without it. Recordings are often silent (-91 dB), so plan for SFX only.
- **Many ffmpeg builds have no `drawtext`.** All type is drawn with Pillow, so never depend on ffmpeg for text.
- **SVG logos:** the path regex must be `\sd="` or it matches `id="..."` first and draws nothing. The engine handles `M L H V C S Q T Z` (relative and absolute) and fills even-odd. Arcs are approximated.
- **OpenCV 5 wheels can fail to download.** The project pins `opencv-python-headless<5`.
- **macOS recording names contain a narrow no-break space before AM/PM.** Use a glob in `sources:` (`"... 9.57.23*PM.mov"`).
- **Twitter caps video bitrate at about 25 Mbps.** CRF 15 plus grain hit 42 Mbps. Delivery re-encodes with a cap (`max_mbps`).
- **Captions can collide with content in the bottom third.** Frame the element higher, or move the caption timing.
- **Clamping only at zoom >= 1 made the camera jump** at the crossing. The engine clamps continuously, and only when no keyframe floats the window.
- **Pre-multiplied logo colours make dark fringes.** The lockup renderer stores straight alpha.
- **Work in `/tmp` gets lost.** One shipped cut lost its sources that way. Keep projects in a real folder and commit the cut files.

---

## 8. Definition of done

- `PLAN.md` has the brief, beat map, shot list, pacing budget, review log and changelog.
- `cut.yaml` (and `style.yaml`) are committed and reproduce the masters with one command.
- Every technical gate in `out/<name>-qa/report.md` passes, and every editorial box is ticked by someone who did not build the cut.
- Masters are delivered under new version names, with muted and VO-only variants where relevant.
- The requester has the file paths and a one-paragraph summary: what the cut shows, its length, what was decided on their behalf, and what is still open.
