# cut.yaml reference

All times inside a shot are seconds from the start of that shot. All coordinates are pixels of the source recording or image, so a cut survives any change of output size. Sizes in `style` are pixels at 1080p and scale with the output.

```yaml
name: my-cut                     # used for every output file name
extends: ../style.yaml           # optional: deep-merged first, this file wins

output:
  preset: twitter-16x9           # twitter-16x9 | twitter-1x1 | vertical-9x16 | feed-4x5 | linkedin-16x9 | web-16x9
  # size: [1920, 1080]           # any preset value can be overridden
  # fps: 60
  # max_mbps: 18                 # delivery video bitrate cap
  # lufs: -14                    # loudness target
  dir: out                       # relative to this file
  deliver_to: null               # optional folder that receives a copy of the masters
  crf_master: 15
  crf_delivery: 18
  normalize: true                # loudness-normalise delivered audio

sources:                         # any number; images work too (png, jpg, webp)
  main: "~/Desktop/Screen Recording 2026-10-14 at 9.57.23*PM.mov"   # globs allowed
  settings: recordings/settings.mov
  diagram: assets/architecture.png

style:                           # see RULES.md section 4 for what each knob does
  palette: {bg: "#141415", text: "#F2F2F0", accent: "#A4E42A", alert: "#F26858", muted: "#A5A5A5"}
  fonts: {display: Geist-SemiBold, body: Geist-Medium, mono: GeistMono-Medium}
  grade: {black: 0, gain: 1.0, out_black: 0}
  vignette: 0.22
  grain: 2.2
  grid: {size: 96, strength: 9}
  window: {radius: 24, shadow: 0.6}
  caption: {size: 78, margin: 74, band: 0.82, stagger: 0.05, rise: 30, font: display}
  ring: {width: 3.0, glow: 0.45, pad: 8, radius: 16}
  motion_blur: {enabled: true, max_samples: 14, px_per_sample: 2.5, shutter: 1.0}
  enter: {type: punch, d: 0.3, from: 0.5}     # default entry for every shot but the first
  exit: {type: whip, d: 0.18, k: 2.0}         # default exit for every shot but the last

audio:
  sfx: true
  gain: 1.0
  open_hit: false                # impact on frame 0
  beat: {bpm: 120, from: 0.0, to: 10.0}       # or null
  vo: null                       # narration file; never altered, SFX ducked under it
  duck_db: 8
  seed: 7
  cues:                          # extra sounds; every one should name what it is for
    - {t: 4.2, sound: chime, gain: 0.3, pan: 0.2, why: "PR opened badge"}
    # sounds: whoosh whoosh_down suck impact hit pop click tick err chime key sparkle drone kick hat

allow_dark_frames: false         # renderer aborts on a black frame unless this is true

shots: [...]                     # played in order; each shot's duration sets the edit
```

## Shot: `ui` (a recording) and `image` (a still)

```yaml
- id: failure
  type: ui                       # or image
  source: main                   # key from sources
  duration: 2.75
  src: {start: 11.35, speed: 1.0}            # source time = start + t * speed
  # src: [[0, 11.35], [0.3, 11.65], [2.55, 12.65], [2.75, 12.85]]   # piecewise: ramps, slow-mo, freezes
  enter: punch                   # punch | none | {type: punch, d: 0.3, from: 0.5}
  exit: whip                     # whip | none | {type: whip, d, k} | {type: dive, box: [x0,y0,x1,y1], d: 0.32, scale: 4.4}
  clamp: auto                    # keep the view inside the recording; auto = on unless a keyframe floats the window
  camera:                        # keyframes; the ease on a keyframe shapes the move INTO it
    - {t: 0.0, zoom: 2.2, center: [640, 960]}
    - {t: 0.86, zoom: 2.35}                               # center carries over from the previous keyframe
    - {t: 1.54, frame: [900, 640, 1320, 960], pad: 0.08, ease: inOutCubic}   # frame a box instead of zoom + center
    - {t: 2.6, scale: 2.5, center: [1110, 800], ease: linear}                # scale = screen px per recording px
    - {t: 3.0, zoom: 0.8, tilt: [12, -6], anchor: [142, 67]}                # tilt in degrees; anchor keeps a point on a straight screen path
  kicks: [{at: 0.7, amount: 0.06, decay: 14}]   # quick zoom bump on a state change
  rings:
    - {box: [40, 1042, 639, 1144], at: 0.12, color: alert, pad: 4, radius: 22, until: 2.0}
  pulses:
    - {point: [1151, 787], at: 0.75, color: alert, r: 26}
  caption: {text: "Find where it !broke.!", in: 0.2, out: 2.61, size: 78, font: display}
  clicks: [0.64]                 # SFX only: cursor clicks
  collapses: [0.7]               # SFX only: state collapses
  busy: [[0.3, 3.1]]             # SFX only: data ticks while something streams
```

`zoom` is relative to *cover*: 1.0 means the recording just fills the frame, below 1 the window floats on the background with rounded corners and a shadow, `contain` shows all of it. Eases: `linear inCubic outCubic inOutCubic inExpo outExpo inOutExpo outBack inOutSine`.

Caption markup: `*accent words*`, `!alert words!`. Markers can span several words.

## Shot: `card` (type on the background)

```yaml
- id: hook
  type: card
  duration: 1.3
  lines: ["Your agent ran for *1h 30m.*"]   # one or more lines, same markup as captions
  size: 104
  sub: "Watch every step it took."          # optional smaller line
  in: 0.0                                   # words start landing here, 0.06 s apart
  out: null                                 # optional fade out time
  camera: [{t: 0, zoom: 1.0}, {t: 1.3, zoom: 1.04, ease: inOutSine}]   # default: a slow push
```

## Shot: `end` (lockup, command, tagline)

```yaml
- id: end
  type: end
  duration: 2.75
  lockup:
    mark: assets/mark.svg        # svg (recoloured with mark_color) or png (kept as is)
    mark_color: "#C4DE96"
    tile: {color: "#2C343A", radius: 0.22}   # omit for a bare mark
    wordmark: agentplay
    font: "InterVariable@SemiBold"
    word_color: text
    width: 800                   # final lockup width in px at 1080p
    y: 430                       # final lockup centre y in px at 1080p
  command: {text: "uvx agentplay", prefix: "$ ", at: 0.45, cps: 33}   # typed in a pill
  tagline: {text: "Free · Local · Open source", at: 0.92, size: 46}
  glow: 0.10
```

If the previous shot exits with `dive`, the lockup starts at exactly the size and place the dive ended on and settles into its final position, so the logo in the product becomes the logo on the card.
