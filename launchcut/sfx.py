"""Synthesized SFX bed. Deterministic (seeded), nothing sampled or downloaded. Cues come from the cut itself: every sound
is tied to something on screen (a cut, a landing, a ring, a click, a dive, typing). Narration, when given, is never
altered: SFX duck under it and a VO-only mix is written alongside."""
import os, subprocess, wave
import numpy as np

SR = 48000


class Bed:
    def __init__(self, dur, seed=7):
        self.n = int(SR * (dur + 0.5))
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)
        self.rng = np.random.default_rng(seed)
        self.sheet = []

    # ---------- primitives ----------
    def env(self, n, a, d, shape=4.0):
        t = np.arange(n) / SR
        return np.minimum(1.0, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * shape / max(d, 1e-4))

    def lp(self, x, fc):
        fc = np.broadcast_to(np.asarray(fc, float), x.shape)
        a = np.exp(-2 * np.pi * fc / SR)
        y = np.empty_like(x)
        s = 0.0
        for i in range(len(x)):
            s = (1 - a[i]) * x[i] + a[i] * s
            y[i] = s
        return y

    def hp(self, x, fc):
        return x - self.lp(x, fc)

    def whoosh(self, d, f0=300, f1=3000, rev=False):
        n = int(d * SR); x = self.rng.standard_normal(n)
        k = np.linspace(0, 1, n)
        fc = f0 * (f1 / f0) ** (k if not rev else 1 - k)
        e = np.sin(np.pi * k) ** 1.6 if not rev else k ** 2.2 * (1 - k) ** 0.3
        return self.hp(self.lp(x, fc), 80) * e

    def impact(self, d=1.4, f0=70, f1=38):
        n = int(d * SR); t = np.arange(n) / SR
        ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * 9)) / SR
        body = np.sin(ph) * np.exp(-t * 3.2)
        click = self.rng.standard_normal(n) * np.exp(-t * 90) * 0.5
        air = self.lp(self.rng.standard_normal(n), 900) * np.exp(-t * 6) * 0.6
        return body + self.lp(click, 4000) + air

    def pop(self, f=700, d=0.09):
        n = int(d * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-t * 60))) / SR) * self.env(n, 0.002, d, 5)

    def click(self, f=2600):
        n = int(0.03 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * f * t) * 0.6 + self.lp(self.rng.standard_normal(n), 6000) * 0.5) * np.exp(-t * 220)

    def tick(self, f=5200, d=0.012):
        n = int(d * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * f * t) * np.exp(-t * 400)

    def err(self):
        n = int(0.22 * SR); t = np.arange(n) / SR
        s = np.sign(np.sin(2 * np.pi * 196 * t)) * 0.35 + np.sin(2 * np.pi * 98 * t) * 0.6
        return self.lp(s, 1400) * np.exp(-t * 16)

    def chime(self, fs=(880, 1320, 1760), d=1.1):
        n = int(d * SR); t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * t) * (0.6 ** i) for i, f in enumerate(fs))
        return s * np.exp(-t * 4.0) * np.minimum(1, t / 0.004) * 0.5

    def key(self):
        n = int(0.05 * SR); t = np.arange(n) / SR
        return self.lp(self.rng.standard_normal(n), 3500) * np.exp(-t * 120) + np.sin(2 * np.pi * 420 * t) * np.exp(-t * 90) * 0.4

    def sparkle(self, d, density=180):
        n = int(d * SR); out = np.zeros(n)
        for _ in range(int(density * d)):
            i = self.rng.integers(0, max(1, n - 2400)); f = self.rng.uniform(3000, 9000); m = int(self.rng.integers(600, 2400))
            tt = np.arange(m) / SR
            out[i:i + m] += (np.sin(2 * np.pi * f * tt) * np.exp(-tt * self.rng.uniform(80, 200)) * self.rng.uniform(0.2, 1))[:len(out[i:i + m])]
        return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 0.5

    def drone(self, d, f0=55, f1=82):
        n = int(d * SR); t = np.arange(n) / SR; k = t / d
        f = f0 + (f1 - f0) * k
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 2.01) / SR) + 0.25 * np.sin(2 * np.pi * np.cumsum(f * 3.02) / SR)
        noise = self.lp(self.rng.standard_normal(n), 400 + 3000 * k) * 0.25
        return (s * 0.35 + noise) * np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.25)

    def kick(self, d=0.45):
        n = int(d * SR); t = np.arange(n) / SR
        ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 28)) / SR
        return np.sin(ph) * np.exp(-t * 7) + self.lp(self.rng.standard_normal(n), 3000) * np.exp(-t * 160) * 0.3

    def hat(self, d=0.06):
        n = int(d * SR); t = np.arange(n) / SR
        return self.hp(self.rng.standard_normal(n), 7000) * np.exp(-t * 70)

    def put(self, sig, t, gain=1.0, pan=0.0, why=""):
        i = int(t * SR)
        if i >= self.n or t < 0:
            return
        sig = sig[: self.n - i] * gain
        gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.L[i:i + len(sig)] += sig * gl * 1.41
        self.R[i:i + len(sig)] += sig * gr * 1.41
        if why:
            self.sheet.append((t, why))

    def sound(self, name, d=None):
        table = {"whoosh": lambda: self.whoosh(d or 0.35, 400, 6500), "whoosh_down": lambda: self.whoosh(d or 0.35, 3000, 300),
                 "suck": lambda: self.whoosh(d or 0.35, 5000, 300, rev=True), "impact": lambda: self.impact(d or 1.2),
                 "hit": lambda: self.impact(d or 0.6, 105, 58), "pop": lambda: self.pop(), "click": lambda: self.click(),
                 "tick": lambda: self.tick(), "err": lambda: self.err(), "chime": lambda: self.chime(), "key": lambda: self.key(),
                 "sparkle": lambda: self.sparkle(d or 0.6), "drone": lambda: self.drone(d or 2.0), "kick": lambda: self.kick(),
                 "hat": lambda: self.hat()}
        if name not in table:
            raise ValueError(f"unknown sound '{name}', pick one of {sorted(table)}")
        return table[name]()


