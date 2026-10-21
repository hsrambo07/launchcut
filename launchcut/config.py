"""Load a cut.yaml: defaults, platform presets, `extends:` style files, path and glob resolution, validation.
Every variable a cut can set lives in DEFAULTS or in the per-shot keys documented in REFERENCE.md."""
import copy, glob, os
import numpy as np
import yaml

PRESETS = {
    # size, fps, video bitrate cap (Mbps) and loudness target for each platform
    "twitter-16x9": dict(size=[1920, 1080], fps=60, max_mbps=18, lufs=-14),
    "twitter-1x1": dict(size=[1080, 1080], fps=60, max_mbps=18, lufs=-14),
    "vertical-9x16": dict(size=[1080, 1920], fps=60, max_mbps=18, lufs=-14),   # Reels, Shorts, TikTok
    "linkedin-16x9": dict(size=[1920, 1080], fps=30, max_mbps=15, lufs=-14),
    "feed-4x5": dict(size=[1080, 1350], fps=60, max_mbps=18, lufs=-14),
    "web-16x9": dict(size=[1920, 1080], fps=60, max_mbps=25, lufs=-16),
}

DEFAULTS = {
    "name": "cut",
    "output": {"preset": "twitter-16x9", "dir": "out", "deliver_to": None, "crf_delivery": 16},
    "sources": {},
    "style": {
        # neutral on purpose: every brand's look comes from its own style.yaml (written by the art director)
        "palette": {"bg": "#111111", "text": "#F5F5F5", "accent": "#3B82F6", "alert": "#EF4444", "muted": "#A3A3A3"},
        "fonts": {"display": "InterVariable@SemiBold", "body": "InterVariable@Medium", "mono": "Menlo"},
        "grade": {"black": 0, "gain": 1.0, "out_black": 0},   # out = (in - black) * gain + out_black on recording pixels
        "vignette": 0.12,
        "grain": 0.0,                                          # film grain muddies UI text; add it only for cinematic footage
        "grid": {"size": 96, "strength": 9},                 # background grid seen around the window; strength 0 = off
        "window": {"radius": 24, "shadow": 0.6},             # rounded recording edge + drop shadow when zoom < 1
        "caption": {"size": 78, "margin": 74, "band": 0.82, "stagger": 0.05, "rise": 30, "font": "display"},
        "ring": {"width": 3.0, "glow": 0.45, "pad": 8, "radius": 16},
        "motion_blur": {"enabled": True, "max_samples": 14, "px_per_sample": 2.5, "shutter": 1.0},
        "enter": {"type": "punch", "d": 0.3, "from": 0.5},
        "exit": {"type": "whip", "d": 0.18, "k": 2.0},
    },
    "audio": {
        "sfx": True,
        "gain": 1.0,
        "open_hit": False,          # impact on frame 0
        "beat": None,               # {bpm, from, to} pulse bed, kick on beats, hats on off-beats
        "vo": None,                 # path to narration; never altered, SFX ducked under it
        "dialog": False,            # true: every video shot plays its own recorded sound (talking heads)
        "duck_db": 8,
        "cues": [],                 # manual cues: {t, sound, gain, pan, d}
        "seed": 7,
    },
    "allow_dark_frames": False,
    "subtitles": None,              # {transcript, words, gap, y, size, mode, emphasis, upper, hide_punct, hold, max_width}
}

REQUIRED_SHOT = {"ui": ["source", "duration"], "image": ["source", "duration"], "card": ["duration", "lines"], "end": ["duration"]}


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def resolve_path(p, root):
    p = os.path.expanduser(str(p))
    if not os.path.isabs(p):
        p = os.path.join(root, p)
    if any(ch in p for ch in "*?["):
        hits = sorted(glob.glob(p))
        if not hits:
            raise FileNotFoundError(f"no file matches {p}")
        p = hits[0]
    return p


def hex_bgr(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return np.array([b, g, r], np.float32)


class Cut:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.root = os.path.dirname(self.path)
        raw = self._load(self.path)
        cfg = deep_merge(DEFAULTS, raw)
        preset = PRESETS.get(cfg["output"]["preset"])
        if preset is None:
            raise ValueError(f"unknown preset {cfg['output']['preset']}, pick one of {sorted(PRESETS)}")
        cfg["output"] = deep_merge(preset, cfg["output"])
        self.cfg = cfg
        self.name = cfg["name"]
        self.W, self.H = cfg["output"]["size"]
        self.fps = cfg["output"]["fps"]
        self.style = cfg["style"]
        self.audio = cfg["audio"]
        self.out_dir = resolve_path(cfg["output"]["dir"], self.root)
        self.deliver_to = os.path.expanduser(cfg["output"]["deliver_to"]) if cfg["output"].get("deliver_to") else None
        self.sources, self.enhance = {}, {}
        for k, v in cfg["sources"].items():
            if isinstance(v, dict):                     # {path, enhance: 2, model, sigma}: super-resolve a low-res source
                self.sources[k] = resolve_path(v["path"], self.root)
                if v.get("enhance"):
                    self.enhance[k] = {"scale": int(v["enhance"]), "model": v.get("model", "realesr-animevideov3"),
                                       "sigma": float(v.get("sigma", 1.2)), "method": v.get("method", "sharp")}
            else:
                self.sources[k] = resolve_path(v, self.root)
        if self.audio.get("vo"):
            self.audio["vo"] = resolve_path(self.audio["vo"], self.root)
        self.shots = []
        t = 0.0
        for i, sh in enumerate(cfg.get("shots") or []):
            sh = dict(sh)
            sh.setdefault("id", f"shot{i + 1}")
            typ = sh.setdefault("type", "ui")
            for k in REQUIRED_SHOT.get(typ, []):
                if k not in sh:
                    raise ValueError(f"shot '{sh['id']}' ({typ}) needs '{k}'")
            if typ in ("ui", "image") and sh["source"] not in self.sources:
                raise ValueError(f"shot '{sh['id']}' uses source '{sh['source']}' which is not in sources")
            sh["start"], sh["end"] = t, t + float(sh["duration"])
            sh["index"] = i
            t = sh["end"]
            self.shots.append(sh)
        if not self.shots:
            raise ValueError("cut has no shots")
        self.duration = t
        self.palette = {k: hex_bgr(v) for k, v in self.style["palette"].items()}

    def _load(self, path, depth=0):
        with open(path) as f:
            raw = yaml.safe_load(f) or {}
        if raw.get("extends") and depth < 5:
            base_path = resolve_path(raw.pop("extends"), os.path.dirname(path))
            raw = deep_merge(self._load(base_path, depth + 1), raw)
        return raw

    def color(self, c, default="accent"):
        c = c or default
        if isinstance(c, str) and c.startswith("#"):
            return hex_bgr(c)
        if c not in self.palette:
            raise ValueError(f"unknown colour '{c}', use a palette name {sorted(self.palette)} or #hex")
        return self.palette[c]

    def asset(self, p):
        return resolve_path(p, self.root)

    def shot_at(self, t):
        for sh in self.shots:
            if sh["start"] <= t < sh["end"]:
                return sh
        return self.shots[-1]

    def neighbours(self, sh):
        i = sh["index"]
        prev = self.shots[i - 1] if i > 0 else None
        nxt = self.shots[i + 1] if i + 1 < len(self.shots) else None
        return prev, nxt

    def out(self, *parts):
        os.makedirs(self.out_dir, exist_ok=True)
        return os.path.join(self.out_dir, *parts)
