"""Type, rings, background, pill, SVG marks and logo lockups. Images are float32 BGR 0..255; alphas float32 0..1."""
import glob, math, os, re, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from .ease import c01, ease, seg

FONT_DIRS = [os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "/System/Library/Fonts", "/System/Library/Fonts/Supplemental",
             "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"),
             os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")]
_font_cache, _warned = {}, set()


def find_font_file(name):
    if os.path.isfile(os.path.expanduser(name)):
        return os.path.expanduser(name)
    for d in FONT_DIRS:
        for ext in (".otf", ".ttf", ".ttc"):
            hits = glob.glob(os.path.join(d, "**", name + ext), recursive=True)
            if hits:
                return hits[0]
    return None


def font(spec, size):
    """spec: a path, a file stem like 'Geist-SemiBold', or 'InterVariable@SemiBold' for a named variable-font instance"""
    key = (spec, int(size))
    if key in _font_cache:
        return _font_cache[key]
    name, _, var = spec.partition("@")
    path = find_font_file(name)
    if path is None:
        if spec not in _warned:
            print(f"[launchcut] font '{spec}' not found, using Pillow's default. Install it or point fonts.* at a file.", file=sys.stderr)
            _warned.add(spec)
        f = ImageFont.load_default(size=int(size))
    else:
        f = ImageFont.truetype(path, int(size))
        if var:
            try:
                f.set_variation_by_name(var)
            except Exception:
                print(f"[launchcut] '{name}' has no instance '{var}'", file=sys.stderr)
    _font_cache[key] = f
    return f


def text_rgba(txt, fnt, color):
    """rendered text as (rgb, alpha, baseline_y)"""
    asc, desc = fnt.getmetrics()
    w = int(math.ceil(fnt.getlength(txt))) + 8
    im = Image.new("L", (max(w, 1), asc + desc + 8), 0)
    ImageDraw.Draw(im).text((4, 4), txt, font=fnt, fill=255)
    a = np.asarray(im, np.float32) / 255.0
    rgb = np.empty(a.shape + (3,), np.float32)
    rgb[:] = color
    return rgb, a, asc + 4


def stroke_text(txt, fnt, color, stroke, stroke_color=(0, 0, 0)):
    """text with an outline (for subtitles over bright footage): rgb, alpha, baseline"""
    asc, desc = fnt.getmetrics()
    pad = int(stroke) + 6
    w = int(math.ceil(fnt.getlength(txt))) + 2 * pad
    h = asc + desc + 2 * pad
    sa_im = Image.new("L", (max(w, 1), h), 0)
    ImageDraw.Draw(sa_im).text((pad, pad), txt, font=fnt, fill=255, stroke_width=int(stroke), stroke_fill=255)
    fa_im = Image.new("L", (max(w, 1), h), 0)
    ImageDraw.Draw(fa_im).text((pad, pad), txt, font=fnt, fill=255)
    sa = np.asarray(sa_im, np.float32) / 255.0
    fa = np.asarray(fa_im, np.float32) / 255.0
    sh = cv2.GaussianBlur(np.roll(sa, max(1, int(stroke * 0.6)), axis=0), (0, 0), max(1.0, stroke * 1.2)) * 0.55   # soft drop shadow
    sa = np.maximum(sa, sh)
    a = np.maximum(sa, fa)
    col = np.float32(color)
    sc = np.float32(stroke_color)
    rgb = (col * fa[..., None] + sc * (sa * (1 - fa))[..., None]) / np.maximum(a, 1e-4)[..., None]
    return rgb.astype(np.float32), a, asc + pad


def blit(dst, rgb, a, x, y, alpha=1.0):
    H, W = dst.shape[:2]
    h, w = a.shape
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1 or alpha <= 0:
        return
    aa = a[y0 - y:y1 - y, x0 - x:x1 - x, None] * alpha
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - aa) + rgb[y0 - y:y1 - y, x0 - x:x1 - x] * aa


def parse_markup(text):
    """'*word*' takes the accent colour, '!word!' the alert colour; markers may span several words"""
    out, mode = [], None
    for w in text.split():
        start = w[0] if w[0] in "*!" and mode is None else None
        if start:
            mode = start
            w = w[1:]
        m = mode
        if mode and w.endswith(mode):
            w = w[:-1]
            mode = None
        out.append((w, {"*": "accent", "!": "alert"}.get(m)))
    return out


