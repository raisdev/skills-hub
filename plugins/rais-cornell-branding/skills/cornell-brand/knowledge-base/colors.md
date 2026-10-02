# Colors

As-of 2026-10-02. Source: https://brand.cornell.edu/design-center/colors/ unless a rule says otherwise. Tags: see `_sources.md`.

## Contents
1. Principles
2. Primary palette
3. Secondary palette
4. Accent palette
5. Approved pairings and contrast (WCAG)
6. Things that are NOT in the palette
7. CSS variables (official colors only)

## 1. Principles

- **COL-01 [Official]** Cornell's primary brand color is red (Carnelian). Follow the **"first and only" rule**: on platforms with many colors (websites, brochures) Cornell red should be the first color people see. On color-limited media it should be the only color they see.
- **COL-02 [Official]** Rough usage proportions, "not an exact equation", to be referenced when designing: primary colors ~90% of a layout (red 20%, white 55%, dark gray 15%), secondary ~7%, accents ~3%.
- **COL-03 [Official]** Accent colors must not be used as full-color bleeds, should be used periodically and in moderation, and must **never become the primary color of a school, center, institute or department**.
- **COL-04 [Official]** Avoid developing additional palettes (FAQ, https://brand.cornell.edu/resources/faqs). Use the secondary palette to complement the primary.
- **COL-05 [Official]** Logos may only be shown in carnelian, black or white (see `logos.md`).
- **COL-06 [Official]** All web content must meet the university's web accessibility standard (Policy 5.12), based on WCAG 2.0 level AA: contrast at least **4.5:1 for normal text** and **3:1 for large text**. Large means greater than 24 px, or 19 px and bold.

## 2. Primary palette

| Color | Print | Web hex | Official web pairings | Example uses |
|---|---|---|---|---|
| **COL-10** Carnelian | PMS 187, CMYK 0/100/79/20 | `#B31B1B` | on White `#FFFFFF`, on Light gray `#F7F7F7` | Cornell seal, banners and backgrounds, headlines |
| **COL-11** Dark gray | PMS Cool Gray 11, CMYK 48/36/24/66 | `#222222` | on White, on Light gray | Cornell seal, banners and backgrounds, headlines and body text |
| **COL-12** White | CMYK 0/0/0/0 | `#FFFFFF` | on Carnelian, on Dark gray | Cornell seal, banners and backgrounds, headlines or body text on dark backgrounds |

All tagged [Official].

## 3. Secondary palette (~7%)

Neutral hues used as supplementary colors rather than driving colors.

| Color | Print | Web hex | Official web pairings | Example uses |
|---|---|---|---|---|
| **COL-20** Light gray | n/a | `#F7F7F7` | Carnelian text, Dark gray text | Backgrounds; secondary text on dark backgrounds |
| **COL-21** Dark warm gray | PMS 403, CMYK 14/18/22/42 | `#A2998B` | Black `#000000` text | Neutral background areas |
| **COL-22** Sea gray | PMS 5635, CMYK 29/8/25/24 | `#9FAD9F` | Black `#000000` text | Neutral background areas |

All tagged [Official]. Note the site's own example mock-up in the colors page shows the secondary bar as `#A2998B`, `#F7F7F7`, `#9FAD9F`.

## 4. Accent palette (~3%)

| Color | Print | Web hex | Text allowed? | Official pairings | Example uses |
|---|---|---|---|---|---|
| **COL-30** Blue / **Link blue** | PMS Process Blue, CMYK 100/13/1/2 | `#006699` | yes | on White, on Light gray | Links, buttons |
| **COL-31** Green (graphic) | PMS 369, CMYK 67/0/98/5 | `#6EB43F` | **graphic elements only** | none (not for text) | Line breaks, color blocks without text, small fill areas |
| **COL-32** Green (text, any size) | same family | `#4B7B2B` | any size | on White, on Light gray | text |
| **COL-33** Green (text, large only) | same family | `#578E32` | **large text only** | on White | large text |
| **COL-34** Orange (graphic) | PMS 144, CMYK 0/52/100/0 | `#F8981D` | **graphic elements only** | none | Line breaks, color blocks without text, small fill areas |
| **COL-35** Orange (text, large only) | same family | `#D47500` | **large text only** | on White, on Light gray | large text |
| **COL-36** Secondary red (graphic) | PMS Red 032, CMYK 0/90/60/0 | `#EF4035` | **graphic elements only** | none | Line breaks, color blocks without text, small fill areas |
| **COL-37** Secondary red (text, any size) | same family | `#DF1E12` | any size | on White, on Light gray | text |
| **COL-38** Navy | PMS 7463, CMYK 100/62/12/62 | `#073949` | yes | on White, on Light gray | Neutral background areas |

All tagged [Official]. The graphic/text variants of green, orange and red are the site's own pairing; the site says the graphic variants "highlight important features but are used sparingly".

## 5. Approved pairings and contrast

**COL-40 [Derived]** Contrast ratios below were **computed** by RAIS from the official hex values with the WCAG relative-luminance formula. The site lists the approved pairings (section 2 to 4) but does not publish ratios except the 4.5:1 and 3:1 thresholds in COL-06.

| Foreground on background | Ratio | Passes normal text (4.5) | Passes large text (3) |
|---|---|---|---|
| `#B31B1B` on `#FFFFFF` | 6.80 | yes | yes |
| `#B31B1B` on `#F7F7F7` | 6.35 | yes | yes |
| `#222222` on `#FFFFFF` | 15.91 | yes | yes |
| `#222222` on `#F7F7F7` | 14.85 | yes | yes |
| `#FFFFFF` on `#B31B1B` | 6.80 | yes | yes |
| `#FFFFFF` on `#222222` | 15.91 | yes | yes |
| `#006699` on `#FFFFFF` | 6.25 | yes | yes |
| `#006699` on `#F7F7F7` | 5.83 | yes | yes |
| `#4B7B2B` on `#FFFFFF` | 5.04 | yes | yes |
| `#4B7B2B` on `#F7F7F7` | 4.70 | yes | yes |
| `#DF1E12` on `#FFFFFF` | 4.85 | yes | yes |
| `#DF1E12` on `#F7F7F7` | 4.52 | yes | yes |
| `#073949` on `#FFFFFF` | 12.42 | yes | yes |
| `#578E32` on `#FFFFFF` | 3.95 | **no** | yes (large only, as the site says) |
| `#D47500` on `#FFFFFF` | 3.31 | **no** | yes (large only) |
| `#D47500` on `#F7F7F7` | 3.09 | **no** | yes (large only) |
| `#000000` on `#A2998B` | 7.47 | yes | yes |
| `#000000` on `#9FAD9F` | 8.95 | yes | yes |

**COL-41 [Official]** The "Web accessible combinations" column in sections 2 to 4 is the site's list of approved brand color combinations that meet WCAG 2.0 AA. **[Derived]** A combination that is not listed is not approved; it may still be acceptable if it independently meets COL-06, so compute its ratio and label the result Derived.

Non-pairings worth flagging [Derived]:
- `#B31B1B` on `#222222` is 2.34:1 and `#006699` on `#222222` is 2.55:1. **Carnelian or link blue text on a dark gray background fails** and is not an official pairing.
- `#6EB43F`, `#F8981D` and `#EF4035` on white are 2.54, 2.21 and 3.85: they fail for text, which matches the site's "graphic elements only" note.
- `#A2998B` text on `#F7F7F7` is 2.63:1 and `#9FAD9F` on white is 2.35:1: the two warm/sea grays are background colors, not text colors.

## 6. Things that are NOT in the palette

- **COL-50 [Derived]** The colors on the colors page are treated as the whole official palette, an inference from the FAQ's "development of additional palettes should be avoided" (COL-04). Anything else is unofficial until Brand Communications says otherwise.
- **COL-51 [Official, see SRC-01]** The downloadable palette file (https://brand.cornell.edu/downloads/colors/web/cornell-color-palette.css) lists `#3787b0` as "Link Color". The colors page says `#006699`. **Use `#006699`.** `#3787b0` on white is 4.00:1 [Derived] and fails AA for normal text.
- **COL-52 [Official, see SRC-02]** The same download also lists `#0068ac` (Royal Blue), `#89cce2` (Light Blue), `#c9d6a5` (Light Green) and `#d8d2c9` (Light Brown/Beige). They are not on the colors page. Treat as unapproved and ask Brand Communications before using.
- **COL-53 [Derived]** The site lists dark gray `#222222` as the primary text and headline color and lists pure black `#000000` only for text on the warm and sea grays and for logos in black. The site never says pure black is forbidden elsewhere, but defaulting to `#222222` for text follows its listing.
- **COL-54 [Unspecified]** The site gives no dark-mode palette, no hover/active/focus states, no semantic success/warning/error colors, no gradient or shadow rules, and no tints or opacity rules. Any such choice is a design decision; say so and keep it inside the official palette where possible. Lightened or darkened variants of carnelian are not official colors.

## 7. CSS variables (official colors only)

**COL-60 [Derived]** Paste-ready. Names are RAIS's; values are official.

```css
:root {
  /* Primary */
  --cornell-carnelian: #B31B1B;
  --cornell-dark-gray: #222222;
  --cornell-white: #FFFFFF;
  /* Secondary */
  --cornell-light-gray: #F7F7F7;
  --cornell-dark-warm-gray: #A2998B; /* background only; black text */
  --cornell-sea-gray: #9FAD9F;       /* background only; black text */
  /* Accent (use sparingly, ~3%) */
  --cornell-link-blue: #006699;      /* links and buttons */
  --cornell-navy: #073949;
  --cornell-green-text: #4B7B2B;     /* text at any size */
  --cornell-green-large-text: #578E32; /* large text only */
  --cornell-green-graphic: #6EB43F;  /* no text */
  --cornell-orange-large-text: #D47500; /* large text only */
  --cornell-orange-graphic: #F8981D; /* no text */
  --cornell-red-text: #DF1E12;       /* text at any size */
  --cornell-red-graphic: #EF4035;    /* no text */
}
```
