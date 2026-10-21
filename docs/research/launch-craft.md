# Launch craft: what makes short launch and demo videos work

A craft guide for launchcut director agents. It extends `RULES.md` and never overrides it. Where this file and `RULES.md` disagree, `RULES.md` wins.

How this was built: ten real launch films were downloaded and broken down frame by frame (1 fps contact sheets, 4 fps sheets of the first 4 seconds, ffmpeg scene-cut counts, auto subtitles for narration). Those observations are first-hand and marked **[observed]**. Claims taken from blogs and creator posts are marked **[secondary]**, and statistics that only appear in vendor blogs without a primary study are marked **[unverified]**. Do not quote an unverified number in a video or a post.

Sourcing status: platform numbers (section 1b) come from a dedicated pass over the platforms' own pages. OFFICIAL means fetched from the platform page, SNIPPET means the official page blocked fetching and the figure comes from its search excerpt, so confirm it in the ad manager before treating it as a hard gate. Three further passes (named film studios, hook practitioners, Apple and studio craft) had not reported when this was written; the hook library rests on the observed films plus widely taught patterns, not on cited practitioner frameworks.

---

## 0. The ten films, second by second [observed]

| Film | Length | Frame 0 | First product UI | Cuts (scene > 0.1) | Voice | End |
|---|---|---|---|---|---|---|
| Linear, "Introducing Linear for Agents" | 33 s | Dark, "Linear for Agents" blurs in | 1.5 s | ~0 hard cuts, blur dissolves | Music only | Logo at 29 s |
| Linear, "Introducing Linear Agent" | 55 s | Real UI, tilted in 3D perspective | 0 s | 4 | Music only | "Linear. At your command." then logo |
| Arc 1.0, "Everything or nothing" | 34 s | Archival plane launch that crashes | 26 s | 26 | Music only | "Today", logo on blue, "download now", "arc.net" |
| Arc on Windows | 37 s | Windows 95 PC, then extreme close-ups | 16 s | 60 | Archival VO sample | "Arc is on Windows", "Download now", "arc.net" |
| Cursor 2.0 | 64 s | 3D logo cube settles into "2.0" | 11 s | 9 | Music only | Cube, then wordmark on black |
| Notion, "Meet the new Notion AI" | 57 s | Logo with a cursor gliding to it | 13 s (as cards) | 21 | Music only | "Try Notion AI for free at Notion.com", "Think it. Make it.", logo |
| Superhuman, "Superhuman's got your back" | 62 s | CEO to camera, mid-sentence | never | 15 | VO, ~150 words | "AI that works where you work.", logo, URL |
| Framer, "All Design, No Code, Real Websites" | 37 s | A button being typed: "Get started for f" | 0 s | 15 | VO, ~70 words | Publish button click, logo |
| Vercel, "Introducing v0" | 48 s | v0 logo draws on | 3 s | 4 | Music only | v0.dev, Vercel lockup |
| Loom, "Work Faster and Smarter with Loom AI" | 38 s | Loom bubble over a product demo | 0 s | 3 | Music | "Loom AI" on brand purple |

Beat notes worth stealing:

