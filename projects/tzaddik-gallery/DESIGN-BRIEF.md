# Tzaddik Gallery — Design Brief

## Premise

Tzaddik Gallery is a playful Kind Robots pop-culture database built around the
folkloric idea of 36 righteous people whose existence keeps the world going.
Here, "tzaddik" is deliberately used as a whimsical editorial label for a "just
person": someone whose work, courage, generosity, creativity, public service, or
moral example makes the world feel more habitable.

It is **not** a Jewish religious classification project. A person's religion,
ethnicity, or relationship to Hasidism is neither a requirement nor a selection
criterion. The explanation page should acknowledge the concept being borrowed,
avoid pretending the site's game is authoritative theology, and invite curious
readers to learn more from reliable sources.

## Core product

The feature has three top-level views:

1. **Current 36** — living people currently in the playful canonical set.
2. **Past Tzaddik** — historical/deceased people retained as an educational
   gallery rather than disappearing when they leave the living set.
3. **About the 36** — explains the conceit, editorial philosophy, sourcing, and
   the distinction between community reactions and canonical selection.

Every person gets an image-forward card and a detail page. The detail page
contains a concise sourced biography, the reason they are being proposed,
Wikipedia/Wikimedia provenance, submitter attribution where relevant, community
reaction totals, and a clearly visible **controversy / objections** section.

The controversy section is a guardrail against accidental hagiography, not an
obligation to fabricate a "both sides" paragraph. Include meaningful,
well-sourced objections, disputes, or harms when they exist. When nothing
substantial is documented, say less.

## Large-screen single-page interface

On `lg` and `xl` widths, Tzaddik Gallery should feel like one composed
application screen rather than a long document. The primary navigation switches
between **Living**, **Memorial**, and **Info** without throwing the user into
different visual worlds.

The person/submission view is also a single viewport composition:

- one dominant large portrait/image;
- atmospheric project art or person-derived background treatment behind the
  interface, with contrast controls so text remains readable;
- name, compact bio, source/provenance, and "why this person" pitch visible
  without page scrolling;
- a distinct controversies/objections panel;
- review controls for the current user (vote plus approve/reject/defer where
  authorized);
- comments in their own internally scrollable region so a long discussion does
  not make the whole desktop page grow forever;
- clear previous/next/back-to-gallery navigation without losing the current
  Living/Memorial context.

Treat the viewport as a layout budget. On desktop, page-level vertical scrolling
should be the exception, not the default. Panels that can overflow should own
their scroll behavior deliberately.

For `sm` and `md`, abandon the viewport-lock requirement. Stack the same
information into a conventional readable vertical page with sticky or compact
navigation where useful. Do not shrink the desktop composition until it becomes
a tiny dashboard.

## Community mechanics

Authenticated Kind Robots users can submit a candidate and react to candidates
with an upvote or downvote. Reactions are community signal, not automatic
membership. New submissions enter a pending/community pool. Editors/admins can
approve, archive, correct, or promote records.

The initial canonical 36 is an editorial selection. Silas gets the human gate on
the first set. Future promotion/demotion mechanics can evolve after the core
experience proves itself.

## Sources and overrides

Wikipedia is the default biographical source. Wikimedia/Wikipedia images are the
default image source when usable. Each record should retain machine-readable
source provenance.

Editors may override display copy or imagery, but the override must be explicit
and must not erase the original source. The UI should be able to communicate
where the displayed content came from.

The implementation should fetch/refresh source data through a controlled server
path rather than trusting arbitrary client URLs. Cache enough normalized source
data that the gallery is not hostage to a Wikipedia request on every page load.

## Community correction / source recheck

Every person detail page should expose a clearly visible **Request recheck**
control. This is not a free-form edit button. It asks the server to re-fetch
the record's canonical Wikipedia/Wikimedia sources and compare the latest
source-derived facts against the stored snapshot.

A recheck should cover, at minimum:

- living/deceased status and death date when applicable;
- current lead/biographical summary used by the gallery;
- Wikipedia article identity / redirects;
- Wikimedia image and license/provenance metadata;
- other normalized source-derived fields used by the person card/detail page.

The request should be attributable to the signed-in user, deduplicated/cooldown
protected, and auditable. Store the Wikipedia revision/source timestamp used for
the comparison so editors can see *what changed since what*.

When the fresh source clearly changes an ordinary source-derived field, update
that field and record the refresh. A verified death/living-state change must
also move the person between Living and Memorial as appropriate instead of
leaving a stale gallery classification.

Explicit editor overrides are protected: a Wikipedia refresh must never silently
overwrite intentionally overridden copy or imagery. If fresh source data
conflicts with an override, surface the diff for editor review while preserving
both the source value and override provenance.

A failed or ambiguous refresh should produce a visible review state rather than
silently claiming the record is current. The button should communicate recent
refresh state, for example "checked 2 days ago" or "recheck requested", so users
do not repeatedly hammer the same source.

## Initial seeds

Initial gallery membership is now tracked concretely in `seed-sets.yaml`.
Silas accepted the full 2026-09-26 discovery docket plus his direct nominations
into the first gallery data set.

Direct Silas nominations currently include:

- Living: Cassandra Peterson / Elvira; Greta Thunberg.
- Memorial: Dolly Parton; Steve Irwin; Fred Rogers; Martin Luther King Jr.;
  Stanislav Petrov; Nelson Mandela; Harriet Tubman.

The first LLM discovery batch is also accepted into the initial gallery set.
This seed acceptance does not by itself define the final canonical living 36.

