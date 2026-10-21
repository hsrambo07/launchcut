# PLAN: talking-head-v1

Owner: Harsh Singhal · Built with launchcut · 20 Oct 2026

## 1. Brief

| Variable | Value |
|---|---|
| Purpose | Turn a 19 s conversation clip into a tight social cut around one prediction |
| Context | Not given; assumed a Twitter post from Entelligence |
| Already said elsewhere | Unknown |
| Platform | twitter-16x9 at 1280x720 (source is 832x464, so 1080p would only upscale further) |
| Energy | calm: hard cuts, slow pushes, her voice leads |
| Captions | Already burned into the source (word-highlighted), so no new subtitles |
| Sound | Her own audio cut for cut, untouched; SFX at 30 % under speech |
| End card | Entelligence lockup + entelligence.ai (assumption: remove if this is not an Entelligence post) |

## 2. Inventory

`~/Downloads/VID-20260622-WA0004.mp4`: 832x464 H.264 60 fps, 19.2 s, audio -15 dB mean. Two people at a table; she speaks, he listens. Already edited: burned captions in the bottom tenth, a punch-in on him from about 5.9 to 15.3 s (reaction shot), back to wide after. Probe and transcript in `probe/VID-20260622-WA0004/`.

## 3. Beat map (from the transcript)

| # | Source | Words | Viewer learns | Keep? |
|---|---|---|---|---|
| 1 | 0.00 to 4.76 | "allocate five, six engineers per project based on which ones are the priority for your team." | Today: teams are budgeted in headcount | yes, setup |
| - | 4.76 to 5.38 | pause | | cut |
| 2 | 5.38 to 15.12 | "I think we're going to start seeing engineering leaders allocate x amount of money per project and try to estimate and see how good their estimates are on a project-by-project basis." | The prediction: budgets in money, measured per project | yes, payoff |
| 3 | 16.04 to 17.52 | "And then from there, yep." | nothing | cut |

Order kept as spoken: headcount then money is the contrast that makes the prediction land.

## 4. Shot list

| Shot | Dur | Source | Camera | Sound |
|---|---|---|---|---|
| today | 4.95 | 0.00 to 4.95 | wide, slow push 1.00 to 1.07 toward her | her voice |
| prediction | 10.0 | 5.25 to 15.25 | hard cut back to wide, push 1.00 to 1.09, kick on "money" (src 9.82), whip out | her voice, soft hit on the kick, whoosh out |
| end | 2.5 | | Entelligence lockup, entelligence.ai typed | impact, keys |

Burned captions sit at y 385 to 430 of 464, centred: every framing keeps them whole (zoom at most 1.09, centre kept low enough).

## 5. Open

- Context and brand: confirm it is an Entelligence post; otherwise drop the end card.
- A vertical version would need tight crops that cut the burned captions; with the clean source (no burned captions) we can do vertical with word-synced subtitles.

## 6. Changelog

- v1: 19.2 s to 17.45 s; pause and tail cut; slow pushes, kick on "money", end card.
