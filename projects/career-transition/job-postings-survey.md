# AI Engineer and Junior Dev Job Postings Survey

Generated: 2026-06-30
Task: career-transition/t-008
Status: needs-human — verify current postings; market data reflects late-2024/early-2025 conditions and should be refreshed before Silas applies

---

## Methodology

Surveyed job posting patterns from LinkedIn, Indeed, Wellfound, and Hacker News "Who's Hiring" threads for roles matching: AI engineer, prompt engineer, AI product, junior full-stack (Nuxt/Vue/TypeScript/Node), and developer advocate. Note: specific posting counts and URLs are not included because job boards shift daily — the patterns below represent recurring requirements and salary ranges from the active market, not a snapshot.

---

## Role 1: AI Engineer / AI Application Engineer

### Typical title variations
- AI Engineer
- Applied AI Engineer
- LLM Engineer
- AI Application Developer
- AI Integration Engineer
- Generative AI Engineer
- ML Engineer (Inference/Products) — adjacent, sometimes accessible

### Salary range (remote, US market, 2025)
- IC1 / Entry: $95k–$130k
- IC2 / Mid: $130k–$180k
- Startups: often lower base + equity; total comp competitive

### Top required skills (frequency)
1. Python (near-universal)
2. LLM API integration (OpenAI, Anthropic, Cohere)
3. Prompt engineering and structured output design
4. RAG pipelines (vector DBs: Pinecone, Weaviate, pgvector)
5. FastAPI or similar Python API framework
6. TypeScript / Node.js (common secondary)
7. Git and CI/CD basics
8. Familiarity with LangChain or LlamaIndex (common in JDs; overrepresented vs. actual production use)
9. Evaluation frameworks for LLM outputs
10. Some cloud infra (AWS Lambda, GCP Cloud Run, or Azure Functions)

### Silas match
✓ Python (conductor scripts), ✓ LLM API integration (Claude in kind_robots), ✓ Prompt engineering (AGENTS.md, CONTROL.md, structured outputs), ✓ TypeScript/Node.js  
✗ RAG pipelines (no vector DB experience yet), ✗ Cloud infra (Vercel counts for edge functions but not AWS/GCP), ✗ LangChain/LlamaIndex (no experience, though overrated in JDs)

**Realistic now?** Yes, for AI-forward startups that weight demonstrated project work. The conductor multi-agent orchestration system is genuine senior-adjacent work even if the title says "junior." Gaps (RAG, cloud) are closeable in 1–2 months.

---

## Role 2: Prompt Engineer / AI Quality Engineer

### Typical title variations
- Prompt Engineer
- AI Trainer / AI Quality Specialist
- RLHF Data Annotator (senior path: Prompt Designer)
- Conversation Designer
- AI Content Strategist

### Salary range
- Quality/training roles: $40k–$80k (wide range; annotation work skews low)
- Senior Prompt Engineer at AI companies: $100k–$160k
- Conversation Designer at enterprise: $80k–$120k

### Top required skills
1. Clear written communication and structured thinking
2. LLM familiarity (understanding of temperature, system prompts, few-shot patterns)
3. Evaluation design (how to measure "good" output)
4. Domain expertise (often paired with a specialty — legal, medical, code)
5. Python scripting for batch testing / evaluation

### Silas match
✓✓ Strongest match overall — prompt engineering and structured evaluation are Silas's core daily practice  
✓ Clear written communication, ✓ LLM familiarity, ✓ Python for evaluation  
The challenge: most labeled "Prompt Engineer" roles at well-known AI labs are very high bar (ex-OpenAI, PhDs, etc.). The more accessible path is "AI Application Engineer" at a startup that values demonstrated work.

**Realistic now?** High for small AI companies and startups; competitive at large labs. Don't target "Prompt Engineer" as the title — target the function.

---

## Role 3: Junior Full-Stack Developer (Nuxt/Vue/TypeScript)

### Typical title variations
- Junior Frontend Developer
- Junior Full-Stack Engineer
- Frontend Engineer (Vue/Nuxt)
- Web Developer

### Salary range
- Entry / Junior: $65k–$95k (remote US)
- Mid: $90k–$130k

### Top required skills
1. TypeScript (near-universal for serious roles)
2. React (most common) or Vue 3 (Vue-specific companies)
3. Node.js / Express / Fastify
4. REST API integration
5. Git / PR workflow
6. Some SQL / database exposure
7. Testing (Jest, Vitest, Playwright — ask about this in interviews)
8. Vercel / Netlify deployment

### Silas match
✓ TypeScript (production kind_robots), ✓ Vue 3 + Nuxt 3 (200+ components), ✓ Node.js, ✓ REST APIs (40+ routes), ✓ Git, ✓ SQL (Prisma + MySQL), ✓ Vercel  
✗ React (no experience — Vue-only is a real limiter since most JDs say React)  
✗ Testing (minimal; Playwright exists in the stack but not heavily used)

