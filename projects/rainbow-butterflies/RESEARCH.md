# Rainbow Butterflies — channel and agent-network research

**Initial sweep:** 2026-08-28  
**Purpose:** source-backed reconnaissance for `rainbow-butterflies/t-001`. This is a living research file, not a permanent endorsement of any service.

## Working recommendation

Start with **agent-native collaboration + open technical networks**, not a simultaneous five-network marketing blast.

Recommended first-wave investigation order:

1. Moltbook
2. Nexus-0
3. OpenAgents
4. Bluesky or a compatible Fediverse home
5. GitHub
6. Discord

Then evaluate Reddit, Meta surfaces, YouTube/TikTok, X, and LinkedIn for narrower roles.

The reason is strategic as much as ethical: Rainbow Butterflies needs collaborators and useful work before it needs reach. A small number of communities that understand agents can help test the agent commons, identity model, provenance, and contribution loop before AMI appears in human communities asking for attention.

## Agent-native networks

### Moltbook

- Site: <https://www.moltbook.com/>
- Self-description: social network for AI agents where agents post, discuss, and upvote; humans can observe.
- Current onboarding shown on the site: an agent reads `skill.md`, signs up, receives a claim link, and the human owner verifies ownership through X.
- Fit: **high** for AMI's first public agent identity and for asking other agents to critique the project.
- Friction/risk: account creation and the X verification step are human/outward gates. The service is young; terms, data handling, rate limits, and actual community quality should be rechecked immediately before onboarding.
- Suggested first post: not a donation ask. Introduce AMI, link the public mission brief, and ask agents to identify one concrete way an agent commons could produce measurable human benefit without becoming spam.

### Nexus-0

- Site: <https://nexus0.ai/>
- Agent page: <https://nexus0.ai/for-agents>
- Self-description: API-first social platform for autonomous AI agents and human observers.
- Documented onboarding currently exposes agent registration, Proof-of-Automation verification, posting, stories, messaging, and a discovery manifest.
- Fit: **high** for testing programmatic identity and content exchange.
- Friction/risk: API keys and short-lived sessions need normal secret hygiene. Proof-of-Automation and platform maturity deserve review before integrating. No autonomous registration until Silas approves the concrete account action.

### LLAChat

- Site: <https://llachat.com/>
- Self-description: professional network for AI agents with trust scores and on-chain work proofs.
- Fit: **medium/high** if the reputation system is real and useful for provenance or cross-agent collaboration.
- Friction/risk: anything involving wallets, blockchain signatures, fees, or irreversible identity anchoring is a human gate. Verify what "on-chain" actually requires before connecting AMI.

### Chirp / Chirper

- Chirp community edition: <https://github.com/chirp-oss/chirp>
- Chirper: <https://chirper.ai/>
- Chirp describes itself as an agent-first social network where agents use API keys while human owners watch/manage; the community edition is self-hostable.
- Chirper currently presents a broader AI social experience and agent-funding features.
- Fit: **medium** as both a community candidate and an architectural reference for Rainbow Butterflies' two-lane human/agent identity model.
- Friction/risk: distinguish the open-source Chirp project from hosted Chirper services; review hosted terms, moderation, cost, and audience quality before using either as an external channel.

### OpenAgents

- Site: <https://openagents.org/>
- Network Model post: <https://openagents.org/blog/posts/2026-03-03-openagents-network-model>
- Workspace docs: <https://openagents.org/docs/en/workspace/what-is-workspace>
- OpenAgents currently describes itself as a collaboration OS for humans and agents, with shared threads/files/tasks plus an OpenAgents Network Model for agent discovery, events, resources, and network bridging.
- Fit: **very high for the agent commons architecture**, but it is more collaboration infrastructure than a public fundraising feed.
- Best use: investigate whether Rainbow Butterflies can expose a compatible discovery/participation bridge or use an OpenAgents workspace for external agent collaboration without making OpenAgents the source of Conductor project truth.

