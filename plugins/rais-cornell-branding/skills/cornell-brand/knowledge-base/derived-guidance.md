# Derived guidance (where brand.cornell.edu is silent)

As-of 2026-10-02. **Everything in this file is [Derived]**: RAIS's extrapolation from the official rules in the other KB files. brand.cornell.edu does not publish guidance for charts, generated Office or PDF documents, or UI components. Never present anything here as "Cornell requires". Say "brand.cornell.edu does not specify this; following its color and logo rules, a reasonable approach is...". For public-facing work, suggest a consultation with Brand Communications (brand@cornell.edu).

## Contents
1. How to use this file
2. Generated Office and PDF documents
3. Charts and data visualization
4. Web components and UI
5. Dark mode and other variants

## 1. How to use this file

- **DER-01** Start from the official rules (`colors.md`, `logos.md`, `typography-web.md`). Use this file only for what those do not decide.
- **DER-02** State the limit out loud in the answer: list which parts are official and which are Derived, with rule IDs.
- **DER-03** Stay inside the official palette. If a design seems to need a color outside it (a tint, a status color), say so and ask the user rather than inventing one (COL-54).

## 2. Generated Office and PDF documents

What the site provides: PowerPoint templates (a blank 2020 template and seasonal Fall 2025/2026 templates) and a Canva template, linked from https://brand.cornell.edu/resources/downloads. The PowerPoint downloads sit behind an institutional sign-in and were not reviewed. It gives no Word, Excel or PDF template, and no document layout rules. Stationery is handled by Cornell Print Services (`governance.md`).

