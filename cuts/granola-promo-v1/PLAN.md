# PLAN: granola-promo-v1 (v2)

Owner: Harsh Singhal · Built with launchcut · 21 Oct 2026 · Script: `SCRIPT.md` · v1 preserved as `PLAN-v1.md`, `SCRIPT-v1.md`, `cut-v1.yaml`

## 0. Rights (blocker, do not publish until cleared)

- Footage and voice belong to Kevin Stratvert ("Granola AI Tutorial for Beginners", video `-ia0DaaS7Ho`, published 2026-08-06). Publishing this cut needs **a licence from the creator** and, because it is a promo in Granola's name, **Granola's consent** (the original is a Granola-sponsored video; whether Granola holds re-use rights is unknown). Source: `research/brief.md`, Rights and risks.
- If it ships with his voice: credit him on screen and in the post, and keep the sponsorship disclosure. The `end` shot has no credit field, so for now the credit goes in the post copy: "Footage and voice: Kevin Stratvert, from his Granola-sponsored tutorial." An on-screen credit needs either a new end-card field or a small label on S5 (see open questions).
- Fallback if not cleared: brief's plan (music and type only, press-kit screenshots). The labels in this cut survive that; the narration does not.

## 1. Brief

| Variable | Value |
|---|---|
| Purpose | Make someone who has tried bot recorders believe one thing: Granola builds on your notes and keeps them yours, and every generated line can be checked |
| Context | Standalone X and LinkedIn post, nothing around it (ASSUMED in the brief) |
| Already said elsewhere | Nothing |
| Audience | People in back-to-back meetings who have tried Otter, Fireflies or Fathom |
| Sources | `main`: `~/Downloads/Granola AI Tutorial for Beginners_206_291.mp4`, 640x360, 29.97 fps, 85 s. **Needs `enhance: 2`** in `sources` (RULES rule 12; `cut-v1.yaml` lacks it). Logo: `brand/logos/Granola_lockup_black_lg.png`. Style: `style.yaml` |
| Platform | twitter-16x9 at 1280x720, 30 fps (from `style.yaml`) |
| Length | 23.44 s (target 20 to 30) |
| Energy | calm: locked holds, soft 0.22 s dissolves, two hard joints inside continuous takes, one deliberate eased camera move (S3). No whips, no punches, no drift |
| Hook | H2 "Result first" from `research/hooks.md`: labelled note at frame 0, narrator enters at 2.00 s |
| Narration | The tutorial narrator, four whole phrases, `audio.dialog: true`, speed 1 |
| Subtitles | Word-synced, plate style, every spoken word |
| Captions | One: "See where it came from." (S3, narrator muted there) |
| Sound | Narration plus a sparse, low SFX bed tied to rings, clicks, keys and the end card |
| End card | Official black lockup, URL pill "granola.ai", line "The AI notepad for back-to-back meetings" |
| Hide | Share link (source 0 to 10.5 s), extension nag (1.5 to 5.8 s), fine print at source y about 352 to 358 in the scrolled view, black frames from 84.0 s. None of these is in any frame box below |

## 2. Structure

**T2 The Standalone Hook, stretched to LinkedIn length** (launch-craft section 2): hook, the answer, proof, payoff, end card. Why: the post stands alone, so the opening has to carry the idea by itself, and the brief's T3-lite (one promise, two proofs, end card) is T2 with longer holds. Not T3: interstitial type cards would fight a calm, product-first brand and the owner's "UI at frame 0" taste. P5 (output first) shapes the hook: the finished note comes first, the tool that made it comes after.

The hook is already the payoff, so the film escalates rather than reveals: claim (black vs grey), then can I trust the grey (magnifier), then is it still mine (edit turns a grey line black).

## 3. Beat map

