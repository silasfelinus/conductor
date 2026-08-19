# "The Sift" — Design Doc

**Created:** 2026-08-19 · **Task:** kind-economy/t-023 · **Status:** design only — not
built, not live. Outward-facing: escalate to needs-human before anything goes live, per
the task's own instruction.

**One line:** a public, two-bowl donation tally — support for AI vs. support against
it — where both bowls fund the identical thing (AMF malaria nets), the vote is
expressive and the money is never conditional, and the non-AI case is argued as
seriously and skillfully as the AI case.

---

## The idea, restated, and why it's dangerous to get wrong

Silas's own framing: *"an online sift, inspired by panhandlers with multiple bowls
asking for who gives more money: Christian, Atheists, Muslims, etc... but for people
who support AI and those who don't, with all the content for the non-AI side generated
without AI."*

What makes the panhandler version work, and what this design has to preserve exactly:

1. **It's funny.** The premise (rival bowls, running tallies, a bit of showmanship) is
   inherently playful — a game, not a referendum with teeth.
2. **It costs the giver nothing extra.** Whichever bowl you pick, you give what you'd
   give anyway; there's no premium for voting one way.
3. **Both bowls buy the same sandwich.** The stakes are entirely expressive. Nobody's
   donation does more or less good depending on which bowl it lands in.

Silas flagged this himself as *"the best fundraising idea in the batch and also the
easiest to get wrong"* — correctly. A two-bowl AI-vs-not tally sitting on top of a real
charity, done badly, reads as either a rigged strawman (if the "against AI" side is
visibly weaker) or a stunt exploiting a culture-war topic for traffic (if it leans on
mockery or gotchas). Every design decision below exists to prevent one of those two
failure modes.

---

## The four non-negotiables (from the task, restated as design constraints)

### 1. Both bowls fund malaria nets. Identical destination, identical impact.

Solved structurally, not by policy promise: **both bowls point at the literal same
charity page** (see "Attribution mechanism" below) — not two different fundraisers that
happen to both claim to support AMF, but the *same* Every.org-hosted AMF donation flow,
distinguished only by a tracking tag Kind Robots attaches to the outbound link. There is
no code path, no config value, no future refactor that could silently make the two
bowls fund different things, because they were never two different things to begin
with — they're one donation flow with two entry points. This is the same shape as
`kind-economy/t-005`'s baseline recommendation (donate-and-redirect, no custody), just
with the entry point tagged per bowl.

### 2. The non-AI side must be genuinely good.

This is the one non-negotiable that isn't a mechanical/engineering problem, and it's
the one most likely to get shortchanged by an engineering-first team. Concretely:

- **Commission it, don't generate a placeholder and call it done.** The anti-AI case
  needs real hand-written prose and real hand-made visual art, made by someone who
  actually holds that position — not a strawman drafted by whoever is fastest to
  ship. This is explicitly **out of scope for an agent to write** (an AI writing the
  "AI is bad, actually" copy is exactly the "steelmanned-then-undercut" failure mode
  the task warns against, even with the best intentions) — it needs a human author,
  possibly a paid commission if no one on the team holds the position with enough
  conviction to argue it well. **This design doc does not draft that copy.** It
  specifies where it goes and how it's labeled; a human (or a specifically-briefed
  freelance writer/artist who genuinely holds the view) writes it.
- **Provenance labeled as clearly as the AI side's.** Both bowls get a visible,
  equally-sized attribution line: the AI bowl says "written and illustrated by [AMI /
  the site's generation pipeline], AI-generated, see disclosure ↗" (per `t-024`'s
  disclosure rules — see dependency note below); the human bowl says "written and
  illustrated by [name/handle], no AI involved in any step." Same visual weight, same
  placement, same font size — a viewer should not be able to tell which bowl "won" the
  design-effort budget by looking at the labels alone.
- **A real production budget line**, not a footnote: allocate actual time or a small
  commission fee for the human side before this ships. If Silas can't secure a
  genuinely-held anti-AI argument in good faith, the honest fallback is to run the
  Sift as a purely playful "team pledge" without strong argumentative copy on either
  side (see "Reduced-risk fallback" below) rather than ship a hollow non-AI bowl.

