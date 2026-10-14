# PT Preview Content Migration

## Authority And Identity
October 14, 2026: owner explicitly requested a GitHub website named `pt-preview`, based on Life, In Motion, with all public source content and original logo, addressing athletic and geriatric patients. This authorizes this independent preview publication and supersedes the earlier local-only restriction. Production domain, practice accounts, patient collection, outreach and spending are excluded.

Working root: `C:\Users\Admin\OneDrive - CWU\Apps\Prospect-Web-Mockups\pt-preview`, renamed in place with Git history retained. Local concept rollback: `7c83b78`. Repository: https://github.com/ukiahcomputerworks/pt-preview . Intended Pages URL: https://ukiahcomputerworks.github.io/pt-preview/ . `main` is source; GitHub Actions publishes only `site/`. No custom domain or production DNS changes. Dedicated saved AI project remains unregistered, not inferred from Linear/files.

## Inventory And Completeness
Captured sitemap, public navigation and same-host routes with bounded HTTP GETs, 17 route responses including aliases and empty utility. Thirteen unique public editorial routes. `content/practice.json` preserves all substantive source blocks and asset provenance; `content/migration-map.json` accounts for every block, and `content/route-manifest.json` owns the 19 output routes. Raw captures remain locally in ignored `source/`.

Built 16 editorial pages and three aliases:

| Original Source Path | Preview Disposition |
| --- | --- |
| / and /home | New goal-led homepage retains all substantive original copy; /home redirects to home |
| /physical-therapy-1 and /physical-therapy | Full care content, techniques and conditions in accessible disclosures; alias redirects locally |
| /functional-fitness-classes | Both programs retained, separate class times, location and registration paths |
| /golf-performance | Complete TPI assessment copy and source image |
| /meet-the-team | All six staff, credentials, portraits and full bios retained; expanded biography disclosures |
| /testimonials | All four source stories, names and photographs retained without invented outcome claims |
| /contact-us | All contact details retained; source Name/Email/Message UI represented by disabled preview fields, no submission |
| /careers | Full original careers copy and source photograph |
| /insurance and /about | Full insurance list, coverage/exclusion wording retained; /about redirects locally |
| /faqs | All substantive source answers retained; two placeholder answers replaced by office-contact guidance |
| /about-us | Full practice/facility copy retained, including source's two-location statement; no second address invented, office confirmation note added |
| /patient-forms | Source body has no content or downloadable forms. Clear call-for-paperwork guidance; no patient uploads |
| /book-an-appointment | Source heading/intent retained, unrelated business/creative-project template paragraph replaced by call-to-schedule guidance |
| /cart | Empty commerce scaffold, no practice content; intentionally omitted |
| New /sports-rehabilitation and /healthy-aging | Goal-specific pathways using owner ACL/new-knee examples and existing service destinations, no invented protocols |
| New /preview-information | Independent-review scope and external-service/data boundary |

173 captured text blocks after removing duplicate list wrappers: 171 rendered source blocks with case-insensitive text equivalence verified. One original “Our Expertise” label promoted into the shared expertise label; one unrelated booking placeholder paragraph omitted. FAQ placeholder strings were non-paragraph wrapper content, explicitly replaced, not accepted as answers. Titles use owner-required Title Case. Original body wording remains source copy, not independently validated clinical advice. Headline/category additions are creative copy.

## Media And Logo
25 media records captured with source URL, SHA-256 and dimensions; all preserved as optimized local deployment assets. Original bytes remain locally. The practice logo was already RGBA PNG with alpha range 0–255, so no reconstruction or background removal was needed. Transparent artwork retained for the paper header. Photographs optimized and metadata stripped; opaque photo PNGs converted to JPEG. No synthetic patient or staff imagery. Original source credits, names and client copyright retained; source had no separate photographer credit. Preview uses owner-requested source media; any future production rights review remains separate.

## Functional Boundary
Phone, directions, source social links and Firefly email/phone remain intentional external actions. Clinic class booking points to the existing `mendocinopt.as.me` service, without creating a reservation or claiming delivery. No new booking backend, form endpoint, tracking, cookies or browser storage. Disabled message UI cannot collect health information; patient forms route accepts nothing.

## Validation
`scripts/validate_preview.py` checks all source dispositions and rendered text equivalence, 19 routes, required metadata and images, and runs shared colophon/link gates. Seven-route local concept checks are superseded by 527-link migration validation. Negative test rejects an injected legacy-host handoff and restores original. JS syntax passes. Browser checks cover every editorial route at 1440/390/320; no horizontal overflow, one h1, loaded logo, contained footer and no broken loaded images. Mobile expanded Explore menu initially extended left of viewport; fixed by anchoring to header and rechecked at 320px. Keyboard goal selection, Escape menu close and care/biography expansion verified. Full local/live screenshots and exact release evidence remain in `evidence/` and Linear COM-515.

## Design System And Density
Paper/redwood/clay palette, bold Georgia title, Arial body 18px (19px leads), role-specific shared buttons/links/navigation, 44px+ controls and focus outlines. All sixteen editorial routes share header/footer/CTA, a 42–72px page-heading role and common body tokens. Home hero is an intentional 49–88px display variant. Source headings hidden only where duplicate page labels would compete with the new title; content still preserved accessibly. Photo panels preserve aspect except intentional homepage/editorial crops; full portraits retained on team pages.

Reduced homepage scenic image from about 430px to 260px maximum and class photo from 320px to 225px to prevent photographs stretching adjacent text. Goal-photo region changed from 1.7 to 2.1 aspect at desktop; phone keeps 1.7. No fixed/minimum-height filler sections. Biography/service disclosures preserve full content without forcing every visitor through it. No formal WCAG certification or conversion efficacy claim.