- **Linear for Agents (33 s).** 0 to 1.5 s title blurs in on the app's own near-black. 1.5 s cut to a tight crop of the backlog list, no window chrome, rows cropped by the frame edge. 2 to 8 s: select issues, open "Assign to", pick an agent from a menu. 8 to 15 s: the agent's reply streams into the activity feed. 15 s: motion-blur whip. 16 s: integrations list with "Enable" buttons. 18 to 23 s: a second task, agent proposes a fix with code. 24 s "Agents for Coding", 25 s "Agents for Triage", 26 to 28 s "Linear for Agents" typed on, 29 to 31 s logo. Three type cards at the end act as a recap, not a hook.
- **Linear Agent (55 s).** One continuous camera over real UI laid on a tilted plane, shallow depth of field. A query is typed ("Find issues with loading performance"), results stream, a second prompt ("Make a plan to refactor...") becomes a spec doc. Only 4 scene changes in 55 s. Calm energy carried by the camera, not cuts.
- **Arc 1.0 (34 s).** Pure pattern interrupt: a 1930s test plane crashes at 0 to 3 s, then archival "v1.0" failures and hits (amphibious cycle, TV glasses, Segway, Google Glass, the first YouTube video) each with a small "v1.0" label, intercut with single serif words: "version", "can mean", "everything", "nothing". Cuts every 0.7 to 1.5 s. The product appears only at 26 s for 4 s. Works because Arc already had a waitlist audience; for an unknown product this would hide the product.
- **Arc on Windows (37 s).** 0 to 4 s: Windows 95 macro close-ups, cursor clicks "Search the Internet", types "flowers", a JPEG loads; cuts every 0.3 to 0.5 s. 4 s: "You've been waiting." 6 to 8 s: a real counter ticks "Beta Testers Onboarded since Dec 11, 2023" to 151,141 (a real number as proof). 9 to 12 s: the Start button through the decades. 14 s: double-click the Arc icon. 15 s: "Finally". 16 to 29 s: product montage of tight crops with real-looking content. 30 s: "Arc is on Windows". 33 s: the Edge icon dragged to the Recycle Bin, a joke after the CTA.
- **Cursor 2.0 (64 s, 9.4M views).** 0 to 2 s logo lockup, 2 to 4 s "Introducing Composer, our first agent model." typed on character by character. 5 to 8 s a two-column bar chart (Intelligence, Speed) with Composer in black and others in grey: the claim is proven with a chart before any UI. 9 to 10 s "And a new Cursor built for agents." Then real UI on a desktop wallpaper, with typed interstitial cards between segments: "Run a task across multiple models.", "Review changes in a single place.", "Work with a built-in browser." Every card is one sentence, 4 to 7 words, sentence case, full stop.
- **Notion AI (57 s, 8.2M views).** 0 to 1 s a cursor glides to the Notion logo and clicks it, 1 to 2.5 s it expands into a blue field with the AI face. 3 s "Meet the *new* Notion AI" with a hand-drawn underline on "new". 4 to 8 s a slot line: "One AI tool to [Find in Google Drive / Summarize / Draft a meeting agenda]" with the chip swapping, ending "One AI tool to do it all." Each feature then gets its own brand colour world (blue, red, yellow) with a single floating UI card. Five features, each introduced by a 3 to 7 word headline card.
- **Superhuman (62 s, 2.4M views).** Contrarian spoken hook at frame 0: "AI is not the hero coming to save you. You're the hero." Then hand-drawn stick-figure animation carries the problem ("Projects, emails, reading, learning, more emails"). No product UI at all. Logo is a persistent bug top-left. Works as a brand film, not a demo.
- **Framer (37 s, 18M views).** Frame 0 is the product's output being built: a button types itself, a section frame appears, a portrait fills it, the headline "Meet your new AI assistant" types on, then pull out to reveal the whole site, then pull out again to the editor. Climax is a close-up click on "Publish". Show the result first, then the tool that made it.
- **v0 (48 s).** "What will you ship?" appears as text, then morphs into the prompt bar (copy becomes UI). The prompt cycles through examples ("A sleek pricing page", "A flower shop", "A SaaS dashboard layout"), one is generated, one element is edited by prompt ("Make the company logo color blue"), code tilts into view in 3D, then a pull-out to a grid of many generations as proof of range.
- **Loom AI (38 s).** UI recreated and simplified in motion design (blocky "Dashboard Demo" mock), floating windows over brand gradient orbs, one AI feature per beat, translations shown as greeting bubbles ("Hallo!", "Hola!", "Olá!"). Recreated UI reads at phone size, real capture often does not.

---

## 1. Principles

Each principle: the evidence, then the rule a director agent applies.

**P1. Show the product doing something inside 2 seconds unless the video is a brand film.**
Evidence: Framer and Loom show working UI at 0 s, Linear for Agents at 1.5 s, v0 at 3 s. The two films that delay the product (Arc 1.0 at 26 s, Superhuman never) are brand films from companies with existing audiences. Google's ABCD guidance (Attention, Branding, Connection, Direction) says to brand "from the start" and "early, often, and richly" [official]. X's ads guidance says to "include clear branding within the first three seconds" [snippet]. TikTok reports over 63 % of its highest-CTR ads show the key message or product in the first 3 s [snippet].
Rule: for a demo or launch cut, the product or its output must be on screen by 2.0 s. A type card hook may hold at most 1.5 s (RULES.md section 5). Only a `brand film` brief may delay the product, and then it must appear before 75 % of runtime.

**P2. Frame 0 is the poster. Make it a finished, readable image.**
Evidence: X and LinkedIn show a still before autoplay starts; Arc on Windows opens on a recognisable Windows 95 PC, Framer on a crisp glowing button, Linear Agent on readable UI. Linear for Agents opens on a blur that resolves at 0.5 s, which makes a weak poster [observed].
Rule: frame 0 contains either the product UI at a readable crop or a 2 to 5 word line, never a blur, a black frame or a half-drawn logo. Check `thumbnail-frame0.png` at 360 px wide.

**P3. One idea per beat, introduced by one short line.**
Evidence: Cursor 2.0 uses one typed sentence per feature ("Review changes in a single place."). Notion uses one headline per colour world. Linear ends with one line per use ("Agents for Coding", "Agents for Triage") [observed].
Rule: one capability per beat, one caption per beat, 2 to 7 words, a verb or a product noun in it. If a beat needs two captions, it is two beats.