| # | Source @ time | What happens on screen | What the viewer learns | Proof on screen |
|---|---|---|---|---|
| B1 | 53.00 to 57.60 | Finished note, two labels; narrator: "Instead of replacing my notes, it builds on them." | Your lines are black, Granola's additions are grey, both in one note | Black and grey lines side by side, labelled (allowed claims 1, 3, 5) |
| B2 | 67.20 to 69.60 | Scrolled to Responsibilities; Elizabeth's grey line ringed and labelled; "If I want more context about something," | This line was generated, so you might want to check it | Grey tone of the line, "Granola generated" label |
| B3 | 70.60 to 73.86 | Click the magnifying glass beside that line; popover opens | Every generated line has a source | Cursor, click, popover (claim 6) |
| B4 | 73.86 to 78.40 | "TRANSCRIPT SUMMARY" holds; "...a transcript summary of the relevant part of the conversation." | The source is the conversation itself | The popover card, header re-set crisp |
| B5 | 79.00 to 83.74 | Edit a grey line; it turns black; "...type in my changes." | You stay in charge; edited lines are yours | Line flips grey to black at 82.1 (measured: darkest-5% ink 143 to 100) (claim 17) |
| B6 | end card | Lockup, granola.ai, category line | Who it is and where to get it | Official lockup, verbatim H1 |

## 4. Engine facts the producer needs (read before writing cut.yaml)

1. **Every `frame:` keyframe below needs `pad: 0`.** The default pad is 0.08, which would render a 512x288 box at zoom 1.08 instead of 1.25. All boxes below are the exact visible area, 16:9. Zoom = 640 / box width (cover scale is 2.0 screen px per source px at 1280x720).
2. **Muted shots.** `dialog_track` only plays shots with a dict `src` at speed 1. S1a uses a piecewise `src` (a freeze), so set `sound: mute` explicitly. S3 is also `sound: mute`.
3. **Subtitles pick words by midpoint inside each shot's source window.** S1a's window holds "from the conversation." and S3's holds "...I'll click on the magnifying glass,", so both need `subtitles: false`. S5 must end at or before 83.74: the transcript has a stray "is." (83.66 to 83.84, midpoint 83.75) that would otherwise be subtitled; a `fix` entry cannot blank it.
4. **Labels** are pills sized in screen px (about 44 px tall at size 50, 720p), taller than one line pitch of the note. Every anchor below was chosen where the lines above and below are short in x. `until` removes a label with no fade.
5. **Joints.** `style.enter` is a 0.22 s dissolve. S1b and S4 continue the previous shot's take with the same framing and must set `enter: none` (the joint is invisible). A dissolve blends from the previous shot's frozen last frame, so it adds no length.
6. **End card stacking is fixed by the engine:** lockup at `y`, URL pill at y + 244, tagline at y + 400 (px at 1080). The copy is written to that order.
7. Eases: brand easing `cubic-bezier(.16,1,.3,1)` is ease-out-expo, so camera moves use `ease: outExpo`.

Subtitles block (recommended):

```
subtitles:
  transcript: probe/Granola_AI_Tutorial_for_Beginners_206_291/transcript.json
  style: plate          # ink on paper
  words: 5              # every phrase then splits cleanly at its comma (see SCRIPT.md)
  gap: 0.3
  mode: highlight
  size: 54              # 36 px at 720p
  y: 1005               # plate spans about screen y 641 to 699 at 720p
  hold: 0.4
  emphasis: [builds, transcript, changes]
```

With `y: 1005` the plate sits over source y 281 to 305 in S1b (the grey "Enough time..." and "Production begins..." lines; no label there), over the "Continue chat" bar in S2 to S5, which is the point.

## 5. Shot list

Coordinates are source px (640x360). Shot times are seconds from the shot start; cut times in brackets. Label style codes: **INK** = `fill: "#292929"`, `color: "#f7f7f2"`, `edge: "#292929"` (mirrors a black line, means "yours"). **GREY** = `fill: bg`, `color: "#72726e"`, `edge: "#acada8"` (mirrors a grey line, means "Granola's"). **PLAIN** = `fill: bg`, `color: text`, `edge: accent`. All labels `size: 50`, `font: display` (Hanken Grotesk SemiBold). Ring colour `accent` (`#5b6f00`) unless stated.

