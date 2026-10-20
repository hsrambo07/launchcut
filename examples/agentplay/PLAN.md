# PLAN: agentplay-launch-v2

Owner: Harsh Singhal · Built with Claude Code · Shipped 14 Oct 2026 (v1, v2) · Rebuilt in launchcut 20 Oct 2026

## 1. Brief

| Variable | Value |
|---|---|
| Purpose | Show AgentPlay replaying a real coding-agent session: what it did, what it cost, where it broke |
| Context | Quote tweet of the AgentPlay launch film ("The future of coding isn't...") |
| Already said elsewhere | The whole story and manifesto. This cut must not repeat it |
| Audience | Developers who use coding agents and have never seen a replay |
| Platform preset | twitter-16x9 |
| Length target (soft) | Asked for "10 seconds maybe"; 14 s after review |
| Energy | standard |
| Brand | Dark UI, Entelligence lime #A4E42A, Geist + Inter, header lockup = Entelligence mark tile + "agentplay" |
| Captions | On, 4 short ones |
| Narration | None. The recording's audio track is silent (-91 dB) |
| Sound | Synthesized SFX + 120 bpm bed |
| End card | Lockup, `$ uvx agentplay`, "Free · Local · Open source" (README) |
| Must hide | Nothing sensitive in the shots used |

## 2. Sources and inventory

| Source | Path | Specs | Audio | Notes |
|---|---|---|---|---|
| main | `~/Desktop/Screen Recording 2026-10-14 at 9.57.23 PM.mov` | 2982x1638 HEVC, 38.8 s, VFR (avg 54 fps) | silent | AgentPlay viewer on the "Fix duplicate charges on Stripe webhook retries" session |

Spikes and windows from the motion profile, then confirmed on stills: main view at 2.4 s, task clicks at 4.0 to 7.6 s, Errors tab at 9.9 s, timeout row clicked at 11.8 s, replay playing 14.2 to 19.5 s, Edits filter collapses the graph at 25.65 s.

## 3. Beat map

| # | Source @ time | On screen | Viewer learns | Keep? |
|---|---|---|---|---|
| 1 | 14.2 to 20.2 | Replay plays, the tool graph grows over its ghost | It replays a whole agent session | yes |
| 2 | 2.6 to 3.9 | Session card: 6 tasks, 4 subagents, 5 errors, 1h 30m, $8.26 | Every task, call and cost is counted | yes |
| 3 | 11.35 to 12.85 | Timeout row clicked, `get_monitor` node lights red | You can find where it broke | yes |
| 4 | 25.2 to 26.7 | Filter chip collapses the graph to the error path | You can filter to what matters | yes |
| 5 | header | AgentPlay lockup in the viewer header | Name + how to get it | end card |
| - | 0 to 2 | Subagent detail view | (too dense for a short) | no |

## 4. Shot list

| Shot | Dur | Source timing | Camera | Highlights | Caption | Sound |
|---|---|---|---|---|---|---|
| replay | 3.5 | 14.2 @ 1.7x | whole app (0.93) → push into graph | none | *Replay* the whole session. | open hit, ticks, beat |
| session | 2.5 | 2.6 @ 0.5x | punch onto the session card, slow drift | 6 tasks, 4 subagents, 5 errors (alert), cost | Every task, call and *cost.* | pops, error tap |
| failure | 2.75 | 11.35, slowed around the click | errors list → follow click to the red node | timeout row (alert), node pulse | Find where it !broke.! | click, error taps |
| filter | 2.5 | 25.2, slowed in the middle | graph, kick on collapse, push, pull out, dive into logo | none | *Filter* to what matters. | click, suck + impact, dive |
| end | 2.75 | none | lockup lands from the dive | none | none | impact, keys, chime |

## 5. Pacing budget

| Shot | entry | highlights | hold | caption | exit | total |
|---|---|---|---|---|---|---|
| replay | 0 (frame 0) | none | 2.8 s of push | 4 words: 1.7 | 0.3 | 3.5 |
| session | 0.3 | 4 x 0.4 = 1.6 | 0.4 + drift | 5 words: 2.0 | 0.2 | 2.5 |
| failure | 0.3 | ring 0.1, click 0.64, pulse 0.75 | 1.2 after the move | 4 words: 1.7 | 0.2 | 2.75 |
| filter | 0.3 | collapse 0.7 | 1.2 | 4 words: 1.7 | 0.6 (pull out + dive) | 2.5 |
| end | 0 | lockup 0.6, command 0.9 | 1.2 | tagline | none | 2.75 |

Total 14.0 s against a soft 10 s target. v1 at 10 s was too fast to follow (see changelog).

## 6. Claims check

| Claim | Source |
|---|---|
| 6 tasks, 4 subagents, 5 errors, 1h 30m, $8.26 | Session card in the recording |
| `uvx agentplay` | Viewer header "Replay your own: uvx agentplay" |
| Free · Local · Open source | AgentPlay README |

## 7. Review log

| Round | Reviewer | Technical | Editorial | Decision |
|---|---|---|---|---|
| v1 | Harsh | pass | Opened with a type hook; the quoted video already carries the words. Beats too fast to understand | redo |
| v2 | Harsh | pass | Product first, readable | shipped |
| rebuild | side by side against the v2 MP4 at 12 moments | pass | identical framing, highlights and captions | example |

## 8. Changelog

- v1 (10 s): hook card "Your agent ran for 1h 30m.", then the four beats at about 1.5 s each.
- v2 (14 s): hook removed, opens on the product (frame 0 = thumbnail). Middles of shots stretched so each beat lands, highlights and holds; whips kept at full speed. Filter framing raised so the caption clears `get_monitor`. Lesson: when a quote tweet carries the story, the clip shows the product; length is soft, readability is not.
- launchcut rebuild: the same cut expressed as `cut.yaml`, reproducing v2.