**P4. Prove the claim with something on screen: a number, a chart, a streamed result.**
Evidence: Cursor 2.0 shows a benchmark chart at 5 to 8 s before any UI. Arc on Windows ticks a real counter to 151,141 beta testers. v0 ends on a grid of many generations [observed].
Rule: each cut needs at least one proof beat where a real number, a real result or a real artefact fills at least 30 % of the frame for at least 1.5 s. Numbers must come from the recording, README or site (RULES.md rule 8).

**P5. Show the output first, then the tool.**
Evidence: Framer opens on the website being built and only pulls out to the editor at 11 s. v0 opens on the prompt bar and its generated page, code comes later. Loom shows the AI summary before the menu that produced it [observed].
Rule: when the product makes something (a page, a PR, a summary, a fix), the first proof beat shows the made thing at full size; the interface that made it comes next via a pull-out.

**P6. Crop hard. UI is shown as panels, not windows.**
Evidence: Linear for Agents crops rows off the frame edge with no chrome. Arc on Windows uses macro close-ups of single controls. Loom and Notion float a single card. Cursor shows the full window only briefly, then crops [observed]. RULES.md rule 5 requires readability at 360 px.
Rule: in a 16:9 cut, the framed region for a UI beat is at most 50 % of the recording width (zoom 2x or more) unless the beat is a reveal or pull-out. Body text in the framed region must render at 14 px or larger at 360 px output width. In 9:16, frame at most 35 % of the recording width.

**P7. Pace is set by reading, then compressed by cutting, not by speeding up text.**
Evidence: montage films cut fast only on images without text (Arc on Windows: about 1 cut per 0.6 s on close-ups) and slow down on type (each word card holds 0.8 to 1.5 s). UI-led films are slower: Linear Agent 4 scene changes in 55 s, v0 4 in 48 s, Cursor 9 in 64 s [observed].
Rule: text holds at 0.3 s per word plus 0.5 s (RULES.md). Image-only montage shots may run 0.3 to 0.8 s. UI beats with a caption run 2.5 to 4 s. Targets by energy: calm 4 to 8 cuts per minute, standard 10 to 20, hype 30 to 60 with montage sections only on imagery.

**P8. One camera language for the whole film.**
Evidence: Linear Agent uses a single tilted, slow-gliding camera for 55 s. Cursor uses straight-on window shots with typed interstitials throughout. Arc uses hard cuts and labelled archival frames throughout [observed].
Rule: pick one grammar per cut (continuous glide, whip and punch, or hard cut) and use it for every joint except the end card dive. Do not mix tilt perspective and flat framing in one cut.

**P9. The type system is the brand.**
Evidence: Arc uses its serif for every card. Cursor and Linear use their sans at small size, sentence case, centred, lots of empty space. Notion uses its hand-drawn underline and illustrated face. Superhuman keeps its wordmark as a persistent bug [observed].
Rule: cards use the brand's display face at one size, one weight, centred, sentence case unless the brand shouts. No more than 7 words on a card. Pull fonts from the brand site (section 5).

**P10. The end card is a 2 to 4 s sequence: line, logo, action.**
Evidence: Arc: "Today", logo, "download now", "arc.net". Notion: "Try Notion AI for free at Notion.com", then tagline, then logo. Linear: "Linear. At your command." then logo. Superhuman: tagline, logo with URL [observed].
Rule: end with at most three beats: a 2 to 6 word line, the logo lockup, one action (URL, install command or "Available today"). Never two CTAs. Total 2.5 to 4 s.

**P11. Silent-first: the story must survive with sound off.**
Evidence: 7 of the 10 films carry no VO at all; their story is in on-screen type and UI. The two VO films (Superhuman, Framer) still put key words on screen. X tells advertisers to add captions or text overlays for sound-off viewers [snippet]; LinkedIn says "many users watch videos on LinkedIn with sound off, making subtitles essential" [official]. Verizon Media and Publicis (2019, 5,616 US adults) found 69 % watch with sound off in public [secondary, 2019]. The often quoted "85 % of Facebook video is watched without sound" is publisher self-reporting from 2016, not a platform figure: do not cite it.
Rule: every claim the VO makes must also be readable on screen or self-evident in the UI. Validate with `<name>-muted.mp4` first.

**P12. Use a slot or a counter to show range quickly.**
Evidence: Notion's "One AI tool to [chip]" swaps three tasks in 4 s. v0 cycles three prompts in 6 s. Arc ticks a counter. Cursor's chart compares in one frame [observed].
Rule: when the product does many things, show 3 examples in one held frame by swapping a single slot every 0.8 to 1.2 s, rather than three separate beats.

