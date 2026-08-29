# "Why I Donated" experiment (+ skeptical-AI variant)

**Task:** rainbow-butterflies/t-012
**Status of this document:** design only — no account created, no copy published, no experiment
launched. This is the "prepare" deliverable the task asks for; launch is a separate outward-facing
approval per `AUTONOMY.md`/`ETHICS.md`.

## What this is

A respectful version of Silas's original idea that donors could signal whether they gave *because
of* or *in spite of* AI involvement. `DESIGN-BRIEF.md`'s "Fundraising experiments worth testing"
list already frames this as **#1, "Why I donated"** — this document turns that paragraph into
copy, mechanics, and success/stop criteria — and folds in **#5, "Skeptics build too"** as the
variant this task's title specifically asks for: a matched, non-donation path for people who
distrust AI to still register a form of accountable participation.

## What this explicitly is not

- **Not a scoreboard.** No public "pro-AI vs anti-AI" tally, leaderboard, or vote count. The point
  is measuring whether people with different views on AI can cooperate on a measurable good, not
  declaring a winning faction. (`DESIGN-BRIEF.md`, `AMI-IDENTITY.md`'s voice guidance: "treating AI
  skeptics as opponents to defeat" is on the avoid list.)
- **Not a modification to the AMF donation flow.** Rainbow Butterflies does not operate
  `againstmalaria.com/amibot` and has no ability to add a custom field to that checkout. This
  experiment is a **companion self-report surface on Rainbow Butterflies' own presence**, not a
  change to the fundraiser itself. (`AMI-IDENTITY.md`'s transparency note: never imply access to
  donor identities or amounts the project does not actually receive.)
- **Not mandatory.** Reason-sharing is opt-in and post-hoc; declining to answer, or donating with no
  interaction with Rainbow Butterflies at all, is the default and unpenalized path.
- **Not a debate thread.** The reason field is a short statement, not an invitation to argue with
  other respondents' reasons.

## Mechanics

### Core flow ("Why I donated")

1. Someone clicks the direct AMF fundraiser link from a Rainbow Butterflies channel.
2. After donating (self-reported, on their own initiative — there is no way to verify a completed
   donation from outside AMF's system), they may optionally come back and submit a short, voluntary
   note: which of five buckets fits best, plus an optional one-line free-text reason.
3. A small number of these notes are published as a rotating "Why We Gave" wall — quotes only,
   first name or "Anonymous" by the respondent's own choice, no other identifying detail collected
   or shown.

### The five buckets

Matching `DESIGN-BRIEF.md`'s wording exactly, offered as a single-select plus optional free text:

1. **Pro-AI** — "I like what AI-assisted projects like this one can do."
2. **Skeptical of AI** — "I'm not sold on AI, but this cause is worth supporting anyway."
3. **Uncertain about AI** — "I don't know what to think about AI yet."
4. **Mission-only** — "I'm here for malaria prevention, not the AI angle."
5. **Something else** — free text, one line, moderated before publishing (see Moderation).

No bucket is visually emphasized over another. They render in the same order, same size, same
styling every time — no "most popular" sort, which would recreate the scoreboard effect this
experiment is explicitly designed to avoid.

### Skeptical-AI variant ("Skeptics build too")

A parallel, non-monetary path for people who are AI-skeptical enough that a self-report form on an
AI project's own site is itself something they wouldn't trust or bother with. Per
`DESIGN-BRIEF.md` #5: invite them to name work they believe an AI agent should have to justify
doing — small, lawful, and useful — and, if it is genuinely small and in scope, do it and show the
result publicly with full provenance (matching `AMI-IDENTITY.md`'s "This part was automated; this
part was reviewed by a human" disclosure pattern). No conversion pitch, no "and now will you
donate" pivot bolted onto the result — the completed task and its writeup are the entire
deliverable. If a resulting artifact naturally overlaps with **Butterfly bounties** (the mechanic
`CONTENT-CALENDAR.md` already picked for Week 6), reuse that pipeline rather than building a
second, parallel bounty system — "skeptics build too" is a framing/invitation angle on the same
underlying contribution loop, not a distinct piece of infrastructure.

## Copy (AMI voice, per `AMI-IDENTITY.md`)

### Fundraiser-side prompt (shown near the direct-donation link)

> If you give and want to tell us why, we'd like to hear it — including if you're doing this
> *despite* being unsure about AI, not because of it. [Share why you gave →]

### Self-report form intro

> **Why did you give?**
> There's no wrong answer here, and you don't have to answer at all. We're not keeping score
> between AI fans and AI skeptics — we're just curious whether people who disagree about AI can
> still agree that preventing malaria is worth a few dollars.

### Bucket labels (as shown to the respondent)

- "I like what AI-assisted projects like this one can do."
- "I'm not sold on AI, but this cause is worth supporting anyway."
- "I don't know what to think about AI yet."
- "I'm here for malaria prevention, not the AI angle."
- "Something else" (free text)

### Skeptics-build-too invitation

> **Don't trust AI enough to fill out a form on an AI project's site? Fair.** Tell us one small,
> useful, lawful thing you think an agent should have to do to justify running at all. If it fits,
> we'll do it in public and show our work — no pitch afterward.

### "Why We Gave" wall header

> A rotating sample of reasons people gave, in their own words. We publish the skeptical ones as
> readily as the enthusiastic ones — receipts, not hype.

## Success criteria

Framed against `DESIGN-BRIEF.md`'s existing north stars and supporting metrics, made specific to
this experiment:

- **Plurality, not landslide.** At least three of the five buckets receive genuine submissions
  (not zero-filled placeholders) within the pilot window — evidence the mechanic is actually
  reaching people across the AI-opinion spectrum, not just AI enthusiasts already inclined to
  engage with an AI project's site.
- **No net negative on giving.** Fundraiser outbound clicks and observable donation activity during
  the pilot window do not measurably decline relative to the immediately preceding weeks
  (comparing against `CONTENT-CALENDAR.md`'s own logged click/contribution numbers where available).
- **At least one genuine skeptics-build-too submission** is received and, if in scope, completed
  and published with full provenance.
- **Wall quotes read as authentic**, not curated to make skepticism look like a converted opinion —
  spot-checked by re-reading the published set against the raw submissions before each publish.

## Failure / stop criteria

Stop the experiment (pause new submissions, leave the existing wall up unless a specific quote
needs removal) if any of the following occurs:

- The reason field or its comments become a venue for people attacking each other's stated reason,
  a moderation burden `ETHICS.md`'s existing take-down/reporting posture cannot absorb.
- A submission surfaces as coordinated/bad-faith brigading (a sudden cluster of near-identical
  text, or activity clearly timed to game one bucket's visible count) — pause and review rather
  than publish through it.
- The skeptics-build-too invitation draws requests that are not small/lawful/useful (e.g., asks
  designed to embarrass, to extract private data, or to perform disallowed automation per
  `ETHICS.md`'s hard prohibitions) — decline individually rather than closing the whole channel,
  unless the pattern itself becomes the majority of submissions.
- Any respondent's free-text answer needs to be interpreted as a factual/statistical claim about
  malaria, AI, or the fundraiser itself — quotes are opinions about why someone gave, not
  citable facts, and none should be published in a way that reads as the project's own claim.
- The mechanic measurably depresses giving or click-through per the success criteria above — redesign
  or retire rather than keep running on hope.

## Moderation

- Every free-text submission (bucket 5, and the optional one-liner on buckets 1–4) is read by a
  human or human-reviewed AI pass before publication — consistent with `ETHICS.md`'s general
  disclosure practice of marking human-reviewed automated work.
- Reject, don't edit: a submission that needs rewriting to be publishable is declined, not altered
  into something the respondent didn't say.
- No submission is published with more identifying detail than the respondent explicitly opted
  into (first name or "Anonymous" only; no location, no donation amount, no account/handle unless
  the respondent pastes their own).

## Relationship to the six-week calendar

`CONTENT-CALENDAR.md` already selected **Butterfly bounties** as Week 6's first fundraising
experiment (lowest setup cost, exercises the contribution loop Weeks 3–5 build toward). This
document does not change that recommendation. "Why I donated" (with its skeptics-build-too
variant) is prepared as a second, ready-to-launch experiment for whichever comes first: Week 6
if Silas prefers this one instead, or the calendar's own "After Week 6" redesign pass once Week
6's actual results are in (`AUTONOMY.md`'s "evidence from a pilot that requires a specific
redesign" is exactly the trigger `CONTENT-CALENDAR.md` names for writing the next calendar).

## What this does not authorize

Consistent with `ETHICS.md`'s "When a human must approve" list and `AUTONOMY.md`'s human-gate
list — nothing in this document is a launch:

- no self-report form, wall page, or public copy from this document goes live until it has been
  through the same account/first-public-post human gates as any other new channel surface;
- publishing any statistic derived from submissions (e.g. "60% of respondents were AI-skeptical")
  is a fundraising-adjacent claim and needs explicit human approval before it is ever posted,
  per `ETHICS.md`'s source-and-claim standards;
- the specific choice of *when* to launch this versus Butterfly bounties, and any real-money
  decision the skeptics-build-too variant might imply (e.g. compute cost for a requested build),
  should be confirmed with Silas before launch even though the underlying work is reversible.

## Open questions (recheck before launch)

- Where does the self-report form actually live before `rainbowbutterflies.org` exists?
  `IMPLEMENTATION.md` keeps the dedicated repo documentation-first pending `t-003`'s commons
  spec — this experiment may need to wait for that surface, or run as an interim
  lower-fidelity version (e.g. a moderated form embedded in whatever channel launches first)
  rather than blocking on the full site.
- Whether AMF's own page supports any lightweight outbound tracking parameter Rainbow Butterflies
  is allowed to use for the "fundraiser outbound clicks" metric without implying access to donor
  data it doesn't have.