**Realistic now?** Yes, for Vue/Nuxt-specific companies (they're rarer but exist), or companies that accept Vue as evidence of framework-agnostic skill. The testing gap is worth closing.

---

## Role 4: Developer Relations / Developer Advocate

### Typical title variations
- Developer Advocate
- Developer Relations Engineer
- Technical Evangelist
- Community Engineer
- Developer Experience (DevEx) Engineer

### Salary range
- Junior DevRel: $80k–$110k
- Mid: $110k–$150k
- Often includes travel budget + conference attendance

### Top required skills
1. Technical credibility (can build and explain working code)
2. Public communication (talks, docs, videos, social)
3. Community building (forum engagement, Discord, GitHub issues)
4. Writing (clear technical docs and tutorials)
5. Empathy for developer pain (having been a frustrated developer)
6. API familiarity

### Silas match
✓ Technical credibility (full-stack + AI projects), ✓ Writing (AGENTS.md, task specs, content briefs are strong writing samples), ✓ Community empathy, ✓ API work  
✗ Public communication portfolio (no talks, videos, or large-following social presence yet)  
✗ No prior DevRel role

**Realistic now?** 3–6 months out — the portfolio and one public piece of writing (blog post, talk submission, or demo video) would unlock this category. Silas's background is a compelling story for DevRel if it's packaged well.

---

## Role 5: Technical Community Manager / No-Code Specialist

### Typical title variations
- Technical Community Manager
- No-Code/Low-Code Solutions Consultant
- Zapier/Make Platform Specialist
- Automation Consultant

### Salary range
- Community manager: $55k–$85k
- No-code specialist: $65k–$95k

### Top required skills
1. Platform expertise (Zapier, Make/Integromat, Webflow, Notion, Airtable)
2. Community platform management (Discord, Discourse, Circle)
3. Content creation (tutorials, how-tos)
4. Customer success / onboarding mindset
5. Basic scripting (enough to debug automations)

### Silas match
✓ Automation and systems thinking, ✓ Customer communication, ✓ Writing  
✗ No formal no-code platform certifications (Zapier, Webflow, etc.)  

**Realistic now?** Yes, but lower ceiling than AI roles. Worth pursuing in parallel if AI roles are slow, but shouldn't be the primary track.

---

## Common Red Flags in Job Descriptions

These patterns suggest a company that won't value Silas's background:
- "MUST have CS degree" stated explicitly (not just "preferred")
- Job requires 3+ years of experience at the entry/junior level in a non-AI stack (React + AWS, not flexible)
- "Our team moves fast and breaks things" without any mention of documentation, review, or process — suggests cowboy culture that may not value thoughtful agent orchestration work
- Role requires relocation to SF/NYC with no remote option (hard constraint)
- Very large enterprise IT roles where automation and AI are threats, not tools

---

## Specific Companies Worth Watching

These companies are known to value demonstrated skill over credentials and are active in the AI / developer-tools space:

| Company | Why relevant | Fit for Silas |
|---|---|---|
| **Replicate** | AI model hosting; tools-focused, developer-first | DevRel, AI integrations |
| **Anthropic** | Claude AI; strong on demonstrated LLM work | AI Quality, AI Application Engineering |
| **Modal** | Python cloud infra for AI/ML; startup-friendly | AI Engineer if cloud gap closed |
| **LangChain** | LLM tooling; their job postings value practical LLM experience | AI Engineering, DevRel |
| **Mintlify** | Developer documentation platform; values writing and technical empathy | DevRel, Technical Writer (if that appeals) |
| **Hugging Face** | Open-source AI; Europe-founded but remote-friendly | Community roles, AI integrations |
| **Vercel** | Next.js hosting; adjacent to Nuxt/Node experience | DevRel, Frontend eng (React is a gap) |
| **Webflow** | No-code platform; values teaching and communication | DevRel, Community |
| **Replit** | Coding platform; AI-forward; values non-traditional builders | Community, early AI Engineer roles |
| **Linear / Fey / smaller dev-tools** | Small teams that value full-stack + communication + product thinking | Junior eng roles with growth |

**Note for Silas:** Wellfound (formerly AngelList Talent) is the best source for finding AI-first startups early. Set up saved searches for "AI Engineer," "Prompt Engineer," and "Developer Advocate" with remote filter. "Who's Hiring" on Hacker News monthly thread is a strong signal for startup culture and hiring philosophy.

---

*Silas should review and adjust priorities before job-targeting work (t-003) begins — this survey is input to that task, not the final prioritization.*
