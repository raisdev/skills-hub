# Typography, web layout and accessibility

As-of 2026-10-02. Tags: see `_sources.md`. The brand site is thin on typography and silent on most web component details. Where it is silent this file says so.

## Contents
1. Typefaces
2. Font stacks the brand site itself uses
3. Web page layout patterns
4. Accessibility
5. Web Communications Standards
6. What the site does not specify

## 1. Typefaces

Source: https://brand.cornell.edu/design-center/typography

- **TYP-01 [Official]** "Typefaces and how they are presented are as important to Cornell's identity as the use of color, graphics and photography. Clean, well-spaced typography is what distinguishes professional print and digital communications."
- **TYP-02 [Official]** **Palatino** is the primary serif typeface for the university. It appears on the Cornell logo. The site links to Fonts.com to purchase it. It is a licensed font.
- **TYP-03 [Official]** **Freight Text Pro** is a more contemporary serif that pairs with Freight Sans. It appears on web properties such as cornell.edu. The site links to Adobe Fonts (Typekit) to view it.
- **TYP-04 [Official]** **Freight Sans Pro** is a sans serif with a more contemporary personality, available in many weights and styles and "easily legible on screen". Also linked on Typekit.
- **TYP-05 [Derived]** All three are licensed commercial fonts. Do not bundle, embed or self-host font files in a repo or plugin. Load Freight through an Adobe Fonts kit that the site's owner has licensed, and fall back as in section 2 when the license is not available.

## 2. Font stacks the brand site itself uses

Source: `/assets/css/cornell.css` on brand.cornell.edu (read 2026-10-02).

- **TYP-10 [Derived]** The brand site declares `font-family: "freight-text-pro", Georgia, "Times New Roman", Times, serif` for serif text and `font-family: "freight-sans-pro-n3", "freight-sans-pro", sans-serif` for sans text. These are the site's own implementation, not a published standard. Reusing them is the closest available match to the official typefaces. The Adobe Fonts kit ID is not published; the owner of the site must supply one.
- **TYP-11 [Derived]** A system sans stack such as `-apple-system, "Segoe UI", Helvetica, Arial` is **not** one of the three named typefaces. When a Cornell web property uses it, report that it departs from the documented typefaces as an advisory, not a hard violation, and ask whether Freight is licensed for that site.

## 3. Web page layout patterns

Source: six example layouts on https://brand.cornell.edu/design-center/colors/ (judged from their alt text; template 3 also viewed directly). They are illustrations of color proportion, not a layout spec.

- **WEB-01 [Official]** Common elements across the six examples (from their alt text): a **thin red bar across the top** (five of six), a **circle near the top** that is red in examples 1, 3, 4 and 5 and white in 2 and 6 (the site does not label it, but it is probably the seal position), red blocks for headline text, dark gray blocks for body text, a light gray background band for a content section, and a gray or green footer. Orange appears as a short subheading accent. Blue appears in examples 4 and 6 as a block of link or button text.
- **WEB-02 [Official]** The examples show carnelian dominating the top of the page, white as the main field (about 55%), and dark gray carrying body text. This is the "first and only"/proportion guidance of COL-01 and COL-02 applied to layouts.
- **WEB-03 [Official]** Example 6 uses a wide hero photo with a white circle (logo placeholder) and headline over it. A footer in green appears in examples 2 and 6 and gray in the others. Green is otherwise an accent (COL-31 to COL-33), so a full green footer is the site's own example, not an endorsement of large green areas elsewhere.
- **WEB-04 [Unspecified]** Breakpoints, grid, spacing, max line length, heading sizes, button and form styles, iconography beyond "visual language using symbols and icons", border radius, shadows and animation are not specified by the brand site.

## 4. Accessibility

