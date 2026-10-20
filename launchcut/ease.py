"""Easing and interpolation. Every curve maps 0..1 to 0..1."""
import math


def c01(x):
    return max(0.0, min(1.0, x))


def seg(t, a, b):
    """progress of t through [a, b], clamped"""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return c01((t - a) / (b - a))


def lerp(a, b, u):
    return a + (b - a) * u


def lerplog(a, b, u):
    """interpolate scales in log space so zooms feel even"""
    return a * (b / a) ** u


def lerp2(p, q, u):
    return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))


EASES = {
    "linear": lambda u: u,
    "inCubic": lambda u: u ** 3,
    "outCubic": lambda u: 1 - (1 - u) ** 3,
    "inOutCubic": lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2,
    "inExpo": lambda u: 0.0 if u <= 0 else 2 ** (10 * (u - 1)),
    "outExpo": lambda u: 1.0 if u >= 1 else 1 - 2 ** (-10 * u),
    "inOutExpo": lambda u: 0.0 if u <= 0 else 1.0 if u >= 1 else (2 ** (20 * u - 10) / 2 if u < .5 else (2 - 2 ** (-20 * u + 10)) / 2),
    "outBack": lambda u: 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2,
    "inOutSine": lambda u: -(math.cos(math.pi * u) - 1) / 2,
}


def ease(name, u):
    if name not in EASES:
        raise ValueError(f"unknown ease '{name}', pick one of {sorted(EASES)}")
    return EASES[name](c01(u))