Current living status and source metadata must be verified when records are
actually ingested, rather than assumed from this planning document.

## Tags and browsing taxonomy

People can carry multiple editorial tags. Tags describe *how* a person's work or
public contribution is relevant; they are not scores, rankings, identities, or
political endorsements.

Start with this controlled tag set:

- **Politics** — elected office, public administration, legislation, statecraft,
  or sustained political leadership that is materially relevant to the person's
  case for inclusion.
- **Pop Culture** — entertainment, celebrity, television, film, music, sports,
  or other mass-cultural work where public visibility is part of the story.
- **Humanitarian** — disaster relief, poverty relief, refugee support, food,
  shelter, emergency response, or large-scale direct human aid.
- **Science & Medicine** — scientific discovery, engineering, medicine, public
  health, or technical work with strong human benefit.
- **Education** — teaching, schools, literacy, mentorship, educational access,
  or institution-building around learning.
- **Environment** — conservation, climate, ecology, biodiversity, land/water
  protection, or environmental restoration.
- **Civil Rights & Justice** — human rights, anti-discrimination work, legal
  equality, labor rights, criminal-justice reform, or related justice work.
- **Peace & Diplomacy** — conflict prevention, reconciliation, diplomacy,
  nonviolent peacebuilding, arms-risk reduction, or international mediation.
- **Community & Mutual Aid** — durable local care networks, neighborhood or
  grassroots support, social services, or community institutions.
- **Arts & Culture** — artistic or cultural work whose significance goes beyond
  ordinary celebrity and forms part of the inclusion case.
- **Journalism & Truth** — journalism, documentation, whistleblowing,
  fact-finding, public-interest information, or preservation of historical
  truth.
- **Courage & Rescue** — concrete acts of rescue, refusal, witness, protection,
  or personal risk where a specific intervention changed outcomes.

Tags are multi-select and should remain relatively broad. Do not force a person
into one primary category when their contribution spans several domains.

Geography should be modeled separately as structured country/region metadata,
not as tags. Likewise, living/memorial state is a core record status rather than
a tag.

The gallery should support filtering by one or more tags and show tags on cards
and person detail pages. The Daily Tzaddik discovery process should also assign
provisional tags so the review queue can reveal overconcentration, for example
too much Pop Culture and too little Science & Medicine or Community & Mutual
Aid.

Editors may add new controlled tags when a repeated category genuinely fails to
fit the existing set. Avoid one-off micro-tags that turn browsing into taxonomy
confetti.

## Daily discovery roster

Tzaddik Gallery has an ongoing discovery lane inspired by Daily Dream. Once the
core data model and review surfaces exist, each Pacific day the system prepares
**20 sourced suggestions: 10 living and 10 deceased**.

Each suggestion includes:

- a compact biography;
- a short editorial pitch for why the person merits consideration;
- Wikipedia/Wikimedia source and image provenance;
- verified living/deceased status;
- meaningful objections or controversies when documented;
- enough region/field context to notice when the pool is drifting back toward
  familiar US/Anglosphere celebrity names;
- dedupe state against canonical, historical, pending, rejected, deferred, and
  recently suggested people.

This daily roster is explicitly **human-vetted**. Silas may approve, reject,
defer, or investigate a suggestion. LLM research does not automatically add a
person to the canonical 36 or historical gallery. Rejected people should not
immediately boomerang back into tomorrow's docket.

After the finite gallery build is accepted, this daily research/review loop is
the reason the Conductor project should transition from `active` to
`continuous` rather than being marked finished.

## Escaping the Anglosphere gravity well

International breadth is a core editorial feature, not polish. Candidate
research should deliberately look beyond famous US/UK media figures and include
people whose impact is primarily known within Africa, Asia, Latin America, the
Middle East, Oceania, Indigenous communities, and non-English-language public
spheres.

Breadth should span kinds of contribution too: disaster response, medicine,
science, education, labor, human rights, conservation, journalism, civic
infrastructure, mutual aid, arts, diplomacy, and stubborn acts of courage that
changed outcomes.

The goal is discovery, not a geography quota. Each candidate still needs a
specific, sourced case for inclusion.

## Product tone

Warm, slightly absurd, image-forward, and educational. The site should be able
to say "these 36 people are keeping the world running" with a straight enough
face to make the joke work, while the sourcing underneath is serious.

Avoid saintly visual language, halos, religious costume shorthand, or
pseudo-Hasidic aesthetics. The design belongs to Kind Robots and pop-culture
gallery language, not cosplay of a living religion.

## Moderation and safety

- Only authenticated users submit/react.
- Submission does not equal canonical membership.
- Admin/editor actions are auditable.
- Person records must distinguish sourced fact, editorial rationale, community
  reaction, and objections.
- Biographical claims and controversies should be source-backed.
- Do not infer sensitive identity attributes beyond what reliable public
  sources explicitly establish and what is actually relevant.
- Wikipedia being the default source does not make it infallible; overrides and
  editorial review exist for a reason.

## Definition of done

The finite build milestone is done when Kind Robots has a polished responsive
current-36 gallery, historical gallery, concept page, sourced person detail
pages, authenticated submissions/reactions, admin moderation and source
overrides, an internationally researched seed pool, an accepted initial living
36, a working daily 10-living + 10-deceased human-vetted discovery docket, and
verified phone/tablet/desktop visual quality. After that acceptance, the project
continues as a low-priority continuous discovery program.