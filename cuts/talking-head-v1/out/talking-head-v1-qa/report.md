# QA: talking-head-v1

File: `/Users/harshsinghal/Documents/projects/launchcut/cuts/talking-head-v1/out/talking-head-v1.mp4`

## Technical gates

| result | gate | detail |
|---|---|---|
| PASS | codec | h264 yuv420p |
| PASS | size | 1280x720 (preset 1280x720) |
| PASS | frame rate | 60 fps |
| PASS | duration | 17.450s (cut 17.450s) |
| PASS | bitrate | 2.3 Mbps overall (cap 18 video) |
| PASS | loudness | -14.2 LUFS (target -14.0) |
| PASS | true peak | -2.8 dBFS |
| PASS | no black frames | 0 black segments |
| PASS | frame 0 reads as a thumbnail | mean luma 86, contrast 34 |

## Editorial gates (a reviewer who did not build the cut ticks these)

Open `strip-5fps.png`, `phone-width.png` and `thumbnail-frame0.png`, then watch the file once muted and once with sound.

- [ ] Frame 0 shows the thing we are launching and works as the post thumbnail
- [ ] Muted, at phone width, a first-time viewer can say what each beat showed
- [ ] Every caption names something that is on screen at that moment
- [ ] Every highlight lands on the thing the caption names, and holds long enough to read
- [ ] Every claim (numbers, free, open source, commands) traces to the recording, the README or the brief
- [ ] Nothing moves without a reason; transitions stay centred
- [ ] Every sound is tied to something visible; nothing clips; VO (if any) is untouched and clear over SFX
- [ ] The cut fits its context (what the post or the quoted post already says is not repeated)
- [ ] Logo, colours and type match the brand files