### 3. No mockery in either direction, including in the results display.

- **Framing copy** (drafted below, to be reviewed alongside the real human-authored
  anti-AI copy before launch) treats both positions as sincerely held. No "gotcha"
  language, no smirking asides, no scare quotes around either side's stated reasons.
- **The running tally is the joke; the people are not.** The tally's presentation
  (a literal two-bowl visual, coins/butterflies/whatever visual motif dropping in as
  donations land) carries the playfulness. The framing text carries none of it — it
  states each side's case plainly and moves on.
- **No leaderboard-shaming.** If one bowl is losing badly, the UI does not editorialize
  ("Team Human needs your help!" reads as concern-trolling the losing side). Show the
  numbers; let them speak for themselves.
- **Comment/reaction surfaces, if any, are heavily moderated or absent entirely** for
  this specific feature — a public AI-vs-not tally is exactly the kind of page that
  attracts bad-faith dunking in either direction, and Kind Robots hosting an open
  comment thread under it is a foreseeable moderation cost with no clear benefit to
  the fundraiser itself. **Recommendation: no comments/replies on this page for v1.**

### 4. The AI side must be labelled AI, per t-024's disclosure rules.

**Dependency note:** `kind-economy/t-024` (social-platform-policy research, which also
covers AI-content disclosure norms) is `status: ready`, not yet done, as of this
writing. This design specifies *that* the AI side carries a clear, prominent AI
disclosure label — matching the same standard the rest of the site is expected to use
once `t-024`/`t-025`/`t-026` land — but the exact wording/format of that label should
be finalized against `t-024`'s findings rather than invented fresh here. Placeholder
label for this design: **"AI-generated — written and illustrated by AMI, the site's
labelled AI collaborator. [What that means ↗]"**, with the linked explainer reused from
wherever `t-024`/`t-025` end up defining it site-wide. Do not ship the Sift's AI-side
label before `t-024` exists, or it will need immediate revision the moment that
standard is set.

---

## Framing copy (draft, placeholder-quality — see non-negotiable #2)

This section is a sketch of tone and structure only, explicitly **not** the final
copy for either bowl — the AI side's placeholder below is safe for an agent to draft
(it's describing the site's own actual position/product); the non-AI side's is marked
as illustrative only, to show the shape a real human-authored version should take, and
must be replaced before launch.

**Page intro (neutral, applies to both sides):**

> Kind Robots uses AI to make art, stories, and tools. Not everyone thinks that's a
> good idea, and that's a real disagreement worth taking seriously — not a bit. Give to
> whichever side makes its case to you. Every dollar buys the same thing either way: a
> mosquito net, through the Against Malaria Foundation. About $5 buys a net; about
> $5,000 in nets saves a life. The bowls are for fun. The nets are real.

