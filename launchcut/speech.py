"""Dissect speech: word-timed transcript, sentences, pauses, filler words and soundbite candidates.
Needs the optional extra: `uv run --extra speech launchcut transcribe <clip>` (faster-whisper, runs locally on CPU)."""
import json, os, re

FILLERS = {"um", "uh", "erm", "hmm", "like", "basically", "actually", "literally", "so", "yeah", "right", "okay", "ok"}
FILLER_PHRASES = ["you know", "i mean", "kind of", "sort of"]


def transcribe(path, out_dir, model="small.en", language=None, prompt=None):
    """prompt: names and jargon the model should expect, e.g. "Entelligence, AgentPlay, Claude Code"."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("transcription needs the speech extra: uv run --extra speech launchcut transcribe <clip>")
    os.makedirs(out_dir, exist_ok=True)
    import subprocess
    import numpy as np
    # decode with ffmpeg ourselves: faster-whisper's PyAV loader breaks across PyAV releases
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, info = m.transcribe(audio, word_timestamps=True, vad_filter=True, beam_size=5, language=language,
                              condition_on_previous_text=False, initial_prompt=prompt)
    words, segments = [], []
    for s in segs:
        segments.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()})
        for w in s.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)})
    data = {"source": os.path.abspath(path), "model": model, "language": info.language, "duration": info.duration,
            "segments": segments, "words": words}
    js = os.path.join(out_dir, "transcript.json")
    with open(js, "w") as f:
        json.dump(data, f, indent=1)
    md = os.path.join(out_dir, "transcript.md")
    with open(md, "w") as f:
        f.write(analysis_md(data))
    return js, md


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def sentences(words):
    """group words into sentences on terminal punctuation or a long pause"""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        gap = words[i + 1]["s"] - w["e"] if i + 1 < len(words) else 9
        if re.search(r"[.!?]$", w["w"]) or gap > 0.9:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def flags(sent):
    text = " ".join(w["w"] for w in sent)
    low = " " + " ".join(norm(w["w"]) for w in sent) + " "
    fill = [w["w"] for w in sent if norm(w["w"]) in ("um", "uh", "erm", "hmm")]
    soft = [w["w"] for w in sent if norm(w["w"]) in FILLERS - {"um", "uh", "erm", "hmm"}]
    phr = [p for p in FILLER_PHRASES if f" {p} " in low]
    dur = sent[-1]["e"] - sent[0]["s"]
    wpm = len(sent) / dur * 60 if dur > 0 else 0
    conf = sum(w["p"] for w in sent) / len(sent)
    return text, fill, soft + phr, dur, wpm, conf


def analysis_md(data):
    words = data["words"]
    out = [f"# Transcript: {os.path.basename(data['source'])}\n",
           f"{len(words)} words, {data['duration']:.1f}s, model {data['model']}. Times are seconds in the source.\n"]
    if not words:
        return "\n".join(out) + "\nNo speech found.\n"
    talk = sum(w["e"] - w["s"] for w in words)
    out.append(f"Speech covers {talk / data['duration'] * 100:.0f}% of the clip; average {len(words) / max(talk, 1e-6) * 60:.0f} words per minute while talking.\n")
    out.append("## Sentences\n\n| # | start | end | dur | text | hard fillers | soft fillers | wpm | conf |\n|---|---|---|---|---|---|---|---|---|")
    sents = sentences(words)
    cands = []
    for i, s in enumerate(sents, 1):
        text, fill, soft, dur, wpm, conf = flags(s)
        out.append(f"| {i} | {s[0]['s']:.2f} | {s[-1]['e']:.2f} | {dur:.1f} | {text} | {' '.join(fill) or '-'} | {', '.join(soft) or '-'} | {wpm:.0f} | {conf:.2f} |")
        score = (1.0 if 2.5 <= dur <= 12 else 0.4) - 0.25 * len(fill) - 0.08 * len(soft) + (conf - 0.8)
        cands.append((score, i, s, text, dur))
    out.append("\n## Pauses of 0.35 s or more (cut points for jump cuts)\n\n| after word | at | gap |\n|---|---|---|")
    for a, b in zip(words, words[1:]):
        g = b["s"] - a["e"]
        if g >= 0.35:
            out.append(f"| {a['w']} | {a['e']:.2f} | {g:.2f} |")
    out.append("\n## Soundbite candidates (complete, 2.5 to 12 s, few fillers)\n\n| rank | sentence | start | end | text |\n|---|---|---|---|---|")
    for r, (sc, i, s, text, dur) in enumerate(sorted(cands, key=lambda c: -c[0])[:8], 1):
        out.append(f"| {r} | {i} | {s[0]['s']:.2f} | {s[-1]['e']:.2f} | {text} |")
    out.append("\nNext: pick the hook line (the strongest single claim), list the keep ranges, and cut at the pauses above.\n")
    return "\n".join(out) + "\n"