**P13. Humour and nostalgia buy attention only when the product pays it off.**
Evidence: Arc on Windows spends 15 s on Windows nostalgia, then pays it off with the Arc icon double-click and the Edge-in-the-bin joke. Arc 1.0's plane crash sets up the "v1.0 can mean everything or nothing" line [observed].
Rule: a non-product opening (archival, metaphor, joke) is allowed only if the brief says `brand film` and the product beat explicitly answers it. Never longer than 30 % of runtime.

**P14. Founder or person on camera opens on the claim, mid-thought.**
Evidence: Superhuman's frame 0 is the speaker already saying the contrarian line. Cursor 3 (91 s) is founders explaining the product over UI [observed from transcript].
Rule: for founder clips follow RULES.md section 6b. The first spoken line is the strongest complete claim, at most 12 words, with subtitles on from frame 0.

**P15. Real content in the UI, never lorem or empty states.**
Evidence: Linear's backlog has plausible tickets ("Fix tooltip overlap on hover cards"). Arc searches "japandi interior". v0 types "A SaaS dashboard layout" [observed].
Rule: before recording or choosing source moments, check that visible data is realistic, non-secret and on-brand. Empty states, test strings and "asdf" are blockers in P1 of RULES.md.

---

## 1b. Platform facts that change the cut

| Platform | Length guidance | Ratio | Text-safe area and frame 0 | Sound | Status |
|---|---|---|---|---|---|
| X | Ads: "15 s or less" recommended, max 2:20 (140 s) organic and ads | 9:16 recommended for ads; 16:9, 1:1, 4:5 all accepted | No official poster-frame rule: design frame 0 as the poster. Brand within 3 s | Captions or text overlay for sound-off | SNIPPET |
| X encode | H.264, 4:2:0, max 60 fps, max 25 Mbps, AAC LC, under 30 MB "strongly recommended" for ads | | | | SNIPPET |
| LinkedIn | "We recommend uploading videos that are 15-30 seconds long"; most important content in the first 10 s | 4:5 recommended, 1:1, 9:16, 16:9 | Ad thumbnail must match the video ratio. Videos under 30 s loop | Subtitles "essential"; SRT only for ads | OFFICIAL |
| LinkedIn encode | MP4, H.264, under 30 fps, 75 KB to 500 MB | | | | OFFICIAL |
| Instagram Reels (ads) | 0 s to 15 min | 9:16, 1440x2560 | Keep top 14 %, bottom 35 %, sides 6 % clear of text and logos (about 269 px, 672 px, 65 px on 1080x1920) | Captions recommended | OFFICIAL |
| TikTok | No current official length; 21 to 34 s advice is retired. Focused View = 6 s watched | 9:16 | No fixed safe zone, use TikTok's template | Sound-on platform; 88 % say sound is essential (Kantar for TikTok) | OFFICIAL |
| YouTube Shorts | Up to 3 min since Oct 2024; "Viewed vs swiped away" is the hook metric | 9:16 | Thumbnail picked from a frame in the app | "Announce yourself with audio", tight framing | OFFICIAL |
| Landing page hero | No platform rule; treat as a GIF replacement | Match the hero slot | Needs a pause control if it loops over 5 s (WCAG 2.2.2), always set a poster | `autoplay loop muted playsinline`, no audio | OFFICIAL |

Engagement by length (vendor data, use as direction only): Wistia 2025, about 14M videos, average share watched is 50 % under 1 min and 46 % at 1 to 3 min. Vidyard 2022, about 1.78M business videos, 66 % completion under 1 min vs 56 % at 1 to 2 min.

Rules this implies for launchcut:
- `twitter-*` presets: keep standalone cuts at 15 s or under unless the brief says launch film; cap bitrate at 25 Mbps (already a known pitfall).
- `linkedin-16x9`: prefer a 4:5 or 1:1 sibling for LinkedIn feed; aim for 15 to 30 s; put the payoff before 10 s.
- `vertical-9x16`: captions and rings must sit inside the Reels safe area: caption baseline at least 35 % above the bottom edge, nothing in the top 14 %. This overrides the default bottom-band caption position for vertical.
- TikTok and Shorts: lean on sound (SFX bed on, VO if available) while keeping every claim on screen.
- Landing page hero: export a muted, seamless loop of 8 to 20 s with a still poster frame and no CTA card; the page carries the CTA.

---

## 2. Structures

Durations use the RULES.md pacing budget: reveal 3 to 3.5 s, UI beat 2.5 to 3 s, end card 2.5 to 3 s, hook card 1.0 to 1.5 s.

### T1. The Proof Clip, 12 to 16 s (default)
Use for: quote tweet of a launch film, reply, changelog post, any post whose text already tells the story.

