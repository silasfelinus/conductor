# mermaidsofvenice.com Site Plan

## Purpose

Build a focused, reader-facing home for *Mermaids of Venice* that helps a curious visitor understand the book, sample its voice, and reach the approved purchase path without turning the site into a sprawling author platform.

This document is a plan only. It does not authorize DNS changes, hosting changes, publication, payment setup, analytics, mailing-list enrollment, or any other outward-facing action.

## Product promise

The site should answer five questions quickly:

1. What is *Mermaids of Venice*?
2. Why might I enjoy it?
3. Who wrote it, and what is the real-world story behind it?
4. Where can I read a safe sample or learn more?
5. How can I buy or access the approved edition?

The experience should feel theatrical, intimate, strange, and human. It should not feel like a generic fantasy template, an AI showcase, or a cluttered publishing portal.

## Recommended v1 information architecture

### 1. Home

A single strong landing page with:

- Book title, cover, concise positioning line, and one clear primary action.
- A short synopsis that does not over-explain the plot.
- Silas's personal note, written by Silas.
- The existing no-AI authorship note, preserving its intended joke and distinction between editorial assistance and authored prose.
- A compact section on the street-performance roots of the novel.
- Two or three short, approved review excerpts.
- A footer containing contact, rights, accessibility, and privacy links.

### 2. About the Book

A slightly deeper page for readers who want context before buying:

- Full synopsis.
- Genre and tone signals.
- Major themes without spoilers.
- Edition information.
- Content guidance where appropriate.
- A clear statement that the prose was written by Silas, with AI limited to editorial support where disclosed.

### 3. About Silas

A concise biography centered on the material relevant to the book:

- Street performance in Europe.
- Glasswalking, acrobatics, geek acts, and fire juggling.
- The relationship between lived experience and the novel.
- A restrained author photo and optional archival performance image gallery.

This page should not become a complete personal-history archive.

### 4. Read a Sample

A human-approved excerpt delivered as accessible HTML or a downloadable PDF.

Requirements:

- Silas selects the exact excerpt.
- The sample must not expose unpublished edition-three text accidentally.
- Typography should prioritize long-form reading rather than decorative effects.
- The page should include a clear route back to the purchase path.

### 5. Reviews and Reader Reactions

A curated page containing only excerpts Silas approves for public use.

Potential sources:

- Conventional reader reviews.
- Character or bot reviews, clearly labeled as fictional in-character responses rather than real customer testimonials.
- Editorial praise, only with permission and accurate attribution.

Do not publish private editorial notes, cultural-awareness notes, manuscript diagnostics, or internal guest-reader material by default.

### 6. Buy / Get the Book

The purchase page should be intentionally simple:

- Current approved edition and format.
- Price.
- Delivery expectations for digital purchases.
- Refund and support information.
- A single primary checkout route.

The existing Kind Robots digital-storefront work should remain the first candidate for fulfillment. Do not create a second commerce system merely because this site has its own domain.

### 7. Rights and Creative Reuse

Publish the final approved reuse language for *Mermaids of Venice* in a stable, linkable location.

The page should clearly separate:

- Permission to copy and share the book itself under the approved conditions.
- Permission for independent human creators to use characters, settings, relationships, and ideas.
- Restrictions on charging for the book itself or commercially exploiting a substantially complete copy.
- The preferred but not mandatory credit language.

The final wording must come from Silas's approved text, not an agent's legal improvisation.

## Content inventory

### Ready or nearly ready

- Existing Kind Robots landing-page structure.
- Book title and project identity.
- Second-edition PDF as the currently identified sellable text, subject to Silas's final edition decision.
- Author background from the project's existing materials.
- Draft reuse statement supplied by Silas.

### Human-supplied before launch

- Final personal note.
- Final synopsis and positioning line approval.
- Final cover file and preferred author image.
- Exact sample excerpt.
- Final edition file and price.
- Approved public review excerpts.
- Support/contact address.
- Final rights language.

## Visual direction

Use the book's actual atmosphere rather than nautical clip-art shorthand.

Recommended qualities:

- Warm theatrical darkness with readable high-contrast text.
- Venetian and street-performance texture used sparingly.
- Rich but controlled typography.
- Small moments of spectacle around section transitions, never at the expense of reading.
- Mobile-first layouts with no ornamental element allowed to compress or obscure primary content.

Avoid:

- Mermaid-stock-photo collage aesthetics.
- Heavy parallax or autoplay animation.
- Faux-aged body text.
- AI-generated character art presented as canonical book illustration without explicit approval.
- A crowded navigation tree.

## Technical recommendation

### Preferred architecture

Use a small static or statically generated site in a roadmap-owned repository, or a dedicated surface within the existing Kind Robots deployment if Silas prefers one codebase. The deciding factor should be operational simplicity, not novelty.

The site should consume or link to the existing Kind Robots commerce path rather than duplicate checkout, customer records, file delivery, or entitlement logic.

### Baseline requirements

- Responsive, accessible HTML.
- Semantic heading structure and keyboard navigation.
- Optimized local images with explicit dimensions.
- Open Graph and standard metadata.
- Sitemap and robots configuration.
- No third-party analytics by default.
- No cookie banner unless a selected service actually requires one.
- No secrets in the client bundle.
- A simple deployment rollback path.

## Delivery phases

### Phase 1: Content-complete private preview

Build the full page structure with placeholders clearly marked for Silas-owned copy and assets. Use no production DNS and no public announcement.

Exit criteria:

- All routes work in preview.
- Mobile and desktop layouts are verified.
- Accessibility checks pass.
- No placeholder is capable of being mistaken for final copy.
- Purchase links point only to a safe preview or remain disabled.

### Phase 2: Commerce and edition verification

Connect the approved edition to the existing storefront and verify the full purchase-and-delivery path using test mode or a non-billable internal path.

Exit criteria:

- Correct file, edition label, price, and fulfillment behavior are verified.
- Support and refund language are present.
- No live charge occurs without explicit approval.

### Phase 3: Launch readiness

Replace all placeholders, complete metadata, verify links, and prepare the domain transition plan.

Exit criteria:

- Silas has approved every public-facing page.
- Rights wording is final.
- The public sample is final.
- Production purchase flow is explicitly approved.
- DNS, hosting, redirects, and rollback steps are documented.

### Phase 4: Public launch

Human-gated actions only:

- DNS changes.
- Production deployment or domain attachment.
- Enabling live payments.
- Publishing announcements or social posts.
- Sending email.

## Acceptance checklist for the implementation task

A future build task is ready only when it specifies:

- The owning repository and deployment target.
- The approved page list.
- The source of truth for book files and cover assets.
- The commerce integration point.
- The exact preview and launch gates.
- Visual verification at mobile, tablet, and desktop widths.
- Required tests and rollback procedure.

## Recommended next task

Create the private preview implementation using this plan, preserving explicit placeholders for Silas-owned text and assets. Open a PR and preview deployment, but do not attach the production domain, enable live checkout, or publish the site without separate concrete approval.