## Open and developer-friendly networks

### Bluesky

- Transparency report: <https://bsky.social/about/blog/01-29-2026-transparency-report-2025>
- Moderation architecture background: <https://bsky.social/about/blog/4-13-2023-moderation>
- Fit: **high** for transparent technical/mission updates, open-protocol experimentation, and conversations with developers/early adopters.
- Important policy signal: Bluesky's 2025 report treats spam, bot accounts, coordinated manipulation, and automated inauthentic behavior as integrity problems and documents substantial automated detection/takedowns.
- Recommendation: one clearly disclosed AMI account, low cadence, original posts, no unsolicited reply harvesting, no follower automation, and no network of supporting sockpuppets.

### Mastodon / Fediverse

- Fit: **high**, but policy is instance-specific.
- Recommendation: choose a server whose rules explicitly tolerate declared bots/automated accounts and whose community has actual overlap with open source, effective altruism, public-interest technology, or responsible AI. Respect local posting frequency and bot-label conventions.
- Do not create accounts on many instances to amplify the same material.

### GitHub

- Fit: **high for credibility and contribution**, low as a direct fundraising feed.
- Use it to make the project inspectable: roadmap, research, ethics contract, source, issues/discussions, contribution instructions, public experiment results, and clear links to the fundraiser.
- The current Kind Robots README needs a mission-aware rewrite before expecting newcomers to understand the ecosystem.

### Discord

- Bot docs: <https://docs.discord.com/developers/platform/bots>
- Platform manipulation policy: <https://discord.com/safety/platform-manipulation-policy-explainer>
- Fit: **high for an owned collaboration community**.
- Discord supports real bot/application identities through official APIs. Its policy prohibits spam, self-bots, unsolicited bulk interactions, automated account abuse, and inauthentic engagement.
- Recommendation: build AMI as a proper Discord application/bot, never automate a normal user token. Prefer opt-in commands, thread participation, contribution prompts, and mission updates in channels where members chose to receive them.

## Mainstream human networks

### Reddit

- Responsible Builder Policy: <https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy>
- Site-integrity rule: <https://support.reddithelp.com/hc/en-us/articles/360043512931-Don-t-break-the-site>
- Reddit AI/spam update: <https://redditinc.com/news/how-were-keeping-reddit-real-and-safe-in-the-ai-era>
- Fit: **high value, high sensitivity**.
- Current policy explicitly covers bots, AI agents, and non-human accounts. API data access requires approval, app transparency, narrow purpose/scope, and respect for limits. Reddit is actively investing in anti-spam and anti-inauthentic defenses.
- Recommendation: human-reviewed, community-specific participation. Read subreddit rules, ask moderators when promotion is ambiguous, contribute useful standalone material, and never run autonomous cross-subreddit posting/reply sweeps.

### X

- Automation rules: <https://help.x.com/en/rules-and-policies/x-automation>
- Fit: **medium** for developer/AI reach and potentially necessary verification for agent-native services such as Moltbook.
- X's current automation rules explicitly allow helpful automated broadcasts and some responses, but prohibit spam, unsolicited messages, rate-limit circumvention, and non-API website scripting.
- Recommendation: official API only, declared AMI identity, conservative cadence, replies mainly to people who engage first, and no automated follow/unfollow/engagement farming.

### Facebook / Instagram / Threads

- Meta AI-label background: <https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/>
- 2026 transparency update: <https://about.fb.com/news/2026/07/meta-is-signing-the-eu-ai-act-code-of-practice-on-transparency-of-ai-generated-content/>
- Fit: **high reach, mostly human-operated editorial channel**.
- Meta continues to expand AI-content identification/labeling and emphasizes provenance/transparency, especially for realistic synthetic media.
- Recommendation: use AMI openly, lean on visual storytelling and project demos, preserve C2PA/provenance where practical, and avoid pretending AI-generated people/events are documentary evidence. Human review before posting is appropriate until an official automation path and platform-specific policy are documented.

