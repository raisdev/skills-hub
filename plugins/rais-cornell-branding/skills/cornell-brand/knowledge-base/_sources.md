# Knowledge base provenance

**KB as-of date: 2026-10-02.** Built by crawling https://brand.cornell.edu/ on that date. The brand site changes without notice, so treat anything older than a few months as possibly stale and re-verify high-stakes answers against the live page.

## Status tags used in every rule

- **Official**: stated on brand.cornell.edu or in a document it links. The source link follows the rule.
- **Derived**: not stated by the site. It is RAIS's extrapolation or computation (for example a contrast ratio calculated from official hex values). Always say "Derived" when relaying it. Never say "Cornell requires".
- **Unspecified**: the site is silent. Say so plainly: "brand.cornell.edu does not specify this."

Rule IDs are stable. Prefixes: COL colors, TYP typography, WEB web and accessibility, LOG logos, NOM names and copy, MED media, GOV governance, DER derived guidance, SRC source notes.

## Pages crawled (all read in full unless noted)

| Page | URL | Fed into |
|---|---|---|
| Home | https://brand.cornell.edu/ | overview, nav map |
| Logos | /logos/ | logos.md |
| Brand architecture | /logos/brand-architecture | logos.md |
| Lockups: academic | /logos/academic | logos.md |
| Logo usage: non-academic | /logos/non-academic | logos.md |
| Multi-college hierarchy | /logos/multi-college-logo-hierarchy | logos.md |
| Design center | /design-center/ | gallery only, no rules |
| Colors | /design-center/colors/ | colors.md |
| Typography | /design-center/typography | typography-web.md |
| Photography and video | /design-center/multimedia and /design-center/photography/ (identical content) | media-licensing.md |
| Music | /design-center/music | media-licensing.md |
| Copyright and licensing | /design-center/copyright-licensing | media-licensing.md |
| Stationery | /design-center/stationery | only says to contact Cornell Print Services |
| Messaging | /messaging/ | nomenclature.md |
| Founding principle | /messaging/founding-principle | nomenclature.md |
| Nomenclature | /messaging/nomenclature | nomenclature.md |
| Acronyms and abbreviations | /messaging/abbreviations | nomenclature.md |
| Student organizations | /messaging/student-orgs | nomenclature.md |
| Alumni clubs | /messaging/alumni | nomenclature.md |
| Social media | /messaging/social-media | only points to socialmedia.cornell.edu |
| Merchandising | /merchandising | governance.md, logos.md |
| Policies | /policies | governance.md |
| Resources hub | /resources/ | nav map |
| Downloads | /resources/downloads and the older duplicate /downloads/ | logos.md, governance.md |
| Terminology | /resources/terminology | governance.md |
| Photo and video releases | /resources/releases | media-licensing.md |
| FAQs | /resources/faqs | governance.md |

Also read: the brand site's stylesheets (`/assets/css/cornell.css`, `/assets/css/responsive-svg.css`), the downloadable palette `/downloads/colors/web/cornell-color-palette.css`, the licensee guide PDF `/downloads/merchandising/Cornell_Licensing_Brand_Guide.pdf` (pages 4 and 5 are image-only logo galleries, so no text was extractable there), and the Web Communications Standards page at https://universityrelations.cornell.edu/resources/web-comms-standards/. That last page was read through a summarizing fetch, then spot-checked against the saved raw page on 2026-10-02. Confirmed present: the "minimum requirements" wording, the policy numbers (4.3, 4.10, 4.11, 4.16, 5.6, 5.10, 5.12), the contact addresses (brand@, photo@, security-services@, ur-accessibility@cornell.edu) and the "licensed or otherwise properly authorized" sentence. **Not independently verified:** the claim in WEB-24 that the page has no concrete markup requirements (an absence is harder to confirm than a presence), and the paraphrased items in WEB-21 to WEB-23, which were not checked word for word.

## Not reviewed (say so if asked)

- **Gated downloads:** logo zips, the PowerPoint templates (blank 2020 and seasonal Fall 2025/2026), the favicon zip and the video outro zip. These redirect to an institutional sign-in. The site also links a Canva template, which was not opened.
- **Full policy text:** Policy 4.10, 5.12 and the others are only summarized on the brand site. The full policies live on https://policy.cornell.edu/ and were not read.
- **WCAG itself.** Contrast figures in this KB are computed with the standard WCAG relative-luminance formula, not copied from a WCAG document.
- **Downloaded but not analyzed:** `licensed-manufacturers.pdf`, `licensee-list-cornell-8-25-2025.pdf` and the workplace code of conduct PDF. They are vendor lists and labor policy, not design rules.
- **Image content.** Logo artwork and the six web layout examples were judged from alt text; only the logo anatomy image and one of the six layout images (template 3) were also looked at directly.

## Conflicts and oddities in the source (how this KB resolves them)

- **SRC-01 Link blue.** The colors page gives `#006699` (contrast 6.25:1 on white, passes AA). The downloadable palette CSS gives `#3787b0` (4.00:1, fails AA for normal text). **This KB uses `#006699`.**
- **SRC-02 Extra colors in the download.** The palette CSS also lists Royal Blue `#0068ac`, Light Blue `#89cce2`, Light Green `#c9d6a5` and Light Brown/Beige `#d8d2c9`. None appear on the colors page. Treat them as not approved unless Brand Communications says otherwise.
- **SRC-03 Carnelian values.** Web is `#B31B1B` on the colors page. The licensee guide lists RGB 170/20/45 for merchandise. Use `#B31B1B` on screen.
- **SRC-04 Trademark marks.** The merchandising page says the logo must carry ™ (and ® when the name is used alone), while the licensee guide says ™ and ® should not be used on licensed products. Neither says anything about websites. Treat web use as Unspecified.
- **SRC-05 Department logos.** The FAQ says departments, programs, centers and institutes may not have logos. The brand architecture page lets research institutes and centers propose a distinct identity to Brand Communications for review. Resolve by sending the request to Brand Communications.
- **SRC-06 Slips not to copy.** A `brand.cofrnell.edu` typo on the Web Communications Standards page, a literal `[YEAR]` placeholder in the FAQ, and `/downloads` versus `/resources/downloads` showing different seasonal template years (Fall 2025 vs Fall 2026).
- **SRC-07 Emergency banner.** The downloads page source contains an HTML-commented-out "Technical Content" block describing a "web-based emergency notification script that should be installed on all University websites", linking to /messaging/emergency-banner (which returns 404) and an emergency-banner zip. It is hidden on the live page. **Do not present it as a current requirement**, and do not list it as a download. If the user asks, say it appears to have been retired and to confirm with Brand Communications.

## How to refresh this KB

1. Re-fetch each URL in the table above and diff the colors, logo sizes, nomenclature ✔/✘ marks and policy list against the matching file. The nomenclature page marks approved and not-approved variants with icon classes (`icon-check`, `icon-close`) that plain-text extraction loses, so read the raw HTML.
2. Check that no hex value, size, or quoted phrase in a KB file is missing from the source. Remove or re-tag anything that is.
3. Update the as-of date here and in the plugin README, bump the version in `plugin.json`, and record any new conflicts above.