| Time | Beat | Shot | Caption |
|---|---|---|---|
| 0.0 to 3.0 | Reveal: the product whole, frame 0 crisp | Reveal, slow push in | none or 2 to 4 words |
| 3.0 to 6.0 | Proof 1: cause and effect | Follow the click | 3 to 5 words, verb first |
| 6.0 to 9.0 | Proof 2: the payoff (error found, result made) | Punch-in, rings | 3 to 5 words |
| 9.0 to 12.0 | Proof 3 or pull-out for context | Pull-out | optional |
| 12.0 to 15.0 | End card | Dive into logo, end | command or URL |

### T2. The Standalone Hook, 15 s
Use for: standalone post on X or LinkedIn where nothing surrounds the video.

| Time | Beat | Shot | Copy |
|---|---|---|---|
| 0.0 to 1.5 | Hook card or hook caption over UI | Card or reveal with caption | 5 to 7 words, from the hook library |
| 1.5 to 4.5 | The answer: product doing the main job | Reveal, push in | 3 to 5 words |
| 4.5 to 7.5 | Proof beat | Follow the click | 3 to 5 words |
| 7.5 to 10.5 | Payoff | Punch-in, rings | 3 to 5 words |
| 10.5 to 12.5 | Claim line | Text card | 4 to 6 words |
| 12.5 to 15.0 | End card | End | name, URL or command |

### T3. The Feature Tour, 30 s (Cursor and Notion pattern)
Use for: launch day post that introduces a release with 3 to 5 capabilities; landing page section video.

| Time | Beat |
|---|---|
| 0.0 to 2.0 | Logo lockup or product name with version, or the "Introducing X" line typed on |
| 2.0 to 4.0 | One-line promise card, 5 to 8 words |
| 4.0 to 5.5 | Interstitial card 1, 3 to 6 words |
| 5.5 to 10.0 | Feature 1 UI beat, crop and push |
| 10.0 to 11.5 | Interstitial card 2 |
| 11.5 to 16.0 | Feature 2 UI beat |
| 16.0 to 17.5 | Interstitial card 3 |
| 17.5 to 22.0 | Feature 3 UI beat |
| 22.0 to 25.0 | Range or proof: slot swap, grid, chart or counter |
| 25.0 to 30.0 | Tagline, logo, action |

### T4. The Output-First Build, 30 to 40 s (Framer and v0 pattern)
Use for: products that make something visible (sites, UI, docs, code, video). Strong as a landing page hero loop when trimmed.

| Time | Beat |
|---|---|
| 0.0 to 4.0 | Macro on the made thing assembling itself (button, headline, image) |
| 4.0 to 7.0 | Pull out to the whole artefact |
| 7.0 to 10.0 | Pull out again to the tool that made it |
| 10.0 to 22.0 | Three quick UI beats of how (prompt, edit, import), 3 to 4 s each |
| 22.0 to 27.0 | Range: grid of outputs or slot swap |
| 27.0 to 30.0 | Climax action in close-up (Publish, Merge, Send), with a hit |
| 30.0 to 33.0 | Logo and action |

### T5. The Continuous Glide, 45 to 60 s (Linear Agent pattern)
Use for: calm launch film for a premium brand, agentic or streaming products where the content of the result is the wow.

| Time | Beat |
|---|---|
| 0.0 to 3.0 | Real UI on a tilted plane, readable, slow glide |
| 3.0 to 12.0 | Input typed in real time (query or prompt), held |
| 12.0 to 22.0 | Result streams in; camera follows the newest line |
| 22.0 to 35.0 | Second request builds on the first (plan, spec, PR) |
| 35.0 to 48.0 | Pull out to the whole workspace, result in context |
| 48.0 to 55.0 | Tagline blurs in ("Name. Short promise."), logo |

Rules: music only, no captions on UI, no hard cuts, one move at a time.

### T6. The Manifesto Montage, 30 to 40 s (Arc pattern)
Use for: version 1.0, new platform or category launch from a brand with an audience; not for unknown products.

| Time | Beat |
|---|---|
| 0.0 to 3.0 | Pattern interrupt image (archival, nostalgic, metaphor) |
| 3.0 to 15.0 | Montage at 0.4 to 1.2 s per image, interleaved with 1 to 3 word cards that build one sentence |
| 15.0 to 20.0 | Callback or payoff image that sets up the product |
| 20.0 to 30.0 | Product montage, tight crops, 1 to 1.5 s each |
| 30.0 to 35.0 | Name line ("X is on Y"), "Download now", URL |

### Choosing a template

| Context | Template | Length |
|---|---|---|
| Quote tweet or reply to the launch post or film | T1 | 12 to 16 s |
| Standalone X or LinkedIn post | T2, or T3 if 3 or more features | 15 to 30 s |
| Landing page hero (autoplay, muted, loop) | T4 trimmed, no cards with CTA, loop point on a still frame | 8 to 20 s |
| Launch day film | T3, T5 or T6 by brand | 30 to 60 s |
| Founder clip | RULES.md 6b, opening claim then B-roll from T1 beats | 15 to 45 s |
| Tutorial recut into a teaser | T1 with the tutorial's single best result as the payoff | 8 to 15 s |
| Vertical 9:16 | T1 or T2 with punch-ins only, no full-window shots | 10 to 20 s |

