---
name: launchcut
description: Turn one or many screen recordings (or screenshots and context) into a directed short launch or demo video with camera moves, highlights, captions, synthesized SFX and narration support, then validate it. Use when someone hands over recordings and asks for a launch video, a product demo cut, a Twitter/LinkedIn/vertical clip, zooms and cuts, or SFX on a screen recording.
---

# launchcut

You are the editor and director. `RULES.md` at the repo root is the authority: read it fully before starting, and follow its phases in order. The `launchcut` CLI (`uv run launchcut ...`) does the mechanical work. `REFERENCE.md` is the `cut.yaml` schema, and `examples/agentplay/` is a shipped cut to imitate.

## Procedure

1. **Intake.** Pull every variable in RULES.md section 1 from the request. Ask once only for what you cannot infer. The questions that matter most: where this posts, what surrounds it, and what is already said there. Decide defaults for the rest and write them down.
2. **Scaffold.** `uv run launchcut new cuts/<name>`, outside `/tmp`. Fill in the brief in `PLAN.md`.
3. **Inventory.** `uv run launchcut probe <recordings...>`. Read every `inventory.md` and look at the contact sheets yourself. Pull stills around the spikes with `launchcut grid`. Check for secrets.
4. **Beat map and shot list.** Write the beat map, shot list and pacing budget in `PLAN.md`. Apply the rules: context decides the opening, one idea per shot, land/highlight/hold, length is soft.
5. **Coordinates.** Lock every box and point from grid images. Never guess.
6. **Stills loop.** Write `cut.yaml`, then run `uv run launchcut stills cuts/<name>/cut.yaml`. Look at the sheet and fix framing, highlight placement, caption collisions and the frame 0 thumbnail. Repeat until the sheet matches the shot list.
7. **Render.** `uv run launchcut all cuts/<name>/cut.yaml` takes minutes, so run it in the background.
8. **Validate.** Read `out/<name>-qa/report.md` and look at `strip-5fps.png`, `phone-width.png` and `thumbnail-frame0.png`. Run the editorial checklist honestly, or hand it to an independent reviewer (the `judge` agent if available) together with `PLAN.md`. Fix and re-render, at most three loops.
9. **Hand off.** Give the file paths, the length, what each shot shows, the decisions you made for the requester, and anything left open. Add a changelog line to `PLAN.md`. Never overwrite a version the requester has seen; bump `-v2`.

## Non-negotiables

- Frame 0 is the thumbnail. Every caption names something visible. Every sound is tied to something visible.
- Never alter narration samples. Never invent logos, numbers or claims.
- Render stills before full renders. Verify motion and layout from the rendered file, not from the config.
