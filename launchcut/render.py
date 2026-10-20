"""Frame compositor. Shot types: ui (recording or image with a camera), card (type on the background), end (lockup,
typed command, tagline). Motion blur supersamples the camera when it moves fast; everything else is drawn per sample."""
import json, math, os, re, subprocess, sys
import numpy as np
import cv2
from .camera import ShotCamera, CanvasCamera, homog, to_screen
from .draw import Line, background, blit, font, lockup, pill, rounded_mask, sdf_ring, stroke_text, text_rgba
from .ease import c01, ease, lerp, seg
from .media import grade_lut, open_source, source_size


class Renderer:
    def __init__(self, cut, draft=False):
        self.cut, self.draft = cut, draft
        self.W, self.H, self.fps = cut.W, cut.H, cut.fps
        self.k = min(self.W, self.H) / 1080.0              # style sizes are written for 1080p
        st = cut.style
        self.lut = grade_lut(st["grade"])
        self.sizes = {p: source_size(p) for p in set(cut.sources.values())}
        self.readers, self.cams, self.lines, self.frozen = {}, {}, {}, {}
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        v = float(st["vignette"])
        self.vignette = (1 - v * np.clip(((xx - self.W / 2) / (self.W / 2)) ** 2 + ((yy - self.H / 2) / (self.H / 2)) ** 2 - 0.25, 0, 1.5) / 1.5)[..., None]
        band_top = self.H - 380 * self.k
        self.band = (np.clip((yy[:, :1] - band_top) / (self.H - band_top), 0, 1) ** 1.4 * float(st["caption"]["band"]))[..., None]
        self.masks = {}
        for p, (w, h) in self.sizes.items():
            self.masks[p] = rounded_mask(w // 2, h // 2, st["window"]["radius"] / 2)
        self.glow_cache = {}
        self.subs = cut.cfg.get("subtitles")
        self.sub_words, self.sub_cache, self.sub_chunks = [], {}, {}
        if self.subs:
            with open(cut.asset(self.subs["transcript"])) as f:
                self.sub_words = json.load(f)["words"]

    # ---------------- helpers ----------------
    def color(self, c, default="accent"):
        return self.cut.color(c, default)

    def font(self, role, size):
        fonts = self.cut.style["fonts"]
        return font(fonts.get(role, role), size * self.k)

    def cam(self, sh):
        if sh["id"] not in self.cams:
            first, last = sh["index"] == 0, sh["index"] == len(self.cut.shots) - 1
            if sh["type"] in ("ui", "image"):
                w, h = self.sizes[self.cut.sources[sh["source"]]]
                self.cams[sh["id"]] = ShotCamera(sh, w, h, self.W, self.H, self.cut.style, first, last)
            else:
                self.cams[sh["id"]] = CanvasCamera(sh, self.W, self.H, self.cut.style, first, last)
        return self.cams[sh["id"]]

    def world(self, sh):
        if sh["type"] in ("ui", "image"):
            return self.sizes[self.cut.sources[sh["source"]]]
        return self.W, self.H

    def src_time(self, sh, t):
        spec = sh.get("src", {"start": 0.0, "speed": 1.0})
        if isinstance(spec, dict):
            return float(spec.get("start", 0.0)) + t * float(spec.get("speed", 1.0))
        pts = sorted(spec)
        if t <= pts[0][0]:
            return pts[0][1]
        for (t0, s0), (t1, s1) in zip(pts, pts[1:]):
            if t <= t1:
                return s0 + (s1 - s0) * (t - t0) / (t1 - t0)
        return pts[-1][1]

    def reader(self, sh):
        if sh["id"] not in self.readers:
            self.readers[sh["id"]] = open_source(self.cut.sources[sh["source"]], self.lut, self.fps)
        return self.readers[sh["id"]]

    def release_before(self, index):
        for sh in self.cut.shots:
            if sh["index"] < index - 1 and sh["id"] in self.readers:
                self.readers.pop(sh["id"]).close()

    def close(self):
        for r in self.readers.values():
            r.close()
        self.readers.clear()

    def caption(self, dst, sh, t):
        cap = sh.get("caption")
        if not cap:
            return
        cs = self.cut.style["caption"]
        if sh["id"] not in self.lines:
            colors = {k: self.color(k) for k in self.cut.palette}
            self.lines[sh["id"]] = Line(cap["text"], self.font(cap.get("font", cs["font"]), cap.get("size", cs["size"])), colors)
        t_in, t_out = float(cap.get("in", 0.3)), float(cap.get("out", sh["duration"] - 0.15))
        vis = c01((t - t_in + 0.1) / 0.2) * (1 - seg(t, t_out - 0.1, t_out))
        if vis <= 0:
            return
        dst *= (1 - self.band * vis)
        self.lines[sh["id"]].draw(dst, t, t_in, self.W / 2, self.H - cs["margin"] * self.k, t_out,
                                  stagger=cs["stagger"], rise=cs["rise"] * self.k)

    # ---------------- shot types ----------------
    def ui(self, sh, t, frames):
        camera = self.cam(sh)
        cam = camera(t)
        path = self.cut.sources[sh["source"]]
        sw, shh = self.sizes[path]
        ff, fh = frames
        M = homog(cam, sw, shh, self.W, self.H)
        Mh = M @ np.diag([2.0, 2.0, 1.0])
        if cam[2] < 0.8:
            img = cv2.warpPerspective(fh, Mh, (self.W, self.H), flags=cv2.INTER_LINEAR)
        else:
            img = cv2.warpPerspective(ff, M, (self.W, self.H), flags=cv2.INTER_LANCZOS4 if cam[2] > 1.05 and not self.draft else cv2.INTER_LINEAR)
        a = cv2.warpPerspective(self.masks[path], Mh, (self.W, self.H), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
        img = img.astype(np.float32)
        if a.min() < 0.999:
            st = self.cut.style
            centre = to_screen(M, [(sw / 2, shh / 2)])[0]
            bg = background(self.W, self.H, self.color("bg"), st["grid"]["size"] * self.k, st["grid"]["strength"],
                            cam[2] / camera.cover, centre)
            shadow = cv2.GaussianBlur(np.roll(a, int(26 * self.k), axis=0), (0, 0), 34 * self.k)
            bg *= (1 - float(st["window"]["shadow"]) * shadow)[..., None]
            img = bg * (1 - a[..., None]) + img * a[..., None]
        self.overlays(img, sh, t, M, cam)
        self.caption(img, sh, t)
        self.subtitles(img, sh, t)
        return img

    # ---------------- word-synced subtitles ----------------
    def chunks_for(self, sh):
        """words spoken inside this shot's source window, grouped into short chunks that never span a cut"""
        if sh["id"] in self.sub_chunks:
            return self.sub_chunks[sh["id"]]
        cfg = self.subs
        s0, s1 = self.src_time(sh, 0.0), self.src_time(sh, sh["duration"])
        ws = []
        for w in self.sub_words:
            if not (s0 <= (w["s"] + w["e"]) / 2 <= s1):
                continue
            if ws and re.match(r"^[-'’]", w["w"]):          # whisper splits "self -improving", "don 't": glue back
                ws[-1] = {**ws[-1], "w": ws[-1]["w"] + w["w"], "e": w["e"]}
            else:
                ws.append(dict(w))
        out, cur = [], []
        nmax, gap = int(cfg.get("words", 3)), float(cfg.get("gap", 0.35))
        for i, w in enumerate(ws):
            cur.append(w)
            nxt = ws[i + 1] if i + 1 < len(ws) else None
            if len(cur) >= nmax or re.search(r"[.!?,;:]$", w["w"]) or nxt is None or nxt["s"] - w["e"] > gap:
                out.append(cur)
                cur = []
        self.sub_chunks[sh["id"]] = out
        return out

    def subtitles(self, img, sh, t):
        if not self.subs or not sh.get("subtitles", True):
            return
        cfg, k = self.subs, self.k
        ts = self.src_time(sh, t)
        chunks = self.chunks_for(sh)
        cur = None
        for j, ch in enumerate(chunks):
            end = min(chunks[j + 1][0]["s"] if j + 1 < len(chunks) else 1e9, ch[-1]["e"] + float(cfg.get("hold", 0.5)))
            if ch[0]["s"] - 0.04 <= ts < end:
                cur = (j, ch)
        if cur is None:
            return
        j, ch = cur
        size = float(cfg.get("size", 80)) * k
        f = self.font(cfg.get("font", "display"), cfg.get("size", 80))
        emph = {re.sub(r"[^a-z0-9']", "", e.lower()) for e in cfg.get("emphasis", [])}
        mode = cfg.get("mode", "highlight")
        words = []
        for i, w in enumerate(ch):
            txt = w["w"]
            for wrong, right in (cfg.get("fix") or {}).items():
                txt = re.sub(rf"\b{re.escape(wrong)}\b", right, txt)
            if cfg.get("hide_punct", True):
                txt = re.sub(r"[.,;:]+$", "", txt)
            if cfg.get("upper"):
                txt = txt.upper()
            spoken = w["s"] <= ts + 0.02
            if mode == "reveal" and not spoken:
                continue
            active = spoken and (i + 1 == len(ch) or ch[i + 1]["s"] > ts + 0.02)
            role = "accent" if (active and mode == "highlight") or re.sub(r"[^a-z0-9']", "", w["w"].lower()) in emph else "text"
            key = (txt, role, int(size))
            if key not in self.sub_cache:
                self.sub_cache[key] = stroke_text(txt, f, self.color(role), max(2, size * 0.055)) + (f.getlength(txt),)
            words.append(self.sub_cache[key])
        if not words:
            return
        space = f.getlength(" ")
        maxw = self.W * float(cfg.get("max_width", 0.84))
        lines, line, lw = [], [], 0.0
        pad = int(max(2, size * 0.055)) + 6
        for wd in words:
            ww = wd[3]
            if line and lw + space + ww > maxw:
                lines.append((line, lw)); line, lw = [], 0.0
            lw = lw + (space if line else 0) + ww
            line.append(wd)
        lines.append((line, lw))
        y_c = float(cfg.get("y", self.H * 0.70 / k)) * k
        lh = size * 1.18
        u = ease("outExpo", seg(ts, ch[0]["s"] - 0.04, ch[0]["s"] + 0.16))
        rise = 14 * k * (1 - u)
        for li, (line, lw) in enumerate(lines):
            x = self.W / 2 - lw / 2
            base = y_c - (len(lines) - 1) * lh / 2 + li * lh + size * 0.35 + rise
            for rgb, a, bl, ww in line:
                blit(img, rgb, a, x - pad, base - bl, c01(u * 1.5))
                x += ww + space

    def overlays(self, img, sh, t, M, cam):
        rs = self.cut.style["ring"]
        for r in sh.get("rings") or []:
            t0 = float(r["at"])
            if t < t0 or t > float(r.get("until", 1e9)):
                continue
            p = to_screen(M, [(r["box"][0], r["box"][1]), (r["box"][2], r["box"][3])])
            u = ease("outExpo", seg(t, t0, t0 + 0.35))
            kk = lerp(1.35, 1.0, u)
            pad = float(r.get("pad", rs["pad"])) * self.k
            cx, cy = (p[0] + p[1]) / 2
            hw = (p[1][0] - p[0][0]) / 2 * kk + pad
            hh = (p[1][1] - p[0][1]) / 2 * kk + pad
            sdf_ring(img, cx, cy, hw, hh, float(r.get("radius", rs["radius"])) * self.k, self.color(r.get("color")),
                     c01((t - t0) / 0.1), th=rs["width"] * self.k, glow=rs["glow"])
        for pu in sh.get("pulses") or []:
            t0 = float(pu["at"])
            if t < t0:
                continue
            p = to_screen(M, [tuple(pu["point"])])[0]
            r = float(pu.get("r", 26)) * cam[2]
            col = self.color(pu.get("color"))
            u = ease("outExpo", seg(t, t0, t0 + 0.35))
            sdf_ring(img, p[0], p[1], r * lerp(1.6, 1, u), r * lerp(1.6, 1, u), 1e9, col, c01((t - t0) / 0.1), th=3.5 * self.k)
            for k0 in (t0, t0 + 0.4):
                v = seg(t, k0, k0 + 0.7)
                if 0 < v < 1:
                    rr = r * lerp(1, 3.6, ease("outCubic", v))
                    sdf_ring(img, p[0], p[1], rr, rr, 1e9, col, (1 - v) * 0.8, th=2.5 * self.k, glow=0.2)

    def card(self, sh, t):
        st = self.cut.style
        canvas = background(self.W, self.H, self.color("bg"), st["grid"]["size"] * self.k, st["grid"]["strength"])
        key = sh["id"]
        if key not in self.lines:
            colors = {k: self.color(k) for k in self.cut.palette}
            size = sh.get("size", 104)
            self.lines[key] = [Line(txt, self.font(sh.get("font", "display"), size), colors) for txt in sh["lines"]]
            sub = sh.get("sub")
            self.lines[key + ":sub"] = Line(sub, self.font("body", sh.get("sub_size", 44)), {**colors, "text": self.color("muted")}) if sub else None
        lines = self.lines[key]
        size = sh.get("size", 104) * self.k
        lh = size * 1.18
        y0 = self.H / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
        t_in = float(sh.get("in", -0.12 if sh["index"] == 0 else 0.0))   # opening card: first word already on frame 0 (thumbnail)
        n_words = 0
        for i, ln in enumerate(lines):
            ln.draw(canvas, t, t_in + n_words * 0.06, self.W / 2, y0 + i * lh, sh.get("out"), stagger=0.06, rise=40 * self.k)
            n_words += len(ln.items)
        sub = self.lines.get(key + ":sub")
        if sub:
            sub.draw(canvas, t, float(sh.get("sub_in", t_in + n_words * 0.06 + 0.2)), self.W / 2, y0 + (len(lines) - 1) * lh + size * 1.1,
                     sh.get("out"), stagger=0.04, rise=20 * self.k)
        cam = self.cam(sh)(t)
        if abs(cam[2] - 1) < 1e-6 and cam[0] == self.W / 2 and cam[1] == self.H / 2:
            return canvas
        return cv2.warpPerspective(canvas, homog(cam, self.W, self.H, self.W, self.H), (self.W, self.H),
                                   flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    def end(self, sh, t):
        st = self.cut.style
        k = self.k
        img = background(self.W, self.H, self.color("bg"), st["grid"]["size"] * k, st["grid"]["strength"])
        lk = sh.get("lockup") or {}
        key = sh["id"] + ":lockup"
        if key not in self.lines:
            self.lines[key] = lockup(lk, lambda c: self.color(c, "text") if not (isinstance(c, str) and c.startswith("#")) else self.cut.color(c),
                                     self.cut.asset, k) if lk else None
        lock = self.lines[key]
        y_final = float(lk.get("y", self.H / k * 0.4)) * k
        prev, _ = self.cut.neighbours(sh)
        from_dive = prev is not None and prev["type"] in ("ui", "image") and self.cam(prev).exit["type"] == "dive"
        glow = float(sh.get("glow", 0.10)) * seg(t, 0.1, 0.7)
        if glow > 0:
            if "g" not in self.glow_cache:
                yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
                rr = ((xx - self.W / 2) / (700 * k)) ** 2 + ((yy - y_final) / (330 * k)) ** 2
                self.glow_cache["g"] = np.exp(-rr * 2.5)[..., None]
            img += self.glow_cache["g"] * self.color("accent") * glow
        if lock is not None:
            rgb, al = lock
            h, w = al.shape
            if from_dive:
                pc = self.cam(prev)
                start = pc.dive_w * pc.dive_s / w
            else:
                start = 0.92
            u = ease("outExpo", seg(t, 0.12, 0.62))
            sc = lerp(start, 1.0, u)
            cy = lerp(self.H / 2, y_final, u)
            a_in = ease("outCubic", seg(t, 0.0, 0.1)) if from_dive else ease("outCubic", seg(t, 0.0, 0.35))
            rs = cv2.resize(rgb, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)
            ra = cv2.resize(al, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)
            blit(img, rs, ra, self.W / 2 - w * sc / 2, cy - h * sc / 2, a_in)
        cmd = sh.get("command")
        if cmd:
            if isinstance(cmd, str):
                cmd = {"text": cmd}
            f = self.font("mono", 58)
            prefix, typed, at = cmd.get("prefix", "$ "), cmd["text"], float(cmd.get("at", 0.45))
            pu, pa = ease("outExpo", seg(t, at, at + 0.38)), c01((t - at) / 0.15)
            if pa > 0:
                tw = f.getlength(prefix + typed)
                pw, ph = tw + 110 * k, 108 * k
                px, py = self.W / 2 - pw / 2, y_final + 244 * k - ph / 2 + 26 * k * (1 - pu)
                pill(img, px, py, pw, ph, self.color("bg") * 1.55 + 2, self.color("bg") * 3.2 + 4, pa)
                cps = float(cmd.get("cps", 33))
                n = int(min(len(typed), max(0, (t - at - 0.13) * cps)))
                tx = px + 55 * k
                pr, pa_, pb = text_rgba(prefix, f, self.color("muted") * 0.6)
                blit(img, pr, pa_, tx - 4, py + ph / 2 + 20 * k - pb, pa)
                if n:
                    tr, ta, tb = text_rgba(typed[:n], f, self.color("text"))
                    blit(img, tr, ta, tx + f.getlength(prefix) - 4, py + ph / 2 + 20 * k - tb, pa)
                typing = t < at + 0.13 + len(typed) / cps + 0.05
                if t >= at + 0.13 and (typing or int((t - at) * 2.5) % 2 == 0):
                    cx = tx + f.getlength(prefix + typed[:n]) + 4
                    cv2.rectangle(img, (int(cx), int(py + ph / 2 - 29 * k)), (int(cx + 26 * k), int(py + ph / 2 + 29 * k)),
                                  tuple(float(c) for c in self.color("accent")), -1)
        tag = sh.get("tagline")
        if tag:
            if isinstance(tag, str):
                tag = {"text": tag}
            key = sh["id"] + ":tag"
            if key not in self.lines:
                colors = {kk: self.color(kk) for kk in self.cut.palette}
                self.lines[key] = Line(tag["text"], self.font("body", tag.get("size", 46)), {**colors, "text": self.color("muted")})
            self.lines[key].draw(img, t, float(tag.get("at", 0.92)), self.W / 2, y_final + 400 * k, stagger=0.04, rise=20 * k)
        if from_dive and t < 0.18:
            img = self.handoff(prev) * (1 - ease("outCubic", seg(t, 0, 0.18))) + img * ease("outCubic", seg(t, 0, 0.18))
        return img

    def handoff(self, prev):
        """the previous shot's last frame, frozen, so the dive dissolves into the end card"""
        if prev["id"] not in self.frozen:
            te = prev["duration"] - 1e-4
            self.frozen[prev["id"]] = self.ui(prev, te, self.reader(prev).get(self.src_time(prev, te)))
        return self.frozen[prev["id"]]

    # ---------------- frames ----------------
    def draw(self, sh, t, frames=None):
        if sh["type"] in ("ui", "image"):
            return self.ui(sh, t, frames)
        if sh["type"] == "card":
            return self.card(sh, t)
        return self.end(sh, t)

    def motion(self, sh, ta, tb, t):
        cam = self.cam(sh)
        sw, shh = self.world(sh)
        Mi = np.linalg.inv(homog(cam(t), sw, shh, self.W, self.H))
        pts = np.float32([[[self.W / 2, self.H / 2], [self.W * 0.1, self.H * 0.14], [self.W * 0.9, self.H * 0.86],
                           [self.W * 0.1, self.H * 0.86], [self.W * 0.9, self.H * 0.14]]])
        wp = cv2.perspectiveTransform(pts, Mi)
        a = cv2.perspectiveTransform(wp, homog(cam(ta), sw, shh, self.W, self.H))
        b = cv2.perspectiveTransform(wp, homog(cam(tb), sw, shh, self.W, self.H))
        return float(np.abs(a - b).max())

    def frame(self, i):
        tg = i / self.fps
        sh = self.cut.shot_at(tg)
        t = tg - sh["start"]
        frames = self.reader(sh).get(self.src_time(sh, t)) if sh["type"] in ("ui", "image") else None
        mb = self.cut.style["motion_blur"]
        n = 1
        if mb["enabled"] and not self.draft and sh["type"] != "end":
            dt = 0.5 * float(mb["shutter"]) / self.fps
            ta, tb = max(0.0, t - dt), min(sh["duration"] - 1e-4, t + dt)
            n = int(min(mb["max_samples"], max(1, math.ceil(self.motion(sh, ta, tb, t) / mb["px_per_sample"]))))
        if n == 1:
            img = self.draw(sh, t, frames)
        else:
            dt = 0.5 * float(mb["shutter"]) / self.fps
            acc, m = np.zeros((self.H, self.W, 3), np.float32), 0
            for j in range(n):
                ts = t - dt + 2 * dt * (j + 0.5) / n
                if 0 <= ts < sh["duration"]:
                    acc += self.draw(sh, ts, frames)
                    m += 1
            img = acc / max(m, 1)
        return self.finish(img, i), n, sh

    def finish(self, img, i):
        img = img * self.vignette
        g = float(self.cut.style["grain"])
        if g > 0:
            img += np.random.default_rng(i).standard_normal((self.H, self.W, 1), np.float32) * g
        return np.clip(img, 0, 255).astype(np.uint8)

    def render(self, out_path, t_from=0.0, t_to=None):
        t_to = self.cut.duration if t_to is None else t_to
        crf = 23 if self.draft else int(self.cut.cfg["output"]["crf_master"])
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{self.W}x{self.H}",
                                "-r", str(self.fps), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast" if self.draft else "slow",
                                "-crf", str(crf), "-pix_fmt", "yuv420p", "-profile:v", "high", "-color_primaries", "bt709",
                                "-color_trc", "bt709", "-colorspace", "bt709", out_path], stdin=subprocess.PIPE)
        i0, i1 = int(round(t_from * self.fps)), int(round(t_to * self.fps))
        last = None
        try:
            for i in range(i0, i1):
                img, n, sh = self.frame(i)
                if sh["index"] != last:
                    self.release_before(sh["index"])
                    last = sh["index"]
                if img.mean() < 3 and not self.cut.cfg.get("allow_dark_frames"):
                    raise RuntimeError(f"frame {i} ({i / self.fps:.2f}s, shot {sh['id']}) is black; set allow_dark_frames if intended")
                enc.stdin.write(img.tobytes())
                if i % self.fps == 0:
                    print(f"  {i / self.fps:6.2f}s  {sh['id']:<14} blur x{n}", flush=True)
        except BaseException:
            enc.kill()
            raise
        finally:
            self.close()
        enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError("ffmpeg encode failed")
        return out_path

    def stills(self, times, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        paths = []
        for tg in times:
            i = int(round(tg * self.fps))
            img, n, sh = self.frame(i)
            p = os.path.join(out_dir, f"{self.cut.name}_{tg:06.2f}.png")
            cv2.imwrite(p, img)
            paths.append(p)
            print(f"  still {tg:6.2f}s  {sh['id']:<14} blur x{n}")
        self.close()
        sheet = contact_sheet(paths, os.path.join(out_dir, f"{self.cut.name}_sheet.png"))
        return paths, sheet


def contact_sheet(paths, out, cols=3, width=640, labels=None):
    tiles = []
    for j, p in enumerate(paths):
        im = cv2.imread(p)
        im = cv2.resize(im, (width, int(im.shape[0] * width / im.shape[1])), interpolation=cv2.INTER_AREA)
        lab = labels[j] if labels else os.path.basename(p).rsplit("_", 1)[-1].replace(".png", "s")
        cv2.putText(im, lab, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(im, lab, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (90, 230, 255), 2, cv2.LINE_AA)
        tiles.append(im)
    h = max(t.shape[0] for t in tiles)
    tiles = [cv2.copyMakeBorder(t, 0, h - t.shape[0] + 6, 0, 6, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t in tiles]
    while len(tiles) % cols:
        tiles.append(np.full_like(tiles[0], 255))
    rows = [np.hstack(tiles[r:r + cols]) for r in range(0, len(tiles), cols)]
    cv2.imwrite(out, np.vstack(rows))
    return out