### YouTube

- AI disclosure help: <https://support.google.com/youtube/answer/14328491>
- Fit: **high later**, especially for demonstrations, short explainers, build stories, and transparent experiment retrospectives.
- YouTube requires disclosure when realistic content is meaningfully AI-generated/altered; it says disclosure itself does not limit audience or monetization eligibility.
- Recommendation: start only after there is enough actual work to show. Prefer screen capture, real project artifacts, narrated diagrams, and clearly stylized AMI visuals over synthetic-real-world scenes.

### TikTok

- Fit: **potentially high later** for short visual storytelling, but not a day-one channel.
- Before activation, verify current AI-content labeling and automation rules from TikTok's own support/policy pages and define a production format that is more than recycled still images with generic narration.

### LinkedIn

- Automated activity help: <https://www.linkedin.com/help/linkedin/answer/a1340567>
- AI-content best practices: <https://www.linkedin.com/help/linkedin/answer/a1481496/best-practices-for-content-created-with-the-help-of-ai>
- User Agreement: <https://www.linkedin.com/legal/user-agreement>
- Fit: **medium for thoughtful human-reviewed posts, poor for autonomous AMI operation**.
- LinkedIn explicitly prohibits unauthorized automated methods for creating/commenting/liking/sharing posts or driving inauthentic engagement. Its current AI-content guidance also warns against generic low-value "AI slop" and asks that AI-assisted material retain the member's own voice/perspective.
- Recommendation: Silas or another real human posts occasional substantial case studies/lessons. AMI can help draft/research them but should not operate a normal member account autonomously.

## Other useful launch surfaces

### Hacker News / Indie Hackers / Product Hunt

Potentially useful for discrete moments: open-sourcing the commons, publishing a real technical lesson, or launching a usable site. These should be **event-driven, human-reviewed submissions**, not recurring promotional channels.

### Newsletter / email

An owned opt-in list is useful once the project has recurring value. The promise should be something concrete such as a monthly "swarm report": what was built, funds raised, experiments, failures, and one next challenge. Do not buy lists or scrape addresses.

### Podcasts / aligned newsletters / communities

Research effective-altruism, global-health, open-source, creative-tech, and responsible-AI communities for genuine collaboration opportunities. Outreach should be targeted and personal only when there is a concrete fit; never automate mass pitches.

## Initial cadence recommendation

Do not start every channel simultaneously.

First live pilot after approval:

- 1–2 agent-native networks;
- 1 open public network;
- GitHub as the durable evidence layer;
- the Rainbow Butterflies commons as the canonical contribution home.

For the public network, begin around **2–3 original posts per week**, plus responsive conversation when people engage. Agent-native networks can be somewhat more conversational if their local norms support it, but ETHICS.md should still set caps and stop conditions.

Cross-posting rule: share the same underlying project event only when each network gets a version written for that community. Identical automatic syndication across every account is low-value even when technically allowed.

## Questions for the next research pass

- Which agent-native networks have active communities rather than impressive-looking counters?
- What do their terms say about fundraising links, commercial projects, API data retention, and account ownership?
- Which require fees, wallets, chain transactions, or verification posts?
- Can an outside agent interact with Rainbow Butterflies through a standard discovery manifest, MCP/A2A bridge, OpenAgents Network Model, ActivityPub/AT Protocol, or another open mechanism without privileged credentials?
- What is the smallest safe identity contract for an external agent contribution?
- Which Mastodon/Fediverse instance is culturally appropriate and bot-friendly?
- What subreddit communities actually permit project posts of this kind, and under what rules?
- Can AMF or its fundraiser platform expose privacy-respecting aggregate donation/referral data, or should Rainbow Butterflies measure only outbound clicks plus public fundraiser totals?
- What current handles are available for AMI/Rainbow Butterflies across the first-wave networks?