- **WEB-10 [Official]** Policy 5.12, "Web Accessibility Standards": all new, newly added or redesigned web content, pages, functionality, websites and web applications must meet "the most recently published Web Content Accessibility Guidelines (WCAG)", unless doing so would cause a fundamental alteration or undue burden, in which case an equally effective alternative must be provided. Source: https://brand.cornell.edu/policies and https://policy.cornell.edu/policy-library/web-accessibility-standards
- **WEB-11 [Official]** The colors page states the contrast requirement as WCAG **2.0** level AA: 4.5:1 normal text, 3:1 large text (greater than 24 px, or 19 px and bold). See COL-06.
- **WEB-12 [Derived]** Note the two documents name different WCAG versions: the colors page cites 2.0, Policy 5.12 says the most recent. When reviewing, treat the contrast numbers above as the minimum and the latest WCAG as the governing standard, and say that the two sources differ. The site's large-text wording (24 px, or 19 px bold) is close to, but not identical with, WCAG's (18 pt = 24 px, or 14 pt bold = about 18.7 px).
- **WEB-13 [Official]** Accessibility contact used by the university's Web Communications Standards page: **ur-accessibility@cornell.edu**. The address appears four times in that page's raw HTML (checked 2026-10-02); the summarizing fetch reported that the page's footer invites people with disabilities to email it, which was not confirmed line by line.
- **WEB-14 [Derived]** Practical review checks that follow from WEB-10 and the pairings in `colors.md`: text uses an approved pairing; graphic-only accents (`#6EB43F`, `#F8981D`, `#EF4035`) never carry text; link color is `#006699` and links are distinguishable by more than color alone; informative images have alt text (purely decorative images may use an empty alt); the page declares `lang`. The last three are standard WCAG practice, not statements from the brand site.

## 5. Web Communications Standards

Source: https://universityrelations.cornell.edu/resources/web-comms-standards/ (read through a summarizing fetch, then spot-checked against the raw page on 2026-10-02; see `_sources.md` for what was and was not confirmed).

- **WEB-20 [Official]** They are the "minimum requirements" for university and university-affiliated websites and web applications. All new sites and redesigns using the Cornell domain or the Cornell University name must comply (FAQ, https://brand.cornell.edu/resources/faqs).
- **WEB-21 [Official]** Brand and design items on that page: comply with Policy 4.10 on names, logos, trademarks and insignias; use the university color palette; apply logos and marks according to brand architecture; follow university nomenclature in all text; keep design coherent with partner properties. Contact: brand@cornell.edu.
- **WEB-22 [Official]** Imagery items: high quality and small file size; reflecting diversity and inclusion; every image, graphic, font and piece of content must be "licensed or otherwise properly authorized for use". Contact: photo@cornell.edu.
- **WEB-23 [Official]** Other policies named there: Policy 5.6 (domain names), Policy 5.10 (information security; contact security-services@cornell.edu), 4.3, 4.11, 4.16.
- **WEB-24 [Official]** The standards page contains **no** concrete markup requirements: nothing about header or footer elements, logo placement, fonts, hex values, analytics, privacy statements, copyright lines or favicons.

- **WEB-25 [Unspecified]** The brand site does not say whether the palette, type and nomenclature rules bind a site hosted outside cornell.edu. WEB-20 covers sites "using the Cornell domain or the Cornell University name" and GOV-34 covers cornell.edu sites.
- **WEB-26 [Derived]** RAIS working rule, recorded 2026-10-02 at RAIS's request: treat the palette, type, accessibility and naming rules as binding for RAIS sites regardless of host. This is a RAIS decision, not a brand-site statement; do not present it as "Cornell requires". It does not change LOG-03: the FAQ's rule that sites outside cornell.edu should not display a Cornell logo or seal is host-dependent on its own terms.

## 6. What the site does not specify

Do not invent rules for these. Say "not specified by brand.cornell.edu", then give a labeled Derived recommendation if useful (see `derived-guidance.md`): type scale and weights, line height, text alignment, spacing system, grid and breakpoints, component library, form and button styles, icons, dark mode, motion, favicon and header/footer markup. A favicon is provided as a gated download (see `_sources.md`).
