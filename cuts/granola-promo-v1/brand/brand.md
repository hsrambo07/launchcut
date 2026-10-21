# Granola brand reference (for granola-promo-v1)

Researched 2026-10-21 from primary sources. Every value is tagged:

- **VERIFIED**: read directly from a Granola-owned source (URL given, fetched 2026-10-21).
- **ASSUMED**: our inference or a substitute we chose.

Key context: Granola rebranded on 2 Feb 2026 ("Meet the new look Granola", https://www.granola.ai/blog/a-new-look-for-granola, studio Ragged Edge, London). Anything older than that, including the "Say hello to Recipes" video (Sep 2025), shows the **old** brand (soft green gradients, old lowercase sans wordmark). Use old material for pacing only, never for look.

CSS sources (hashed file names, they will rot when Granola redeploys):

- `https://www.granola.ai/_next/static/css/6dbea53cf1487b5c.css` (main: colour tokens, fonts, keyframes)
- `https://www.granola.ai/_next/static/css/c0f4713c5af5fbcf.css` (@font-face)

---

## 1. Taglines and product lines (verbatim, on-site only)

Only these may be used as claims. All VERIFIED.

### Homepage, https://www.granola.ai/
| Line | Where |
|---|---|
| "The AI notepad for back-to-back meetings" | H1 hero (Quadrant, ~110px) |
| "Notes, actions and memory." / "Without a meeting bot." | hero subhead, two lines |
| "The AI notepad for back-to-back meetings. Notes, actions and memory. Without a meeting bot." | meta description |
| "Granola: The AI Notepad for back-to-back meetings" | `<title>` and og:title (the site uses an em dash as the separator; we render it as a colon) |
| "Download for free" | primary CTA |
| "Available for macOS, Windows, iOS, Android" | under CTA |
| "Effortless notes, enhanced instantly." | section H2 |
| "Uses your computer audio, so doesn’t invite a bot" | bullet |
| "Private by default, easy to share if you choose" | bullet |
| "Works with Zoom, Google Meet, Teams and every other meeting app." | bullet |
| "My notes" / "Enhanced" | toggle labels in the demo |
| "For the doers" | giant headline, logo wall |
| "Trusted by teams we admire" | logo wall |
| "Granola helps you before, during and after your meetings." | section H2 |
| "Before the meeting" / "Start your meeting prepared" | step 1 |
| "Granola syncs with your calendar and preps a Brief before every external meeting: who’s attending, what you discussed last time, and what matters now." | step 1 body |
| "In the meeting" / "Give your full attention" | step 2 |
| "Don’t choose between listening and taking good notes. Write down as much or as little as you like - Granola uses meeting context to write clear notes, personal to you." | step 2 body |
| "After the meeting" / "Post-meeting admin, done" | step 3 |
| "Notes, action items, and follow-ups are ready the moment the meeting ends, so you can move things forward." | step 3 body |
| "Granola Chat" / "Perfect meeting memory" | chat section |
| "What did I promise to do in my meetings this week?" | sample chat prompt |
| "Helping busy people through busy days" | testimonials |
| "Works everywhere you do, how you do" | features H2 |
| "Humans in the room, not bots" | feature |
| "Granola doesn’t join your meeting. Instead, it transcribes in the background while you stay present" | feature body |
| "Works with all meeting apps" / "Zoom, Meet, Teams, Huddles, in-person, on-the-go: capture conversations wherever you have them." | feature |
| "Private by default, ready to share" / "Your notes are just for you. Search them, polish them, analyze them, then send them as you like." | feature |
| "Made for in-person meetings too" | feature |
| "Syncs with your calendar" / "One click, and you’ll have every conversation captured and easy to find." | feature |
| "Use your meeting notes anywhere" / "No more copy-pasting meeting transcripts into AI tools." | MCP section |
| "Unlimited meeting notes for free" / "Take as many notes as you’d like. Upgrade to view and work with notes older than 30 days." | closing |
| "Made with ♥ in Shoreditch" | footer |

Homepage quick-action chips shown in the demo UI: "List actions", "Write follow-up email", "Draft project plan". Status labels: "Enhancing notes", "Transcribing", "Ask anything", "Write notes...".

Testimonials on the homepage (quotes from named people, usable only as attributed quotes): Karri Saarinen, CEO of Linear: "Granola was one of those things that just clicked instantly. It’s seamless and very purpose-built." Guillermo Rauch, CEO of Vercel: "It’s actually unbelievable how good Granola is." Nat Friedman: "Granola generates the best meeting notes of anything I’ve tried so far."

### Pricing, https://www.granola.ai/pricing
- "Granola how you wanna" (H1)
- "Get the Granola plan that's right for you and your team, so everyone can be on the same page."
- Tiers: Basic ("Great for a free taste of Granola"), Business ("Great for individuals or small teams"), and a top tier ("Great for larger companies"). Prices omitted on purpose: billing period not checked, and the promo should not show pricing.
- Closing CTA used site-wide (also on blog posts): "Ready for calmer, more productive meetings?" / "Try Granola for a few meetings today. It's free to get started."

### Other product pages
- https://www.granola.ai/chat : "AI chat that actually understands your work" / "Granola Chat combines instant work context with the world's best AI models. So you can be ready for anything."
- https://www.granola.ai/ai-note-taker : "More than just a standard notetaker"
- https://www.granola.ai/enterprise : "Turn meeting notes into company knowledge"
- https://www.granola.ai/customers : "Helping our customers stay present in meetings"
- Nav descriptors: "The AI notepad for people in back-to-back meetings", "AI chat that already knows what you're working on", "Meeting notes on the go and for your phone calls".

### Off-site lines (NOT usable as claims, not on granola.ai)
- "The AI notepad that helps you get the doing done." (LinkedIn and YouTube channel bio). The phrase "Space to get the doing done." also appears inside product UI in the press-kit reel.
- "Meetings in, progress out." and "Ravers and meeting-havers, unite." (LinkedIn posts, https://www.linkedin.com/company/meetgranola)
- "Let back to backs move you forward" (Instagram bio seen inside the press-kit reel)
- "progress over process" (brand blog post; a value statement, not a product claim)

---

## 2. Colour palette

All VERIFIED from `6dbea53cf1487b5c.css` (token names `--color-oats-*` and `--oats-*`; "Oats" is their design system) unless noted.

### Neutrals (warm, slightly olive greys)
| Role | Hex | Token | Notes |
|---|---|---|---|
| Page background | `#ffffff` | `--background: 0 0% 100%`, `theme-color`, webmanifest | body bg |
| Surface (the real "Granola paper") | `#f7f7f2` | `--oats-surface` / neutral-100 | sections, app window, reel bg (sampled `#f6f6f2` from reel frame) |
| Off-white | `#fcfcf8` | neutral-50, `--oats-ink-primary-inverse` | text on dark/green buttons |
| Sunken | `#f2f2ec` | neutral-150 | |
| Soft fill | `#eaebe5` | neutral-200 | Logo-Hero video bg sampled `#e8e9e1` |
| Logo "neutral" | `#ebebe4` | press-kit SVG fill | |
| Hairline | `#d5d5d2` | neutral-300 | dashed guides use `#DEDEDE` |
| Tertiary text | `#acada8` | neutral-400 | |
| Secondary text | `#72726e` | `--oats-ink-secondary` / neutral-600 | |
| Primary text | `#292929` | `--oats-ink-primary` / neutral-800 | H1, body ink |
| Logo black | `#1e1e1e` | neutral-950, press-kit SVG, nav SVG fill | |
| Dark bands | `#292929` | `bg-fill-primary` | the logo wall strip ("Trusted by teams we admire") and the testimonials section |

### Greens (the signature; "granola is green and always should be", a co-founder in the rebrand video https://www.youtube.com/watch?v=i38vvqAca8M; auto-captions, speaker not labelled, so attribution ASSUMED)
| Role | Hex | Token | Evidence |
|---|---|---|---|
| **Signature Granola green** | `#b2c248` | green-300 | logo-square.svg bg, Granola_lockup_green.svg, "Perfect meeting memory" section bg (`bg-oats-green-300`), app icon |
| Lime highlight | `#d1e043` | green-200 | "New" pill on homepage (`bg-[#D1E043]`), end of enhance sweep |
| Accent fill (CTA) | `#5b6f00` | `--oats-fill-accent` / green-500 | "Download for free" button |
| Accent ink | `#788c15` | `--oats-ink-accent` / green-400 | accent text on light |
| Deep olive | `#434625` | green-600 | dark green surfaces (identity imagery) |
| Pale green tint | `#f2f6e1` / `#e5eacd` | green-50 / green-100 | tinted surfaces |
| Recording bars | `#74bd00` | `--oats-system-dancing-bars` | the live-transcription pill bars |

### Secondary and alert
| Role | Hex | Token |
|---|---|---|
| Alert / danger | `#e95d3d` | `--oats-fill-danger` / red-300 (also the end-call button in app UI) |
| Danger ink | `#bd4a30` | red-400 |
| Pink | `#ff91e0` (300), `#ffbcef` (200) | collage/imagery colour |
| Lavender | `#cebef8` (200), `#a191ce` (300) | footer collage backgrounds |
| Yellow | `#febe29` (200) | imagery, sweep |
| Sky | `#d2e4f8` (blue-100) | sweep |

### The "enhance" chroma sweep (signature AI moment)
VERIFIED, `.gradient-text` in the main CSS: text is revealed by a sliding gradient `#292929 0 to 33.33%, #febe29 40%, #ff91e0 45%, #cebef8 50%, #d2e4f8 55%, #d1e043 60%, transparent 66.67%` (animation `gradient-text-slide`, 0.4s to 0.9s ease-in-out). Same chroma tail appears on the logo draw-on in the press-kit Logo-Hero video and on the wordmark reveal in the reel. Use this once per film for the "notes get enhanced" beat; it is their own motif.

---

## 3. Typography

| Use | Granola's font (VERIFIED) | How we know | Free? |
|---|---|---|---|
| Display / headings | **Quadrant Notepad** (custom cut of Quadrant, Matter of Sorts, designer Vincent Chan) | `--font-quadrant`, `--font-display` in CSS; woff2 name table reads "Quadrant Notepad Regular, 2026 Matter of Sorts". Rebrand post: "Quadrant, a slightly mechanical slab serif for display" | No, commercial |
| Body / UI | **KMR Melange Grotesk** (kimera, Michael Clasen) | `--font-sans`, `--font-melange`; woff2 name table "KMR Melange Grotesk, Copyright 2024 by kimera". Rebrand post: "Melange, a neutral but subtly characterful UI font" | No, commercial |
| Mono | **JetBrains Mono** | `--font-mono: "Jetbrains Mono", ui-monospace, SFMono-Regular, Menlo...` | Yes, OFL, Google Fonts |

Usage seen on site (VERIFIED from class names): headlines Quadrant 400 (never bold), tracking -0.02em to -0.015em, leading 0.93 to 1.05; body Melange at 400/430 ("book")/500; buttons `font-book` (430), pill-shaped (`rounded-full`).

**Licensing:** the woff2 files on granola.ai are Granola's licensed webfonts. Do not extract or use them in the cut. Use substitutes, or ask Granola for the fonts.

### Substitutes (ASSUMED, picked by rendering side-by-side specimens: `ref/font-substitutes-display.png`, `ref/font-substitutes-body.png`)
| Use | Pick | Why | Alt | Mac-only fallback |
|---|---|---|---|---|
| Display | **Besley** (Google Fonts, 400) | Same Clarendon slab character: curly-tailed 2, curved y tail, bracketed slab serifs | Roboto Serif at weight ~340, opsz 40 (closest width, softer) | Charter (preinstalled) |
| Body | **Hanken Grotesk** (Google Fonts, 400/500) | Neutral grotesk, similar proportions and spacing to Melange | Inter | SF Pro (system) |
| Mono | **JetBrains Mono** (Google Fonts) | Their actual mono | | Menlo |

Set display a touch tight (tracking -0.02em) to match their headlines. If Besley is not installed on the render Mac, fall back to Charter rather than Georgia.

---

## 4. Logo

**Official files downloaded** to `~/Documents/projects/launchcut/cuts/granola-promo-v1/brand/logos/`. Source: Granola's public press kit, linked from the site footer "Press" (https://grano.la/press redirects to Google Drive folder `1Shu_OoSSJEA0hO46kgm22_yCOAoh5N8O`, "Public Press Kit", folder Logos > For screen). VERIFIED.

| File | What it is |
|---|---|
| `Granola_lockup_black.svg` / `_green.svg` / `_neutral.svg` / `_white.svg` | Spiral + "granola" wordmark, viewBox 1850x500; fills `#1e1e1e`, `#b2c248`, `#ebebe4`, white |
| `Granola_lockup_black_lg.png` / `_green_lg.png` / `_neutral_lg.png` | Same, 5550x1500 PNG, transparent |
| `Granola_idea-spring_*.svg` | The spiral mark alone ("idea spring"), 485x500 |
| `Granola_the-notes_*.svg` | Lockup "granola the notes." (wordmark + Quadrant line), 3664x500 |
| `logo-square.svg` / `.png` | App-icon style: `#1e1e1e` spiral on `#b2c248` square, 1024x1024 |
| `wordmark-site-nav.svg` | Inline SVG copied verbatim from the homepage nav (viewBox 0 0 5017 1350, fill `#1E1E1E`) |
| `site-icon.png` | https://www.granola.ai/icon.png (550x550, the schema.org logo) |
| `apple-touch-icon.png` | https://www.granola.ai/favicon/apple-touch-icon.png (180x180) |
| `favicon-96x96.png` | https://www.granola.ai/favicon/favicon-96x96.png |
| `favicon.svg` | https://www.granola.ai/favicon/favicon.svg. Note: a PNG wrapped in SVG, not a vector |

og:image: https://www.granola.ai/og-image.png (1024x537), saved as `ref/og-image.png`.

Logo notes: the spiral is hand-drawn and "deliberately imperfect" (rebrand post). The wordmark is lowercase "granola"; in copy the name is always capitalised "Granola". Black on light, or black on Granola green, are the two hero treatments seen. Never trace, redraw, recolour outside the four supplied colourways, or animate letters apart without reason; their own reveals are a stroke draw-on of the spiral and a chroma-to-black fill on the wordmark.

---

## 5. Visual and motion style

### Overall
- **Light.** Warm off-white paper (`#f7f7f2`) with near-black ink. Dark `#292929` bands only for the logo wall strip and testimonials. App also has a dark mode in CSS, but marketing is light. VERIFIED.
- **Airy, editorial density.** Big Quadrant headlines, generous whitespace, dashed vertical guide lines (`#DEDEDE`, 8px dash), cards with 28px radius and soft shadows (`0 0 0 6px rgba(71,67,42,0.05)`). VERIFIED from homepage markup.
- Stated intent (rebrand post): "approachable and optimistic, a bit rough around the edges, but sharp enough to feel like a serious tool. Calm, but with energy underneath."

### Illustration and imagery (VERIFIED from `ref/identity-*.png`, `ref/footer-*.jpg`, `ref/og-image.png`, press reel)
Two registers side by side:
1. **Calm product register:** clean app windows on paper, Quadrant headings, traffic-light chrome, pill buttons.
2. **Expressive collage register:** risograph and halftone textures, saturated flat fields (Granola green, pink `#ff91e0`, lavender, yellow), cut-out photo objects (egg, moon, seashell, rocket, mountains), giant vertical Quadrant type running off the edge, hand-drawn loops and thin line scribbles, calendar-grid numerals. A co-founder in the rebrand video (speaker ASSUMED, auto-captions): "the illustrations are kind of rough".
Product is often shown **as a framed window floating over a collage panel** (split screen: collage left, product right), or a phone on a wood desk with stationery (Field Notes style). Real UI, not mockups.

### How they show product UI
- macOS window with red/yellow/green dots, rounded corners, white or `#f7f7f2` canvas, cropped to the note area. Headings inside the app are Quadrant (e.g. "Team Stand-up", "Coffee chat with Sinead").
- Tight crops of a single component (the recording pill with green bars, the "Notes / Enhanced" toggle, a call card) centred on flat green or paper.
- Homepage demo: the note "enhances" with the chroma sweep; transcript and enhanced notes cross-fade; chat chips appear.

### Motion and pace
- **Press-kit Logo-Hero** (`ref/presskit-Logo-Hero-Asset_02.mp4`, 2560x1440, 60fps, 5.6s, no audio): one continuous shot on `#e8e9e1`; the spiral draws on as a stroke with a pink/lime/orange chroma tail, settles to black, then the wordmark appears beside it. No cuts. VERIFIED.
- **Press-kit Granola reel** (`ref/presskit-Granola-reel.mp4`, 1920x1080, 30fps, 22.5s, no audio): brand sizzle with about 8 beats of 2.5 to 3s; two short stutter bursts (wordmark letters cycling colours, about 5 frames per flash) are animated builds inside a shot, not hard cuts. Sequence: spiral draw-on, app icon in context (dock, menu bar, Instagram), wordmark chroma reveal, phone on desk, iPad modal, collage egg, recording pill over a lake, Quadrant headline typing in ("Hit the pitch out the..."), phone notes, "Notes / Enhanced" toggle, "The Tingle of starting" (Quadrant + handwritten script), event photo, call card on green, type specimen "AaBb 012345". VERIFIED.
- **CSS motion** (VERIFIED): most-used easing `--ease-out-expo: cubic-bezier(.16,1,.3,1)`; also `--ease-in-out-expo: cubic-bezier(.87,0,.13,1)`. Small, quiet UI moves: `slideUpAndFade` 2px, dialog scale 0.96 to 1, `fade-in-up` 20px. Logo stroke keyframes (`logoStroke`, stroke-dashoffset draw). Chroma keyframes `chromaColor` cycle white, `#febe29`, `#ff91e0`, `#cebef8`, `#d1e043`.
- **Launch video, pre-rebrand, pacing reference only:** "Say hello to Recipes" (https://www.youtube.com/watch?v=ekSyfD7uoiU, 30 Sep 2025, 43s, about 1.9M views). 7 shots, about 6s each: presenter to camera in a homely office, alternating with UI cards on a soft background, burned-in captions, ends on wordmark with a typing cursor. Script is plain and first-person ("Today, we're announcing recipes." ... "Try a recipe today in the Granola app.").
- Takeaway for us (ASSUMED): calm holds of 2.5 to 3s, ease-out-expo moves, one chroma flourish for the AI beat, end on spiral draw-on and lockup. Avoid whip-pans, glitch, neon, dark tech gradients.

### Sources not reachable
- X/Twitter @meetgranola: attempted, rate-limited (HTTP 429). Not used.
- LinkedIn company page: reachable (public), used for voice only.
- YouTube @meetgranola: titles and descriptions read; auto-captions pulled for two videos.

---

## 6. Tone of voice

Five adjectives, each with on-site quotes (VERIFIED):

1. **Calm** : "Ready for calmer, more productive meetings?" (all pages); "Give your full attention"; brand post: "Granola becomes a calming presence."
2. **Human / present** : "Humans in the room, not bots"; "it transcribes in the background while you stay present"; "Helping our customers stay present in meetings".
3. **Plain-spoken, short** : "Post-meeting admin, done"; "Notes, actions and memory. Without a meeting bot."; "Start your meeting prepared".
4. **Warm, a little playful** : "Granola how you wanna"; "For the doers"; "Made with ♥ in Shoreditch"; "Helping busy people through busy days".
5. **Quietly confident (shows, does not shout)** : "Effortless notes, enhanced instantly."; "Perfect meeting memory"; the rebrand post: "It doesn’t look like something a committee would produce, which is the point."

### Words they use
notepad (not notetaker), notes, enhanced, meetings, back-to-back, present, doers, context, Brief, follow-ups, action items, "without a meeting bot", private by default, "move things forward", calm/calmer, progress. British spellings appear ("deprioritised", "analyse" on LinkedIn), with some US spellings on-site ("analyze"). Sentence case headlines, full stops on short lines.

### Words and moves they avoid (ASSUMED from absence and contrast)
- Calling Granola a "notetaker" or "meeting assistant bot"; they position against that ("More than just a standard notetaker", "AI notepad vs notetaker"). The word "notetaker" appears on-site only on comparison/SEO pages and in a customer quote, never as their own name for the product.
- "AI-powered", "revolutionary", "supercharge", "10x", hype superlatives. "Seamless" only appears inside a customer quote.
- Exclamation marks in product copy (rare; only in blog titles like "Granola for Android is here!").
- Shouty caps in UI copy (caps appear only in expressive collage art, e.g. "SPEAK IT INTO EXISTENCE").
- Generic AI gradients: the co-founders say the old brand had "gradients that looked like every AI company" and they moved away from it.

---

## 7. Ready-to-paste style block

```yaml
style:
  palette:
    bg: "#f7f7f2"      # VERIFIED --oats-surface (page body is #ffffff; surface is the brand paper)
    text: "#292929"    # VERIFIED --oats-ink-primary
    accent: "#b2c248"  # VERIFIED oats-green-300, signature Granola green (logo, app icon)
    alert: "#e95d3d"   # VERIFIED --oats-fill-danger
    muted: "#72726e"   # VERIFIED --oats-ink-secondary
  fonts:
    display: "Besley"          # ASSUMED substitute for Quadrant Notepad (commercial). Mac fallback: Charter
    body: "Hanken Grotesk"     # ASSUMED substitute for KMR Melange Grotesk (commercial). Mac fallback: SF Pro
    mono: "JetBrains Mono"     # VERIFIED their actual mono, free (OFL, Google Fonts). Mac fallback: Menlo
```

Extra tokens worth keeping next to the block (all VERIFIED): CTA fill `#5b6f00`, accent ink `#788c15`, lime `#d1e043`, logo black `#1e1e1e`, recording bars `#74bd00`, chroma sweep `#febe29 #ff91e0 #cebef8 #d2e4f8 #d1e043`, easing `cubic-bezier(.16,1,.3,1)`.

---

## 8. Files in this folder

- `logos/`: official logo files (see section 4).
- `ref/`: reference only, not for the cut unless cleared: `og-image.png`, `identity-08.png`, `identity-12.png`, `identity-15124.png`, `identity-154.png`, `identity-instagram-43.png` (rebrand blog images), `seriesc-hero.png`, `footer-1.jpg`, `footer-3.jpg`, `feature-humans.jpg`, `watchog.jpg` (site imagery), `presskit-Granola-reel.mp4`, `presskit-Logo-Hero-Asset_02.mp4` (press kit Video folder), `font-substitutes-display.png`, `font-substitutes-body.png` (our specimen comparisons).
- Press kit also has Photos, Product screenshots (e.g. "Granola home.png", "Granola note.png", "NEW Granola Chat.png", "Recipes.png") and stickers, not downloaded.