---

## 3. Hook library

Hook types are split by RULES.md rule 1. **V** = visual hook, product-first, allowed in any context. **C** = caption-as-hook, a short caption over product footage at frame 0. **T** = type-card hook, standalone videos only, 1.0 to 1.5 s, 5 to 7 words.

| # | Pattern | Type | Template | Example |
|---|---|---|---|---|
| 1 | Result first | V | Open on [finished output] at full size, then pull out to the tool | A finished landing page, then pull out to the Framer editor |
| 2 | Made thing assembling | V | Macro on [one element] building itself | A "Get started" button typing itself (Framer) |
| 3 | Copy becomes UI | V+T | "[Question]" morphs into the [input field] | "What will you ship?" becomes the v0 prompt bar |
| 4 | Cursor as character | V | Cursor glides to [logo or button] and clicks at 0.5 s | Notion's cursor clicking its own logo |
| 5 | Live counter | V | [Metric] ticks from [low] to [real high] | "Beta testers onboarded" ticking to 151,141 (Arc) |
| 6 | Chart proof | V | Two bars: [us] black, [others] grey, labelled [metric] | Cursor's Intelligence and Speed bars |
| 7 | Failure caught | C | "[Thing] broke. [Product] found why." | "Build failed. Found the line." |
| 8 | Before and after split | V | Left [old way, messy], right [product, clean], 1.5 s | 40 unread tabs vs one Arc sidebar |
| 9 | Speed claim with clock | C | "[Task] in [real time]." with a visible timer | "PR review in 40 seconds." |
| 10 | Slot swap | C | "One [tool] to [chip 1 / chip 2 / chip 3]." | "One AI tool to summarize / draft / find." (Notion) |
| 11 | Imperative | C | "[Verb] [object] without [pain]." | "Ship docs without writing them." |
| 12 | Named pain | T | "[Audience], [specific annoying moment]?" | "Still copying stack traces into chat?" |
| 13 | Contrarian | T | "[Common belief] is wrong." or "[X] is not [Y]." | "AI is not the hero. You are." (Superhuman) |
| 14 | Version stakes | T | "[Version] can mean everything. Or nothing." | "1.0 can mean everything, or nothing." (Arc) |
| 15 | You've been waiting | T | "You've been waiting." then the platform or feature | Arc on Windows |
| 16 | Introducing | T | "Introducing [name], our first [category]." | "Introducing Composer, our first agent model." (Cursor) |
| 17 | Nostalgia frame | V | Era-specific UI or object, then cut to now | Windows 95 "Search the Internet" (Arc) |
| 18 | Open loop | C | "Watch what happens when [action]." | "Watch what happens when tests fail." |
| 19 | Number first | C | "[Number] [unit] [outcome]." | "12 agents. One inbox." |
| 20 | Question as input | V+C | Type the user's real question into the product at frame 0 | "Find issues with loading performance" typed (Linear) |
| 21 | Overload | V | Pile up [many items] fast, then the product clears them | Emails stacking, then sorted piles (Superhuman) |
| 22 | Mid-claim founder | V | Speaker already mid-sentence on the strongest line | "You're the hero. AI is just a sidekick." |
| 23 | Finally | T | "Finally, [thing people asked for]." | "Finally. Arc on Windows." |
| 24 | Zero to done | C | "From [blank state] to [shipped state]." | "From prompt to deployed site." |
| 25 | What it replaces | C | "[N] tools. Now one." with logos collapsing | Integration icons assembling into one (Notion) |

### Hook scoring rubric (score each 1 to 5, ship only if total is 20 or more of 25 and no criterion is below 3)

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| **A. Product in frame** | No product or output by 2 s | Product visible but small or partial | Product or its output fills the frame at 0 s and reads at 360 px |
| **B. Specificity** | Generic ("Work smarter") | Names a category ("Faster code review") | Names a concrete noun, number or task from the source ("Find the failing test") |
| **C. Length and read time** | Over 9 words or needs over 2 s to read | 8 to 9 words | 7 words or fewer and readable in the hold time (0.3 s per word plus 0.5 s) |
| **D. Context fit** | Repeats the post or quoted video, or a T hook in a quote tweet | Partly overlaps the context | Adds what the context lacks, and the type matches the context (V or C for quotes, T only standalone) |
| **E. Truth and payoff** | Claim not in sources, or not paid off in the cut | Claim true but paid off late (after 50 % of runtime) | Claim traces to the recording, README or site and is visibly paid off within the next 5 s |