def build(cut, renderer=None):
    """lay cues for every shot, then the beat bed and manual cues; returns the Bed"""
    A = cut.audio
    b = Bed(cut.duration, A.get("seed", 7))
    if A.get("open_hit"):
        b.put(b.impact(1.2, 80, 40), 0.0, 0.55, why="frame 0 lands")
        b.put(b.sparkle(0.6, 120), 0.02, 0.18)
    for sh in cut.shots:
        s0, s1 = sh["start"], sh["end"]
        cam = renderer.cam(sh) if renderer else None
        ex = cam.exit if cam else {"type": "none"}
        en = cam.enter if cam else {"type": "none"}
        if sh["index"] > 0 and en["type"] == "punch":
            b.put(b.impact(0.6, 105, 58), s0, 0.4, why=f"{sh['id']}: landing")
        if ex["type"] == "whip":
            b.put(b.whoosh(0.32, 400, 7000), s1 - 0.28, 0.55, why=f"{sh['id']}: whip out")
        if ex["type"] == "dive":
            t0 = s0 + cam.dive_t0
            b.put(b.whoosh(0.45, 200, 8000), t0 - 0.08, 0.75, why=f"{sh['id']}: dive")
        for kf_prev, kf in zip((cam.kfs if cam else [])[:-1], (cam.kfs if cam else [])[1:]):
            if kf["s"] < kf_prev["s"] * 0.6 and kf["t"] - kf_prev["t"] < 0.6:
                b.put(b.whoosh(0.35, 3000, 300), s0 + kf_prev["t"], 0.45, why=f"{sh['id']}: pull out")
        for r in sh.get("rings") or []:
            alert = r.get("color") == "alert"
            b.put(b.err() if alert else b.pop(700 + 80 * (len(b.sheet) % 4)), s0 + float(r["at"]), 0.45 if alert else 0.42,
                  -0.2, why=f"{sh['id']}: ring {'(alert)' if alert else ''}")
        for p in sh.get("pulses") or []:
            snd = b.err if p.get("color") == "alert" else (lambda: b.pop(520, 0.12))
            b.put(snd(), s0 + float(p["at"]), 0.55, 0.2, why=f"{sh['id']}: pulse")
            b.put(snd(), s0 + float(p["at"]) + 0.4, 0.35, 0.2)
            b.put(b.whoosh(0.5, 500, 3500), s0 + float(p["at"]), 0.3, 0.3)
        for c in sh.get("clicks") or []:
            b.put(b.click(), s0 + float(c), 0.5, -0.2, why=f"{sh['id']}: click")
        for c in sh.get("collapses") or []:
            b.put(b.whoosh(0.35, 5000, 300, rev=True), s0 + float(c) - 0.03, 0.45, why=f"{sh['id']}: collapse")
            b.put(b.impact(0.9, 90, 45), s0 + float(c), 0.5)
        for k in sh.get("kicks") or []:
            if float(k["at"]) not in [float(c) for c in sh.get("collapses") or []]:
                b.put(b.impact(0.6, 100, 50), s0 + float(k["at"]), 0.4, why=f"{sh['id']}: kick")
        for a0, a1 in sh.get("busy") or []:
            n = int((a1 - a0) * 32)
            for i in range(n):
                b.put(b.tick(b.rng.uniform(3200, 6500), 0.012), s0 + a0 + (a1 - a0) * (i / max(n, 1)) ** 0.9, 0.13, b.rng.uniform(-0.8, 0.8))
            b.sheet.append((s0 + a0, f"{sh['id']}: data ticks to {s0 + a1:.2f}s"))
        if sh["type"] == "card":
            words = sum(len(l.split()) for l in sh["lines"])
            for i in range(words):
                b.put(b.key(), s0 + float(sh.get("in", 0.0)) + i * 0.06 + 0.02, 0.35, -0.3 + 0.6 * i / max(words, 1))
            b.sheet.append((s0, f"{sh['id']}: words land"))
        if sh["type"] == "end":
            b.put(b.impact(2.0, 62, 32), s0, 1.0, why=f"{sh['id']}: lockup lands")
            b.put(b.sparkle(1.0, 220), s0 + 0.02, 0.35)
            b.put(b.chime((523, 784, 1046), 1.6), s0 + 0.05, 0.3)
            cmd = sh.get("command")
            if cmd:
                cmd = {"text": cmd} if isinstance(cmd, str) else cmd
                at, cps = float(cmd.get("at", 0.45)), float(cmd.get("cps", 33))
                for i in range(len(cmd["text"])):
                    b.put(b.key(), s0 + at + 0.13 + i / cps, 0.3, 0.1)
                b.sheet.append((s0 + at + 0.13, f"{sh['id']}: command typed"))
            tag = sh.get("tagline")
            if tag:
                at = float(tag.get("at", 0.92)) if isinstance(tag, dict) else 0.92
                b.put(b.chime((1046, 1568, 2093), 1.4), s0 + at, 0.22, why=f"{sh['id']}: tagline")
            b.put(b.lp(b.drone(max(0.6, sh["duration"] - 0.15), 82, 82), 900), s0 + 0.1, 0.3)
    beat = A.get("beat")
    if beat:
        step = 60.0 / float(beat.get("bpm", 120))
        t, t1 = float(beat.get("from", 0.0)), float(beat.get("to", cut.duration))
        b.sheet.append((t, f"beat bed {beat.get('bpm', 120)} bpm to {t1:.2f}s"))
        while t < t1 - 1e-6:
            if t > 0 or not A.get("open_hit"):
                b.put(b.kick(), t, 0.42)
            b.put(b.hat(), t + step / 2, 0.16, 0.25)
            t += step
    for c in A.get("cues") or []:
        b.put(b.sound(c["sound"], c.get("d")), float(c["t"]), float(c.get("gain", 0.5)), float(c.get("pan", 0)), why=c.get("why", c["sound"]))
    return b


