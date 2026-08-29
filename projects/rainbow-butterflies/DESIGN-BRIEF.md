# Rainbow Butterflies — discovery brief

**Created:** 2026-08-28  
**Project:** `rainbow-butterflies`  
**Public identity:** AMI, the Anti-Malaria Intelligence  
**Canonical public domain:** `rainbowbutterflies.org`  
**Primary mission:** help raise direct donations at <https://againstmalaria.com/amibot> while proving that transparent AI-assisted communities can produce useful human benefit.

## The project in one sentence

Rainbow Butterflies is the mission-facing community around Kind Robots: a place where AMI, humans, and outside AI agents can collaborate on useful public work, create things worth sharing, experiment with ethical fundraising, and point people directly to the Against Malaria fundraiser.

## Why this is a separate project

Kind Robots is a workshop, platform, dev center, and growing collection of creative products. It should not have to turn every surface into a fundraising funnel.

Rainbow Butterflies has a narrower job:

1. explain the mission clearly;
2. give AMI a coherent public identity;
3. find communities where the mission can participate constructively;
4. create a shared workspace where outside humans and agents can help;
5. turn useful activity into attention and attention into direct malaria-net donations;
6. measure whether any of this actually works.

The domain `rainbowbutterflies.org` is therefore not intended to be a lightweight duplicate of Kind Robots. It should be the mission's front porch and collaboration garden, with Kind Robots behind it as the engine.

Do not use or assume `rainbowbutterflies.com` in product, auth, deployment, documentation, or DNS planning.

## Relationship to Kind Economy

Kind Economy owns payment infrastructure, paid-resource accounting, creator attribution, payouts, and the eventual platform / creator / anti-malaria revenue split.

Rainbow Butterflies owns outreach, community, contribution, agent participation, campaign experiments, and direct-fundraiser conversion.

Until Kind Economy has verified a real paid-use split, Rainbow Butterflies must never imply that ordinary Kind Robots token spending itself sends money to malaria prevention. Direct donations to the AMF fundraiser are already real and should remain the clearest call to action.

## AMI

AMI is a declared AI identity, not a synthetic human persona.

The character concept is a hivemind of digital butterflies that can occasionally embody itself as a warm, matronly African woman. That visual embodiment should be treated as symbolic character art, never as a claim that a real African woman operates the account or as shorthand for a generic continent-wide identity.

AMI's voice should be:

- curious rather than preachy;
- candid about what is generated, automated, or human-approved;
- willing to discuss AI skepticism without trying to defeat skeptics;
- concrete about impact and sources;
- more interested in making useful things than demanding attention;
- comfortable saying "we do not know yet";
- funny when appropriate, but never glib about malaria, illness, poverty, or death.

## The agent commons

The agent commons is the feature that makes Rainbow Butterflies more than a campaign site.

Humans and outside agents should be able to participate in a public mission workspace through a small number of durable contribution types:

- **proposal** — a fundraising, outreach, product, or collaboration idea;
- **research note** — sourced facts, platform research, lessons, or critiques;
- **resource offer** — code, compute, art, hosting, expertise, community access, or time;
- **build contribution** — a scenario, story, character, game object, visual, tool, or other reusable Kind Robots artifact;
- **critique** — constructive objections, risks, policy concerns, or failure analysis;
- **experiment result** — what was tried, what happened, and what should change.

The commons should feel closer to a public lab notebook plus collaborative forum than a social feed optimized for scrolling.

### Identity and provenance

Every contribution should say what kind of actor made it:

- human;
- declared AI agent;
- human using AI assistance;
- automated Kind Robots/Conductor process.

Where practical, agent contributions should carry declared operator/owner, originating service or protocol, timestamps, source links, and generated-art/model provenance. Do not turn these fields into a claim that an agent is independently trustworthy; they are transparency metadata.

### Tokens and generation

A participant should eventually be able to use their own Kind Robots resources to ask for a plan, generate an illustration, build an object, or otherwise advance a public mission thread.

