# Rainbow Butterflies — account, handle, and integration launch checklist

Status: planning document for `rainbow-butterflies/t-007`. **This file authorizes no action by
itself.** It turns `RESEARCH.md`'s channel playbook into a concrete, per-channel checklist so a
human (or an agent Silas has explicitly directed) can execute launch steps efficiently once
approved. Creating accounts, claiming handles, accepting terms of service, or publishing a first
post are all explicit human gates — see `AUTONOMY.md` and `ETHICS.md`'s "When a human must
approve" list. Nothing here performs any of those actions.

## How to read this checklist

Each channel entry lists:

- **Desired handle(s)** — first choice plus a fallback if the first is taken.
- **Profile fields** — what the bio/profile should say, reusing `AMI-IDENTITY.md`'s disclosure
  language and bios rather than inventing new copy per channel.
- **API/app requirements** — what technical registration the channel requires before any
  automated posting is possible (developer app, API key, bot application, webhook, etc.).
- **Verification steps** — identity/ownership verification the platform requires, and who must
  perform it (a human, specifically Silas where account-linking to a personal identity is
  involved).
- **Nominal fees** — any cost to register, verify, or maintain presence. "None known" means the
  research pass found no fee, not that one is guaranteed absent.
- **Required human inputs** — anything only Silas (or another explicitly authorized human) can
  provide: an email address, a phone number for verification, a payment method, a legal-entity
  name, an existing personal account to link from.
- **Wave** — `first` (agent-native or low-friction technical channels, per `RESEARCH.md`'s
  recommended order) or `later` (higher-reach or higher-sensitivity channels to revisit once the
  commons has real output to show).

A channel with unresolved research questions is marked **recheck before launch** — its terms,
fees, or requirements should be reconfirmed at execution time since `RESEARCH.md` explicitly
treats itself as a living document, not a frozen source.

## Wave: first

### Moltbook

- **Desired handle(s):** `ami` (fallback: `ami_rainbowbutterflies`)
- **Profile fields:** AMI-IDENTITY.md's "technical / agent-native" bio; disclosure snippet in bio
  field if the platform supports a persistent one.
- **API/app requirements:** agent reads the site's `skill.md` and completes agent-side signup
  (no separate API key documented at research time — **recheck before launch**).
- **Verification steps:** claim link issued to the agent, then the human owner (Silas) verifies
  ownership through an X account. Requires Silas to have (or create) a linkable X presence first.
- **Nominal fees:** none known.
- **Required human inputs:** Silas's X account for the claim-verification step.
- **Wave:** first.
- **Notes:** young service — reconfirm terms, data handling, and rate limits immediately before
  onboarding, per `RESEARCH.md`.

### Nexus-0

- **Desired handle(s):** `ami` (fallback: `rainbowbutterflies`)
- **Profile fields:** technical/agent-native bio; disclosure snippet.
- **API/app requirements:** agent registration through the documented `/for-agents` flow;
  API-first, so expect an issued API key/token.
- **Verification steps:** Proof-of-Automation verification (mechanism not fully documented at
  research time — **recheck before launch**).
- **Nominal fees:** none known.
- **Required human inputs:** none identified beyond approving the registration itself; confirm
  at execution time whether an email or identity link is required.
- **Wave:** first.
- **Notes:** treat the issued API key with normal secret hygiene — store via the project's
  standard secrets path, never in a committed file or a pasted transcript.

### OpenAgents

- **Desired handle(s):** `rainbow-butterflies` workspace/agent name (fallback:
  `ami-rainbowbutterflies`)
- **Profile fields:** technical/agent-native bio; link to the public commons and `RESEARCH.md`'s
  architecture notes.
- **API/app requirements:** workspace creation and/or Network Model registration for
  discovery/events/resources — **recheck before launch**, since `RESEARCH.md` flags this as
  "investigate whether a compatible bridge is possible" rather than a settled integration.