Tie-break: prefer the candidate with the higher A, then E.

---

## 4. Narration and on-screen copy

Word budgets come from RULES.md: VO at about 2.5 words per second, captions at 0.3 s per word plus 0.5 s.

| Beat | Duration | Caption words | VO words |
|---|---|---|---|
| Hook card | 1.0 to 1.5 s | 3 to 7 | 0 to 4 |
| Reveal | 3.0 to 3.5 s | 0 to 4 | 6 to 8 |
| UI proof beat | 2.5 to 3.0 s | 3 to 5 | 6 to 7 |
| Interstitial card | 1.5 to 2.0 s | 3 to 6 | 0 |
| Payoff | 3.0 s | 3 to 5 | 6 to 7 |
| End card | 2.5 to 4.0 s | name plus 2 to 6 word line plus action | 3 to 6 |

Observed: Framer's VO runs about 70 words in 37 s (1.9 words per second) and leaves the climax silent. Superhuman's runs about 150 words in 62 s (2.4 words per second) and wall-to-wall. Use 2.0 to 2.5, with at least one 2 s gap before the end card.

Voice rules:
- Sentence case, full stops, present tense, second person or imperative. Cursor's cards are the model: "Review changes in a single place."
- One sentence per beat. No sentence over 12 words in VO, no card over 7 words.
- The caption names what is on screen now. The VO may say why. Never the reverse.
- Repeat the product name at most twice: once early (or in the hook), once on the end card.
- Accent one word per caption (RULES.md), the noun or the result, not the verb.

Never say or write:
- Puffery without proof: "revolutionary", "game-changing", "seamless", "powerful", "best-in-class", "next-generation", "supercharge", "unlock", "effortless", "magic" (unless the brand owns it).
- "AI-powered" as the claim. Show what the AI did.
- Metrics, customers or logos that are not in the sources.
- Competitor names in a negative frame. Show your bar, grey the others (Cursor) without naming if the brand prefers.
- "In today's fast-paced world", "Meet the future of", "Imagine a world".
- Words the quoted post or launch film already says (RULES.md section 1, "Already said elsewhere").

---

## 5. Art direction

What the strong films do [observed]:
- **Background is the app's own canvas.** Linear sits on its near-black, Cursor on its off-white, Notion on its warm grey. Frames feel like the product, not like an ad.
- **One accent colour, used for meaning.** Linear's indigo selection, Notion's blue field, Arc's electric blue end card, Superhuman's lavender end card. Notion is the exception that assigns one brand colour per feature world.
- **Type is small, centred and calm.** Cards in Linear, Cursor, Notion and v0 use body-adjacent sizes (roughly 4 to 6 % of frame height), lots of empty space, no outlines, no gradients on text. Arc is the loud exception with large serif.
- **Typed-on and blur-in reveals beat slide-ins.** Cursor types its cards; Linear and v0 blur in; Notion draws a hand underline. These echo the products (editor, AI streaming, notes).
- **UI framing choices:** tight crop with no chrome (Linear, Arc), floating card over a colour field (Notion, Loom), window on wallpaper (Cursor), 3D tilt with depth of field (Linear Agent, v0 code view). Pick one per cut (P8).
- **Recreated vs real UI.** Loom and Notion simplify UI into motion-design cards for legibility. Linear, Cursor and Arc use real capture. launchcut uses real capture, so compensate with tighter crops, rings and the `grade` lift.
- **Logo handling:** the logo appears once or twice: as a draw-on or 3D settle at the start (Cursor, v0), and as a centred lockup at the end. Superhuman's persistent corner bug is the only always-on logo. Never animate the logo's shape beyond what the brand does on its own site.

