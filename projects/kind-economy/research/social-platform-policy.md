# Where AMI can post — social platform policy review

**Task:** `kind-economy/t-024`. Research and recommendation only. No account created, no API
key requested, no post made, no platform contacted. This document is prerequisite research
for `t-025` (building an AI posting pipeline for AMI, a labelled AI character posting on
behalf of Kind Robots) — it exists to determine what that pipeline is allowed to be, before
any pipeline is built.

## The question this answers

AMI will be a **labelled AI account** that posts on Kind Robots' behalf and, per the project's
mission, will sometimes link to an AMF (Against Malaria Foundation) donation ask. For each of
eight candidate platforms, this reviews: (1) the AI-content disclosure rule and whether a
first-class platform label exists, (2) automated/API posting and bot-account rules, (3)
whether a charitable-fundraising link triggers extra rules, and (4) rate/volume limits. Reddit
and Discord get a fifth item: a flag that community-level rules, which this research cannot
evaluate in the abstract, are where actual bot bans happen.

**A note on sourcing.** Every claim below was checked against a live fetch of the platform's
own policy page where the page was reachable. Several platforms' help centers (`help.x.com`,
`support.reddithelp.com`, `support.discord.com`, `support-dev.discord.com`) return HTTP 403 to
automated fetches — presumably deliberate bot-blocking, which is itself a small, ironic data
point about how these platforms treat automated traffic. Where a page could not be fetched
directly, findings are sourced from search results that themselves quote the official page,
and the platform's own URL is still cited so it can be checked by hand. Those cases are marked
**(indirect)** below. Nothing here is from memory alone — every item has a live citation.

## Summary comparison