class Line:
    """one line of words that rise in with a stagger"""

    def __init__(self, text, fnt, colors, base="text"):
        space = fnt.getlength(" ")
        self.items, x = [], 0.0
        for w, role in parse_markup(text):
            rgb, a, bl = text_rgba(w, fnt, colors[role or base])
            self.items.append((x, rgb, a, bl))
            x += fnt.getlength(w) + space
        self.width = x - space

    def draw(self, dst, t, t_in, cx, base_y, t_out=None, stagger=0.05, rise=30.0, alpha=1.0):
        x0 = cx - self.width / 2
        fade = 1.0 if t_out is None else 1 - seg(t, t_out - 0.12, t_out)
        for i, (x, rgb, a, bl) in enumerate(self.items):
            ti = t_in + i * stagger
            u = ease("outExpo", seg(t, ti, ti + 0.4))
            al = c01((t - ti) / 0.12) * fade * alpha
            blit(dst, rgb, a, x0 + x - 4, base_y - bl + rise * (1 - u) - 14 * (1 - fade), al)


def sdf_ring(dst, cx, cy, hw, hh, r, color, alpha, th=3.0, glow=0.45):
    """anti-aliased rounded-rect (or circle when r >= hw, hh) outline with an outer glow"""
    if alpha <= 0.01:
        return
    H, W = dst.shape[:2]
    m = 40
    x0, x1 = int(max(cx - hw - m, 0)), int(min(cx + hw + m, W))
    y0, y1 = int(max(cy - hh - m, 0)), int(min(cy + hh + m, H))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    X, Y = xx - cx, yy - cy
    r = min(r, hw, hh)
    qx, qy = np.abs(X) - (hw - r), np.abs(Y) - (hh - r)
    d = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r
    a = np.clip(th / 2 + 0.5 - np.abs(d), 0, 1) + np.exp(-np.maximum(d, 0) / 12.0) * (d > 0) * glow
    a = (np.clip(a, 0, 1) * alpha)[..., None]
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + color * a


def background(W, H, color, grid=96.0, strength=9.0, scale=1.0, anchor=None):
    img = np.empty((H, W, 3), np.float32)
    img[:] = color
    if strength <= 0:
        return img
    g = max(grid * scale, 24.0)
    ax, ay = (W / 2, H / 2) if anchor is None else (float(anchor[0]), float(anchor[1]))
    lines = np.zeros((H, W), np.float32)
    for x in np.arange(ax % g, W, g):
        cv2.line(lines, (int(round(x)), 0), (int(round(x)), H), 1.0, 1, cv2.LINE_AA)
    for y in np.arange(ay % g, H, g):
        cv2.line(lines, (0, int(round(y))), (W, int(round(y))), 1.0, 1, cv2.LINE_AA)
    if float(np.mean(color)) > 128:            # light brand: grid lines are a touch darker than the paper
        img -= lines[..., None] * strength * 0.6
    else:
        img += lines[..., None] * strength
    return img


def rounded_mask(w, h, r):
    m = np.zeros((h, w), np.uint8)
    r = int(r)
    cv2.rectangle(m, (r, 0), (w - 1 - r, h - 1), 255, -1)
    cv2.rectangle(m, (0, r), (w - 1, h - 1 - r), 255, -1)
    for c in [(r, r), (w - 1 - r, r), (r, h - 1 - r), (w - 1 - r, h - 1 - r)]:
        cv2.circle(m, c, r, 255, -1, cv2.LINE_AA)
    return m


def pill(dst, x, y, w, h, fill, edge, alpha, radius=None):
    m = rounded_mask(int(w), int(h), int(radius if radius is not None else h / 2 - 1)).astype(np.float32) / 255
    e = np.clip(m - cv2.erode(m, np.ones((5, 5), np.uint8)), 0, 1)
    f = np.empty(m.shape + (3,), np.float32)
    f[:] = fill
    blit(dst, f, m, x, y, alpha * 0.95)
    f[:] = edge
    blit(dst, f, e, x, y, alpha)


