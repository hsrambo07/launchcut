# Prior art: what open-source video tools do that launchcut could adopt

Written 2026-10-21. Scope: programmatic video engines, auto-editors, word alignment, caption tools, screen recorders with auto zoom, smart reframing, upscaling, LLM video agents, plus a measured answer to "why does our 640x360 to 1280x720 output look bad".

Evidence levels used below:
- **[measured]**: run on this machine (ffmpeg 8.1.2, OpenCV 4.14 and opencv-contrib 5.0) with the scripts in `docs/research/bench/`.
- **[source]**: read from the project's code on 2026-10-21; file paths are given.
- **[recall]**: from prior knowledge, not re-fetched. Check the linked file before coding against an exact default.

Related: `docs/research/launch-craft.md` (another session) covers platform specs, safe zones, structures and hooks. This file does not repeat them.

Note on in-flight work: as of this writing another session has uncommitted changes in the working tree that add `launchcut enhance` (Real-ESRGAN `realesr-animevideov3` plus detail transfer), a `source magnification` QA row (WARN above 3x) and set the default `grain` to 0. The recommendations below build on that work rather than replace it.

---

## 1. Projects at a glance

| Project | What it does | License | Technique worth knowing (code location) | Verdict |
|---|---|---|---|---|
| [Remotion](https://github.com/remotion-dev/remotion) | React frames screenshotted in headless Chrome, piped to ffmpeg | Remotion License, source available, not OSS (free up to 3 employees) | `spring()` defaults damping 10, mass 1, stiffness 100, analytic closed form (`packages/core/src/spring/spring-utils.ts`); `measureSpring` threshold 0.005 that must hold for 20 frames; `interpolate(..., {output: 'perceptual-scale'})` interpolates zoom in area space; `CameraMotionBlur` shutterAngle 180, samples 10, samples trail backwards, N shrinks near frame 0; h264 default CRF 18, yuv420p, x264 preset unset (libx264 medium), concurrency `min(8, cpus/2)` [source] | Adapt the spring, settle rule and blur parameters; no code (license) |
| [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | Generator-based animation in TypeScript | MIT | Spring presets as (mass, stiffness, damping, v0): Plop 0.2/20/0.68/0, Smooth 0.16/15.35/1.88/0, Strike 0.03/20/0.9/4.8, Euler at 120 Hz (`packages/core/src/tweening/spring.ts`); `Camera.centerOn(node)`; ffmpeg audio `amix normalize=0` [source] | Adapt: preset table as named eases for pops; `normalize=0` in SFX mixes |
| [Revideo](https://github.com/redotvideo/revideo) | Headless Motion Canvas fork | MIT | `workers: N` renders frame slices in parallel then `-f concat -safe 0 -c copy` (`packages/renderer/server/render-video.ts`, `packages/ffmpeg/src/utils.ts`) [source] | Adopt chunked parallel rendering |
| [editly](https://github.com/mifi/editly) | Declarative JSON5 editing on ffmpeg | MIT | gl-transitions, default 0.5 s; Ken Burns `zoomAmount` 0.1 linear; `acrossfade=c1=tri:c2=tri`; encode `libx264 -profile:v high -preset medium -crf 18` (`src/index.ts`); `dynaudnorm=g=5:maxgain=30`; no ducking [source] | Skip; launchcut's camera is already richer |
| [ShortGPT](https://github.com/RayVentura/ShortGPT) | LLM pipeline for faceless shorts | MIT | Composable JSON editing steps merged by z-order (`shortGPT/editing_framework/editing_steps/*.json`); captions split at 15 chars or 5 words (`editing_utils/captions.py`) [source] | Skip, except the "one reusable step per file" idea for style presets |
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Topic to script, TTS, stock clips, captions | MIT | Script is ground truth for text, Whisper for time: greedy merge of cues while Levenshtein similarity rises, accept above 0.8 (`app/services/subtitle.py::correct`); explicit `scale=out_color_matrix=bt709:out_range=tv,setparams=...` on every write (`app/services/video.py`); caption pop `scale = 1 - exp(-6p) cos(2.5 pi p)` over 0.18 s [source] | Adopt script-matched subtitles and the pinned matrix flags |
| [auto-editor](https://github.com/WyattBlue/auto-editor) | Cuts silence and low motion from recordings | Unlicense; now written in Nim, not Python | Per-frame audio value = peak `max(abs(sample))/32767` per 1/timebase chunk, loud if above 0.04 (`src/analyze/audio.nim`, `src/editmethods.nim`); `--margin 0.2s` then `--smooth 0.2s,0.1s` (silences under 0.2 s kept, loud runs under 0.1 s cut, `src/lib/editutil.nim`); motion method = fraction of changed pixels after `scale=400:-1,format=gray,gblur=sigma=9`; exports FCP7 xmeml, FCPXML 1.11, Shotcut, Kdenlive, OTIO, no EDL [source] | Adopt the algorithm (30 lines of numpy) |
| [WhisperX](https://github.com/m-bain/whisperX) | Whisper plus wav2vec2 forced alignment and diarization | BSD-2-Clause | Character-level CTC trellis and Viterbi backtrack (English `WAV2VEC2_ASR_BASE_960H`, `whisperx/alignment.py`); pyannote VAD onset 0.5, offset 0.363; word-boundary MAE 64.8 ms TIMIT in Nyra's benchmark; digits align poorly [source] | Skip as a dependency (torch, pyannote, HF token) |
| [stable-ts](https://github.com/jianfch/stable-ts) | Stabilises Whisper timestamps | MIT (v2.19.1) | `suppress_silence` moves word edges out of silent spans found by quantising normalised loudness (`stabilization/nonvad.py`: 99.9th percentile reference, 20 ms units, k=5 pooling, 20 levels); default regroup `da` = split on sentence punctuation, on gaps over 0.5 s, on commas only past 50 chars, max 70 chars, clamp word durations at 2.5x median; `refine()` mutes audio around boundaries; `stable_whisper.load_faster_whisper()` wraps our backend [source] | Adopt, or port the snap |
| [CrisperWhisper](https://github.com/nyrahealth/CrisperWhisper) | Verbatim Whisper that keeps um, uh, repetitions | Code MIT, weights Nyra non-commercial research license | Attention heads supervised by Montreal Forced Aligner, Viterbi with an energy blank state; gaps of 0.1 s or less split evenly (`crisperwhisper/word_timing.py`); MAE 29.6 ms TIMIT [source] | Skip the weights; borrow the 0.1 s gap rule |
| [showtime](https://github.com/FavioVazquez/showtime) | Agent skill for editing talking footage | MIT | Word edge energy snap: 10 ms RMS dB, voiced if above `max(p10 + 12, peak - 40, -65)`, trim each word to voiced frames then grow start back up to 150 ms and end forward up to 250 ms (`skills/showtime/lib/st/footage/refine.py`); filler gap scan of voiced, wordless runs of 150 to 800 ms with a held-vowel acoustic score (`fillers.py`) [source] | Adopt (pure numpy) |
| [SupoClip](https://github.com/FujiwaraChoki/supoclip) | Most complete open OpusClip clone | AGPL-3.0 | Virality as four 0 to 25 subscores (hook, engagement, value, shareability) plus hook type; second-pass comparative rerank because isolated scores are not comparable; 2 to 5 s cold-open teaser (`backend/src/ai.py`); captions colour the active word only, never scale it, because scaling reflows a centred line and makes it vibrate (`backend/src/media/captions.py`) [source] | Adapt ideas only (AGPL) |
| [captacity](https://github.com/unconv/captacity) | Burned-in captions with MoviePy | MIT | Chunk words greedily by measured pixel width within `line_count` lines, never past a sentence end; shadow = blurred copy, radius `0.1 * font_size`, no offset [source] | Adapt the pixel-fit chunking |
| [pycaps](https://github.com/francozanardi/pycaps) | CSS-styled captions via Playwright | MIT | `max_width_ratio` 0.8, 2 lines; hype preset 72 px at 1920 tall, word zoom-in 0.12 s from 0.8 with 5% overshoot; colours: active #FFFF00, spoken #FFFFFF, upcoming #DDDDDD [source] | Adapt numbers; skip Chromium |
| [clipsai](https://github.com/ClipsAI/clipsai) | Long video to clips and speaker-aware 9:16 resize | MIT, inactive since 2024 | TextTiling on transcript embeddings; resize merges diarization with scene changes inside 0.25 s, 13 frames per segment, active speaker = face whose mouth aspect ratio moves most, one static crop per segment (`clipsai/resize/resizer.py`) [source] | Adapt "who talks = mouth movement" and "one crop per segment" |
| [AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | LLM picks highlights, crops to 9:16 | MIT | LLM returns `{start_time, end_time, score 0 to 100, hook_sentence, virality_reason}` with hook in first 3 s (`shorts_generator/highlights.py`); Haar face plus EMA 0.15 crop smoothing (`local/clipper.py`) [source] | Skip; launch-craft.md hook rubric is stronger |
| [Cap](https://github.com/CapSoftware/Cap) | Open Screen Studio alternative (Rust, wgpu) | AGPL-3.0 for rendering and app crates | Cursor events logged separately (`crates/project/src/cursor.rs`); zoom segment per click `[t-300 ms, t+2500 ms]`, merge gaps up to 2.5 s, amount 2.0 (`apps/desktop-gpui/src/editor_edits.rs`); spring stiffness 200, damping 40, mass 2.25 (zeta 0.94); focus = dead-zone clusters of cursor moves (0.5/amount wide, 0.7/amount tall); edge snap 0.25 (`crates/rendering/src/zoom_spring.rs`, `zoom.rs`); radial blur for zooms (13 taps, weights `4(p - p^2)`) vs 21-tap directional for pans (`shaders/composite-video-frame.wgsl`) [source] | Adapt numbers and algorithms; no code (AGPL) |
| [OpenScreen](https://github.com/siddharthvaddem/openscreen) | Electron Screen Studio alternative | MIT | Dwell-based zoom suggestions: run while per-sample move up to 0.02 UV, keep runs of 450 to 2600 ms, centres at least 1800 ms apart (`timeline/zoomSuggestionUtils.ts`); `easeOutScreenStudio = cubicBezier(0.16, 1, 0.3, 1)`; zoom depths 1.25, 1.5, 1.8, 2.2, 3.5, 5.0; frame-rate independent follow `f = 1 - (1 - base)^(dt / 25 ms)` [source] | Adopt (MIT): dwell detector and the bezier |
| [Screenize](https://github.com/syi0808/screenize) | Swift intent-driven auto camera | Apache-2.0 | Springs as response and damping ratio (position 0.35 s, zoom 0.55 s, zeta 0.90); zoom ranges per intent (click 1.5 to 2.5, typing 2.0 to 2.5, reading 1.0 to 1.3, max 2.8); dead zone 0.75 of half-view with hysteresis 0.15 (`Generators/ContinuousCamera/DeadZoneTarget.swift`) [source] | Adopt the dead zone and intent table |
| [screenstudio-alt-skill](https://github.com/connerkward/screenstudio-alt-skill) | Python plus Swift event logger, offline polish | MIT | 60 Hz cursor, click and key JSONL logger (`src/events-log.swift`); click clusters by 2.5 s gap, pre 0.45 s, post 1.0 s, ramp 0.55 s; edge-aware zoom floor; idle = input gaps intersected with `freezedetect=n=0.003:d=1.5` (`src/polish.py`) [source] | Adopt: closest analog to launchcut |
| [Recordly](https://github.com/webadderallorg/Recordly) | Electron recorder with auto zoom | AGPL-3.0 plus branding terms | Click strength by what follows: double-click 1500, text selection 1300, dropdown 1200, text field 1100, plain 900 [source] | Adapt the idea only |
| [Screenity](https://github.com/alyssaxuu/screenity) | Chrome recorder | GPL-3.0 | Live CSS 1.5x zoom on hotkey [source] | Skip |
| [Google AutoFlip](https://github.com/google-ai-edge/mediapipe/tree/master/mediapipe/examples/desktop/autoflip) | Saliency-aware reframing | Apache-2.0 (legacy, Bazel) | Per scene: steady if focus spread under `motion_stabilization_threshold_percent` (proto 0.30, graph 0.5), else tracking with a degree-4 polynomial fit under Cauchy loss 0.5 (`quality/polynomial_regression_path_solver.cc`) [source] | Adapt the steady-or-fit rule in numpy |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Scene change detection | BSD-3-Clause | `ContentDetector(threshold=27)`, `AdaptiveDetector(adaptive_threshold=3.0, window_width=2, min_content_val=15)` (`scenedetect/detectors/`) [source] | Adapt the adaptive ratio in `probe` |
| [OpenCV YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) | Small ONNX face detector in core OpenCV | MIT | `cv2.FaceDetectorYN`, 15 values per face (box, 5 landmarks, score) [source] | Adopt; replaces Haar |
| [One Euro filter](https://github.com/casiez/OneEuroFilter) | Adaptive low-pass for jittery signals | BSD-3-Clause | `cutoff = mincutoff + beta * abs(dx)`, defaults mincutoff 1.0, beta 0.0, dcutoff 1.0 [source] | Adopt for causal smoothing |
| [Spring-It-On](https://github.com/orangeduck/Spring-It-On) | Spring and damper reference code | MIT | `halflife_to_damping(h) = 4 ln2 / h`, closed-form critical spring, double spring for S-curves [source] | Adopt |
| [OpenCV dnn_superres](https://github.com/opencv/opencv_contrib/tree/4.x/modules/dnn_superres) | ESPCN, FSRCNN, LapSRN, EDSR | Apache-2.0 module; model repos linked in section 4 | Regression-trained SR, no GAN; measured in section 2 | Adapt, clean sources only |
| [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) / [ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) | GAN super resolution | BSD-3-Clause / MIT | `realesrgan-x4plus` rewrites glyphs on UI text; `realesr-animevideov3` is the most faithful [measured, `cuts/granola-promo-v1/qa-quality/sr_compare.png`] | Adapt behind a consistency gate |
| [video-use](https://github.com/browser-use/video-use) | Claude Code and Codex editing skill (closest agent analog) | MIT | EDL JSON with `{source, start, end, beat, quote, reason}`; 30 ms audio fades at every join; self-eval renders a filmstrip plus waveform plus word labels at every cut, plus or minus 1.5 s (`helpers/timeline_view.py`); critic sub-agent told to "roast, not praise"; at most 3 self-eval passes [source] | Adopt the cut-boundary filmstrip and waveform check |
| [vidloop](https://github.com/yugt/vidloop) | Coder plus video-model judge loop | No license (ideas only) | Judge describes blind first, then answers a 12 to 14 item yes/no checklist; each check sampled 5 times, majority wins; pass at 9/10; always revise best-so-far; measured facts injected, not judged [source] | Adapt for the launchcut judge |
| [Code2Video](https://github.com/showlab/Code2Video) | Manim agent with an MLLM layout critic | MIT | Critic sees a labelled 6x6 anchor grid and returns at most 3 fixes in grid coordinates as JSON (`prompts/stage4.py`) [source] | Adapt: grid-labelled stills for the critic |
| [TheoremExplainAgent](https://github.com/TIGER-AI-Lab/TheoremExplainAgent), [HKUDS VideoAgent](https://github.com/HKUDS/VideoAgent), [Director](https://github.com/video-db/Director), LAVE ([arXiv:2402.10294](https://arxiv.org/abs/2402.10294)) | Other LLM video agents | MIT, MIT, MIT, paper only | Visual self-reflection that ends on an `<LGTM>` token; judge then reflect on the verdict; Director only loops on exec errors; LAVE is plan, approve, execute [source] | Skip, small ideas only |

## 2. The quality question: 640x360 to 1280x720 looks bad

### 2.1 What we measured

Ground truth: a native 2982x1638 AgentPlay recording, area-downscaled to 1280x720. Low-res source: that frame area-downscaled to 640x360 ("clean"), and the same frame after an x264 CRF 30 round trip ("lossy", close to a YouTube 360p download such as the Granola source). Scripts: `docs/research/bench/upscale_bench.py`, `encode_bench.py`, `predenoise.py`. Visual: `docs/research/prior-art-upscale-sheet.png`.

**Upscalers, luma PSNR and SSIM against ground truth, CPU time per 720p frame:**

| Method | Clean PSNR / SSIM | Lossy PSNR / SSIM | ms/frame |
|---|---|---|---|
| cv2 INTER_LINEAR | 32.78 / 0.928 | 30.46 / 0.870 | 3 |
| cv2 INTER_CUBIC | 33.30 / 0.937 | 30.52 / 0.870 | 2 |
| cv2 INTER_LANCZOS4 (launchcut today) | 33.17 / 0.935 | 30.48 / 0.869 | 11 to 21 |
| Lanczos4 + luma unsharp (sigma 1.0, amount 0.5) | 33.01 / 0.933 | 30.38 / 0.863 | 23 |
| ffmpeg `scale=flags=spline+accurate_rnd+full_chroma_int` | 33.28 / 0.939 | 30.53 / 0.873 | 83 (pipe overhead) |
| ffmpeg `lanczos` + `cas=strength=0.5` | 33.32 / 0.941 | 30.51 / 0.870 | 78 |
| ESPCN x2 (dnn_superres) | 33.79 / 0.946 | 30.54 / 0.874 | 87 |
| FSRCNN x2 | 33.63 / 0.943 | 30.51 / 0.872 | 125 |
| LapSRN x2 | 33.61 / 0.943 | 30.54 / 0.874 | 485 |
| EDSR x2 | 34.72 / 0.959 | 30.55 / 0.874 | 31 800 |

Findings:
1. **On a lossy 360p source every method lands within 0.2 dB.** The detail is gone before we touch it. Pre-cleaning does not help either: ffmpeg `deblock`, `spp=4`, `nlmeans=s=1.5`, and `cv2.fastNlMeansDenoisingColored(h=3)` before Lanczos all moved PSNR by less than 0.05 dB at CRF 24 and CRF 30.
2. **On a clean low-res source, deterministic SR buys a little.** ESPCN x2 is +0.6 dB over Lanczos at 87 ms/frame. EDSR is +1.5 dB but costs 32 s per frame and, in the sheet, turned "webhook retries" into something like "webhook rulries". That is a regression model inventing a glyph, not a GAN.
3. **GAN SR rewrites letters.** In `cuts/granola-promo-v1/qa-quality/sr_compare.png`, `realesrgan-x4plus` draws "approvεd" and "chocolatə"; `realesr-animevideov3` x2 is the most faithful of the GANs but still changes stroke weight.
4. **Sharpening lowers fidelity scores** (expected) and amplifies compression blocks on lossy sources. Use it lightly and on luma only.

**Encode path, 4 s hold at 60 fps from the clean source (VMAF and PSNR-Y against a lossless no-grain render):**

| Case | Delivered Mbps | VMAF | PSNR-Y |
|---|---|---|---|
| A. launchcut today: per-frame grain 1.5, CRF 15 master then CRF 18 delivery | 1.73 | 94.2 | 45.1 |
| B. no grain, master then delivery | 1.16 | 93.8 | 46.8 |
| C. no grain, single encode | 1.08 | 94.4 | 47.2 |
| D. static grain 1.5, single encode | 1.94 | 94.4 | 43.0 |
| E. no grain, single encode, `-tune animation` | 0.98 | 94.9 | 47.3 |
| F. no grain, single, `aq-mode=3:deblock=-1,-1:psy-rd=1.0,0.0` | 1.34 | 94.7 | 47.6 |
| G. no grain, single encode, 30 fps | 0.65 | 95.6 | 47.8 |
| I. no grain, single encode, 60 fps, **locked hold (no 6% drift)** | **0.14** | **96.2** | **48.8** |

Findings:
5. **The slow zoom drift on holds is the most expensive thing in the encode.** Every frame resamples the UI at a new sub-pixel phase, so text shimmers and the encoder pays for a new picture every frame: 7.7x the bitrate of a locked hold and 1.6 dB lower PSNR. On a 2x upscaled source the shimmer is visible.
6. **Grain costs 60% more bits and about 2 dB on text,** and static grain is no better because the UI moves under it. VMAF scores grain slightly up (a known VMAF bias toward added texture), so do not trust VMAF alone here.
7. **The double encode costs about 0.4 dB and 0.6 VMAF.** Small, but free to remove.
8. **The 18 Mbps cap is not the problem at 720p.** These clips need 1 to 2 Mbps. Bitrate starvation only bites at 1080p60 with grain, which is where the 42 Mbps pitfall in RULES.md came from.
9. **Colour matrix is fine on ffmpeg 8.1.2.** Piping bgr24 into libx264 with `-colorspace bt709` produced a bt709 matrix (max error 2 code values on accent, alert and blue swatches), and decoding a tagged bt709 source to bgr24 was within 1 code value. MoneyPrinterTurbo's source pins `scale=out_color_matrix=bt709` because older ffmpeg builds converted RGB to YUV with BT.601 regardless of tags. That did not reproduce on 8.1.2, but the pin costs nothing and protects other machines (flags below).

### 2.2 Recommendations, in order of payoff

1. **Get a better source.** Nothing in the pipeline recovers a YouTube 360p download. Ask for the original capture, or re-record at native Retina resolution (macOS records at 2x; Cap and Screen Studio record native and export 1080p or 4K). Put this in RULES.md intake: "source under 1080p: ask for the original before anything else".
2. **Budget magnification.** Text from a lossy 360p source stays readable to about 2x screen px per source px, and from a clean one to about 3x. The in-flight `source magnification` QA row warns at 3x; make it source-aware: `limit = 2.0 if source_is_lossy else 3.0`, where `source_is_lossy = bits_per_pixel < 0.1` with `bpp = bitrate / (w * h * fps)` from ffprobe. Above the limit, frame wider or float the window.
3. **Lock holds on upscaled sources.** In `ShotCamera.__call__`, when the camera is not moving (`|ds/dt| / s < 0.002` per frame and centre speed under 0.05 screen px per frame) and source magnification is at least 1.5, snap: `s` to the nearest of `{1, 1.5, 2, 3}` x cover when within 4%, and `cx, cy` so that `W/2 - cx*s` and `H/2 - cy*s` are integers. Replace the "slow drift 5 to 10%" advice in RULES.md section 3 with "no drift on holds when magnification is above 1.5x".
4. **Use a deterministic upscale and gate any SR.** Default: one resampling from source to screen (the existing single `warpPerspective`), INTER_CUBIC or LANCZOS4 (within 0.15 dB of each other; cubic rings less on block edges and is 5x faster). Optional SR in `enhance`: ESPCN x2 for clean sources (`sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel("ESPCN_x2.pb"); sr.setModel("espcn", 2); up = sr.upsample(bgr)`, needs `opencv-contrib-python-headless<5`). For any SR, GAN or not, add a **back-projection consistency gate**: `back = cv2.resize(up, (w, h), interpolation=cv2.INTER_AREA)`; luma PSNR of `back` vs the source must be at least 38 dB per frame, else fall back to cubic for that frame. This catches invented glyphs, because a rewritten letter no longer downsamples to the pixels we actually have.
5. **Grain off for UI, background only if wanted.** The default is now 0 (in flight). If a brand wants texture, apply it only where the window mask `a` is below 0.5: `img += noise * g * (1 - a)[..., None]`.
6. **Encode once.** Pipe raw frames into a single ffmpeg with two outputs: the delivery encode and a lossless archive.

```
ffmpeg -f rawvideo -pix_fmt bgr24 -s 1280x720 -r 30 -i - \
  -vf "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int" \
  -map 0:v -c:v libx264 -preset slow -crf 18 -tune animation -x264-params aq-mode=3 \
  -maxrate 18M -bufsize 36M -g 60 -pix_fmt yuv420p -profile:v high \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart picture-delivery.mp4 \
  -map 0:v -c:v ffv1 -level 3 -pix_fmt bgr0 master.mkv
```

   `deliver.py` then only muxes audio with `-c:v copy`, which it already does for the muted and VO variants. Keep `crf_master` as the archive knob only if someone needs an H.264 master.
7. **x264 settings for UI.** `-tune animation` measured 10% fewer bits and +0.5 VMAF on UI. x264's animation tune is deblock 1:1, psy-rd 0.4, aq-strength 0.6, two extra B-frames and doubled refs [recall, x264 `common/base.c`]. Add `aq-mode=3` for dark-mode UIs (variance AQ biased toward dark areas, which protects dark gradients from banding). Avoid `-tune stillimage` for moving cuts (psy-rd 2.0 adds ringing around text) and `-tune grain` (spends bits on noise). Keyframe every 2 s (`-g 2*fps`).
8. **Frame rate: 30 fps for upscaled or text-heavy cuts.** Measured 40% fewer bits and +1.2 VMAF over 60 fps for a hold. Keep 60 only when whips and whip-heavy camera work dominate and the source is crisp. Most screen recordings are 30 fps or VFR anyway, so 60 fps just duplicates source frames between camera samples. Add `fps: 30` to a new `upscaled-16x9` preset or make `twitter-16x9` choose 30 when source fps is 30 or lower.
9. **Chroma: stay 4:2:0, fix the conversion.** Platforms transcode to 4:2:0 regardless, and High 4:4:4 Predictive H.264 does not play in most browsers and phones. Use `full_chroma_int` and an explicit `out_color_matrix` (above) so coloured text (red errors, accent chips) does not smear more than it has to. On decode, add `-sws_flags accurate_rnd+full_chroma_int` (or `scale=in_color_matrix=auto:flags=accurate_rnd+full_chroma_int`) to the `media.py` ffmpeg command so 4:2:0 chroma is interpolated properly before the warp.
10. **Re-set the text that matters.** When a number or label must read at phone width and the source cannot carry it, draw it fresh with Pillow as a callout (a pill or card tied to the ring), copying the exact string from the recording. This stays inside rule 8 (real things only) and is what makes Screen Studio style cuts look sharp: the overlays are native resolution even when the footage is not.

---

## 3. Ranked improvements for launchcut

Ranked by visible payoff per hour of work. Items 1 to 3 come out of the measurements in section 2.

### 1. Single-pass encode with UI encoder settings
- Where: `render.py` `Renderer.render` encoder args, first ffmpeg call in `deliver.py`.
- What: the two-output command in 2.2 item 6 (delivery H.264 plus lossless FFV1 archive from the same raw pipe). `deliver.py` then only muxes audio with `-c:v copy`. Add `-tune animation -x264-params aq-mode=3`, `-g 2*fps`, and the explicit `scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int`. Default `fps` to 30 when the source is 30 fps or lower.
- QA: add a gate that ffprobe reports `color_space=bt709` on the delivery.
- Gain: about 0.4 dB from no generation loss, 10% fewer bits, one x264 pass instead of two.

### 2. Locked holds and a magnification budget
- Where: `camera.py` `ShotCamera.__call__`, and the in-flight magnification row in `qa.py`.
- Snap: measure velocity as `self(t + 1/fps)` minus `self(t)`. If `abs(ds)/s < 0.002` and `hypot(dcx, dcy) * s < 0.05` px, and source magnification `s / upf` is at least 1.5, then:
  - snap `s` to the nearest of `{1, 1.5, 2, 3} * cover` when within 4%;
  - snap `cx, cy` so that `W/2 - cx*s` and `H/2 - cy*s` are whole pixels.
- Budget: WARN at 2x for lossy sources and 3x for clean ones. A source is lossy when `bitrate / (w * h * fps) < 0.1` bits per pixel.
- Gain: holds cost 7.7x fewer bits and the text stops shimmering.

### 3. Consistency-gated super resolution in `enhance`
- Where: the in-flight `launchcut/enhance.py`.
- What:
  - Keep `realesr-animevideov3` as the GAN option.
  - Add ESPCN x2 as the default for clean sources: `sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel("ESPCN_x2.pb"); sr.setModel("espcn", 2)`. This needs `opencv-contrib-python-headless<5` as an optional extra.
  - Gate every SR frame by back-projection: `back = cv2.resize(up, (w, h), interpolation=cv2.INTER_AREA)`. Keep the frame only if its luma PSNR against the source frame is at least 38 dB; otherwise fall back to cubic for that frame.
  - Log the per-frame scores so the stills loop can show where it fell back.
- Gain: sharper text when the source can carry it, and a hard stop on invented glyphs.

### 4. Click and dwell driven zoom suggestions (Cap, OpenScreen, screenstudio-alt-skill)
- Best input is an event log, which every serious Screen Studio clone records. Accept `sources.<name>.events: events.jsonl` with `{t, x, y, type: move|down|up|key}`, as in Cap's `CursorMoveEvent`/`CursorClickEvent` or screenstudio-alt-skill's 60 Hz Swift logger.
- Without a log, detect the cursor from pixels:
  - `cv2.matchTemplate(gray, tpl, cv2.TM_CCORR_NORMED, mask=alpha)` with macOS arrow and I-beam templates at scales 1 and 2.
  - Wrap the result in `np.nan_to_num` and accept hits at 0.9 or more.
  - Search a 200 px window around the last hit and fall back to the full frame.
- Click inference: a dwell (OpenScreen: per-sample move up to 0.02 of the frame for 450 to 2600 ms) followed within 0.5 s by a frame-diff spike within 150 px of the cursor.
- Segments (Cap rule): each click becomes `[t - 0.3, t + 2.5]` s; merge segments with gaps of 2.5 s or less; ignore clicks in the last 1 s. Zoom amount comes from intent (Screenize): click 1.5 to 2.5, typing 2.0 to 2.5, reading 1.0 to 1.3, never above the magnification budget from item 2.
- Probe writes these as suggested `camera` keyframes, `clicks` and `pulses` in `inventory.md`. The agent still chooses.
- Spikes: in `probe.events` replace `median * 8` with PySceneDetect's adaptive ratio `d[i] / mean(neighbours within 2 samples) > 3.0`. Scrolling then stops producing false spikes.

### 5. Spring camera ease
- Where: `ease.py` and `camera.py`.
- Formula (critically damped, Holden). With half-life `h`:
  - `y = 2 ln2 / h`, `j0 = x0 - goal`, `j1 = v0 + j0 * y`
  - `x(t) = goal + exp(-y t) * (j0 + j1 t)`
  - `v(t) = exp(-y t) * (v0 - j1 y t)`
- Apply it to `log(s)`, `cx` and `cy`. Retarget at each keyframe and carry velocity across, as Cap does.
- Defaults from the surveyed tools, which all sit at zeta 0.9 to 0.95:
  - zoom half-life 0.14 s (Cap's 200/40/2.25 is 156 ms and settles in about 0.45 s);
  - pan half-life 0.10 s.
- Settle rule (Remotion `measureSpring`): done when within 0.005 of the target for 20 consecutive frames. Use it to compute the hold that RULES.md section 3 requires.
- Also add `easeOutScreenStudio = cubic-bezier(0.16, 1, 0.3, 1)` (OpenScreen) as a named ease for punch-ins.
- Motion blur per Remotion: express `shutter` as an angle (default 180 degrees) and shrink the sample count near shot starts. Cap uses a cheaper alternative for pure zooms: a 13-tap radial blur toward the zoom centre, weights `4(p - p^2)`.

### 6. Word edge snapping and a silence pass for talking heads (showtime, stable-ts, auto-editor)
- Where: `speech.py`, right after faster-whisper and before the pause list.
- Snap (showtime `refine.py`):
  - Compute 10 ms RMS in dB; a frame is voiced if above `max(p10 + 12, peak - 40, -65)`.
  - Trim each word to its first and last voiced frame.
  - Grow the start back up to 150 ms and the end forward up to 250 ms over voiced frames, never into a neighbouring word. Minimum word length 50 ms.
- Silence pass (auto-editor):
  - Per-frame peak `max(abs(x)) / 32767` above 0.04 means loud.
  - Dilate by 0.2 s each side.
  - Keep silences under 0.2 s; cut loud runs under 0.1 s.
  - Write `keep.yaml` of `[start, end]` ranges.
- VAD: faster-whisper defaults to `min_silence_duration_ms=2000, speech_pad_ms=400`, and its VAD joins are known to stretch word times (faster-whisper issues 120 and 230). Pass `vad_parameters=dict(min_silence_duration_ms=500, speech_pad_ms=200)`. Keep the pause list derived from word gaps, as today.

### 7. Fillers Whisper hides
- Add OpenAI's documented prompt to `initial_prompt`: `"Umm, let me think like, hmm... Okay, here's what I'm, like, thinking."` Join it after the names from `--prompt`. Only the last 224 tokens count.
- Acoustic gap scan (showtime `fillers.py`): voiced runs of 150 to 800 ms that no word covers are filler candidates.
  - Confirm one with a held-vowel score `clip((vr - 0.4)/0.4) * clip((steady - 0.55)/0.3) * clip((0.25 - f0_cv)/0.15) >= 0.75`, where:
    - `vr` is the fraction of 30 ms frames with autocorrelation of at least 0.5 in 70 to 400 Hz;
    - `steady` is the mean cosine similarity of consecutive log spectra;
    - `f0_cv` is pitch std divided by mean.
  - Flag them in `transcript.md` as cut candidates.

### 8. Captions and subtitles that fit and do not vibrate
- Chunking (captacity): replace "3 words" with greedy pixel fit, as many words as fit in `max_width * W` on at most 2 lines, never past a sentence end.
- Active word: colour only, never per-word scale. Scaling changes advance width and reflows the centred line (SupoClip's comment). Pop the whole chunk once instead: scale 0.92 to 1.0 over 140 ms (ASS `\fscx92\fscy92\t(0,140,\fscx100\fscy100)`).
  - Pillow alternative: lay out at scale 1.0, then draw only the active word scaled about its own centre in its fixed slot.
- Colours (pycaps hype): active accent, spoken words text colour, upcoming words at about 85% brightness.
- Vertical safe zone at 1080x1920. The union of Meta (14% top, 35% bottom, 6% sides) and measured TikTok and Shorts templates is:
  - top 288 px, bottom 672 px, left 65 px, right 192 px;
  - plus a 300 px right column below y = 840.
  - Captions therefore sit between y = 1000 and 1248. Add a `vertical-9x16` default `subtitles.y` of 1120 and a QA check that no caption pixel crosses those bounds. Platform details are in `launch-craft.md` 1b.

### 9. Script-matched subtitles (MoneyPrinterTurbo)
- When a script exists (VO or `SCRIPT.md`), the script is ground truth for words and Whisper for timing.
- Greedily merge consecutive recognised chunks while the Levenshtein similarity `1 - dist/maxlen` to the current script line keeps rising, and accept the match above 0.8.
- Within a matched line, map words with `difflib.SequenceMatcher(None, asr, script).get_opcodes()`:
  - copy the script spelling and keep the ASR times on equal-length replacements;
  - spread times linearly elsewhere.
- This retires most of `subtitles.fix`.

### 10. Soundbite ranking that knows hooks (SupoClip, clipsai)
- Keep the current score as a pre-filter (top 12 sentences or phrase spans).
- An LLM scores each 0 to 25 on hook, engagement, value and shareability, with a hook type. A second, comparative pass then reranks them together, because isolated scores are not comparable.
- Boundaries: clipsai's TextTiling depth score `(left_peak - gap) + (right_peak - gap)` over sentence-embedding similarity, with a cut where depth exceeds mean + std. Run it with k = 5 sentences so a soundbite never starts mid-topic.
- Optional cold open: the strongest 2 to 5 s line replayed before the clip. Combine with the rubric in `launch-craft.md` section 3.

### 11. YuNet faces and a steady-or-fit vertical crop (AutoFlip, Screenize)
- Detector:
  - `det = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (w, h), 0.9, 0.3, 5000)`, with `det.setInputSize((w, h))` per frame size.
  - `_, faces = det.detect(bgr)` returns Nx15 (box, 5 landmarks, score) or None.
  - Downscale to about 640 px wide first and run at 5 fps. The model is 230 KB, MIT, in core OpenCV 4.8 and up.
- Path, per shot:
  - Steady if the face centre spread is under 0.3 of the frame width: one fixed crop, eyes about 1/3 from the top.
  - Otherwise fit `numpy.polyfit(t, x, 4)` with Cauchy IRLS weights `1 / (1 + (r/0.5)^2)`.
  - Or use Screenize's dead zone: stay still while the face is inside 0.75 of the half-view, with hysteresis 0.15, and correct only by the overshoot plus 45% of the remaining distance.
- clipsai rule: the crop changes only at a speaker change or a cut.

### 12. Agent QA that sees what single stills miss (video-use, vidloop, Code2Video)
- Cut-boundary sheet (video-use `helpers/timeline_view.py`), for every cut on the delivered file:
  - a 10-frame filmstrip over plus or minus 1.5 s;
  - a waveform envelope;
  - word labels and silence bands.
  - This catches jumps, audio pops and subtitles hidden behind overlays.
- Also add 30 ms audio fades at every dialog join (`afade=t=in:d=0.03`). The current 8 ms fades click on some voices.
- Judge protocol (vidloop):
  - describe the stills blind first;
  - then answer a binary checklist written from PLAN.md;
  - sample each check 5 times and take the majority;
  - pass at 9 of 10;
  - always revise from the best version so far;
  - feed measured facts (duration, LUFS, magnification) to the judge instead of asking it to judge them.
- Stills for the critic (Code2Video): overlay a labelled grid (A1 to F6) or the cut's box ids, and cap feedback at 3 fixes per round expressed in those coordinates. The fixes then map straight onto `cut.yaml`.

### Also worth doing later
- Parallel chunked render (Revideo, Remotion):
  - split on shot boundaries into `min(8, cpus/2)` processes, each calling `Renderer.render(out, t_from, t_to)`;
  - encode each chunk with `-force_key_frames 0` and `-x264-params open-gop=0`;
  - join with `-f concat -safe 0 -i list.txt -c copy`.
- Optional libass backend for subtitles (`\kf` karaoke, `\t` animation) if Pillow drawing becomes the bottleneck.

## 4. Sources

Source files were fetched on 2026-10-21 from default branches (via raw.githubusercontent.com unless noted).

Engines and editors:
- Remotion: https://github.com/remotion-dev/remotion. Files: `packages/core/src/spring/{index,spring-utils,measure-spring}.ts`, `packages/core/src/{interpolate,easing,v5-flag}.ts`, `packages/renderer/src/{crf,ffmpeg-args,get-concurrency,pixel-format,image-format,prespawn-ffmpeg}.ts`, `packages/renderer/src/options/{x264-preset,color-space}.tsx`, `packages/motion-blur/src/CameraMotionBlur.tsx`. License: https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
- Motion Canvas: https://github.com/motion-canvas/motion-canvas. Files: `packages/core/src/tweening/{timingFunctions,spring}.ts`, `packages/2d/src/lib/components/Camera.ts`, `packages/ffmpeg/server/FFmpegExporterServer.ts`
- Revideo: https://github.com/redotvideo/revideo. Files: `packages/renderer/server/render-video.ts`, `packages/ffmpeg/src/{ffmpeg-exporter-server,utils}.ts`
- editly: https://github.com/mifi/editly. Files: `src/{index,audio,easings,transition,configuration,util}.ts`, `src/sources/image.ts`
- ShortGPT: https://github.com/RayVentura/ShortGPT (branch stable). Files: `shortGPT/editing_framework/editing_steps/*.json`, `core_editing_engine.py`, `editing_utils/captions.py`, `prompt_templates/editing_generate_videos.yaml`
- MoneyPrinterTurbo: https://github.com/harry0703/MoneyPrinterTurbo. Files: `app/services/{video,subtitle,voice,task}.py`

Speech, cutting, captions:
- auto-editor: https://github.com/WyattBlue/auto-editor. Files: `src/analyze/{audio,motion}.nim`, `src/{editmethods,cli,conductor}.nim`, `src/lib/editutil.nim`, `src/render/smart.nim`, `src/exports/{fcp7,fcp11}.nim`
- WhisperX: https://github.com/m-bain/whisperX. Files: `whisperx/{alignment,asr,__main__}.py`, `whisperx/vads/pyannote.py`. Paper: https://www.robots.ox.ac.uk/~vgg/publications/2023/Bain23/bain23.pdf
- faster-whisper: https://github.com/SYSTRAN/faster-whisper. Files: `faster_whisper/{transcribe,vad}.py`. Issues: https://github.com/SYSTRAN/faster-whisper/issues/120, https://github.com/SYSTRAN/faster-whisper/issues/230
- stable-ts: https://github.com/jianfch/stable-ts. Files: `stable_whisper/{result,default}.py`, `stabilization/nonvad.py`, `whisper_word_level/{faster_whisper,original_whisper}.py`, `non_whisper/refinement.py`
- CrisperWhisper: https://github.com/nyrahealth/CrisperWhisper. File: `crisperwhisper/word_timing.py`. Benchmark: https://www.nyra-labs.com/research/attention-to-aligner
- showtime: https://github.com/FavioVazquez/showtime. Files: `skills/showtime/lib/st/footage/{refine,fillers,util,transcribe}.py`
- Whisper filler prompt: https://developers.openai.com/cookbook/examples/whisper_prompting_guide, https://developers.openai.com/api/docs/guides/speech-to-text
- clipsai: https://github.com/ClipsAI/clipsai. Files: `clipsai/clip/{clipfinder,texttiler,text_embedder}.py`, `clipsai/resize/{resizer,resize}.py`
- AI-Youtube-Shorts-Generator: https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator (also https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator). Files: `shorts_generator/highlights.py`, `shorts_generator/local/clipper.py`
- SupoClip: https://github.com/FujiwaraChoki/supoclip. Files: `backend/src/ai.py`, `backend/src/caption_templates.py`, `backend/src/media/captions.py`
- captacity: https://github.com/unconv/captacity. Files: `captacity/{__init__,segment_parser}.py`
- pycaps: https://github.com/francozanardi/pycaps. Files: `src/pycaps/template/preset/{default,hype}/*`, `layout/definitions.py`, `animation/builtin/primitive/pop_in_primitive.py`, `renderer/css_subtitle_renderer.py`
- auto-subtitle: https://github.com/m1guelpf/auto-subtitle
- ASS tags: https://aegisub.org/docs/latest/ass_tags/
- Safe zones: https://www.facebook.com/business/ads-guide/update/image/instagram-reels, https://www.upload-post.com/tools/safe-zone-checker/ (measured TikTok and Shorts templates; third party)

Cameras, cursors, reframing:
- Cap: https://github.com/CapSoftware/Cap. Files: `crates/rendering/src/{spring_mass_damper,zoom_spring,zoom,cursor_interpolation,lib}.rs`, `crates/rendering/src/layers/{cursor,click_ripple}.rs`, `crates/rendering/src/shaders/composite-video-frame.wgsl`, `crates/project/src/{configuration,cursor}.rs`, `apps/desktop-gpui/src/editor_edits.rs`
- OpenScreen: https://github.com/siddharthvaddem/openscreen. Files: `src/components/video-editor/timeline/zoomSuggestionUtils.ts`, `src/components/video-editor/videoPlayback/{zoomSpring,motionSmoothing,cursorFollowUtils,constants,zoomRegionUtils,mathUtils}.ts`, `src/lib/cursor/cursorPathSmoothing.ts`
- Recordly: https://github.com/webadderallorg/Recordly. Files: `src/components/video-editor/timeline/zoomSuggestionUtils.ts`, `videoPlayback/{cursorFollowCamera,cursorSway}.ts`
- Screenize: https://github.com/syi0808/screenize. Files: `Screenize/Generators/GenerationSettings.swift`, `Generators/ContinuousCamera/{SpringDamperSimulator,DeadZoneTarget}.swift`
- screenstudio-alt-skill: https://github.com/connerkward/screenstudio-alt-skill. Files: `src/events-log.swift`, `src/polish.py`, `docs/ARCHITECTURE.md`
- Screenity: https://github.com/alyssaxuu/screenity. Files: `src/pages/Content/utils/{ZoomContainer,CursorModes}.jsx`
- AutoFlip: https://github.com/google-ai-edge/mediapipe/tree/master/mediapipe/examples/desktop/autoflip. Files: `autoflip_graph.pbtxt`, `quality/{cropping.proto,kinematic_path_solver.proto,scene_camera_motion_analyzer.cc,polynomial_regression_path_solver.cc}`
- Autocrop-vertical: https://github.com/kamilstanuch/Autocrop-vertical (no license)
- PySceneDetect: https://github.com/Breakthrough/PySceneDetect. Files: `scenedetect/detectors/{content,adaptive,hash,histogram}_detector.py`
- YuNet: https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet. API: https://docs.opencv.org/4.x/df/d20/classcv_1_1FaceDetectorYN.html
- One Euro filter: https://github.com/casiez/OneEuroFilter, https://gery.casiez.net/1euro/
- Springs: https://theorangeduck.com/page/spring-roll-call, https://github.com/orangeduck/Spring-It-On (`common.h`, `springdamper.c`, `doublespring.c`), https://www.ryanjuckett.com/damped-springs/

Agents:
- video-use: https://github.com/browser-use/video-use. Files: `SKILL.md`, `helpers/{render,timeline_view,grade,transcribe,pack_transcripts}.py`
- vidloop: https://github.com/yugt/vidloop
- Code2Video: https://github.com/showlab/Code2Video. Files: `src/agent.py`, `prompts/stage4.py`
- TheoremExplainAgent: https://github.com/TIGER-AI-Lab/TheoremExplainAgent. Files: `src/core/video_renderer.py`, `task_generator/prompts_raw/prompt_visual_self_reflection.txt`
- HKUDS VideoAgent: https://github.com/HKUDS/VideoAgent. Files: `environment/agents/multi.py`, `environment/roles/vid_editor.py`, `environment/roles/vid_rhythm/rhythm_detector.py`
- Director: https://github.com/video-db/Director. Files: `backend/director/core/reasoning.py`, `backend/director/agents/editing/agent.py`
- LAVE: https://arxiv.org/abs/2402.10294

Upscaling and encoding:
- OpenCV dnn_superres: https://github.com/opencv/opencv_contrib/tree/4.x/modules/dnn_superres. Models: https://github.com/fannymonori/TF-ESPCN, https://github.com/Saafke/FSRCNN_Tensorflow, https://github.com/fannymonori/TF-LapSRN, https://github.com/Saafke/EDSR_Tensorflow
- Real-ESRGAN: https://github.com/xinntao/Real-ESRGAN, https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan
- ffmpeg filters and scaler: https://ffmpeg.org/ffmpeg-filters.html, https://ffmpeg.org/ffmpeg-scaler.html
- x264 tunes and AQ: https://code.videolan.org/videolan/x264/-/blob/master/common/base.c, https://trac.ffmpeg.org/wiki/Encode/H.264
- VMAF: https://github.com/Netflix/vmaf
- Platform specs: `docs/research/launch-craft.md` section 1b

Local evidence:
- `docs/research/bench/upscale_bench.py`, `encode_bench.py`, `predenoise.py`. Run with `python -I <script> <workdir> [<modeldir>]`. The workdir needs `gt720.png`; models are the four `*_x2.pb` files above.
- `docs/research/prior-art-upscale-sheet.png`: ground truth vs upscalers, clean and lossy rows.
- `cuts/granola-promo-v1/qa-quality/sr_compare.png`: Lanczos vs animevideov3 vs x4plus on the Granola source.