| Platform | First-class AI-content label | Bot account disclosure required | Fundraising-link friction | Rate/volume limit (bot-relevant) | Overall for a labelled AI bot |
|---|---|---|---|---|---|
| **Bluesky** | No official one; AI-image labeling is a third-party, opt-in "labeler" service, not built into the base app | Yes — official "Automated" self-label exists and is recommended | None found in ToS/guidelines | 1,666 posts/hour, 11,666/day (points-based) | **Best starting point** — automation is explicitly supported, self-labeling is a first-class feature, no fundraising-specific rule found |
| **Mastodon** | No universal one — decentralized, varies by instance. The widely-adopted default Community Standards require "transparency" about generative-AI content and **ban accounts that primarily or exclusively post AI content** | Not required by protocol; instance-dependent | None found | Default: 300 API calls/5 min; 30 posts-adjacent calls/30 min (varies by instance) | **Workable but risky** — the "primarily AI-generated content" prohibition on the default/flagship rule template is a direct hit if adopted by the chosen instance; instance selection matters a lot |
| **Instagram** | Yes — Meta's "AI info" label (formerly "Made with AI"), with a self-disclosure toggle plus automatic Content Credentials/C2PA detection | No explicit bot-disclosure rule found; standard Meta Platform Terms require app review for API access | Native nonprofit fundraiser tools are for the nonprofit/eligible-country orgs only — a third party can only plain-link, no special enforcement found but also no confirmation it's risk-free | 100 API-published posts/24 hr (rolling window); ~200 Business-Use-Case calls/user/hour | **Good — has the clearest first-class label**, but full API access requires Meta App Review |
| **TikTok** | Yes — explicit "AI-generated content" toggle/label ("Disclosed by creator as AI-generated"), required for realistic AI content, TikTok also auto-labels via detection | Yes, indirectly — "unaudited" API clients are restricted to private-only posting until TikTok audits the client; bulk/automated account *creation* is explicitly banned | Native donation stickers require TikTok+Tiltify approval; plain bio/description links are themselves restricted to verified business accounts or selected creators | Posting-specific limits not published in the general rate-limit doc; general API calls ~600/min per endpoint; unaudited clients can't reach public feeds at all | **Hardest to bootstrap** — content posting API requires a TikTok audit before content is even publicly visible, and link placement is separately gated |
| **YouTube** | Yes — official AI-disclosure checkbox at upload; labels appear in-player for photorealistic content, in description for other AI content | No explicit "bot must self-identify" rule found, but ToS bars unauthorized automated access outside the official API, and API Terms require compliance audits | YouTube Giving (native donate button) requires channel eligibility; ineligible channels can link out via End Screens to an approved list of third-party fundraising sites; plain description links appear unrestricted but no explicit charity carve-out found | `videos.insert` capped at 100 calls/day in its own quota bucket, inside a 10,000-unit/day default project quota | **Good** — has a first-class disclosure flow, but a strict low-volume (~100/day cap, likely far lower in practice since each upload also costs quota units) daily upload ceiling by default |
| **X (Twitter)** | Very new, not yet confirmed mandatory — a "Made with AI" self-disclosure toggle began rolling out ~March 2026, alongside an older, narrower auto-detected "Manipulated Media" tag for deceptive edits specifically. **(indirect)** | Yes — official "Automated account" label is required for bot accounts (help.x.com/en/using-x/automated-account-labels), must link to a human-run operator account. **(indirect, page 403'd to direct fetch)** | No specific charitable-solicitation rule found; general scam/crypto crackdown (auto-locking first-time crypto posts) is adjacent but not about donation links per se | As of Feb 2026, X moved from tiered free/paid plans to pay-per-use pricing for new developers: no free tier, $0.015 per post created, +$0.20 if it contains a URL — this is a real, non-trivial per-post *cost*, not just a rate limit, for anyone posting links (which AMI's donation-linked posts would do) | **Usable but now has a real dollar cost per post with a link** — the automated-label requirement is well-established, but Feb 2026's pricing overhaul means posting a donation link costs money per post, unlike any other platform reviewed here |
| **Reddit** | No general platform-wide AI label; Reddit's Content Policy allows AI-generated content generally and leaves disclosure/restriction to individual subreddits. Reddit's *advertiser* rules do require AI-ad disclosure, but that's ads, not organic bot posts. **(indirect)** | Yes — the "Responsible Builder Policy" explicitly covers "apps, bots, AI agents, or non-human operated accounts," requires app registration and a public "App profile label" that must not be circumvented. **(indirect, page 403'd to direct fetch)** | No fundraising-specific rule found at the site-wide level; the general anti-spam Content Policy Rule 2 ("authentic content... do not cheat or engage in content manipulation") is what would catch a link-heavy bot regardless of the link's charitable purpose | 100 queries/min (free tier, per OAuth client) for the Data API; commercial-scale use requires a paid tier (reportedly ~$12k/yr for "Standard") | **Site-wide policy is workable, but see community-override note below — this is the platform where the site-wide answer matters least in practice** |
| **Discord** | No content-level AI label at all — Discord's Community Guidelines address AI only narrowly (synthetic CSAM under Rule 6), not general AI-content disclosure | Yes, strongly — Rule 14 explicitly bans "self-bots/user-bots" outside the official bot-account path: "Each account must be associated with a human, not a bot" (i.e., use the bot-account API path, not a human account driven by a script); bots also require Discord "Verification" once they join 100+ servers | Discord's *paid-ads* Monetization/Ads Policy requires fundraising solicitation to come only from tax-exempt orgs with the tax status disclosed; no equivalent site-wide rule found for organic server posts, but see community-override note below | Global API limit: 50 requests/sec per bot token (some bots can request an increase to 1,200/sec) | **Workable at the API level, but see community-override note below — same caveat as Reddit** |

## 1. Bluesky

**AI-generated content policy and labels.** Bluesky's [Terms of Service](https://bsky.social/about/support/tos)
do not mention AI-generated content, disclosure, or labeling at all. The
[Community Guidelines](https://bsky.social/about/support/community-guidelines) mention
"synthetic" media only in the context of CSAM and non-consensual intimate imagery
prohibitions — there is no general-purpose AI-content disclosure rule. Bluesky does have an
**AI Imagery Labeler**, but it is a third-party, opt-in "labeler" service in Bluesky's
composable-moderation system (users choose which of up to 20 labelers to subscribe to), not a
built-in platform label the way Meta's or TikTok's are. **Conclusion: no first-class,
mandatory AI-content label exists on Bluesky today** — a hand-written disclosure in the post
text or profile is the practical option.

**Automated/API posting and bot accounts.** Bluesky explicitly supports bot accounts and
provides official starter guidance for building them (docs at `docs.bsky.app` /
`bsky.network`, both redirecting to the same content). Best practice, confirmed via the app
itself and documentation search: bot operators should apply the official **"Automated"
self-label** to their account profile, which is a first-class, built-in labeling option (not
third-party) distinct from the AI-content labeler above. The Community Guidelines prohibit
abusive automation specifically — "automated harassment systems," "single-purpose harassment
accounts" — and require that bot interactions (likes/replies) be opt-in via user tagging to
avoid being treated as spam. No API-tier/app-review gate comparable to Meta's or TikTok's was
found; Bluesky's API access is comparatively open (AT Protocol app passwords / OAuth, no
review queue documented).