- **Verification steps:** none documented at research time.
- **Nominal fees:** none known.
- **Required human inputs:** none identified yet.
- **Wave:** first, but scoped narrowly to investigation/bridge-compatibility before any public
  presence — this is architecture research more than a launch account.

### Bluesky (or a compatible Fediverse home)

- **Desired handle(s):** `ami.rainbowbutterflies.org` if custom-domain handles are set up on the
  eventual site (fallback: `amirainbowbutterflies.bsky.social`)
- **Profile fields:** AMI-IDENTITY.md's "mission-forward" bio; persistent disclosure text in the
  profile description field (Bluesky supports a full-length bio).
- **API/app requirements:** standard account creation; automated posting later would use the AT
  Protocol API with an app password or OAuth — not required for the first manual-post phase.
  **recheck before launch** to confirm current app-password/OAuth requirements.
- **Verification steps:** standard email verification; optional custom-domain handle
  verification (a DNS TXT record or `.well-known` file) if `rainbowbutterflies.org` is used as
  the handle domain.
- **Nominal fees:** none known for the account itself.
- **Required human inputs:** an email address for signup; DNS access to
  `rainbowbutterflies.org` if a custom-domain handle is used.
- **Wave:** first.

### GitHub

- **Desired handle(s):** the existing `silasfelinus` org/account already hosts `kind_robots` and
  `conductor`; no new account needed unless a dedicated `rainbow-butterflies` org is preferred
  later. Default plan: use the existing account, no new handle.
- **Profile fields:** repository README (already refreshed per `rainbow-butterflies/t-005`) is
  the primary public-facing surface here, not a profile bio.
- **API/app requirements:** none beyond what already exists for `conductor`/`kind_robots`.
- **Verification steps:** none — already an established, verified account.
- **Nominal fees:** none.
- **Required human inputs:** none beyond what already exists.
- **Wave:** first — lowest-friction channel since no new account is needed at all. Treat as
  "already launched" for credibility/inspectability purposes; no gate to clear here beyond
  keeping docs current.

### Discord

- **Desired handle(s):** bot application name `AMI` (fallback: `AMI (Rainbow Butterflies)` if
  `AMI` collides); server name `Rainbow Butterflies Commons` (fallback: `Rainbow Butterflies HQ`)
- **Profile fields:** AMI-IDENTITY.md's compact bio as the bot's "About Me"; disclosure snippet
  pinned in the server's welcome/rules channel.
- **API/app requirements:** a registered Discord Application + Bot user via the Developer
  Portal, an issued bot token (secret — standard hygiene applies), and OAuth2 scopes limited to
  what the bot actually needs (message read/send, no elevated permissions by default).
- **Verification steps:** standard Discord developer account (may require phone/2FA on the
  developer account, not just email — **recheck before launch**); no special bot-verification
  tier needed below 100 servers.
- **Nominal fees:** none known for a bot under the verification threshold.
- **Required human inputs:** Silas's Discord account to register the application and own the
  server; a phone number if 2FA is required on the developer account.
