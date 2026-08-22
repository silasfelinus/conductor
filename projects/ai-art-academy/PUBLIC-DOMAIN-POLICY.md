# AI Art Academy — Public Domain Policy

date: 2026-07-10
status: active (task t-006)
scope: governs every artwork, artist, style entry, starter image, LoRA, and marketing
mention in the AI Art Academy. Stricter than the law on purpose — see §4.

This policy implements the DESIGN-BRIEF.md ethical boundary ("only public-domain art
and artists who are no longer living") as concrete, checkable rules. When a rule here
and convenience conflict, the rule wins. When the rule itself is ambiguous, escalate
per §5 — never guess.

---

## 1. What counts as public domain (the works we may include)

### 1.1 US publication cutoff (verified 2026-07-10)

- In the United States, works **published in 1930 or earlier** are in the public
  domain as of 2026. Works published in 1930 entered the US public domain on
  **January 1, 2026** (Public Domain Day 2026 — verified via Duke Law's Center for
  the Study of the Public Domain, the Library of Congress copyright blog, and NPR's
  Public Domain Day 2026 coverage; Piet Mondrian's 1930 *Composition with Red, Blue
  and Yellow* was among the named entrants).
- This is a **rolling cutoff**: each January 1, one more year enters. The general
  rule for pre-1978 published works is `current year − 96` (95-year term). In 2027
  the cutoff becomes 1931, and so on. **Do not hardcode "1930" in app copy or seed
  data — store the rule, or re-derive the year at content-review time.**

### 1.2 Death + 70 (most non-US jurisdictions)

- The EU, UK, and many other jurisdictions use **life of the author + 70 years**.
  As of 2026 that means artists who **died in 1955 or earlier**. Also rolling:
  `current year − 70`.
- Kind Robots serves users outside the US, so US-publication PD alone is not enough.

### 1.3 Our combined rule (conservative, both prongs required)

An artwork is Academy-eligible only if **BOTH** hold:

1. **Artist died more than 70 years ago** (in 2026: died before 1956), AND
2. **The work was created/published on or before the US cutoff year**
   (in 2026: 1930 or earlier).

This is deliberately stricter than any single jurisdiction requires. It keeps us
clear in the US, the EU/UK, and death+70 jurisdictions simultaneously, and it
automatically enforces the "dead artists only" brief rule with a comfortable margin —
no artist who died within living memory of a working peer community qualifies.

Practical consequences (2026):

- Van Gogh (d. 1890), Monet (d. 1926), Klimt (d. 1918), Hokusai (d. 1849),
  Cézanne (d. 1906), Seurat (d. 1891): **eligible**.
- Mondrian (d. 1944) passes prong 1, and his pre-1931 works pass prong 2 — eligible
  work-by-work; his 1930s+ works are not yet eligible.
- Matisse (d. 1954) passes prong 1 in 2026, but most of his famous works are
  post-1930 — **mostly ineligible** for now; check per-work.
- Picasso (d. 1973), Dalí (d. 1989), Frida Kahlo (d. 1954 — but works largely
  post-1930), O'Keeffe (d. 1986): **not eligible** (fail one or both prongs).
- Anonymous/corporate/undated works: if either prong can't be established from a
  reputable source, treat as **not eligible** and escalate per §5 if the work matters.

## 2. Digitization licenses we accept

### 2.1 The legal backdrop (Bridgeman / Meshwerks)

Under *Bridgeman Art Library v. Corel* (S.D.N.Y. 1999) and the reasoning extended in
*Meshwerks v. Toyota* (10th Cir. 2008), a **faithful photographic reproduction of a
public-domain 2D work does not acquire a new US copyright** — there is no originality
in exact copying. So a museum's photo of a PD painting is itself PD in the US.

**But we do not rely on Bridgeman alone.** Some non-US jurisdictions recognize
reproduction rights, some museums assert contractual terms, and relying on a
litigation position instead of an explicit grant is exactly the kind of ambiguity
this policy exists to remove. Bridgeman is our safety net, not our sourcing strategy.

### 2.2 Accepted grants for the image file, in preference order

1. **CC0 / Creative Commons Zero** — explicit waiver by the holding institution.
   Verified examples (2026-07-10):
   - **The Met Open Access** (metmuseum.org/policies/image-resources, program
     announced 2017): images of works the Met believes to be public domain are CC0 —
     "use, share, and remix — without restriction," including commercially; tombstone
     data is CC0 too.
   - **Art Institute of Chicago Open Access** (artic.edu/open-access/open-access-images):
     50,000+ images under CC0 Public Domain Designation, any purpose including
     commercial, plus a public API (api.artic.edu) serving the same data under CC0.
   - Also in this tier: Cleveland Museum of Art Open Access (CC0, 34,000+ images),
     Smithsonian Open Access (CC0), Paris Musées (CC0).
2. **Public Domain Mark / "no known copyright restrictions"** — e.g. Wikimedia
   Commons PD-Art/PD-old tags, Flickr Commons "no known copyright restrictions",
   Library of Congress "no known restrictions". Acceptable when the underlying work
   passes §1.3 and the tag is consistent with what we know of the work.
3. **Museum open-access terms equivalent to PD** — institution-specific programs
   that permit unrestricted reuse including commercial (e.g. **Rijksmuseum
   Rijksstudio** high-res downloads, **National Gallery of Art (US) open access**
   images of PD works, **Getty Open Content**). Read the actual terms once per
   institution, record the terms URL in the provenance record, and re-check if the
   institution revises its program.

### 2.3 Not accepted

- CC BY / CC BY-SA / CC BY-NC for the *digitization* of a PD work — attribution or
  share-alike conditions contaminate the "remix freely" promise. (CC BY on genuinely
  copyrighted modern content is out of scope entirely — Academy content is PD-only.)
- "Free for editorial/personal use" image banks, press images, auction-house photos.
- Screenshots from books, documentaries, or paywalled databases.
- Any image where the underlying **work** fails §1.3, regardless of the file's license.
- 3D works (sculpture) photographed by third parties: the *photograph* has its own
  copyright (Bridgeman covers only 2D faithful repro). Only institution-granted CC0
  photos of sculpture qualify.

## 3. Provenance: recorded per image, no exceptions

Every image the Academy stores, displays, or ships as seed data carries a provenance
record. No record → the image does not ship. Schema (JSON, one object per image):

```json
{
  "workTitle": "Under the Wave off Kanagawa (The Great Wave)",
  "artist": "Katsushika Hokusai",
  "artistDied": 1849,
  "year": "ca. 1830-32",
  "collection": "The Metropolitan Museum of Art",
  "accessionId": "JP1847",
  "sourceUrl": "https://www.metmuseum.org/art/collection/search/45434",
  "license": "CC0",
  "licenseTermsUrl": "https://www.metmuseum.org/policies/image-resources",
  "retrievedDate": "2026-07-10"
}
```

Field rules:

- `workTitle`, `artist`, `year` — as given by the holding institution (tombstone data).
- `artistDied` — required; this is the §1.3 prong-1 check made permanent.
- `collection` + `accessionId` — the institution and its own identifier (accession
  number, object number, or stable object ID). This is what makes the record
  re-verifiable years later even if URLs rot.
- `sourceUrl` — the page we actually downloaded from (object page, not homepage).
- `license` — one of `CC0`, `PD-Mark`, `Open-Access-Terms` (with `licenseTermsUrl`
  required for the latter).
- `retrievedDate` — download date; licenses get re-checked if an institution
  changes its program.

These records live in the starter-library manifest
(see docs/starter-image-library.md) and, for curriculum example works, in the
`academy-styles` registry entries.

### 3.1 Artist portraits (ai-art-academy/t-072)

The "Meet the masters" gallery uses the same schema plus two fields, because a
portrait/photograph/sculpture has a maker distinct from the person shown:

- `depicts` — the curriculum artist pictured (must match the owning entry's `name`).
- `kind` — `self-portrait` | `portrait` | `photograph` | `sculpture`.

`artist`/`artistDied` always describe whoever **made the image** — the §1.3
prong-1 check applies to the image's creator, not the person depicted. For a
self-portrait these are the same person; for a portrait, photograph, or
sculpture made by someone else (e.g. a photographer's portrait of a painter),
`artist` is that other person and `artistDied` is their death year. Never a
generated likeness in this field — a verified image, or the field stays unset.
Coverage is expected to be partial: many named artists (anonymous painters,
artists who left no documented likeness) legitimately have none. Records live
in `AcademyArtist.portrait` in the `academy-styles` registry, tracked the same
pending-until-media-sync way as example works (see
`config/academy-artist-portraits-pending.json` in kind_robots).

## 4. Style imitation rules (policy, stricter than law)

Legal baseline: **styles are not copyrightable.** Copyright protects specific
expression, not techniques, palettes, or aesthetics. Prompting "in an impressionist
style" — or even "in the style of [living artist]" — is not, by itself, copyright
infringement under current US law.

**Our policy is deliberately stricter than that baseline:**

1. **Movements and long-dead artists only.** Academy style entries may reference an
   art **movement** (Impressionism, Ukiyo-e, Art Nouveau, Bauhaus, Baroque…) or a
   **named artist who passes §1.3 prong 1** (died 70+ years ago). Nothing else.
2. **No living-artist names, anywhere.** Not in prompt templates, not in curriculum
   text, not in marketing copy, not in style-card names, not in generation metadata
   we display. This includes recently deceased artists inside the 70-year window and
   active brands/studios (per DESIGN-BRIEF.md: "Disney", "Gorillaz", "DB4RZ" style
   entries stay in the generic Style Lab as Silas's existing call but are **excluded
   from the Academy registry** — never presented as lessons, never given bios).
3. **LoRAs named for living creators are excluded from the Academy registry** —
   even if the LoRA file itself is openly licensed. A permissive license on the
   weights does not change whose signature style it monetizes. (t-003 hunt rule:
   skip them; don't just relabel them.)
4. **No "style laundering."** Don't rename a living artist's style to a euphemism
   ("modern whimsical webcomic style, you know the one") to sneak it in. If the
   entry only makes sense by reference to a living creator, it doesn't belong.
5. Why stricter than law: the Academy's promise is that everything it teaches is
   free heritage — safe to study, remix, and monetize. Working artists' signature
   styles are their livelihood; imitating them by name is legal but is not what
   this product is for.

## 5. Escalation rule

When a case is **genuinely ambiguous** — publication date unclear, artist death date
disputed, an institution's terms don't clearly permit commercial reuse, a work is PD
in the US but arguably not in the EU, a LoRA's subject is a "school of" attribution:

1. **Do not include the item** in the Academy while ambiguous (default-deny).
2. **Add a `needs-human` line item** to `projects/ai-art-academy/roadmap.yaml`
   describing the specific question, what was checked, and the decision Silas needs
   to make — following the soft-gate pattern (t-002 style: "FOR SILAS: … TO APPROVE: …").
3. **Do not park the task.** The task that surfaced the ambiguity continues with the
   item excluded; the escalation rides in parallel. A single doubtful painting never
   blocks a curriculum PR.
4. If the same ambiguity keeps recurring, propose a policy amendment here instead of
   escalating case-by-case.

## 6. Verification log (what was checked for this policy, 2026-07-10)

- **US cutoff**: Public Domain Day 2026 confirmed 1930-published works entered the
  US public domain on 2026-01-01 — Duke Law CSPD (web.law.duke.edu/cspd/publicdomainday/2026/),
  Library of Congress copyright blog ("Lifecycle of Copyright: 1930 Works in the
  Public Domain"), NPR (2025-12-26). Sound recordings run on a separate schedule
  (1925 recordings entered 2026) — irrelevant to us but noted to avoid confusion.
- **Met Open Access**: CC0 for images of PD works + tombstone data, unrestricted
  including commercial use (metmuseum.org/policies/image-resources; program launched
  2017-02-07 with Creative Commons and Wikimedia as partners).
- **AIC Open Access**: CC0 Public Domain Designation on 50,000+ images, any purpose
  including commercial, no permission needed; public API under CC0
  (artic.edu/open-access/open-access-images, artic.edu/open-access/public-api).
- Direct fetches of museum pages were blocked by the sandbox egress proxy in this
  session; verification above is via web-search excerpts of the named official pages.
  The starter-library task re-verifies per-image object pages the same way.