# ---------------- SVG marks (paths only; enough for most logo files) ----------------
_NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def svg_paths(path):
    src = open(path).read()
    vb = re.search(r'viewBox="([^"]+)"', src)
    view = [float(v) for v in re.split(r"[ ,]+", vb.group(1).strip())] if vb else None
    ds = re.findall(r'<path\b[^>]*?\sd="([^"]+)"', src, re.S)   # \sd= so id="..." never matches
    if not ds:
        raise ValueError(f"{path}: no <path d=...> found")
    return ds, view


def flatten(d, steps=24):
    toks = re.findall(r"[MmLlHhVvCcSsQqTtZzAa]|" + _NUM, d)
    polys, cur, i = [], [], 0
    x = y = sx = sy = 0.0
    cmd, last_ctrl = None, None

    def num():
        nonlocal i
        v = float(toks[i]); i += 1
        return v

    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
        rel = cmd.islower()
        C = cmd.upper()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if C == "M":
            if cur: polys.append(cur)
            x, y = num() + ox, num() + oy
            sx, sy = x, y
            cur = [(x, y)]
            cmd = "l" if rel else "L"
            last_ctrl = None
        elif C == "L":
            x, y = num() + ox, num() + oy; cur.append((x, y)); last_ctrl = None
        elif C == "H":
            x = num() + ox; cur.append((x, y)); last_ctrl = None
        elif C == "V":
            y = num() + (y if rel else 0.0); cur.append((x, y)); last_ctrl = None
        elif C in "CS":
            if C == "C":
                p1 = (num() + ox, num() + oy)
            else:
                p1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_ctrl else (x, y)
            p2 = (num() + ox, num() + oy)
            p3 = (num() + ox, num() + oy)
            for k in range(1, steps + 1):
                u = k / steps
                cur.append(tuple((1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * a + 3 * (1 - u) * u * u * b + u ** 3 * c
                                 for p0, a, b, c in zip((x, y), p1, p2, p3)))
            x, y = p3
            last_ctrl = p2
        elif C in "QT":
            if C == "Q":
                p1 = (num() + ox, num() + oy)
            else:
                p1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_ctrl else (x, y)
            p2 = (num() + ox, num() + oy)
            for k in range(1, steps + 1):
                u = k / steps
                cur.append(tuple((1 - u) ** 2 * p0 + 2 * (1 - u) * u * a + u * u * b for p0, a, b in zip((x, y), p1, p2)))
            x, y = p2
            last_ctrl = p1
        elif C == "A":
            for _ in range(5): num()                      # arcs: approximated by a straight segment
            x, y = num() + ox, num() + oy
            cur.append((x, y))
            last_ctrl = None
        elif C == "Z":
            if cur: polys.append(cur)
            cur = []
            x, y = sx, sy
            last_ctrl = None
    if cur:
        polys.append(cur)
    return polys


def svg_mask(path, size, ss=4):
    """even-odd filled alpha of an SVG mark, fitted into a size x size box"""
    ds, view = svg_paths(path)
    polys = [p for d in ds for p in flatten(d)]
    pts = np.array([q for p in polys for q in p])
    if view:
        vx, vy, vw, vh = view
    else:
        vx, vy = pts.min(0)
        vw, vh = pts.max(0) - pts.min(0)
    S = size * ss
    k = S / max(vw, vh)
    ox, oy = (S - vw * k) / 2, (S - vh * k) / 2
    acc = np.zeros((S, S), bool)
    for p in polys:
        if len(p) < 3:
            continue
        im = Image.new("1", (S, S), 0)
        ImageDraw.Draw(im).polygon([(ox + (px - vx) * k, oy + (py - vy) * k) for px, py in p], fill=1)
        acc ^= np.asarray(im, bool)
    m = Image.fromarray((acc * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    return np.asarray(m, np.float32) / 255


def image_mask(path, size):
    im = Image.open(path).convert("RGBA")
    im.thumbnail((size, size), Image.LANCZOS)
    a = np.zeros((size, size), np.float32)
    rgb = np.zeros((size, size, 3), np.float32)
    w, h = im.size
    x0, y0 = (size - w) // 2, (size - h) // 2
    arr = np.asarray(im, np.float32)
    a[y0:y0 + h, x0:x0 + w] = arr[..., 3] / 255
    rgb[y0:y0 + h, x0:x0 + w] = arr[..., 2::-1]
    return rgb, a


def logo_image(path, width):
    """an official logo file (PNG with alpha, or a single-colour SVG) at the given width"""
    if path.lower().endswith(".svg"):
        ds, view = svg_paths(path)
        vw, vh = (view[2], view[3]) if view else (1, 1)
        h = int(round(width * vh / vw))
        a = svg_mask(path, int(width), ss=3)
        a = a[(a.shape[0] - h) // 2:(a.shape[0] - h) // 2 + h] if a.shape[0] > h else a
        fill = re.search(r'fill="(#[0-9a-fA-F]{6})"', open(path).read())
        col = np.empty(a.shape + (3,), np.float32)
        hx = (fill.group(1) if fill else "#000000").lstrip("#")
        col[:] = (int(hx[4:6], 16), int(hx[2:4], 16), int(hx[0:2], 16))
        return col, a
    im = Image.open(path).convert("RGBA")
    h = int(round(width * im.height / im.width))
    im = im.resize((int(width), h), Image.LANCZOS)
    arr = np.asarray(im, np.float32)
    return arr[..., 2::-1].copy(), arr[..., 3] / 255


def lockup(cfg, colors, resolve, scale_ref=1.0):
    """[tile with mark] + wordmark, rendered once at its final width; or the brand's own logo file via `image:`."""
    width = float(cfg.get("width", 800)) * scale_ref
    if cfg.get("image"):
        return logo_image(resolve(cfg["image"]), width)
    tile_h = width * 0.27                         # proportions of a typical app-header lockup
    font_spec = cfg.get("font", "InterVariable@SemiBold")
    word = cfg.get("wordmark", "")
    gap = tile_h * 0.33
    f = font(font_spec, 100)
    wl = f.getlength(word) if word else 0
    # solve the font size so tile + gap + word fills the requested width
    if word:
        fs = max(8, int((width - tile_h - gap) / wl * 100))
        f = font(font_spec, fs)
        wl = f.getlength(word)
    total_w = int(math.ceil(tile_h + (gap + wl if word else 0))) + 8
    H = int(math.ceil(tile_h)) + 8
    rgb = np.zeros((H, total_w, 3), np.float32)
    al = np.zeros((H, total_w), np.float32)
    t = int(round(tile_h))
    tile = cfg.get("tile")
    if tile:
        tm = rounded_mask(t, t, t * float(tile.get("radius", 0.22))).astype(np.float32) / 255
        col = np.empty((t, t, 3), np.float32)
        col[:] = colors(tile.get("color", "#2C343A"))
        blit(rgb, col, tm, 0, (H - t) / 2)
        al[(H - t) // 2:(H - t) // 2 + t, 0:t] = np.maximum(al[(H - t) // 2:(H - t) // 2 + t, 0:t], tm)
    mark = cfg.get("mark")
    if mark:
        mp = resolve(mark)
        ms = int(round(t * (0.65 if tile else 1.0)))
        if mp.lower().endswith(".svg"):
            ma = svg_mask(mp, ms)
            mrgb = np.empty((ms, ms, 3), np.float32)
            mrgb[:] = colors(cfg.get("mark_color", "accent"))
        else:
            mrgb, ma = image_mask(mp, ms)
        mx, my = (t - ms) / 2, (H - ms) / 2
        blit(rgb, mrgb, ma, mx, my)
        sl = al[int(my):int(my) + ms, int(mx):int(mx) + ms]
        sl[:] = np.maximum(sl, ma[:sl.shape[0], :sl.shape[1]])
    if word:
        wr, wa, bl = text_rgba(word, f, colors(cfg.get("word_color", "text")))
        bbox = f.getbbox(word)
        ink_mid = (bbox[1] + bbox[3]) / 2 + 4        # text_rgba pads 4 px
        wx, wy = t + gap - 4, H / 2 - ink_mid - (bbox[3] - bbox[1]) * 0.04
        blit(rgb, wr, wa, wx, wy)
        x0, y0 = int(round(wx)), int(round(wy))
        hh, ww = wa.shape
        y1, x1 = min(y0 + hh, H), min(x0 + ww, total_w)
        al[max(y0, 0):y1, x0:x1] = np.maximum(al[max(y0, 0):y1, x0:x1], wa[max(0, -y0):y1 - y0, :x1 - x0])
    rgb = np.where(al[..., None] > 1e-3, rgb / np.maximum(al[..., None], 1e-3), 0)   # straight alpha, no dark fringes
    return rgb.astype(np.float32), al
