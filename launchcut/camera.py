"""Shot cameras. A camera state is (cx, cy, s, rx, ry): recording point (cx, cy) sits at screen centre, s screen px per
recording px, rx/ry tilt in degrees. zoom 1.0 means the recording just covers the frame; below 1 the window floats."""
import math
import numpy as np
import cv2
from .ease import ease, lerp, lerplog, lerp2, seg


def homog(cam, sw, sh, W, H, f=2200.0):
    cx, cy, s, rx, ry = cam
    src = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])
    X = (src[:, 0] - cx) * s
    Y = (src[:, 1] - cy) * s
    a, b = math.radians(rx), math.radians(ry)
    Y2 = Y * math.cos(a)
    Z2 = Y * math.sin(a)
    X3 = X * math.cos(b) + Z2 * math.sin(b)
    Z3 = -X * math.sin(b) + Z2 * math.cos(b)
    d = f / (f + Z3)
    dst = np.float32(np.stack([X3 * d + W / 2, Y2 * d + H / 2], 1))
    return cv2.getPerspectiveTransform(src, dst)


def to_screen(M, pts):
    return cv2.perspectiveTransform(np.float32([pts]), M)[0]


def parse_move(spec, default, first_or_last):
    """enter/exit spec: 'none', a type name, or a dict; style default fills the gaps"""
    if first_or_last and spec is None:
        return {"type": "none"}
    if spec is None:
        return dict(default)
    if isinstance(spec, str):
        spec = {"type": spec}
    return {**default, **spec} if spec.get("type", default["type"]) == default["type"] else dict(spec)