### S1a `poster` [0.00 to 1.92]
- type ui, source main, duration **1.92**, `sound: mute`, `subtitles: false`, first shot (no enter).
- src (piecewise, freeze then play): `[[0, 53.00], [0.50, 53.00], [1.92, 54.42]]`. Frame 0 at 53.00 is verified clean (no cursor, no selection, no toolbar; the cursor sits at about (282, 343), below the box, and only enters the bottom edge after 54.4).
- camera: locked, `{t: 0, frame: [83, 25, 595, 313], pad: 0}` (zoom 1.25). Heading "Product Launch Planning" (x 137 to 317, y 31 to 48) through "Production begins next week" (y 296 to 306) in frame.
- labels, both present at frame 0 (`at: -0.6` so the 0.4 s rise has finished):
  - L1 "What I wrote", INK, `anchor: [229, 108]`, `side: right`. Sits right of the black line "Finalize the recipe" (text x 147 to 225, y 103 to 113). Pill about x 233 to 330, y 99 to 117.
  - L2 "Granola generated", GREY, `anchor: [406, 125]`, `side: right`. Right of the grey line "Taste test feedback: mostly positive, two consistent themes" (x 147 to 402, y 120 to 130). Pill about x 410 to 541, y 116 to 134. Neighbours: "Finalize the recipe" ends x 225 above, "More chocolate in every bite" ends x 278 below, so no overlap.
- Measured tones at 55.0: black lines darkest-5% ink about 100, grey lines about 150. The pair are adjacent lines, so the tone contrast is visible right next to the labels.
- sound: `audio.cues` `{t: 0.05, sound: chime, gain: 0.15, why: "labelled poster frame"}`.