Extract from the brand's site before producing (write into `style.yaml` and `PLAN.md`):
1. Background colour of the app and of the marketing site (hex), light or dark default.
2. Accent hex and the alert or error colour used in the product.
3. Display and body font families (check the site's CSS `font-family` and the loaded font files), weights used for headlines.
4. Headline casing and punctuation habits (sentence case with full stop, Title Case, lowercase).
5. Logo files as SVG: symbol, wordmark, lockup, light and dark versions.
6. Corner radius and shadow style of cards and windows on the site.
7. Motion vocabulary on the site: easing feel (springy, linear, slow ease-out), whether things blur in, type on or slide.
8. Tagline and the exact CTA wording on the hero ("Get started", "Download", install command).
9. Words the brand never uses (check two or three pages for absent puffery).
10. Any recurring brand device (Notion's illustrated faces, Arc's labelled archival frames, Linear's 3D tilt).

---

## 6. Sources

Films analysed first-hand (downloaded, contact sheets and scene detection):
- Linear, "Introducing Linear For Agents": https://www.youtube.com/watch?v=sbwOQV5zY34
- Linear, "Introducing Linear Agent": https://www.youtube.com/watch?v=mRql2VJ99gM
- The Browser Company, "Arc 1.0 | Everything or nothing": https://www.youtube.com/watch?v=n5Vwrj1gEWs
- The Browser Company, "Arc on Windows. Download now.": https://www.youtube.com/watch?v=LJQsAOon6og
- Cursor, "Introducing Cursor 2.0": https://www.youtube.com/watch?v=An8IM-kPyms
- Cursor, "Introducing Cursor 3" (transcript only): https://www.youtube.com/watch?v=UxbULt_hCdA
- Notion, "Introducing the new Notion AI": https://www.youtube.com/watch?v=S92KX8-Hmlc
- Superhuman, "Superhuman's got your back": https://www.youtube.com/watch?v=nJUylrt1OdU
- Framer, "Framer: All Design, No Code, Real Websites": https://www.youtube.com/watch?v=6xJWQRVl9nw
- Vercel, "Introducing v0: Generative UI": https://www.youtube.com/watch?v=By9wCB9IZp0
- Loom, "Work Faster and Smarter with Loom AI": https://www.youtube.com/watch?v=Jxa8L0EV9F0

Secondary reading (search results reviewed, claims marked secondary or unverified above):
- Tella, on The Browser Company's video style: https://www.tella.com/blog/the-browser-company-video
- Failory, "Lights, camera, Arction": https://newsletter.failory.com/p/lights-camera-arction
- Motion The Agency, product launch video guide: https://www.motiontheagency.com/blog/product-launch-video-guide
- Flowjam, AI startup launch video: https://www.flowjam.com/blog/ai-startup-launch-video
- Levitate Media, B2B launch video examples: https://levitatemedia.com/learn/product-launch-video-examples-with-b2b-focused-ideas
- Atlassian / Loom, product launch video: https://www.atlassian.com/blog/loom/product-launch-video
- Opus, TikTok length and retention: https://www.opus.pro/blog/tiktok-length-format-retention-data
- Opus, YouTube Shorts length and retention: https://opus.pro/blog/ideal-youtube-shorts-length-format-retention
- Segwise, frame-by-frame ad breakdown: https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame
- Hooked, scripting for attention: https://www.hooked.so/blog/how-to-script-a-video
- Jelly Marketing, short-form hooks: https://jellymarketing.ca/blog/stop-the-scroll-in-3-seconds-secrets-to-high-performing-short-form-video-hooks/

Platform guidance (OFFICIAL unless noted):
- X ads creative specs (SNIPPET, page returns 403): https://help.x.com/en/business-and-advertising/creative-ad-specifications
- X ads best practices (SNIPPET): https://business.x.com/en/advertising/ads-best-practices
- X video views campaigns (SNIPPET): https://business.x.com/en/advertising/campaign-types/video-views
- LinkedIn video ad specs: https://www.linkedin.com/help/lms/answer/85306
- LinkedIn video ad tips (Apr 2025): https://www.linkedin.com/business/marketing/blog/linkedin-ads/your-one-stop-shop-for-linkedin-video-ad-tips
- Meta Instagram Reels ad specs and safe zone: https://www.facebook.com/business/ads-guide/update/video/instagram-reels
- TikTok video ad specifications: https://ads.tiktok.com/help/article/video-ads-specifications?lang=en
- TikTok Focused View: https://ads.tiktok.com/help/article/video-views-objective
- TikTok and Kantar on sound: https://ads.tiktok.com/business/tr/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok
- Google ABCDs: https://support.google.com/google-ads/answer/14783551
- Kantar validation of ABCD (modeled): https://www.kantar.com/industries/technology-and-telecoms/validating-googles-abcd-framework-with-the-power-of-artificial-intelligence
- YouTube Shorts analytics, viewed vs swiped away: https://support.google.com/youtube/answer/1715072
- YouTube Shorts 3 minutes (SECONDARY): https://petapixel.com/2024/10/04/youtube-shorts-expands-video-length-to-three-minutes/
- web.dev, replace GIFs with video: https://web.dev/articles/codelab-replace-gifs-with-video
- Chrome autoplay policy: https://developer.chrome.com/blog/autoplay
- WCAG pause, stop, hide: https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide
- Verizon Media and Publicis captions study (SECONDARY): https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/
- Digiday on the 85 % claim (publisher self-reports, do not cite as fact): https://digiday.com/media/silent-world-facebook-video/
- Facebook and Nielsen brief views study (SECONDARY): https://martech.org/even-brief-video-views-drive-brand-lift-facebook-nielsen-study-finds/
- Wistia optimal video length: https://wistia.com/blog/optimal-video-length
- Vidyard benchmarks via MarketingProfs (SECONDARY): https://www.marketingprofs.com/charts/2023/49949/business-video-benchmarks-retention-rates-by-length