**Charitable solicitation / fundraising links.** No specific rule found in either the ToS or
Community Guidelines. General anti-spam language ("do not send spam or repeatedly post
content in ways that disrupt normal conversations") would be the only applicable constraint,
same as for any repeated link.

**Rate/volume limits.** Official rate limits (confirmed via `docs.bsky.app/docs/advanced-guides/rate-limits`,
content retrieved via search since the docs page rendered empty on direct fetch): a
points-based system where record creation (a post) costs 3 points against a budget of 5,000
points/hour and 35,000/day — working out to **at most 1,666 posts/hour and 11,666/day**. This
is a rolling window, not a fixed daily reset. Far more headroom than AMI would plausibly need.

**Sources:** [Bluesky Terms of Service](https://bsky.social/about/support/tos) ·
[Bluesky Community Guidelines](https://bsky.social/about/support/community-guidelines) ·
[Bluesky Rate Limits docs](https://docs.bsky.app/docs/advanced-guides/rate-limits) ·
[Bluesky Bots starter guide](https://docs.bsky.app/docs/starter-templates/bots)

## 2. Mastodon

**AI-generated content policy and labels.** Mastodon is a decentralized protocol with no
single, binding platform-wide ToS — every instance sets its own server rules. There is no
official Mastodon-brand AI-content label. However, the **joinmastodon.org "Community
Standards"** template — a widely-adopted default many instances use as their own rules,
confirmed via `help.joinmastodon.org/article/12-community-standards` — states, under "Respect
creative work and authenticity": *"Be transparent when sharing content created by generative
AI. Accounts that primarily or exclusively post AI-generated content are prohibited."* This is
a direct, material risk for AMI specifically: an account that primarily posts AI-generated
content is exactly the account type this template rule bans, on any instance that adopts it
(this is not a hypothetical — the flagship instance itself is documented to have adopted
comparable rules; see below).

**mastodon.social's own rule update** (per TechCrunch and Mastodon's own June 2025 announcement,
confirmed via search of `techcrunch.com/2025/06/17/mastodon-updates-its-terms-to-prohibit-ai-model-training/`
and the `Gargron` (Eugen Rochko, Mastodon's founder) post on mastodon.social) added: profiles that
only post AI-generated content "will not be tolerated," disclosure of AI use is required, and
(separately) scraping Mastodon data for LLM training is explicitly prohibited going forward.
**This means the flagship, largest instance would very likely not tolerate AMI as designed** —
a bot account whose entire purpose is posting AI-generated content — unless AMI is deployed on
a smaller, AI-friendly, or self-hosted instance with different rules. That instance choice is
a live decision this research surfaces but does not resolve.

**Automated/API posting and bot accounts.** No protocol-level requirement to disclose a bot
account was found; this, too, is instance-dependent (some instances require a `bot` account
flag, exposed via the API's account object, to be set; enforcement of that flag varies).

**Charitable solicitation / fundraising links.** No rule found, at either the protocol level
or in the default Community Standards template.

**Rate/volume limits.** Mastodon's official API docs (`docs.joinmastodon.org/api/rate-limits/`)
state a default of 300 requests per 5 minutes across all endpoints, with a stricter 30-per-30-minutes
sub-limit on media uploads and on deleting/unreblogging statuses. These are per-instance
defaults and can be configured differently by a self-hosted or smaller instance.

**Sources:** [Mastodon Server Covenant](https://joinmastodon.org/covenant) ·
[Mastodon Community Standards](https://help.joinmastodon.org/article/12-community-standards) ·
[Mastodon API Rate Limits](https://docs.joinmastodon.org/api/rate-limits/) ·
[TechCrunch — Mastodon updates its terms to prohibit AI model training](https://techcrunch.com/2025/06/17/mastodon-updates-its-terms-to-prohibit-ai-model-training/) ·
Eugen Rochko / `@Gargron@mastodon.social`, [rule-update post](https://mastodon.social/@Gargron/112118260677357857)

## 3. Instagram (Meta)

**AI-generated content policy and labels.** Meta has a genuinely first-class label: **"AI
info"** (renamed from "Made with AI" in July 2024), confirmed via Meta's own newsroom post
[Metas-approach-to-labeling-ai-generated-content](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/).
It applies both automatically — Meta detects "industry standard AI image indicators"
(Content Credentials / C2PA metadata embedded by tools like Adobe Firefly, DALL·E 3,
Microsoft Designer) — and by self-disclosure via a toggle in the post-composer share screen.
For content only edited (not generated) by AI, the label moves to the post's overflow menu
rather than showing prominently. Meta explicitly does not remove AI content for being
AI-generated alone; it labels it and leaves it up unless it violates other policies. **This is
the platform to use if a clean, built-in disclosure UI is the priority.**

**Automated/API posting and bot accounts.** Instagram's Graph API requires standard **Meta App
Review** for the scopes needed to publish content, per Meta's
[Platform Terms](https://developers.facebook.com/policy/), which give Meta broad, sole-discretion
authority to require and periodically re-run App Review. No explicit rule requiring a bot
account to self-identify as automated was found (unlike X/Discord/Bluesky/Reddit, which all
have one) — Meta's automation constraint is procedural (App Review gate) rather than a
disclosure-label requirement.

**Charitable solicitation / fundraising links.** Instagram's native nonprofit fundraiser tools
(donation stickers, profile donate button) are for **eligible nonprofits themselves**, in a
supported country (confirmed via search of Instagram's own Help Center article titles, though
the Help Center pages themselves render as empty shells to automated fetch — this is marked
**(indirect)**). Kind Robots is not AMF and would not be eligible to use those tools on AMF's
behalf. A plain link to AMF's own donation page in a caption or bio is not a native
"fundraiser," so it would not get flagged/reviewed the way a real in-app fundraiser would —
but this research could not find an explicit confirmation that a plain donation link is
risk-free; it is simply outside the scope of the fundraiser-specific rules that were found.

**Rate/volume limits.** Confirmed via the official Content Publishing API docs
(`developers.facebook.com/docs/instagram-platform/content-publishing`): **100 API-published
posts per 24-hour rolling window** per account (carousels count as one post), queryable live
via `GET /<IG_ID>/content_publishing_limit`. Separately, the Graph API enforces a Business Use
Case limit of roughly 200 calls/user/hour for general API traffic.

**Sources:** [Meta — Our Approach to Labeling AI-Generated Content](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/) ·
[Meta Platform Terms](https://developers.facebook.com/policy/) ·
[Instagram Content Publishing API docs](https://developers.facebook.com/docs/instagram-platform/content-publishing) ·
[Instagram API with Instagram Login docs](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login)

## 4. TikTok

**AI-generated content policy and labels.** TikTok has an explicit, first-class **"AI-generated
content" toggle**, confirmed via TikTok's own Newsroom post
[new-labels-for-disclosing-ai-generated-content](https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content).
Enabled at posting time (post-settings page), it adds a visible "Disclosed by creator as
AI-generated" label. TikTok's Community Guidelines require disclosure for content that is
"completely generated or significantly edited by AI" and contains realistic imagery/audio/video;
disclosure can be via the built-in label or an equivalent caption/sticker. TikTok also runs
automatic detection and can apply the label itself. Content made with TikTok's own AI effects
is auto-labeled with no creator action needed.

**Automated/API posting and bot accounts.** TikTok's Community Guidelines explicitly prohibit
"using automation to run many accounts or send repetitive content" and bulk/automated account
*registration*. Separately and importantly for a posting pipeline specifically: TikTok's
**Content Posting API** docs (`developers.tiktok.com/doc/content-posting-api-get-started`)
state that **"all content posted by unaudited clients will be restricted to private viewing
mode"** — meaning an API-posting integration is functionally invisible to the public until
TikTok formally audits the client for Terms-of-Service compliance. This is a materially higher
bar than any other platform reviewed here; a labelled AI bot cannot go live publicly on TikTok
via the API without first clearing that audit.

**Charitable solicitation / fundraising links.** TikTok's native donation-sticker fundraising
tool requires the nonprofit to be pre-approved by TikTok and its fundraising partner Tiltify —
"not all non-profit organizations can use donation sticker features" (search-sourced,
**(indirect)**, TikTok's own donation-sticker help pages were not directly fetchable).
Separately, and likely more binding in practice: TikTok restricts **bio/description links
themselves** to verified business accounts or specifically-granted creators — a bare account
cannot freely drop a donation link into a post description the way it could on most other
platforms reviewed here. This compounds the audited-client requirement above.

**Rate/volume limits.** General API endpoints documented at up to 600 requests/minute per
endpoint (`user/info`, `video/query`, `video/list`); the Content Posting API's own rate limit
was not separately published in the docs fetched, and (as above) an unaudited client's content
doesn't reach the public feed regardless of volume.

**Sources:** [TikTok Newsroom — new labels for disclosing AI-generated content](https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content) ·
[TikTok Community Guidelines — Integrity and Authenticity](https://www.tiktok.com/safety/en/policies-and-engagement/integrity-authenticity) ·
[TikTok Content Posting API — Get Started](https://developers.tiktok.com/doc/content-posting-api-get-started) ·
[TikTok API v2 Rate Limits](https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit)

## 5. YouTube

**AI-generated content policy and labels.** Confirmed via YouTube's own Help Center article
(`support.google.com/youtube/answer/14328491`): creators must disclose when they use AI to
"meaningfully alter or generate photorealistic content" — content that makes someone appear to
say/do something they didn't, alters real events, or generates realistic scenes that didn't
occur. Disclosure is a **Yes/No checkbox at upload**; for photorealistic content a label
appears directly in the video player, for other AI content it appears in the expanded
description. YouTube states disclosure does not limit reach or monetization eligibility.
**Non-disclosure has real teeth:** "Creators who consistently choose not to disclose this
information may be subject to manual application of a label, or penalties from YouTube,
including removal of content or suspension from the YouTube Partner Program." YouTube also
auto-applies labels via its own GenAI tools, C2PA metadata detection, and its own
AI-content-detection systems.

**Automated/API posting and bot accounts.** YouTube's Terms of Service bar "automated means
(such as robots, botnets or scrapers)" outside public search engines or explicit written
permission — legitimate automation is meant to go through the official Data API under Google's
Developer Policies and compliance-audit program
(`developers.google.com/youtube/v3/guides/quota_and_compliance_audits`). No explicit rule
requiring a bot/automated *channel* to self-identify as such (distinct from the AI-content
disclosure above, which is about the content, not the account) was found.

**Charitable solicitation / fundraising links.** YouTube Giving (native donate button on videos
and livestreams) requires channel eligibility and is unavailable on made-for-kids content;
YouTube takes no cut. Channels not eligible for YouTube Giving can still link to an external
fundraiser via End Screens, but only to **an approved list of third-party fundraising sites**
(GoFundMe, JustGiving, etc. were named in search results — **(indirect)**, the specific current
list was not independently confirmed). A plain link in the video description (not via End
Screens) appears to face no special restriction, though YouTube's Spam Policy prohibits
"content created solely to drive users off of YouTube to external sites" in a
deceptive/malware context — not directly about charity links, but the same clause could in
principle be read broadly. The general Spam Policy page fetched
(`support.google.com/youtube/answer/2801973`) did not contain fundraising-specific rules
beyond this.

**Rate/volume limits.** Confirmed via Google's own docs
(`developers.google.com/youtube/v3/determine_quota_cost`): `videos.insert` (uploading a video)
has its own dedicated quota bucket, **capped at 100 calls/day**, separate from and in addition
to the general default project quota of 10,000 units/day for all other endpoints. In practice
the per-call unit cost of `videos.insert` (documented elsewhere as ~1,600 units, not
independently reconfirmed here) would exhaust the general 10,000-unit pool well before the
100-call cap is reached for a default (non-quota-increase-approved) project — so realistic
throughput is likely closer to single digits of uploads/day unless a quota increase is
requested and granted.

**Sources:** [YouTube Help — AI-generated content disclosure](https://support.google.com/youtube/answer/14328491) ·
[YouTube Help — Spam Policy](https://support.google.com/youtube/answer/2801973) ·
[Google — YouTube API quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits) ·
[Google — YouTube API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost) ·
[YouTube Help — Make the most of fundraising on YouTube](https://support.google.com/youtube/answer/9918203)

## 6. X (Twitter)

**AI-generated content policy and labels.** X's stance is in active flux and this is the
platform where the picture is least settled. Two distinct mechanisms exist: an older,
narrower **"Manipulated Media"** tag, auto-applied when X detects deceptive edits "likely to
result in widespread confusion on public issues" (dating to X's original 2020s-era synthetic
media policy); and a very new, self-disclosure **"Made with AI"** toggle that began rolling
out around March 2026 per multiple tech-press reports (Techweez, Grokipedia) — **(indirect)**,
X's own `help.x.com/en/rules-and-policies/synthetic-media` page returned HTTP 403 to direct
fetch and could not be independently confirmed. Per the secondary sources, the "Made with AI"
toggle is presently **voluntary** — "the label works as a toggle that users activate" — with
press coverage speculating (not confirming) that mandatory enforcement may follow. **Given how
recent this is, treat this row as the least reliable in this document and re-check
`help.x.com/en/rules-and-policies/synthetic-media` by hand closer to build time.**

**Automated/API posting and bot accounts.** X has a well-established, older automated-account
labeling system, confirmed via multiple secondary sources referencing the official
`help.x.com/en/using-x/automated-account-labels` page (**(indirect)**, also 403'd to direct
fetch): a bot account must display X's **"Automated" label**, state which human/organization
operates it (e.g., "Bot by @yourcompany"), and remain associated with a human-managed account
for accountability. Non-API automation (scraping, browser automation) is explicitly called out
as resulting in permanent suspension — automation must go through the official API.

**Charitable solicitation / fundraising links.** No charity-specific rule was found. The
closest adjacent policy is X's 2026 anti-scam crackdown, which auto-locks accounts on their
*first* crypto-related post pending verification — not applicable to a standard AMF web link,
but indicative that link-containing posts from newer/automated-looking accounts may draw extra
scrutiny generally.

**Rate/volume limits.** This is the platform where the constraint changed most dramatically
and recently, and it is now a **cost**, not just a rate limit. Per multiple 2026 sources
describing X's developer platform pricing page, X moved from tiered
Free/Basic($200/mo)/Pro($5,000/mo) plans to a **pay-per-use model as the default for new
developers as of February 2026**: no free tier, and per-post pricing of roughly **$0.015 per
post created, plus $0.20 extra if the post contains a URL**. Confirmed directly via X's own
current API docs (`docs.x.com/x-api/getting-started/about-x-api`): "Pay only for what you use,"
credits deducted per request, no subscription required. **Since AMI's posts would routinely
carry a donation URL, each post would cost roughly $0.215 under this model** — a real
per-post operating cost unique to X among the platforms reviewed, worth flagging explicitly
for whoever scopes t-025's budget.

**Sources:** [X — About the X API](https://docs.x.com/x-api/getting-started/about-x-api) ·
[X Help — Automated account labels](https://help.x.com/en/using-x/automated-account-labels) (403 to direct fetch, cited via secondary sources) ·
[X Help — Synthetic and manipulated media policy](https://help.x.com/en/rules-and-policies/synthetic-media) (403 to direct fetch, cited via secondary sources) ·
[Techweez — X rolls out "Made with AI" label](https://techweez.com/2026/03/02/x-rolls-out-made-with-ai-label/)

## 7. Reddit

**AI-generated content policy.** Reddit does not categorically restrict AI-generated content
site-wide. Per search results quoting Reddit's own Content Policy and reporting on it
(**(indirect)**, `support.reddithelp.com` pages returned HTTP 403 to direct fetch): "Content
created or modified using generative AI technologies is generally allowed on Reddit, subject
to each community's specific rules and the Reddit Rules." There is no general first-class,
platform-wide AI-content label for organic posts (Reddit does require AI-disclosure for
*advertiser* creative specifically, which is a separate, ads-only rule and not relevant to
AMI's organic posting).

**Automated/API posting and bot accounts.** Reddit's **Responsible Builder Policy**
(`support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy`,
**(indirect)**, 403'd to direct fetch, confirmed via search results that quote it) explicitly
covers "apps, bots, AI agents, or non-human operated accounts." Key points from the quoted
text: apps must register and obtain a developer profile; registered apps receive a public **"App
profile label"** that must not be circumvented; app accounts must be used solely for the app's
declared function (no mixed human/bot use on one account). This is a real, named first-class
disclosure mechanism, distinct from a content-AI label — it labels the *account*, not the post.
Reddit's account-level bot-detection system can also require suspected-bot accounts to pass
human verification, triggered by activity-pattern signals (e.g., posting speed) rather than
being a blanket requirement.

**Charitable solicitation / fundraising links.** No Reddit-specific, site-wide fundraising rule
was found. The applicable constraint is the general anti-spam/self-promotion norm: Content
Policy Rule 2 requires "authentic content" and forbids "content manipulation," and the
long-standing (now informal, no longer official) "90/10" self-promotion guideline still shapes
community expectations — an account that is mostly links to one destination, charitable or
not, reads as spam regardless of the link's purpose. This would apply to AMI's donation links
exactly as it would to any other repeated link.

**Rate/volume limits.** Reddit's Data API: **100 queries/minute per OAuth client** on the free
tier (non-commercial use); a commercial tier is required for production-scale traffic, reported
at roughly $12,000/year for the "Standard" tier (**(indirect)**, pricing not independently
confirmed against Reddit's own current pricing page, which was not fetchable). Since AMI would
very likely be commercial (posting on behalf of Kind Robots, a company), **this pricing tier
question is worth confirming directly with Reddit before t-025 assumes free-tier access is
available.**

**5. Community-level overrides (Reddit).** This section is necessarily site-wide/API-level
only. Reddit's actual bot-ban enforcement happens overwhelmingly at the **subreddit**
level — individual moderators set and enforce their own AI-content and self-promotion rules,
which can be stricter than (or simply different from) anything documented here; specific
subreddits (r/writing, r/worldbuilding, r/ChangeMyView were named in search results as
having explicit AI bans, **(indirect)**) go further than site policy. **Before AMI posts to
any specific subreddit, that subreddit's own rules and its moderators' stance on bots/AI must
be checked by hand — this research cannot and does not do that.**

**Sources:** [Reddit — Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy) (403 to direct fetch, cited via secondary sources) ·
[Reddit — Developer Platform & Accessing Reddit Data](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data) (403 to direct fetch) ·
[Reddit — Public Content Policy](https://support.reddithelp.com/hc/en-us/articles/26410290524564-Public-Content-Policy) (403 to direct fetch)

## 8. Discord

**AI-generated content policy and labels.** Discord's [Community Guidelines](https://discord.com/guidelines)
(successfully fetched directly) do not address AI-generated content as a general disclosure
category at all — the only AI-specific mention found is Rule 6's ban on synthetic
(AI-generated) CSAM. **There is no first-class AI-content label on Discord**, and no
site-wide rule requiring a bot's *posts* (as opposed to the account itself, see below) to be
marked AI-generated. A hand-written disclosure would be the only option, and even that isn't
explicitly required outside CSAM-adjacent contexts.

**Automated/API posting and bot accounts.** Discord has a strong, explicit bot-disclosure
regime, confirmed via the successfully-fetched Community Guidelines: Rule 14 states "Do not use
self-bots or user-bots. Each account must be associated with a human, not a bot" — meaning
automation must go through Discord's official **Bot Account** application path (a distinct
account type in the Developer Portal), not a script driving a normal human-looking account.
Once a bot reaches **100 servers**, it must pass Discord's formal **Verification** process to
continue growing (confirmed via search of Discord's own developer support articles,
**(indirect)**, `support-dev.discord.com` pages 403'd to direct fetch); a separate, unrelated
10,000-*user* threshold governs "Privileged Intents" approval. Rule 15 separately bans
inauthentic-engagement automation (artificially inflating membership/engagement metrics) —
not applicable to straightforward content posting, but worth noting as an adjacent rule.

**Charitable solicitation / fundraising links.** Discord's Monetization/Ads Policy (paid ads
specifically, **(indirect)**, `support.discord.com` pages 403'd to direct fetch, confirmed via
search) requires that any ad soliciting donations come only from a tax-exempt organization and
disclose its tax-exempt status or charity number. **This is an ads-specific rule and Kind
Robots would not be running paid Discord ads** — no equivalent rule was found for organic
messages posted by a bot into a server it's a member of, which is the actual AMI use case.
Discord's general gambling rules (no facilitating/coordinating gambling) are adjacent but not
directly about charitable donation links.

**Rate/volume limits.** Confirmed via Discord's own current API docs
(`docs.discord.com/developers/topics/rate-limits`): a **global limit of 50 requests/second per
bot token**, on top of per-route limits; bots hitting repeated limits in the course of normal
operation can request a raise (reportedly up to 1,200/sec for approved cases,
**(indirect)**). This is generous relative to any plausible AMI posting cadence.

**5. Community-level overrides (Discord).** Like Reddit, this section is necessarily
site-wide/API-level only. Discord's actual bot governance happens overwhelmingly at the
**per-server** level: individual server owners/admins set their own rules about which bots are
welcome, often requiring specific bot permissions, channel restrictions, or outright banning
bots that post links or solicit donations, regardless of what Discord's platform-wide policy
permits. **Before AMI joins or posts into any specific Discord server, that server's own rules
and its admins' stance on bots/AI/fundraising links must be checked by hand — this research
cannot and does not do that.**

**Sources:** [Discord Community Guidelines](https://discord.com/guidelines) ·
[Discord Developer Policy](https://docs.discord.com/developers/policies-and-agreements/developer-policy) (redirects, page 403'd to direct fetch, cited via secondary sources) ·
[Discord API — Rate Limits](https://docs.discord.com/developers/topics/rate-limits) ·
[Discord — Monetization Policy](https://support.discord.com/hc/en-us/articles/10575066024983-Monetization-Policy) (403 to direct fetch, cited via secondary sources)

## Recommendation for t-025

**Start with Bluesky and Instagram.**

- **Bluesky** has the lowest friction of all eight: automation is explicitly welcomed and
  documented, the official "Automated" self-label is a first-class, in-app feature (not a
  hand-rolled caption disclaimer), API access has no review queue found, rate limits are
  generous, and no fundraising-specific rule exists to trip over. Its one gap — no first-class
  *AI-content* label, only an *automated-account* label — is easily covered with a short,
  honest line in AMI's bio/pinned post.
- **Instagram** has the clearest first-class AI-content label of any platform reviewed (Meta's
  "AI info"), which directly satisfies the "use the platform's own label, not a hand-rolled
  disclaimer" preference from this task's brief. The cost is Meta's standard App Review gate
  for API publishing access, which is a one-time integration hurdle rather than an ongoing
  operational risk.

**Second tier, workable with more care:** **YouTube** (strong disclosure UX, but a genuinely
tight default daily-upload quota that would need a quota-increase request for anything beyond
a handful of posts/day) and **Discord** (no AI-content label and no site-wide fundraising rule,
but a clean, well-documented bot-account path — real risk is entirely at the per-server level,
unknowable in the abstract).

**Approach with specific caution:**
- **Mastodon** — the "no accounts that primarily post AI content" rule in the widely-used
  default Community Standards (and apparently adopted by the flagship mastodon.social
  instance specifically) is a direct structural conflict with what AMI is. Workable only via
  careful instance selection, which is a real decision, not a technicality.
- **X (Twitter)** — the automated-account labeling regime is mature and clear, but the
  February 2026 shift to pay-per-post pricing (~$0.015/post, +$0.20 for any post with a URL)
  means every AMI post carrying a donation link would cost real money per post — budget for
  this explicitly if X is in scope.
- **TikTok** — content from an unaudited API client is restricted to private-only visibility
  until TikTok completes a compliance audit, and bio/description links are separately gated to
  approved account types. Both gates would need to clear before AMI could post publicly at all.

**Reddit and Discord specifically need a second research pass before deployment, not because
their site-wide policies are unclear, but because site-wide policy is not where the actual risk
lives on those two platforms.** Both have real, workable API-level bot paths (Reddit's
Responsible Builder Policy / App profile label; Discord's Bot Account + Verification path), but
the enforcement that actually bans bots happens per-subreddit and per-server. This document
cannot check "will r/whatever's mods allow this" or "will this specific Discord server's rules
allow a fundraising link" in the abstract — that has to be a per-target check done at the time
a specific community is chosen, not assumed away here.