### S1b `builds` [1.92 to 5.10]
- type ui, duration **3.18**, `src: {start: 54.42, speed: 1}` (54.42 to 57.60), `enter: none` (same take as S1a).
- Heard: "Instead of replacing my notes, it builds on them." Cut points sit in measured dips: 54.42 (-74 dB, onset 54.50), 57.60 (-64 dB, "them." decays by 57.56).
- camera: locked, `{t: 0, frame: [83, 25, 595, 313], pad: 0}`.
- labels: L1 and L2 repeated with `at: -1`, `until: 2.88` (src 57.30, the start of the tutorial's scroll).
- Known: the tutorial scroll starts at src 57.33 (motion 1.2 at 57.3, 9.2 at 57.4), so the last 0.27 s shows the page starting to glide up, then S2 dissolves in. Labels drop at 2.88 so they never ride the scroll. Check in stills (open question 3).
- Word times (shot-local): "Instead" 0.08 (speech onset), "notes," 1.62, "builds" 2.26, "them." 2.82.

### S2 `context` [5.10 to 7.50]
- type ui, duration **2.40**, `src: {start: 67.20, speed: 1}` (67.20 to 69.60), enter: default dissolve 0.22.
- Heard: "If I want more context about something," (dips at 67.22, -66 dB, and 69.60, -54 dB).
- camera: locked, `{t: 0, frame: [24, 8, 616, 341], pad: 0}` (592x333, zoom 1.08). Bottom 341 keeps the fine print (y 352 to 358) out.
- rings: `{box: [145, 188, 476, 214], at: 0.92}`, Elizabeth's line "Elizabeth: coordinate with production, update packaging artwork, liaise with print vendor, create social media posts, coordinate with retail partners" (grey, measured ink 140), on "context" (src 68.12).
- labels: L3 "Granola generated", GREY, `anchor: [300, 187]`, `side: above`, `at: 1.32`. Pill about x 224 to 376, y 162 to 183, clear of "Responsibilities" (x 137 to 208) and "Production begins next week" (y 144 to 153).
- Word times: "If" 0.06, "context" 0.92, "something," 1.84 to 2.36.

### S3 `magnifier` [7.50 to 10.76]
- type ui, duration **3.26**, `src: {start: 70.60, speed: 1}` (70.60 to 73.86), `sound: mute`, `subtitles: false`, enter: default dissolve 0.22.
- camera, the one deliberate move in the film: `{t: 0, frame: [24, 8, 616, 341], pad: 0}` then `{t: 0.80, frame: [66, 58, 578, 346], pad: 0, ease: outExpo}` (zoom 1.08 to 1.25, toward the magnifier). Locked after 0.80.
- On screen: cursor on Elizabeth's line at about x 250, reaches the magnifier at 1.00 (src 71.6), clicks at 1.70 (src 72.3), skeleton loader 1.90 to 2.70, text streams from 2.80 (src 73.4).
- rings: `{box: [494, 188, 506, 200], at: 1.05, until: 1.80, radius: 14}` on the magnifying glass at (500, 194). A ring, not a pulse: pulses sound as error taps.
- caption: `{text: "See where it *came from.*", in: 0.85, out: 3.20}` (5 words, style caption font serif). It sits over the card's bottom padding and the chat bar; the card's body text ends at y 297, clear.
- clicks: `[1.70]`. busy: `[[2.80, 3.26]]`.
- LinkedIn payoff check: the click lands at 9.20 in the cut, the answer is on screen by 10.3.

### S4 `summary` [10.76 to 15.30]
- type ui, duration **4.54**, `src: {start: 73.86, speed: 1}` (73.86 to 78.40), `enter: none` (same take as S3).
- Heard: "and here I could see a transcript summary of the relevant part of the conversation." (start in the dip after "glass," at 73.82 to 73.86, -50 dB; end in silence at 78.40, -83 dB, before the popover closes at 78.5).
- camera: locked, `{t: 0, frame: [66, 58, 578, 346], pad: 0}`.
- rings: `{box: [200, 205, 508, 318], at: 1.28, radius: 12}`, the whole popover card, on "transcript" (src 75.14).
- labels: L4 "TRANSCRIPT SUMMARY" (exact case on screen), PLAIN, `anchor: [296, 218]`, `side: right`, `at: 1.72` on "summary" (src 75.58). Header text is x 210 to 293, y 215 to 222; pill about x 300 to 452, y 209 to 227, inside the card's header row, above the body (y 233).
- Word times: "and" 0.28, "transcript" 1.28, "summary" 1.72, "conversation." ends 4.38.

### S5 `yours` [15.30 to 20.04]
- type ui, duration **4.74**, `src: {start: 79.00, speed: 1}` (79.00 to 83.74), enter: default dissolve 0.22 (reads as the popover closing in place).
- Heard: "If I want to make any edits to these notes, here I could click in and type in my changes." (start in the dip at 79.00, -54 dB; end at 83.74, after "changes." and before the stray "is.").
- camera: locked, `{t: 0, frame: [66, 58, 578, 346], pad: 0}` (same as S4).
- On screen: cursor travels to "Production begins next week" (x 157 to 281, y 144 to 153) and clicks in at 1.90 (src 80.9). "ideally by Tuesday" appears at 2.90 (src 81.9) and the whole line turns black at 3.10 (src 82.1). Final line "Production begins next week ideally by Tuesday" spans x 157 to 362.
- rings: `{box: [153, 141, 366, 157], at: 1.14}` on "edits" (src 80.14), enclosing the line and the space the typed words will fill.
- labels: L5 "ideally by Tuesday" (exact string), INK, `anchor: [323, 157]`, `side: below`, `at: 3.20`, just after the line turns black and before "type in my changes" (3.74). Pill about x 254 to 392, y 161 to 178, clear of "Responsibilities" (x 137 to 208) and Elizabeth's line (y 190).
- clicks: `[1.90]`. Keys: `audio.cues` at cut 18.20, 18.26, 18.32, `{sound: key, gain: 0.25, why: "ideally by Tuesday appears in the line"}`.
- Word times: "If" 0.04, "edits" 1.14, "notes," 2.06 to 2.30, "click" 2.90, "type" 3.74, "changes." ends 4.72.

### E `end` [20.04 to 23.44]
- type end, duration **3.40**, enter: default dissolve 0.22 (from S5's last frame).
- lockup: `{image: brand/logos/Granola_lockup_black_lg.png, width: 600, y: 430}`. Settles 0.12 to 0.62 (engine default, ease out expo).
- command: `{text: "granola.ai", prefix: "", at: 1.05, cps: 20}` (pill at y 674; typed by 1.68).
- tagline: `{text: "The AI notepad for back-to-back meetings", at: 0.55, size: 46, font: serif}` (y 830).
- glow: 0 (no green haze on the paper).
- Rendered top to bottom: lockup, granola.ai, category line. One action only.

### Audio block

```
audio:
  dialog: true
  sfx: true
  gain: 0.35
  open_hit: false
  beat: null
  cues:
    - {t: 0.05, sound: chime, gain: 0.15, why: "labelled poster frame"}
    - {t: 18.20, sound: key, gain: 0.25, why: "ideally by Tuesday appears in the line"}
    - {t: 18.26, sound: key, gain: 0.25, why: "ideally by Tuesday appears in the line"}
    - {t: 18.32, sound: key, gain: 0.25, why: "ideally by Tuesday appears in the line"}
```

Sound map: rings pop (S2 6.02, S3 8.55, S4 12.04, S5 16.44), clicks (9.20, 17.20), ticks while the popover streams (10.30 to 10.76), keys (18.20), end card landing, URL keys and tagline chime. Nothing under a spoken word is louder than a pop at gain 0.35. Each narrator joint is cut inside a measured dip, 8 ms engine fades.

## 6. Pacing budget

RULES formula: land, highlights 0.4 s apart, hold at least 0.8 s after the last, read time 0.3 s per word + 0.5 s.

| Shot | Dur | Land | Highlights | Hold after last | On-screen text, read time needed / given | Fits |
|---|---|---|---|---|---|---|
| S1a + S1b | 1.92 + 3.18 | frame 0 (no move) | labels present from 0 | 4.80 s of labels | 5 words, 2.0 / 4.80 | yes |
| S2 | 2.40 | 0.22 (dissolve) | ring 0.92, label 1.32 (0.40 apart) | 1.08 | 2 words, 1.1 / 1.08 | yes (subtitles carry the line) |
| S3 | 3.26 | 0.80 (move ends) | ring 1.05, click 1.70 | 1.56 after click | 5 words, 2.0 / 2.35 | yes |
| S4 | 4.54 | 0 (continuous) | ring 1.28, label 1.72 (0.44 apart) | 2.82 | 2 words, 1.1 / 2.82 | yes |
| S5 | 4.74 | 0.22 (dissolve) | ring 1.14, label 3.20 | 1.54 | 3 words, 1.4 / 1.54 | yes |
| E | 3.40 | 0.62 (lockup settles) | line 0.55, URL 1.05 | 1.72 after URL typed | 7 words, 2.6 / 2.85 | yes |
| **Total** | **23.44** | | | | | |

Magnification: maximum zoom 1.25 of cover = 2.5 screen px per source px, under the 3x gate. Source is enhanced 2x once (`enhance: 2`). No shot frames tighter than 512x288 source px.

Readability at 360 px wide: UI body text does not read at phone size (about 6 px). What reads: the slab heading, black vs grey tone, labels (33 px at 720p, about 9 px at 360 wide), caption and subtitles (36 px at 720p). Check `phone-width.png`; if the labels are too small, raise to `size: 56` and re-check the pill clearances listed above.

## 7. Open questions

1. **Rights** (section 0): creator licence and Granola consent before publishing. Credit Kevin Stratvert in the post; an on-screen credit needs an engine field (a small `credit` line on the `end` shot) or a PLAIN label on S5. Producer's call; post copy is the default.
2. **Brand within 3 s vs logo only on the end card.** The logo stays on the end card as briefed. Brand presence before 3 s is carried by the word "Granola" in the "Granola generated" label at frame 0 and by the product's own slab heading.
3. **Hook exit.** The tutorial's scroll shows for 0.27 s (cut 4.83 to 5.10) after the labels drop at 4.80. Judge it in the stills loop. If it reads as a glitch rather than a glide, end S1b at 57.60 anyway (the word needs it) and shorten the S2 dissolve to 0.15 s; do not cut into "them."
4. **Label size and colour** on a phone: GREY labels use `#72726e` text on paper (about 4.7:1). If they read too faint at 360 px, keep the grey edge and switch the text to ink.
5. **CTA wording.** The URL pill types "granola.ai". Granola's own button says "Download for free"; the engine's pill is a mono command pill, which suits a URL better. Swap if the requester prefers the button wording.
6. **"is." tail.** S5 ends at 83.74. Listen to the last 50 ms; if a syllable of "is" is audible, end at 83.72.
7. **No-voice fallback** if the licence fails: keep S1a with labels "My notes" / "Enhanced" (hooks.md H2 fallback; note "Enhanced" names the whole view), mute all shots, carry B2 to B5 with captions only.

## 8. Changelog

- v1: 85 s tutorial cut to a 50 s promo; cold open on "Instead of replacing my notes, it builds on them."; dark palette, plain-type end card.
- v2: rebuilt to 23.44 s for a standalone X/LinkedIn post (brief: v1 was too long, generic beat 2, proved the wrong thing, no brand, no CTA). Hook H2 result-first: labelled note at frame 0, narrator at 2.00 s. Proofs changed from decisions and owners to the two things only Granola shows: trace a grey line to its transcript summary, and an edited grey line turning black. Light paper look from `style.yaml`, locked holds at zoom 1.08 to 1.25 with one eased move, soft dissolves, crisp re-set labels, plate subtitles, official lockup and verbatim H1 on the end card, `enhance: 2`. Rights blocker recorded.

## 9. Review log

| Date | Phase | Reviewer | Input | Verdict | Fixes |
|---|---|---|---|---|---|
| 2026-10-21 | 3, stills | lc-art-director | `out/stills/granola-promo-v2_*.png` (0.0, 3.5, 5.05, 6.8, 8.6, 9.6, 12.6, 16.8, 19.2, 20.15, 22.5 s), full size and at 360 px wide | **REVISE** | (1) S1a `poster` 0.0, S1b `builds` to 4.80, S2 `context` 6.42: all three "Granola generated" labels to `fill: "#eaebe5", edge: "#eaebe5", color: "#292929"` (Granola's neutral-200 chip; today grey text on paper reads as another note line at 360 px and the edge shows only as corner brackets). (2) E `end` 22.5: `tagline: {..., size: 56, color: text}` (the verbatim H1 is ink on granola.ai, now a small grey footnote), `lockup.y: 380` (block sits about 40 px low at 720p), and `style.fonts.mono` to JetBrains Mono, Granola's VERIFIED mono (download to `brand/fonts/` first; Menlo is not their face). (3) S3 `magnifier` 8.35 to 10.70: `caption.size: 48` and `style.caption.margin: 50` ("from." runs into the "Write follow up email" chip and at 9.6 sits on the popover's bottom edge). (4) S4 `summary` 12.48: label to `anchor: [258, 219], size: 32, fill: "#ffffff", edge: "#ffffff"` (size 44 is a sticker: pill end lands on the card ring at x 333, text starts 14 px left of the body copy, green corner brackets). (5) Subtitles, 2.0 to 20.0: `active: text` (karaoke green on "my", "to", "of" is the generic look; engine routes `emphasis` through `active` too, so drop `emphasis` and keep green for rings and the caption accent). Non-blocking: S5 ring box right edge 366 to 380 (typed "Tuesday" and the I-beam touch the ring at 19.2); `style.ring.glow: 0` (magnifier ring is a lime blob at 8.6); subtitle plate is about 5 px off the frame bottom, left as is because every other `y` slices a note line in S1b. Engine note: `draw.pill()` draws an edge only on the rounded corners (straight runs never erode at the mask boundary), so every label needs `edge` equal to `fill` until fixed; the subtitle plate and end-card URL pill show the same brackets and are not fixable from yaml. Logo handling is correct (official black lockup on paper, clear space, no recolour). |
| 2026-10-21 | 4, full render | lc-critic | `out/granola-promo-v2.mp4` (23.43 s), `out/granola-promo-v2-qa/` (report, strip-5fps, phone-width, cuts, thumbnail-frame0), frames at 0.0, 3.0, 4.95, 5.2, 6.6, 8.6, 9.6, 12.7, 18.6, 19.6, 20.15, 22.5 s, re-transcript `/tmp/lc-critic/granola-promo-v2/`, per-0.1 s RMS of mix, voice and sfx stems, sfx spectrogram 19.5 to 23.4 s, v1 frames at 0 and 20 s | **REVISE, 79/100** (hook 13, clarity 13, craft 13, brand 15, quality 12, truth 13) | (1) S5 `yours` 18.50 to 20.04: the label "ideally by Tuesday" repeats words already legible in the line, so muted the payoff ("an edited grey line is yours") rides only on a subtle tone flip. Change to `{text: "What I wrote", anchor: [323, 157], side: below, at: 3.20, size: 50, fill: "#292929", color: "#f7f7f2", edge: "#292929"}` so it rhymes with frame 0 (true: the whole line renders black, claim 5 and 17). (2) E `end` 20.04 to 23.44, engine/plan change: `sfx.py` hard-codes `b.impact(2.0, 62, 32)` at gain 1.0 (line 174) plus an 82 Hz `drone` bed for the whole card. Measured: sfx stem -19 dB RMS at 20.0 and about -34 dB held to 23.2, against -34 dB for every ring pop; spectrogram is 20 to 170 Hz rumble. A boom and drone on a calm brand, and the plan promised a "soft landing". Gate both the impact and the drone behind a new `audio.end_hit` (default true, like `open_hit`), set `end_hit: false`; the stem is peak-normalised, so then lower `audio.gain` until ring pops still measure about -34 dB RMS in `-sfx.wav`. (3) Joins: `context` add `enter: none` (5.10 dissolve blends two text pages at zoom 1.25 and 1.08 mid-scroll, ghosted text at 5.2) and `end` add `enter: none` (at 20.15 the lockup settles over readable note text and the S5 label; with `none` it cuts to paper and the lockup fades in over 0.35 s). (4) Rights, conditional on the licence (answers open question 1, since `end()` draws no labels or captions): on `yours` add `{text: "Footage and voice: Kevin Stratvert, Granola-sponsored tutorial", anchor: [322, 64], side: over, at: 0.3, size: 28, fill: bg, color: muted, edge: bg}` over the clipped top strip. Open questions closed: Q3, the 0.27 s scroll before 5.10 reads as a glide under a dissolve but as a small jump with fix 3; acceptable either way, keep 57.60 because "them." ends at 57.56. Q6, voice stem is -18 dB at 19.9, -27 at 20.0, silent by 20.1 and the re-transcript has no "is", so 83.74 stands. Non-blocking: re-transcript hears "here I can see" and "here I can click" where subtitles say "could" (11.46, 18.10); listen, and if it is "can" set `subtitles.fix: {granola: Granola, could: can}`. Both labels at frame 0 departs from hooks.md H2 (second label at 0.6 s), a fair trade for a complete poster. v1 problems: dark look fixed (paper, official lockup), length fixed (23.4 vs 50 s), soft text partly fixed (labels and header re-set crisp, max zoom 1.25, encode transparent against the FFV1 master); body UI text stays source-limited at 360p, not a regression. Every spoken phrase is whole at every join; claims all trace to allowed claims 1, 3, 5, 6, 7, 17. |
