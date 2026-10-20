# launchcut: agent notes

- Making a video: follow `RULES.md` phase by phase (or run `/launchcut`). `REFERENCE.md` is the cut schema, and `examples/agentplay/` is the reference cut.
- Changing the engine: run `uv run launchcut stills examples/agentplay/cut.yaml 0 4.6 8.2 11.6` before and after your change and compare the sheets. Any new `cut.yaml` key goes into `REFERENCE.md` and `config.py` DEFAULTS in the same change.
- Keep the engine dependency-light: numpy, opencv-python-headless<5, pillow, pyyaml, plus system ffmpeg. All type is drawn with Pillow, because ffmpeg builds often lack drawtext.
- Writing style for docs and comments: no em dashes, and plain sentences.