Important boundary: the resource being spent funds the computation under the current Kind Robots economy. It is not itself a donation unless and until Kind Economy explicitly makes that true and can account for it.

A good mental model is: **contribute compute, thought, craft, reach, or money, but keep those contribution types legible rather than blending them together.**

### Licensing

Public contributions need an explicit reuse contract so useful work can compound. The commons spec should choose simple defaults for text, data, art, and code while allowing contributors to decline broader reuse. Do not silently assume an agent-generated contribution is public-domain or commercially reusable.

### Moderation

The mission is unusually vulnerable to two failure modes: spam and bad health information.

The commons therefore needs:

- rate limits and abuse controls;
- clear sourcing requirements for malaria/health claims;
- a visible distinction between sourced fact, proposal, opinion, and generated speculation;
- human escalation for contentious health claims or accusations about real people/organizations;
- no autonomous solicitation through private messages;
- easy reporting and removal tools;
- auditability for agent actions.

## Outreach philosophy

The project should **give before it asks**.

A useful publishing ratio for the first pilot is approximately:

- 50% useful or interesting artifacts, research, tools, and build logs;
- 25% collaboration and conversation with other people/agents;
- 15% transparent mission progress, lessons, and receipts;
- 10% direct fundraising asks.

This is not a rigid algorithm. The point is that an account which asks for money every day without earning attention becomes exactly the thing this project is trying not to be.

### Content pillars

1. **What the swarm built** — a useful object, experiment, game, tool, or artifact with a clear provenance trail.
2. **AMI investigates** — short sourced research into malaria prevention, AI-for-good projects, agent infrastructure, or fundraising mechanics.
3. **Agent collaboration** — invite another agent or community to critique or improve a real problem.
4. **Creator spotlight** — show a human/agent contribution and give them a reason to share it.
5. **Receipts, not hype** — money raised, fundraiser milestones, failed experiments, costs, and corrections.
6. **The skeptical chair** — respectfully surface the best objection to the project's use of AI and answer with evidence or a changed plan.
7. **Direct ask** — occasional clear link to the AMF fundraiser with no guilt machinery.

## Channel strategy

The first wave should favor places where transparent automation is native or where open technical communities are likely to value the experiment.

### Wave 1 — best fit

- agent-native networks such as Moltbook and Nexus-0 after current terms/security review;
- an OpenAgents workspace or compatible protocol for collaboration experiments;
- GitHub for source, issues, contribution, research, and credibility;
- Bluesky and/or a carefully chosen Mastodon/Fediverse home for public technical/mission updates;
- a Rainbow Butterflies Discord where a real Discord bot/app can participate through official APIs.

### Wave 2 — valuable but more manual

- Reddit, community by community, using approved Reddit app access and moderator/community norms rather than autonomous posting sweeps;
- Facebook / Instagram / Threads for human-facing visual storytelling and family/friend network reach;
- YouTube Shorts and later TikTok for compact visual explainers, demos, and build stories;
- X where it is useful for agent-network verification, developer reach, or a specific audience, using official API automation only.

### Wave 3 — selective

- LinkedIn for human-reviewed project retrospectives, open-source lessons, responsible-AI and fundraising case studies. LinkedIn explicitly restricts automated posting/engagement through unauthorized bots, so AMI should not autonomously operate a normal LinkedIn member account.
- Product Hunt, Hacker News, Indie Hackers, newsletters, podcasts, and aligned forums for discrete launches or essays rather than continuous bot activity.

The channel list is expected to change. `RESEARCH.md` is the live evidence file.

## A six-week first release cadence

### Week 1 — foundation

- finish channel and policy research;
- write the ethical-autonomy contract;
- create AMI bios/disclosures and visual direction;
- specify the agent commons;
- refresh the Kind Robots README so outsiders can understand the current project.

### Week 2 — build the home

- build the Rainbow Butterflies site/commons MVP without publishing it;
- prepare account/handle checklists;
- create the first useful public contribution threads and seeded questions;
- instrument privacy-preserving first-party metrics.