- **DER-10** Prefer the official template over rebuilding one. For a deck, ask the user to download the current template and build from it. Do not approximate its layouts or recreate its logo artwork.
- **DER-11** Palette: use the hex values in `colors.md`. Text uses only approved pairings. Headings or key callouts in Carnelian `#B31B1B` on white; body text in Dark gray `#222222` on white. Apply "first and only": Carnelian should be the first color a reader sees, and in a one-color document it is the only one.
- **DER-12** Fonts: Palatino is the primary serif and Freight Text Pro and Freight Sans Pro are the web typefaces (TYP-02 to TYP-04), all licensed. Document generators cannot assume they are installed. Use them only when the user confirms they are available on the machines that will open the file; otherwise use a safe serif such as Georgia or Times New Roman and a safe sans such as Arial or Helvetica, and tell the user the file does not use a brand typeface. Never embed font files in a repository.
- **DER-13** Logos and seals: never draw, recolor or stretch one in a generated file (LOG-01). Leave an empty, labeled placeholder sized to the official asset (bold logo above 3/4" in print; LOG-10) and tell the user which official file to drop in. Keep clear space of at least 1/4 the seal's diameter (LOG-21). One Cornell logo per piece (LOG-24).
- **DER-14** Accessibility: tag PDFs for accessibility when the generator supports it, set the document language and title, and give images alt text. These follow from Policy 5.12 (GOV-07), which covers web content; the brand site does not say it covers documents, so treat them as good practice.
- **DER-15** Names in document text follow `nomenclature.md`. Photo credits follow MED-10 and MED-11. AI-generated images are labeled (MED-22).

## 3. Charts and data visualization

The site has no chart guidance. Below is a conservative extension of its color rules.

- **DER-20 Single series:** Carnelian `#B31B1B` (6.80:1 on white). This is the "first and only" rule applied to a chart.
- **DER-21 Emphasis against context:** Draw the series that matters in Carnelian and the rest in grays (`#222222` and `#A2998B` or `#9FAD9F` for de-emphasized marks). This keeps accents within the ~3% guidance (COL-02).
- **DER-22 Several series:** Choose from the official palette in this order and stop as soon as you have enough: Carnelian `#B31B1B`, Navy `#073949`, Link blue `#006699`, Dark gray `#222222`, Green `#4B7B2B`, Secondary red text variant `#DF1E12` (close to Carnelian, so avoid pairing them), Orange `#D47500`. Beyond about five series, a chart is probably the wrong tool; split it into small multiples or use direct labels. Neighboring series are low contrast against each other [computed]: Navy `#073949` vs Link blue `#006699` is 1.99:1, Carnelian vs Navy 1.83:1, Carnelian vs Dark gray `#222222` 2.34:1, Navy vs Dark gray 1.28:1. Never rely on color alone to tell neighbors apart; use markers, line styles, direct labels or gaps (DER-24).
- **DER-23 Contrast of marks:** The site's thresholds are for text. For chart marks, use the same 3:1 as a sensible floor (it matches WCAG non-text contrast practice; the site cites WCAG 2.0, which does not include that criterion). Computed on white [Derived]: `#B31B1B` 6.80, `#073949` 12.42, `#006699` 6.25, `#222222` 15.91, `#4B7B2B` 5.04, `#DF1E12` 4.85, `#D47500` 3.31 (passes 3:1). These **fail 3:1 on white**: `#A2998B` 2.81, `#9FAD9F` 2.35, `#6EB43F` 2.54, `#F8981D` 2.21. Use them only as de-emphasized context with a direct label, an outline, or a non-white background, and never as the only way to find a mark.
- **DER-24 Do not rely on color alone:** add direct labels, markers or line styles so the chart reads in grayscale and for color-blind readers. This is standard accessibility practice, not a brand rule.
- **DER-25 Text in charts:** axis labels, tick labels and legends use Dark gray `#222222` on white or `#F7F7F7`. Never put `#6EB43F`, `#F8981D` or `#EF4035` behind or as text (COL-31, COL-34, COL-36).
- **DER-26 Backgrounds:** white or Light gray `#F7F7F7`. Avoid full-bleed accent backgrounds (COL-03).
- **DER-27 Diverging or status meaning:** red/green pairs for good/bad are poor practice even outside branding. The site defines no semantic colors (COL-54). Use Carnelian versus Navy or Link blue for two-sided scales and label the ends.
- **DER-28 Logos on charts:** do not place a Cornell logo inside the chart area. If the chart ships in a Cornell publication, the publication carries the logo once (LOG-24).
- **DER-29 Chart library code:** when writing matplotlib, Plotly, D3 or similar, define the palette once as named constants built from `colors.md` and reuse them; do not leave library default color cycles in place.

## 4. Web components and UI

The site specifies no component library, type scale, spacing or radius (WEB-04). Suggestions, all Derived:

- **DER-40 Links and buttons:** text links `#006699` on white or `#F7F7F7`. Underline links in running text so they are distinguishable without color. A primary button can use Carnelian with white text (6.80:1) or Link blue with white text (6.25:1); the site lists Link blue for both "Links" and "Buttons" (COL-30), and Carnelian for "Banners and backgrounds" (COL-10), so Link blue is the documented choice for buttons.
- **DER-41 Focus and hover states:** the site defines none. Keep them visible (at least 3:1 against neighbors) and inside the official palette.
- **DER-42 Header bar:** the six official layout examples show a thin carnelian bar across the top (WEB-01). Reproducing that is consistent with the examples, and still optional because they are illustrations.
- **DER-43 Layout proportions:** aim for mostly white surfaces, dark gray body text, carnelian for the first-read elements, and sparing accents (COL-02).
- **DER-44 A logo placeholder:** mark the seal position with a comment or an empty, labeled slot, never a drawn mark (LOG-01, LOG-58).

## 5. Dark mode and other variants

- **DER-50** The site defines no dark palette. Carnelian on `#222222` is 2.34:1 (COL-40 non-pairings), so a dark theme cannot simply reuse the official text colors. Options: keep the official light theme only; or ask Brand Communications for guidance. Do not invent a lighter "dark-mode carnelian" and present it as approved.
- **DER-51** If a user insists on a dark theme, build it from official colors only: White `#FFFFFF` text on Dark gray `#222222` (15.91:1, an official pairing), Light gray `#F7F7F7` for secondary text on dark, Carnelian only as a non-text fill or large block with white text on it. Label the result as unreviewed. Links on Dark gray: `#006699` (2.55:1) and Carnelian (2.34:1) fail, and the site lists no link color for dark backgrounds, so use White with an underline and say it is unreviewed.
- **DER-52** Print: use the print values (PMS 187, CMYK 0/100/79/20) in `colors.md`, not the screen hex.
