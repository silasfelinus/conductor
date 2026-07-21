# Job Targeting — Role Types and Companies to Watch

Generated: 2026-07-21
Task: career-transition/t-003
Status: needs-human — Silas should steer which roles to prioritize before downstream tasks (cover letters, portfolio writeups, interview prep) proceed
Input: projects/career-transition/skills-map.md (approved 2026-07-01)

---

## How to read this

For each of the 5 target role types from `notes_from_silas`, in the order given there. Salary figures are current remote US-market data pulled live in July 2026 (see Sources at the end) — treat them as directional ranges, not quotes for any specific listing.

---

## Role 1: AI Engineer / AI Wrangler / Prompt Engineer / AI Product

### Title variations seen in postings
AI Engineer, Applied AI Engineer, LLM Engineer, AI Application Developer/Engineer, AI Integration Engineer, Generative AI Engineer, Prompt Engineer, AI Product Engineer/Manager (hybrid roles).

### Realistic salary range (remote, US, 2026)
- Entry/junior, no prior title in the field: **$80k–$130k** (survey-average entry-level prompt engineer pay was ~$97k; junior "no prior AI job" listings commonly run $60k–$95k, but Silas's 25 years of adjacent practitioner experience should place him above the bare-entry band)
- Mid-level with a shipped portfolio: **$130k–$180k**
- Outlier: Anthropic has posted a "Prompt Engineer and Librarian" role at $335k — not representative, but shows the ceiling exists for the right specialist framing (communication + judgment, not a CS pedigree)

### Core skills hiring managers screen for
- **Has:** comfort with a major LLM API (Claude — direct, deep experience), prompt engineering fundamentals, understanding of context windows/tokens, multi-agent orchestration design (conductor is a genuinely rare, concrete example most candidates don't have)
- **Missing/thin:** a named evaluation framework (e.g., promptfoo, braintrust) — worth naming conductor's own TALKBACK/LEARNING.yaml ledger as a bespoke eval-and-feedback loop in interviews; no RAG-pipeline-specific project (conductor's dependency resolution and multi-agent state machine is adjacent but not a RAG demo)

### Company types most likely to hire this background
AI-first startups, developer-tools companies building on top of LLM APIs, agencies doing AI implementation consulting, and — per Anthropic's own hiring pattern above — AI labs themselves for evangelist/community-facing AI roles that value communication over ML depth.

### Companies worth watching
1. **Anthropic** (Claude for Startups / Claude Partner Network ecosystem) — not just as an employer directly, but the $100M partner network (Infosys, KPMG, Stainless, etc.) is now hiring implementation/AI-engineer talent across dozens of partner firms
2. **Vercel** — AI SDK team, Nuxt/Vue-adjacent (Next.js sibling ecosystem), remote-friendly
3. **Supabase** — born-remote (180+ people, 35+ countries), actively building AI/vector-search features, portfolio-first hiring signals
4. **PostHog** — remote, engineering-culture-forward, hiring product engineers and technical roles broadly
5. **Retool / n8n / Zapier / Make** — all building AI-agent and LLM-integration features into no-code platforms; directly overlaps conductor's orchestration experience
6. Smaller AI-agent startups building on the Claude Partner Network (Stainless-adjacent SDK/tooling shops) — worth periodic HN "Who's Hiring" scans since this is a fast-moving, newly-forming layer

### Realistic timeline
**Now**, with the right framing. This is the strongest-fit role type given 25 years of AI practitioner experience plus a genuinely unusual live artifact (conductor) to demo. The main gap (no named eval framework, no RAG demo) is closeable in weeks by adding a lightweight eval to an existing project, not months.

---

## Role 2: Junior Full-Stack Dev (Nuxt/Vue/TypeScript/Node)

### Title variations seen in postings
Junior Full-Stack Developer, Frontend Developer (Vue/Nuxt), Full-Stack Engineer (Node/TypeScript), Web Application Developer.

### Realistic salary range (remote, US, 2026)
- Vue.js remote average: **~$59/hr** (~$123k/yr full-time equivalent), range roughly $49–$68/hr
- Nuxt.js specifically: **~$58/hr** average, $49–$64/hr range
- Junior-titled roles typically land at the lower end of these bands, but kind_robots (200+ Vue SFCs, Prisma, Nuxt server routes, CI) is a stronger portfolio than most "junior" applicants bring — realistic target **$75k–$100k** rather than bottom-of-band

### Core skills hiring managers screen for
- **Has:** Vue 3/Nuxt 3 (strong), TypeScript (strong), Prisma (strong — many junior candidates haven't touched an ORM this deeply), REST API design, Git/GitHub workflow, CI (GitHub Actions)
- **Missing/thin:** formal testing culture (unit tests, TDD) — flagged in skills-map as closeable; no cloud infra beyond Vercel serverless — most junior Nuxt roles don't require this, so lower priority to close

### Company types most likely to hire this background
Small-to-mid product companies running Vue/Nuxt stacks, agencies building client Nuxt sites, and any of the dev-tools companies above that also need frontend engineers (not just AI specialists).

### Companies worth watching
1. **Nuxt.com's own enterprise/jobs board** (nuxt.com/enterprise/jobs) — companies that specifically use Nuxt list openings there, a self-filtering source
2. Vercel, Supabase (again — both have Vue/Nuxt-adjacent surface area even though their core stacks lean React)
3. Small agencies/studios doing client Nuxt work (regional, often more open to nontraditional backgrounds and remote junior hires than large orgs)
4. Any startup already in the AI-tooling list above that needs a generalist full-stack hire rather than an AI specialist

### Realistic timeline
**Now.** This is the most immediately defensible role type on raw technical evidence — kind_robots is a real, deployed, non-trivial Nuxt/Prisma app. The main work is packaging (portfolio writeup, README, demo video), not skill-building.

---

## Role 3: Developer Relations / Developer Advocate

### Title variations seen in postings
Developer Advocate, DevRel Engineer, Developer Relations Manager, Community Engineer, Technical Evangelist.

### Realistic salary range (remote, US, 2026)
- Junior developer advocate average: **~$116k** (based on active junior-titled remote postings)
- Junior developer relations (broader title) average: **~$143k**
- Developer advocate overall range: **$41.5k–$170k**, average ~$86k — wide spread driven by company size/stage
- Read: junior-titled DevRel postings currently skew higher than the "average across all levels" figure, likely because DevRel titles compress fast at small companies — treat $90k–$130k as the realistic junior band

### Core skills hiring managers screen for
- **Has:** public-facing communication under pressure (11 years casino dealing — genuinely rare, concrete evidence), improvisation (street performing), technical depth to actually build the demos being advocated for (kind_robots + conductor), writing ability (this very roadmap/TALKBACK corpus is a writing sample)
- **Missing/thin:** no public speaking reel, no existing content (blog posts, conference talks, YouTube) — this is the single biggest gap for this role type and the most fixable one (a demo video or two would close most of it)

### Company types most likely to hire this background
Dev-tools companies with active developer communities (exactly the AI-agent/no-code list above), open-source-adjacent companies, and API-first startups that need someone to explain their product to other developers.

### Companies worth watching
1. **Anthropic** — the "Claude Evangelist, Startups" role spotted this cycle is precisely this role type, aimed at exactly this kind of nontraditional-but-technical candidate; worth monitoring their careers page even if this specific req isn't a fit
2. Supabase, PostHog, n8n, Vercel — all have active DevRel/community functions per their remote-first culture signals
3. Smaller, earlier-stage AI-agent startups building on Claude/OpenAI APIs — DevRel is often the first non-founder hire at this stage, more accessible to a nontraditional candidate than at a mature company

### Realistic timeline
**3 months with portfolio work** — specifically, recording 1-2 short demo videos of kind_robots or conductor (a real, working multi-agent system is genuinely differentiated content) would move this from "plausible" to "strong."

---

## Role 4: Technical Community Manager

### Title variations seen in postings
Community Manager (Technical/Developer-focused), Developer Community Lead, Community Engineer.

### Realistic salary range (remote, US, 2026)
- Community Manager (remote, all industries): average **~$98k**, range **$36k–$162k**
- Technical/developer-focused community roles trend toward the middle-to-upper part of this band given the specialized audience

### Core skills hiring managers screen for
- **Has:** empathy-driven communication (adult support work), reading audiences live (street performing), patient technical communication with non-technical users (grade-school IT admin), systematic routine-building (runbook/process instincts)
- **Missing/thin:** no track record moderating/growing an actual online community (Discord, forum, GitHub Discussions) — closeable by simply starting to participate visibly in a community Silas already touches (Nuxt, Vue, or an AI-agent Discord)

### Company types most likely to hire this background
Same dev-tools/AI-agent list as Roles 1 and 3 — community manager and DevRel roles often sit on the same team and get posted by the same companies.

### Companies worth watching
Same short-list as Role 3 (Supabase, PostHog, n8n, Anthropic-ecosystem startups) — at this company size/stage, "community manager" and "developer advocate" postings frequently overlap or get combined into one req.

### Realistic timeline
**3 months with portfolio work**, same gating factor as Role 3: visible community participation is the missing evidence, not a skill gap.

---

## Role 5: No-Code/Low-Code Platform Specialist

### Title variations seen in postings
No-Code Automation Specialist, Low-Code Developer, Automation Engineer, Workflow Automation Specialist.

### Realistic salary range (remote, US, 2026)
- No-code automation specialist: **$65k–$130k**, average ~$107k
- Low-code developer: average **~$103k**, range $77.6k–$138.8k

### Core skills hiring managers screen for
- **Has:** REST API and webhook fundamentals (strong, via kind_robots' 40+ API routes), JSON/data transformation (strong, via conductor's entire YAML-driven state machine), AI API integration (strong), database basics (strong via Prisma)
- **Missing/thin:** direct hands-on time in a named no-code platform itself (n8n, Zapier, Make, Retool) — Silas's skills are the *engineering* skills underneath these platforms but not necessarily platform-specific UI fluency; likely closeable in days/weeks given the underlying competence is already there

### Company types most likely to hire this background
The no-code/automation platform vendors themselves (they hire people who understand both the platform and the API layer it wraps), plus any company using these tools internally for an ops/automation role.

### Companies worth watching
1. **n8n** — open-source-friendly, remote-friendly team, workflow-automation core product
2. **Zapier** — long-standing remote-first culture, large automation user base
3. **Retool** — internal-tools/low-code platform, values engineers who understand the underlying app-building problem
4. **Make** (formerly Integromat) — same category as n8n/Zapier

### Realistic timeline
**Now, for platform-vendor engineering roles** (the underlying skills transfer directly); **6+ months** if targeting a pure "citizen automation" role at a non-vendor company, since those postings often screen for platform-specific certifications Silas doesn't have yet.

---

## Cross-role summary

| Role | Timeline | Best current evidence | Biggest gap |
|---|---|---|---|
| AI Engineer / Prompt Engineer | Now | conductor (multi-agent orchestration) | Named eval framework, RAG demo |
| Junior Full-Stack (Nuxt/Vue) | Now | kind_robots (200+ SFCs, Prisma, CI) | Testing culture, packaging/portfolio writeup |
| Developer Relations / Advocate | 3 months | Communication background + real projects to demo | No public speaking/content reel yet |
| Technical Community Manager | 3 months | Empathy/communication background | No visible community-moderation track record |
| No-Code/Low-Code Specialist | Now (vendor) / 6+ mo (non-vendor) | API/data/automation engineering underneath conductor | Platform-specific UI hands-on time |

**Recommended sequencing for Silas to consider:** Role 1 (AI Engineer) and Role 2 (Junior Full-Stack) are both "now" and share the same portfolio evidence (kind_robots + conductor) — a single strong portfolio writeup and resume could target both simultaneously. Roles 3 and 4 share the same 3-month gap (visible public content/community presence) and could be closed by the same handful of actions (demo videos, community participation). Role 5 is the most standalone — worth pursuing opportunistically at the vendor companies listed rather than as a primary track, unless Silas has a particular interest in workflow-automation tooling specifically.

---

*This document needs Silas's review before cover-letter (t-006), portfolio writeup (t-005), or interview-prep (t-007) work proceeds — those tasks are `waiting` on this one.*

## Sources

- [$43-$43/hr Remote Ai Prompt Engineer Jobs Hiring Now — ZipRecruiter](https://www.ziprecruiter.com/Jobs/Remote-Ai-Prompt-Engineer)
- [Remote AI Jobs That Pay $100K+ in 2026](https://abhyashsuchi.in/remote-ai-jobs-that-pay-100k-us-uk-canada/)
- [How To Become A Prompt Engineer In 2026 (No Degree) - Classes Place](https://classesplace.com/how-to-become-prompt-engineer-2026/)
- [1,127 ai prompt engineer Jobs in Remote, July 2026 | Glassdoor](https://www.glassdoor.com/Job/remote-ai-prompt-engineer-jobs-SRCH_IL.0,6_IS11047_KO7,25.htm)
- [Is Being a Self-Taught Developer Still Viable in 2026?](https://www.inapps.net/blog/is-being-a-self-taught-developer-still-viable)
- [Why Self-Taught Developers Could Be Your Company's Secret Weapon — CoderPad](https://coderpad.io/blog/hiring-developers/why-you-should-hire-self-taught-developers/)
- [293 developer relations Jobs in Remote, July 2026 | Glassdoor](https://www.glassdoor.com/Job/remote-developer-relations-jobs-SRCH_IL.0,6_IS11047_KO7,26.htm)
- [Developer Relations Careers and Salary Guide 2026 | JobRise Blog](https://jobrise.io/en/blog/developer-relations-careers-guide-2026/)
- [$49-$75/hr Nuxt Js Jobs (NOW HIRING) — ZipRecruiter](https://www.ziprecruiter.com/Jobs/Nuxt-Js)
- [Nuxt Jobs — nuxt.com/enterprise/jobs](https://nuxt.com/enterprise/jobs)
- [No-Code Automation Specialist: Salary & Hire Guide 2026 — Kreante](https://www.kreante.co/post/the-role-of-an-nocode-automation-specialist-key-skills-and-responsibilities)
- [Low Code Developer: Average Salary & Pay Trends 2026 | Glassdoor](https://www.glassdoor.com/Salaries/low-code-developer-salary-SRCH_KO0,18.htm)
- [2026 Community Manager Salary in Remote | Built In](https://builtin.com/salaries/us/remote/community-manager)
- [Applied AI Claude Evangelist, Startups @ Anthropic — General Catalyst Job Board](https://jobs.generalcatalyst.com/companies/anthropic/jobs/79002337-applied-ai-claude-evangelist-startups)
- [Anthropic invests $100 million into the Claude Partner Network](https://www.anthropic.com/news/claude-partner-network)
- [Supabase Jobs - Remote 4 Day Week Jobs (2026)](https://4dayweek.io/company/supabase/jobs)
- [Work From Anywhere jobs at Supabase](https://www.realworkfromanywhere.com/companies/supabase)
