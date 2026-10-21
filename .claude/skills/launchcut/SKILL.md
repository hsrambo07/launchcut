---
name: launchcut
description: Produce a directed short launch, promo or demo video from screen recordings, talking-head clips, screenshots or plain context, with a crew of agents (researcher, art director, hook writer, director, critic) who learn the company and the craft first, then execute with launchcut and validate. Use when someone hands over footage and asks for a launch video, promo, product demo cut, social clip, zooms and cuts, captions or SFX.
---

# launchcut

If you are not inside the launchcut repo, it lives at `~/Documents/projects/launchcut` (clone: `https://github.com/hsrambo07/launchcut`). Run every `uv run launchcut` command from that directory, and keep cut folders under `cuts/` there, never in `/tmp`.

You are the producer. You run a crew of subagents, defined in `.claude/agents/`, and you do the editing yourself. **No cut is directed before the company and the craft are learned.** Nothing in this repo is tied to one brand: every job learns its own brand.

Read these first:

- `RULES.md`, the authority.
- `docs/research/launch-craft.md`: structures, the hook library and the rubric.
- `docs/research/prior-art.md`: techniques and quality.

`REFERENCE.md` is the `cut.yaml` schema.

## Procedure

1. **Intake.** Pull the RULES.md section 1 variables from the request. Ask once only for what matters and cannot be inferred: where this posts, what surrounds it, what is already said there. Decide the rest and write it down.

2. **Scaffold and inventory.**
   ```
   uv run launchcut new cuts/<name>
   uv run --extra speech launchcut probe <sources...> --transcribe --out cuts/<name>/probe
   ```
   Look at the contact sheets yourself.
   - If any source is below 720p, add `enhance: 2` to it in `cut.yaml`. It is cached, so the cost is paid once.

3. **Learn, in parallel.** Spawn `lc-researcher` and `lc-art-director` (phase 1 and 2) together, giving each the cut folder, the source paths and the request.
   - **Gate:** `research/brief.md`, `brand/brand.md` and `style.yaml` exist, and every value is marked VERIFIED or ASSUMED.

4. **Hooks.** Spawn `lc-hook-writer`. Pick one of its top 3, or ask the requester when the context is unclear.
   - **Gate:** `research/hooks.md` exists with scored candidates.

5. **Direction.** Spawn `lc-director`.
   - **Gate:** `SCRIPT.md` and `PLAN.md` exist, the beats each teach one thing, and the pacing budget adds up.

6. **Coordinates.** Lock every box and point with `uv run launchcut grid <src> <t> --box ...`. Never guess.

7. **Edit.** Write `cut.yaml` with `extends: style.yaml`. Then run `uv run launchcut stills cuts/<name>/cut.yaml <key moments>` and look at the sheet yourself, then hand it to `lc-art-director` (phase 3).
   - Loop until the sheet matches `SCRIPT.md` and the art director approves.

8. **Render.** Run `uv run launchcut all cuts/<name>/cut.yaml` in the background. It renders, mixes, delivers and runs QA.

9. **Critique.** Spawn `lc-critic` on the delivered file.
   - On REVISE: apply the fixes, re-render as `-v2`, and send it back to the critic.
   - At most three loops, then escalate the open questions to the requester.

10. **Hand off.**
    - The file paths and the length.
    - The hook used and why.
    - A beat-by-beat summary.
    - The brand sources used.
    - The decisions made for the requester.
    - The critic's verdict.
    - Rights notes.

    Add a changelog line to `PLAN.md`. Never overwrite a version the requester has seen.

## Non-negotiables

- Learn the company before directing. Use the brand's own palette, type and logo files, never another job's. If a logo file can't be found, use the name in the brand's type and say so.
- Frame 0 is the thumbnail. Every caption names something visible. Every sound is tied to something visible.
- Never alter narration samples. Never invent logos, numbers or claims; claims come from the brief's allowed-claims table or the footage.
- Quality: grain stays off on UI footage, low-res sources get enhanced, and the QA magnification gate must not WARN on a shipped cut.
- Render stills before full renders. Verify from the rendered file, not from the config.