class ShotCamera:
    def __init__(self, shot, sw, sh, W, H, style, is_first, is_last):
        self.sw, self.sh, self.W, self.H = sw, sh, W, H
        self.dur = float(shot["duration"])
        self.cover = max(W / sw, H / sh)
        self.contain = min(W / sw, H / sh)
        self.kfs = []
        prev_c = (sw / 2, sh / 2)
        for kf in shot.get("camera") or [{"t": 0.0, "zoom": 1.0}]:
            k = {"t": float(kf.get("t", 0.0)), "ease": kf.get("ease", "inOutCubic"),
                 "rx": float(kf.get("tilt", [0, 0])[0]), "ry": float(kf.get("tilt", [0, 0])[1]), "anchor": kf.get("anchor")}
            if "frame" in kf:
                x0, y0, x1, y1 = kf["frame"]
                pad = float(kf.get("pad", 0.08))
                k["s"] = min(W / ((x1 - x0) * (1 + 2 * pad)), H / ((y1 - y0) * (1 + 2 * pad)))
                k["c"] = ((x0 + x1) / 2, (y0 + y1) / 2)
            else:
                z = kf.get("zoom", 1.0)
                k["s"] = float(kf["scale"]) if "scale" in kf else (self.contain if z == "contain" else float(z) * self.cover)
                k["c"] = tuple(kf["center"]) if "center" in kf else prev_c
            prev_c = k["c"]
            self.kfs.append(k)
        self.kfs.sort(key=lambda k: k["t"])
        self.enter = parse_move(shot.get("enter"), style["enter"], is_first)
        if self.enter.get("type") == "dissolve":
            self.enter = {"type": "none"}
        self.exit = parse_move(shot.get("exit"), style["exit"], is_last)
        self.kicks = shot.get("kicks") or []
        tilted = any(k["rx"] or k["ry"] for k in self.kfs)
        auto = all(k["s"] >= self.cover - 1e-6 for k in self.kfs) and not tilted
        c = shot.get("clamp", "auto")
        self.clamp = auto if c == "auto" else bool(c)
        if self.exit["type"] == "dive":
            x0, y0, x1, y1 = self.exit["box"]
            self.dive_p = ((x0 + x1) / 2, (y0 + y1) / 2)
            self.dive_w = x1 - x0
            self.dive_s = float(self.exit.get("scale", 0.45 * W / self.dive_w))
            self.dive_t0 = self.dur - float(self.exit.get("d", 0.32))

    def _pair(self, t):
        ks = self.kfs
        if t <= ks[0]["t"]:
            return ks[0], ks[0], 0.0
        for a, b in zip(ks, ks[1:]):
            if t <= b["t"]:
                return a, b, ease(b["ease"], seg(t, a["t"], b["t"]))
        return ks[-1], ks[-1], 0.0

    def base(self, t):
        a, b, u = self._pair(t)
        s = lerplog(a["s"], b["s"], u)
        if b["anchor"] and a is not b:
            # keep the anchor point travelling in a straight line on screen while the zoom changes
            P = b["anchor"]
            qa = (self.W / 2 + (P[0] - a["c"][0]) * a["s"], self.H / 2 + (P[1] - a["c"][1]) * a["s"])
            qb = (self.W / 2 + (P[0] - b["c"][0]) * b["s"], self.H / 2 + (P[1] - b["c"][1]) * b["s"])
            q = lerp2(qa, qb, u)
            c = (P[0] - (q[0] - self.W / 2) / s, P[1] - (q[1] - self.H / 2) / s)
        else:
            c = lerp2(a["c"], b["c"], u)
        return [c[0], c[1], s, lerp(a["rx"], b["rx"], u), lerp(a["ry"], b["ry"], u)]

    def _clamp(self, cx, cy, s):
        hw, hh = self.W / (2 * s), self.H / (2 * s)
        cx = self.sw / 2 if 2 * hw >= self.sw else min(max(cx, hw), self.sw - hw)
        cy = self.sh / 2 if 2 * hh >= self.sh else min(max(cy, hh), self.sh - hh)
        return cx, cy

    def _pre_dive(self, t):
        cx, cy, s, rx, ry = self.base(t)
        e = self.enter
        if e["type"] == "punch":
            s *= lerplog(float(e.get("from", 0.5)), 1.0, ease("outExpo", seg(t, 0, float(e.get("d", 0.3)))))
        x = self.exit
        if x["type"] == "whip":
            s *= lerplog(1.0, float(x.get("k", 2.0)), ease("inCubic", seg(t, self.dur - float(x.get("d", 0.18)), self.dur)))
        for k in self.kicks:
            if t > k["at"]:
                s *= 1 + float(k.get("amount", 0.06)) * math.exp(-(t - k["at"]) * float(k.get("decay", 14)))
        if self.clamp:
            cx, cy = self._clamp(cx, cy, s)
        return (cx, cy, s, rx, ry)

    def __call__(self, t):
        if self.exit["type"] != "dive" or t < self.dive_t0:
            return self._pre_dive(t)
        c0x, c0y, s0, _, _ = self._pre_dive(self.dive_t0)
        P = self.dive_p
        u = seg(t, self.dive_t0, self.dur)
        q0 = (self.W / 2 + (P[0] - c0x) * s0, self.H / 2 + (P[1] - c0y) * s0)
        q = lerp2(q0, (self.W / 2, self.H / 2), ease("outCubic", u))
        s = lerplog(s0, self.dive_s, ease("inOutCubic", u))
        return (P[0] - (q[0] - self.W / 2) / s, P[1] - (q[1] - self.H / 2) / s, s, 0.0, 0.0)

    def M(self, t):
        return homog(self(t), self.sw, self.sh, self.W, self.H)


class CanvasCamera(ShotCamera):
    """camera for text cards and end cards: the world is the output canvas itself"""

    def __init__(self, shot, W, H, style, is_first, is_last):
        shot = dict(shot)
        shot.setdefault("camera", [{"t": 0.0, "zoom": 1.0}, {"t": float(shot["duration"]), "zoom": 1.04, "ease": "inOutSine"}]
                        if shot.get("type") == "card" else [{"t": 0.0, "zoom": 1.0}])
        shot["clamp"] = False
        if shot.get("type") == "end":
            shot.setdefault("enter", "none")
        super().__init__(shot, W, H, W, H, style, is_first, is_last)