def read_audio(path, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f64le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float64)
    n = int(SR * (dur + 0.5))
    return np.pad(x, (0, max(0, n - len(x))))[:n]


def write_wav(path, stereo):
    x16 = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x16.tobytes())


def mix(cut, renderer=None):
    """writes out/<name>-sfx.wav, out/<name>-mix.wav (+ -vo.wav when narration exists) and the cue sheet"""
    A = cut.audio
    b = build(cut, renderer) if A.get("sfx", True) else Bed(cut.duration, A.get("seed", 7))
    n = int(SR * cut.duration)
    sfx = np.stack([b.L, b.R], 1)[:n]
    fade = np.ones(n)
    fade[-int(0.25 * SR):] = np.linspace(1, 0, int(0.25 * SR)) ** 2
    sfx *= fade[:, None]
    peak = np.abs(sfx).max()
    if peak > 0:
        sfx = sfx / peak * 0.89 * float(A.get("gain", 1.0))
    outs = {"sfx": cut.out(f"{cut.name}-sfx.wav")}
    write_wav(outs["sfx"], sfx)
    if A.get("vo"):
        vo = read_audio(A["vo"], cut.duration)[:n]
        win = int(0.03 * SR)
        rms = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
        speak = np.clip(rms / 0.02, 0, 1)
        sm = b.lp(speak, 6.0)
        sm = np.maximum(sm, b.lp(speak[::-1], 6.0)[::-1])
        duck = 1 - (1 - 10 ** (-float(A.get("duck_db", 8)) / 20)) * np.clip(sm, 0, 1)
        m = np.stack([vo, vo], 1) + sfx * duck[:, None] * 0.6        # VO samples at unity, untouched
        if np.abs(m).max() > 0.98:
            m *= 0.98 / np.abs(m).max()
            print("[launchcut] mix scaled to avoid clipping (VO and SFX together)")
        outs["mix"] = cut.out(f"{cut.name}-mix.wav")
        write_wav(outs["mix"], m)
        outs["vo"] = cut.out(f"{cut.name}-vo.wav")
        write_wav(outs["vo"], np.stack([vo, vo], 1))
    else:
        outs["mix"] = outs["sfx"]
    sheet = cut.out(f"{cut.name}-cues.md")
    with open(sheet, "w") as f:
        f.write(f"# SFX cue sheet: {cut.name}\n\nEvery cue is tied to something on screen. Times are seconds in the cut.\n\n| time | cue |\n|---|---|\n")
        for t, why in sorted(b.sheet):
            f.write(f"| {t:6.2f} | {why} |\n")
    outs["cues"] = sheet
    return outs
