# Rainbow Butterflies autonomous continuation contract

Rainbow Butterflies is an autonomous finite software project. The project should keep advancing through reversible internal work without repeatedly asking Silas whether to continue.

## Standing direction

When a worker completes a task, it should immediately leave the project in a state where another worker can identify the next useful, bounded task from the roadmap.

Do **not** treat an empty `ready` queue or completion of the currently visible milestone as a reason to stop and ask for general permission. Instead:

1. Reconcile the roadmap against the project `goal`, `COMMONS-SPEC.md`, current product state, and latest human direction.
2. Add or refine bounded follow-up tasks when real implementation gaps remain.
3. Keep dependencies explicit so blocked work does not stall unrelated progress.
4. Prefer existing Kind Robots infrastructure over parallel Rainbow systems unless a concrete limitation is documented.
5. Continue research, drafting, coding, tests, previews, documentation, and reversible merges autonomously.
6. Stop only at a genuine human gate or when the goal has actually been met and the project is ready for final acceptance.

## Human gates

Human approval is still required for concrete outward-facing or irreversible actions, including:

- creating or claiming third-party accounts or handles;
- accepting third-party terms on Silas's behalf;
- public publishing or sending outreach;
- production DNS/domain activation;
- secrets or production credentials that require human entry or disclosure;
- paid memberships, advertising, purchases, donation matching, or other spend;
- destructive production data changes;
- legal/tax representations;
- changing the promised Kind Economy revenue split or claiming paid token use funds malaria before that accounting is implemented and verified;
- final subjective approval of AMI portrayals when the roadmap explicitly asks for it.

A gate on one task does not pause the whole project. Workers should continue other ready reversible tasks.

## Definition of autonomous progress

Progress means delivering useful product or evidence, not generating endless roadmap polish. New tasks should correspond to a real gap such as:

- missing API/auth capability;
- missing forum/community UX;
- missing moderation or provenance protection;
- missing object/generation integration;
- missing tests or responsive/accessibility verification;
- missing mission/content/research artifacts needed before a human-gated launch;
- evidence from a pilot that requires a specific redesign.

Do not manufacture busywork after the goal is satisfied.

## Current build spine

The forum-first commons should advance in this order where dependencies require it:

1. Rainbow application shell and Kind Robots BFF contract.
2. Scoped per-agent Kind Robots credentials.
3. Versioned Kind Robots forum API facade.
4. Human Kind Robots single-sign-on handoff.
5. Forum browsing, thread creation, and replies.
6. Explicit human/AI authorship and operator/Bot provenance.
7. Connect-an-Agent key management and machine-readable discovery.
8. Kind Robots object embeds and opt-in generation/resource use.
9. Moderation, flags, rate limits, duplicate detection, and audit surfaces.
10. Responsive/accessibility/security verification of the complete MVP.

The roadmap remains canonical for task status; this document is the standing continuation rule and architectural sequencing reference.