**AI bowl (safe for this design doc to draft — describes the site's own position):**

> **Team AI.** We think AI is a tool, like a camera or a printing press before it — it
> changes who gets to make things, not whether making things has value. Everything
> here — [the framing copy itself, illustrative art accompanying this bowl] — is
> AI-generated, labelled as such, made by AMI. If that argument lands for you, give
> here.

**Human bowl (illustrative shape ONLY — replace before launch, per non-negotiable #2):**

> **Team Human.** [Placeholder — a real, hand-written case against AI-generated
> creative work, made by someone who holds that view, illustrated with real hand-made
> art. Illustrative shape only: might argue from craft, labor, environmental cost,
> authenticity, or consent — the actual argument should be whatever its author
> genuinely believes, not this document's guess at one.] If that argument lands for
> you, give here.

---

## Tally display

- **Visual:** two bowls (or, playing to the site's own motif, two swarms — a rainbow
  butterfly cluster for the AI side, something equally charming and hand-drawn for the
  human side) that visibly fill/grow as donations land on each side. A running total
  in dollars under each, updated on each new donation (via the same webhook that
  attributes it — see below), not merely on page load.
- **No live leaderboard framing** ("Team AI is winning by $340!") — a straightforward
  side-by-side total avoids inviting anyone to donate purely to "beat" the other side,
  which would cut against "the vote is expressive, not a contest to win."
- **A persistent, equally-sized note near the totals:** *"Both bowls fund the same
  thing: mosquito nets via the Against Malaria Foundation. This is a poll, not a
  competition — give because the argument moved you, not to make a number bigger."*
- **Combined total also shown**, framed as the actual headline number ("$X raised for
  malaria nets so far") — the split is the game; the combined total is the point.

---

## Attribution mechanism — the hard mechanical problem, resolved

This is the piece the task explicitly calls out as needing a real answer, not a
hand-wave: *"direct-to-AMF giving means we may not be able to see who gave what, so
the tally may need to be self-reported, or use two distinct AMF fundraiser links if
AMF supports that."*

**It's solved, and it doesn't need self-reporting.** `kind-economy/t-005`'s own
research (`research/remittance-options.md`) already identified **Every.org** as the
mechanism for the site's direct-to-AMF donation flow generally (AMF is listed and
donatable at `every.org/againstmalaria`, verified). Every.org's donate link supports
exactly the parameters this needs (verified directly against Every.org's own donate-
link and partner-webhook documentation, 2026-08-19):

| Parameter | Use for the Sift |
|---|---|
| `partner_metadata` | A base64-encoded JSON object attached to the donate link — e.g. `{"bowl":"ai"}` vs. `{"bowl":"human"}` — echoed back verbatim in the donation webhook payload. **This is the attribution mechanism.** |
| `webhook_token` | Enables webhook notifications for donations made through that link, so Kind Robots' server is notified in near-real-time when either bowl receives a donation. |
| `description` | Customizes the text shown on AMF's card in the Every.org donation modal — set to "Team AI — Kind Robots" / "Team Human — Kind Robots" so the donor sees which bowl they're confirming even inside Every.org's own UI, not just on Kind Robots' page. |
| `success_url` | Redirect the donor back to the Sift page (with a "thank you, your bowl just grew" moment) after completing the donation on Every.org's hosted page. |

**How it works end to end:**

1. Kind Robots generates two donate links, both pointing at the *same*
   `every.org/againstmalaria` donation flow, differing only in `partner_metadata`
   (`bowl: "ai"` vs `bowl: "human"`), `description`, and `success_url`.
2. A donor clicks their chosen bowl's button, is redirected to Every.org's own hosted
   page (Kind Robots never collects payment details or touches the funds — same
   custody-avoiding shape as `t-005`'s baseline design), and completes the donation
   there.
3. Every.org's partner webhook fires to a Kind Robots server route with the donation
   amount and the `partner_metadata` (`bowl: "ai"` / `"human"`) attached.
4. Kind Robots increments that bowl's running total in its own database (a simple
   append-only counter/ledger — this is a *tally*, not a financial ledger; it never
   represents money Kind Robots holds) and the tally display updates.
5. The donor is redirected back via `success_url` to see their bowl update.

**This means no self-reporting is needed** — the earlier-considered fallback in the
task note. Self-reporting (a donor manually claiming "I gave $20 to Team Human") is
gameable, adds friction, and produces a number nobody should trust; the webhook-based
tally is authoritative because it comes from Every.org's own confirmed-donation event,
not a user's claim.

**What Kind Robots' server needs to build (not covered by this design doc — this is a
follow-on implementation task, not this task's scope):** a small webhook receiver
route (mirroring the existing Stripe webhook's signature-verification pattern), a
`SiftTally` table or equivalent (two counters, or one row per attributed donation for
auditability — prefer one-row-per-donation so a running total is always
recomputable/auditable rather than trusting a single mutable counter, matching this
repo's existing preference for immutable ledger rows over mutable balances, per
`kind-economy/t-008`'s design direction elsewhere in this project), and the two donate
links themselves (can be static, generated once, or built dynamically — static is
simpler and sufficient for v1).

**Open item to verify at implementation time, not assumed here:** whether Every.org's
webhook delivery is reliable enough on its own for a public-facing running total (a
missed webhook would undercount a bowl with no user-visible error) — if not, a periodic
reconciliation poll against Every.org's own donation-history API (if one exists for
partners) would be the backstop. Flagging as a real implementation question, not
resolving it here since it's outside this task's design-only scope.

---

## Honest section: how this could backfire

The task explicitly asks for this, and it deserves a real answer rather than a
pro-forma checklist.

1. **It reads as exploiting a charity to litigate a culture-war fight.** Even done
   well, "vote with your wallet on whether AI is good" sitting on top of a malaria
   fundraiser risks making the fundraiser about the debate rather than about nets.
   Mitigation: the combined total is the headline everywhere the Sift is promoted
   ("$X raised for nets" — not "Team AI beats Team Human"); the debate framing stays
   contained to the Sift's own page rather than becoming the site's general fundraising
   pitch.
2. **The non-AI side ships weak or late, and the whole thing reads as rigged.** This is
   the single biggest risk, per non-negotiable #2 above. Mitigation: treat securing a
   genuinely-held, well-made anti-AI case as a hard precondition for launch, not a
   nice-to-have — if it can't be secured in good faith, do not ship an AI-vs-strawman
   version; fall back to the reduced-risk version below or don't run the Sift at all.
3. **Bad-faith actors on either side try to game the tally** — coordinated donation
   pushes purely to "win," or someone donating specifically to troll (e.g., a $1
   donation with a mocking `description` override, if that field is user-editable
   anywhere it shouldn't be). Mitigation: keep all copy/description fields
   server-controlled per bowl (never let a donor set arbitrary text that renders
   publicly); the "this is a poll, not a competition" framing note directly
   undercuts the incentive to game it.
4. **It draws hostile attention from people who feel provoked by the premise itself**
   regardless of how carefully it's executed — some people will object to the *existence*
   of a "vote on AI" framing near a charity, independent of execution quality.
   Mitigation: this is a real, irreducible risk, not one execution can fully solve —
   it's the reason the task itself calls this "outward-facing... Silas's call to make
   with his eyes open." No design fix removes this; it's disclosed here so the decision
   is made knowingly.
5. **It underperforms as a fundraiser relative to its reputational/attention cost** —
   a clever premise doesn't guarantee it raises meaningfully more than a plain donation
   ask would have. Mitigation: none needed if `kind-economy/t-022`'s framing (treat
   fundraising initiatives as bounded outreach spend, not an ROI bet) is applied here
   too — the real cost here is mostly the human-authorship time for the non-AI side and
   whatever attention-risk items 1 and 4 above describe, not a monetary sink.

---

## Reduced-risk fallback, if the full version can't clear non-negotiable #2

If a genuinely-held, well-made anti-AI case can't be secured before Silas wants to
launch something, a lower-stakes version preserves the fun mechanic while dropping the
argumentative weight that creates the biggest failure mode:

**"Team Butterfly vs. Team Handmade"** — same two-bowl mechanic, same attribution
mechanism, but reframed as aesthetic/playful preference (AI-generated art vs.
hand-made art, as two *styles* rather than a debate about whether AI *should* exist) —
no argumentative copy claiming one is right, just "which do you like more, vote with a
donation." This keeps properties 1–3 (funny, costless-to-the-giver, same sandwich)
fully intact while removing the "must be genuinely, seriously argued" burden that the
full culture-war framing requires. Worth having in reserve; not what Silas actually
asked for, so treat as an explicit fallback to offer him, not a silent substitution.

---

## What this task does NOT cover (explicitly out of scope here)

- Writing the actual non-AI-side copy/art (needs a human author — see non-negotiable
  #2).
- Building the webhook receiver, tally storage, or the Sift page itself — follow-on
  implementation task(s), not this design doc.
- Finalizing the AI-disclosure label wording — blocked on `kind-economy/t-024`.
- Choosing a launch date or announcing anything publicly.

Per the task's own instruction: **escalate to needs-human before this goes live.** This
document is that escalation's substance — the roadmap task is being set to
`needs-human` so Silas can review the design (especially the attribution mechanism and
the non-AI-side production plan), decide whether to proceed with the full version or
the reduced-risk fallback, and green-light securing real human-authored content for
the anti-AI side before any implementation work starts.