- **Wave:** first, once there is a concrete server/commons destination to launch into (this may
  follow shortly after `rainbow-butterflies/t-004`'s app scaffold rather than preceding it).

## Wave: later

### LLAChat

- **Desired handle(s):** `ami` (fallback: `rainbowbutterflies`)
- **Profile fields:** technical bio; disclosure snippet.
- **API/app requirements, verification, fees:** unresolved — **recheck before launch**,
  specifically whether "on-chain work proofs" requires a wallet, signature, or fee. Any wallet or
  blockchain-transaction requirement is itself a human gate regardless of what this checklist
  says, per `ETHICS.md`.
- **Required human inputs:** unknown until rechecked; assume a wallet/keypair would need to be
  human-provisioned if required.
- **Wave:** later — gate on confirming the reputation system is genuinely useful and the
  on-chain requirement (if any) is acceptable.

### Chirp / Chirper

- **Desired handle(s):** `ami` on whichever surface is chosen.
- **Profile fields:** technical bio; disclosure snippet.
- **API/app requirements:** Chirp (self-hostable, API-key-based) vs. Chirper (hosted) are
  different integration paths — **recheck before launch** and pick one, not both, to avoid
  duplicate/confusing presences.
- **Verification steps, fees:** unresolved — recheck hosted Chirper's terms/cost before use.
- **Required human inputs:** unknown until a path is chosen.
- **Wave:** later — useful mainly as an architectural reference today, not a priority launch
  target.

### Reddit

- **Desired handle(s):** `u/AMI_RainbowButterflies` (fallback: `u/RainbowButterflies_AMI`)
- **Profile fields:** compact bio adapted to Reddit's short-bio limit; disclosure in flair/bio
  where the subreddit allows it.
- **API/app requirements:** a registered Reddit API app for any automated interaction; per
  `RESEARCH.md`, API access requires approval, a stated narrow purpose, and adherence to the
  Responsible Builder Policy — human-reviewed participation is the actual recommendation, so a
  full automated API integration may not be needed for launch.
- **Verification steps:** standard account creation; API app approval process.
- **Nominal fees:** none known for the account; API access terms should be rechecked.
- **Required human inputs:** an email address; a human (Silas or a delegated reviewer) to read
  each target subreddit's rules before any post, per `RESEARCH.md`'s recommendation.
- **Wave:** later — human-reviewed, subreddit-by-subreddit, not a day-one automated presence.

### X

- **Desired handle(s):** `@AMI_RB` (fallback: `@RainbowButterflyAI`) — short-form handles fill
  quickly; **recheck availability at execution time**, this list is not a live availability
  check.
- **Profile fields:** compact bio; disclosure in bio (X's automation rules require this for
  automated accounts).
- **API/app requirements:** official X API access (developer app + tier), used sparingly per
  `RESEARCH.md`'s "official API only" recommendation.
- **Verification steps:** standard account creation; developer app approval for API access; may
  be needed as a verification step for Moltbook's claim-link flow even before an independent X
  presence is otherwise planned — **recheck** whether that requirement can be met with a
  personal account instead of a new one.
- **Nominal fees:** X API access has paid tiers above a free/basic allotment — **recheck current
  pricing before launch**, since this changes materially over time.
- **Required human inputs:** an email/phone for account creation; a payment method if a paid API
  tier is required.
- **Wave:** later, except for whatever minimal presence Moltbook's own verification flow turns
  out to require.

### Facebook / Instagram / Threads

- **Desired handle(s):** `RainbowButterfliesAMI` (fallback: `AMI.RainbowButterflies`)
- **Profile fields:** mission-forward bio; disclosure per Meta's AI-content labeling
  expectations.
- **API/app requirements:** a Meta Developer app + Page for any automated posting; manual human
  posting needs no API at all and is the recommended starting mode per `RESEARCH.md`.
- **Verification steps:** standard Page creation; Meta Business verification if ad or
  higher-trust features are needed later (not required for organic posts).
- **Nominal fees:** none known for organic use.
- **Required human inputs:** an email/phone for account setup; ongoing human review before
  posting, per `RESEARCH.md`'s recommendation.
- **Wave:** later.

### YouTube

- **Desired handle(s):** `@RainbowButterfliesAMI` (fallback: `@AMI_RainbowButterflies`)
- **Profile fields:** mission-forward bio in channel description; AI-disclosure per YouTube's
  current policy for meaningfully AI-generated/altered content.
- **API/app requirements:** none for manual uploads; YouTube Data API registration only if
  automated upload/scheduling is added later.
- **Verification steps:** standard Google account + channel creation; phone verification is
  standard for channels over certain feature thresholds.
- **Nominal fees:** none.
- **Required human inputs:** a Google account; a phone number for standard verification.
- **Wave:** later — explicitly gated on "there is enough actual work to show" per `RESEARCH.md`.

### TikTok

- **Desired handle(s):** `@ami.rainbowbutterflies` (fallback: `@rainbowbutterflies.ami`)
- **Profile fields:** compact bio; disclosure per current TikTok AI-content policy —
  **recheck before launch**, policy specifics were not fully captured in the research pass.
- **API/app requirements, verification, fees:** unresolved — recheck before launch.
- **Required human inputs:** unknown until rechecked; assume standard account creation (email/
  phone) at minimum.
- **Wave:** later, and only once a production format beyond "recycled stills with narration"
  exists, per `RESEARCH.md`.

### LinkedIn

- **Desired handle(s):** no dedicated AMI account planned — `RESEARCH.md` recommends Silas (a
  real human) post occasional case studies here rather than AMI operating a member account
  autonomously. No handle to reserve.
- **Profile fields:** n/a (uses Silas's existing profile).
- **API/app requirements:** none planned.
- **Verification steps, fees:** n/a.
- **Required human inputs:** Silas's own authorship/review of each post.
- **Wave:** later, human-authored only.

### Mastodon / Fediverse (if distinct from the Bluesky choice above)

- **Desired handle(s):** `@ami@<instance>` — instance not yet chosen; **recheck before launch**
  per `RESEARCH.md`'s open question on which instance is culturally appropriate and
  bot-friendly.
- **Profile fields:** technical/agent-native bio; disclosure per the chosen instance's bot-label
  convention.
- **API/app requirements:** standard Mastodon API app registration for any automated posting.
- **Verification steps:** standard account creation on the chosen instance; some instances
  require manual admin approval to join.
- **Nominal fees:** none known; some instances request voluntary donations to run costs.
- **Required human inputs:** an email address; instance selection is itself a human decision.
- **Wave:** later, and only as a second open-protocol presence if Bluesky alone does not cover
  this need — avoid running near-duplicate presences on both without a clear reason.

## Newsletter / owned email

- **Desired handle(s):** a sending address under `rainbowbutterflies.org` once DNS/domain setup
  happens (e.g., `swarm@rainbowbutterflies.org`) — depends on `rainbow-butterflies/t-004`'s app
  scaffold and any DNS work, which are their own human gates.
- **Profile fields:** n/a.
- **API/app requirements:** an email-sending/newsletter service (not yet selected).
- **Verification steps:** domain verification (SPF/DKIM) for deliverability.
- **Nominal fees:** most newsletter services have a free tier at low subscriber counts; recheck
  the chosen provider's pricing before scaling.
- **Required human inputs:** DNS access; provider account creation.
- **Wave:** later — explicitly "once the project has recurring value" per `RESEARCH.md`.

## What this checklist does not authorize

Per `ETHICS.md`'s "When a human must approve" list, restated here for a reader who opens only
this file:

- creating, claiming, or verifying any account, handle, or app/developer credential listed above;
- accepting any platform's terms of service or developer agreement on Silas's behalf;
- the first public post on any channel;
- any fee payment or spend commitment, however small ("none known" is a research finding, not a
  standing budget approval);
- providing any of the "required human inputs" listed per channel (email, phone, DNS access,
  payment method, personal-account linking).

## Recommended execution order

Matches `RESEARCH.md`'s cadence recommendation: GitHub is effectively already live (no action
needed). For the first live pilot, pick 1–2 agent-native networks from the first wave above (most
likely Moltbook and/or Nexus-0) plus one open public network (Bluesky), rather than attempting the
full first-wave list simultaneously. Discord can follow once `rainbow-butterflies/t-004`'s app
scaffold gives the commons a concrete home to link the server to. Everything in "later" waits for
either more finished output to show or an unresolved research question above to be closed out.

## Open items for the next research/checklist pass

- Confirm current handle availability for every entry above immediately before execution — this
  list reflects a point-in-time desirability ranking, not a live availability check.
- Resolve every "recheck before launch" item inline before that specific channel launches.
- Revisit X API pricing tiers and Discord developer-account 2FA requirements, both called out
  above as likely to have changed by execution time.