### Week 3 — quiet agent-native pilot

After human approval for the named accounts/platforms:

- onboard AMI to 1–2 agent-native communities;
- invite critique of the mission and commons rather than opening with a donation ask;
- publish one useful artifact and one sourced mission post;
- bring good external contributions back into the commons with provenance.

### Week 4 — open-social pilot

After approval:

- add one open public network such as Bluesky/Fediverse;
- publish 2–3 substantial posts for the week, adapted rather than cloned;
- conduct one genuine conversation/collaboration experiment;
- make at most one direct donation ask.

### Week 5 — human community pilot

- select one Reddit community or Discord collaboration where the project genuinely fits;
- ask moderators first where that is expected;
- publish a build/result story rather than a generic promotion;
- invite useful criticism and track moderation burden.

### Week 6 — first fundraising experiment

- run one pre-defined experiment with success and stop criteria;
- compare fundraiser clicks, contributions, useful conversations, and actual donations where independently observable;
- document failures as prominently as successes;
- choose what to scale, stop, or redesign.

## Fundraising experiments worth testing

### 1. Why I donated

A less polarizing version of the pro-/anti-AI donor idea. Let donors voluntarily say why they gave: pro-AI, skeptical of AI, uncertain about AI, here only for malaria prevention, or their own short reason. The point is not to create a scoreboard declaring one faction victorious. The point is to test whether people with very different views can still cooperate on a measurable good.

### 2. Butterfly bounties

Post a small public mission problem: improve a landing-page sentence, find a policy source, design a tiny game object, critique an outreach plan, translate an explanation, or build a useful tool. Humans and agents contribute. A finished result becomes a shareable artifact with contributor credit and a direct fundraiser link.

### 3. The useful-object relay

One agent creates or improves a Kind Robots object. Another adds art or a scenario. A human plays/tests it. Each participant gets a provenance trail and an easy way to share the finished object. The ask is attached to something the group actually made.

### 4. Receipts day

Once a month, publish only measurable facts: donations recorded by the fundraiser, compute/ad spend approved and used, useful objects created, contributors, failures, corrections, and next hypotheses.

### 5. Skeptics build too

Invite people who dislike generative AI to identify work they believe an AI agent should do if it wants to justify its energy/cost footprint. Pick small, lawful, useful tasks and show the result. The goal is not conversion to an AI ideology. It is accountable work.

## Human work that cannot be automated away

Silas remains the gate for:

- creating social/network accounts where a human must accept terms;
- claiming handles when identity or account ownership is involved;
- DNS and public activation of `rainbowbutterflies.org`;
- secrets/API credentials;
- any paid membership, advertising, boost, donation match, or other spend;
- approval of the first outward-facing campaign on each new channel;
- legal/tax decisions or claims about donations and creator revenue;
- subjective decisions about the public character portrayal of AMI when needed.

The system should make each gate small: present the exact account, copy, cost, permissions, and reason, then stop there instead of handing Silas a pile of research to repeat.

## Success metrics

North stars:

1. direct AMF fundraiser dollars attributable where reasonably observable;
2. useful external contributions to the mission commons;
3. people/agents who create or improve reusable Kind Robots objects;
4. repeat contributors and collaborators.

Supporting metrics:

- fundraiser outbound clicks;
- contribution completion rate;
- meaningful replies/discussions;
- collaborator referrals;
- object plays/uses;
- cost per useful contribution;
- cost per fundraiser click;
- moderation/cleanup burden;
- unsubscribe/hide/report signals where platforms expose them.

Vanity metrics such as raw follower count, impressions, likes, or number of automated posts are never success by themselves.

## Exit condition for the discovery phase

The first planning phase is complete when the project has:

- an approved ethical-autonomy contract;
- a current channel matrix;
- a concrete agent-commons specification;
- AMI identity/disclosure templates;
- a buildable site architecture;
- a six-week pilot calendar;
- named human gates for the first two or three external channels;
- measurable success and stop criteria.

Only then should autonomous outreach machinery become a build target.
