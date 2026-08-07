#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one occurrence, found {count}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def regex_once(path: str, pattern: str, repl: str, *, flags: int = 0) -> None:
    text = read(path)
    updated, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{path}: regex expected one match, found {count}: {pattern}")
    write(path, updated)


def ensure_goal(path: str, goal: str) -> None:
    text = read(path)
    head = text.split("milestones:", 1)[0]
    if re.search(r"^goal:\s*", head, re.MULTILINE):
        return
    match = re.search(r"^(kind:\s*[^\n]+\n)", text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"{path}: missing kind line")
    block = "goal: >\n" + "\n".join(f"  {line}" for line in goal.splitlines()) + "\n"
    text = text[: match.end()] + block + text[match.end() :]
    write(path, text)


def task_span(text: str, task_id: str) -> tuple[int, int]:
    match = re.search(rf"(?m)^(\s*)- id: {re.escape(task_id)}\s*$", text)
    if not match:
        raise RuntimeError(f"task {task_id} not found")
    indent = match.group(1)
    next_match = re.search(rf"(?m)^{re.escape(indent)}- id: \S+\s*$", text[match.end() :])
    end = match.end() + next_match.start() if next_match else len(text)
    return match.start(), end


def set_task_field(path: str, task_id: str, field: str, value: str) -> None:
    text = read(path)
    start, end = task_span(text, task_id)
    block = text[start:end]
    task_indent = re.match(r"^(\s*)- id:", block).group(1)  # type: ignore[union-attr]
    field_indent = task_indent + "  "
    pattern = rf"(?m)^{re.escape(field_indent)}{re.escape(field)}:\s*.*$"
    if re.search(pattern, block):
        block = re.sub(pattern, f"{field_indent}{field}: {value}", block, count=1)
    else:
        first_nl = block.find("\n")
        block = block[: first_nl + 1] + f"{field_indent}{field}: {value}\n" + block[first_nl + 1 :]
    write(path, text[:start] + block + text[end:])


def add_task_field_block(path: str, task_id: str, field: str, body: str) -> None:
    text = read(path)
    start, end = task_span(text, task_id)
    block = text[start:end]
    task_indent = re.match(r"^(\s*)- id:", block).group(1)  # type: ignore[union-attr]
    field_indent = task_indent + "  "
    if re.search(rf"(?m)^{re.escape(field_indent)}{re.escape(field)}:", block):
        return
    rendered = f"\n{field_indent}{field}: >\n" + "\n".join(
        f"{field_indent}  {line}" if line else "" for line in body.splitlines()
    ) + "\n"
    block = block.rstrip() + rendered + "\n"
    write(path, text[:start] + block + text[end:])


def set_milestone_field(path: str, milestone_id: str, field: str, value: str) -> None:
    text = read(path)
    milestones_start = text.index("milestones:")
    tasks_start = text.index("\ntasks:")
    section = text[milestones_start:tasks_start]
    match = re.search(rf"(?m)^(\s*)- id: {re.escape(milestone_id)}\s*$", section)
    if not match:
        raise RuntimeError(f"{path}: milestone {milestone_id} missing")
    indent = match.group(1)
    abs_start = milestones_start + match.start()
    next_match = re.search(rf"(?m)^{re.escape(indent)}- id: \S+\s*$", section[match.end() :])
    abs_end = milestones_start + (match.end() + next_match.start() if next_match else len(section))
    block = text[abs_start:abs_end]
    field_indent = indent + "  "
    pattern = rf"(?m)^{re.escape(field_indent)}{re.escape(field)}:\s*.*$"
    if not re.search(pattern, block):
        raise RuntimeError(f"{path}: milestone {milestone_id} lacks {field}")
    block = re.sub(pattern, f"{field_indent}{field}: {value}", block, count=1)
    write(path, text[:abs_start] + block + text[abs_end:])


def append_milestones(path: str, block: str, sentinel: str) -> None:
    text = read(path)
    if sentinel in text:
        return
    marker = "\ntasks:"
    index = text.index(marker)
    text = text[:index].rstrip() + "\n" + block.rstrip() + "\n" + text[index:]
    write(path, text)


def append_tasks(path: str, block: str, sentinel: str) -> None:
    text = read(path)
    if sentinel in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_override(slug: str, *, status: str | None = None, priority: str | None = None) -> None:
    path = "project-overrides.yaml"
    text = read(path)
    match = re.search(rf"(?ms)^  - slug: {re.escape(slug)}\n(?P<body>.*?)(?=^  - slug: |\Z)", text)
    if not match:
        raise RuntimeError(f"override {slug} not found")
    block = match.group(0)
    if status is not None:
        if not re.search(r"(?m)^    status:", block):
            raise RuntimeError(f"override {slug} has no status")
        block = re.sub(r"(?m)^    status:\s*[^\n#]+", f"    status: {status}", block, count=1)
    if priority is not None:
        if not re.search(r"(?m)^    priority:", block):
            raise RuntimeError(f"override {slug} has no priority")
        block = re.sub(r"(?m)^    priority:\s*[^\n#]+", f"    priority: {priority}", block, count=1)
    write(path, text[: match.start()] + block + text[match.end() :])


def reconcile_overrides() -> None:
    replace_once(
        "project-overrides.yaml",
        "# status:   active | paused | retired | finished",
        "# status:   active | continuous | paused | retired | finished",
    )
    replace_override("animation-manager", status="continuous", priority="low")
    replace_override("dream-cycle", status="continuous", priority="low")
    replace_override("newsfeed", status="finished")


def reconcile_davinci() -> None:
    path = "projects/davinci/roadmap.yaml"
    ensure_goal(
        path,
        "Ship a genuinely playable, visually coherent Da Vinci life simulator that has been\n"
        "tested on phone, tablet, and desktop, uses art throughout the run, and has verified\n"
        "art coverage for all 1,024 deterministic endings before the project is called finished.",
    )
    append_milestones(
        path,
        """  - id: m5
    title: "VERIFY — playtest the real experience across devices"
    weight: 20
    status: in-progress

  - id: m6
    title: "ART & POLISH — coherent styling, run art, and all 1,024 ending assets"
    weight: 30
    status: not-started
""",
        "- id: m5",
    )
    append_tasks(
        path,
        """  - id: t-017
    milestone: m5
    title: "Audit and playtest Da Vinci end-to-end on phone, tablet, and desktop"
    status: ready
    owner: null
    passes: 0
    stakes: reversible
    note: >
      The prior 16/16 task count proved backend/narration capability, not product completion.
      Use the current preview/production surface and the responsive-layout tooling to play a
      complete run at phone, tablet, and desktop widths. Record every hidden/unreachable
      control, broken transition, confusing state, empty/decorative region, and visual defect.
      Turn concrete findings into scoped follow-up tasks rather than declaring the project done
      because the old list ran out. This is the new completion-reconciliation entry point.

  - id: t-018
    milestone: m6
    title: "Audit actual art coverage for all 1,024 Da Vinci endings"
    status: ready
    owner: null
    passes: 0
    stakes: reversible
    note: >
      Verify the seeded LifeEnding/Milestone records against real delivered assets, not path
      strings or queued prompts. Produce exact counts for ending icons/heroes that exist,
      resolve to an image, are still queued, or are missing. Also inventory contextual art
      during the run itself. The expected universe is exactly 1,024 outcome keys.

  - id: t-019
    milestone: m6
    title: "Generate, distribute, and verify every missing Da Vinci ending asset"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-018
    note: >
      Consume t-018's exact missing list in bounded idempotent batches through the existing
      ArtJob pipeline. Do not create duplicate jobs for already-rendered or already-queued
      endings. Close only when all 1,024 endings have the required delivered art and the
      verifier reports zero gaps.

  - id: t-020
    milestone: m6
    title: "Integrate contextual art throughout the playable Da Vinci run"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-017
    note: >
      The narrator already proposes artPrompt but the old roadmap explicitly deferred
      LifeRunArt consumption. Add a coherent in-run art treatment so chapters, transitions,
      and the final ending do not feel like a text prototype wrapped around a finished API.
      Reuse shared Kind Robots art/provenance infrastructure; do not invent a parallel store.

  - id: t-021
    milestone: m6
    title: "Da Vinci visual style and interaction polish pass"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: [t-017, t-020]
    note: >
      Apply the Interface Vision sequence to this product: first make every state work, then
      make its controls/layout consistent with current kr-* primitives, then make it visually
      intentional. Verify phone/tablet/desktop with rendered preview geometry and screenshots.

  - id: t-022
    milestone: m5
    title: "FOR SILAS: visually accept the finished Da Vinci experience"
    status: waiting
    owner: silas
    passes: 0
    stakes: reversible
    gate_human: true
    approved_by_human: false
    depends_on: [t-019, t-021]
    note: >
      FOR SILAS: after the automated playtest, 1,024-ending art audit/generation, and polish
      tasks are complete, review a short phone/tablet/desktop screenshot set and play one run.
      TO APPROVE: confirm the experience now feels finished, or leave concrete visual/gameplay
      notes. This is the product-completion gate; 16/16 historical tasks was not one.
""",
        "- id: t-017",
    )


def reconcile_interface_vision() -> None:
    path = "projects/interface-vision/roadmap.yaml"
    ensure_goal(
        path,
        "Finish the entire user-facing Kind Robots front end in three explicit phases: make\n"
        "every reachable page work on phone/tablet/desktop with no hidden or unreachable UI;\n"
        "make the implementation consistent around shared kr-* primitives and responsive\n"
        "patterns; then make every surface visually polished enough for human beta acceptance.",
    )
    append_milestones(
        path,
        """  - id: m4
    title: "PHASE 1 — MAKE IT WORK: every reachable surface, every device class"
    weight: 40
    status: in-progress

  - id: m5
    title: "PHASE 2 — MAKE IT CONSISTENT: shared kr-* vocabulary and responsive composition"
    weight: 30
    status: not-started

  - id: m6
    title: "PHASE 3 — MAKE IT PRETTY: deliberate visual polish and human acceptance"
    weight: 30
    status: not-started
""",
        "- id: m4",
    )
    append_tasks(
        path,
        """  - id: t-102
    milestone: m4
    title: "Build the canonical reachable-surface and responsive acceptance inventory"
    status: ready
    owner: null
    passes: 0
    stakes: reversible
    note: >
      Enumerate every actually reachable user-facing route/surface from the current app/nav
      graph and assign phone/tablet/desktop checks to each. Use the Vercel preview responsive
      audit plus targeted browser verification; capture hidden/unreachable controls, clipped
      content, nested-scroll fights, duplicate headers, dead routes, and device-only failures.
      The inventory must be numeric and shrink-to-zero. Admin-only surfaces come last.

  - id: t-103
    milestone: m4
    title: "Drive Phase 1 responsive/functionality findings to zero"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-102
    note: >
      Work the t-102 inventory in scoped slices until every reachable page passes phone,
      tablet, and desktop geometry with no hidden/unreachable elements. Split findings into
      dedicated tasks when they are larger than one PR; keep this umbrella open until the
      authoritative counter is zero. Passing TypeScript is not evidence that a page works.

  - id: t-104
    milestone: m5
    title: "Drive live front-end consistency onto shared kr-* components and composition rules"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-103
    note: >
      Inventory live bespoke equivalents of the established kr-* layout, note, gallery,
      narrative, card, toolbar, pane, and art primitives. Migrate real reachable callers,
      consolidate duplicate implementations, and delete/park losers only after callers move.
      Preserve deliberately bespoke surfaces. Add or extend shrink-only ratchets so consistency
      cannot silently drift backward after this phase closes.

  - id: t-105
    milestone: m6
    title: "Polish every reachable Kind Robots surface page-by-page"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-104
    note: >
      This is the deliberately subjective third phase that prior work mostly skipped. Apply the
      chosen Storybook design language where appropriate: clean hierarchy, generous useful art,
      friendly controls, minimal container nesting, calm spacing, readable narrative/text areas,
      and intentional empty/loading/error states. Produce reviewable screenshots rather than
      closing from source inspection alone.

  - id: t-106
    milestone: m6
    title: "FOR SILAS: visual beta-readiness acceptance of the complete front end"
    status: waiting
    owner: silas
    passes: 0
    stakes: reversible
    gate_human: true
    approved_by_human: false
    depends_on: t-105
    note: >
      FOR SILAS: review a representative screenshot atlas covering the reachable front end at
      phone/tablet/desktop widths, plus any surfaces the automated audit marks unusual.
      TO APPROVE: confirm the site is visually ready for beta or identify pages that need another
      polish pass. Interface Vision is not finished merely because its previous 102 tasks closed.
""",
        "- id: t-102",
    )


def reconcile_academy() -> None:
    path = "projects/ai-art-academy/roadmap.yaml"
    replace_once(path, "autonomous: true", "autonomous: false")
    replace_once(
        path,
        "  This is the TEST RUN of the autonomous project initiative: Claude has full reign over\n"
        "  this project and art-styler.vue. Art generation via our backend is fully supported and\n"
        "  pre-approved. Escalate only actual human gates. Keep the project running even without\n"
        "  my input — when there's nothing to do, do a style pass, upgrade the roadmap, or\n"
        "  generate more art inspirations (never-idle rule, AGENTS.md).",
        "  The autonomous never-idle experiment ended 2026-08-07 by Silas direction. The Academy\n"
        "  is a finite active project, not a permanent continuous program. Its completion bar now\n"
        "  includes a polished accessible web experience plus installable/testable iOS and Android\n"
        "  Academy apps. Art generation remains internally authorized, but empty task queues trigger\n"
        "  scope reconciliation rather than invented continuous-improvement work.",
    )
    set_milestone_field(path, "m6", "title", '"Completed autonomous continuous-improvement experiment"')
    set_milestone_field(path, "m6", "status", "done")
    append_milestones(
        path,
        """  - id: m7
    title: "SHIP — polished accessible Academy on web, iOS, and Android"
    weight: 25
    status: in-progress
""",
        "- id: m7",
    )
    set_task_field(path, "t-010", "status", "done")
    set_task_field(path, "t-010", "recurring", "false")
    add_task_field_block(
        path,
        "t-010",
        "outcome_note",
        "Silas ended the Academy's never-idle experiment on 2026-08-07. The recurring lane had\n"
        "become a source of constant low-priority churn while finite product work remained.\n"
        "Existing completed lane history stays intact, but this task no longer rearms. Future\n"
        "Academy work must correspond to a finite roadmap gap, especially mobile delivery and\n"
        "verified front-end quality.",
    )
    append_tasks(
        path,
        """  - id: t-061
    milestone: m7
    title: "Audit the Academy mobile-delivery state and choose the smallest durable iOS/Android path"
    status: ready
    owner: null
    passes: 0
    stakes: reversible
    note: >
      No Academy iOS/Android implementation is documented in the current roadmap, and a repo/PR
      search on 2026-08-07 found no Academy-specific iOS, Android, or Capacitor delivery work.
      Audit the current Kind Robots app/mobile infrastructure before choosing architecture. Reuse
      an existing wrapper/PWA/native shell if one exists; otherwise propose the smallest maintainable
      approach that exposes the full Academy/remix experience without forking business logic.

  - id: t-062
    milestone: m7
    title: "Ship an installable/testable Android Academy app build"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-061
    note: >
      Implement the Android side of t-061's chosen shared delivery path. The build must expose the
      real Academy timeline/styles/remix flow, preserve authentication/maturity/accessibility rules,
      and be testable on an Android device/emulator. Public Play Store submission remains a separate
      outward-facing human gate.

  - id: t-063
    milestone: m7
    title: "Ship an installable/testable iOS Academy app build"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: t-061
    note: >
      Implement the iOS side of the same shared delivery path, keeping feature parity with Android
      and web. Produce a testable simulator/device build. App Store publication, certificates, and
      account/billing actions remain human-gated outward-facing steps.

  - id: t-064
    milestone: m7
    title: "Accessibility and cross-platform visual QA for Academy web/iOS/Android"
    status: waiting
    owner: null
    passes: 0
    stakes: reversible
    depends_on: [t-062, t-063]
    note: >
      Verify keyboard/screen-reader semantics where applicable, touch target sizing, reduced motion,
      image alt/provenance presentation, error/loading states, and the complete lesson/remix flow.
      Include phone/tablet/desktop web plus representative iOS/Android device sizes. Fix findings;
      do not close from source inspection alone.

  - id: t-065
    milestone: m7
    title: "FOR SILAS: visually accept Academy web, iOS, and Android builds"
    status: waiting
    owner: silas
    passes: 0
    stakes: reversible
    gate_human: true
    approved_by_human: false
    depends_on: t-064
    note: >
      FOR SILAS: review the polished Academy on web plus installable/testable iOS and Android builds.
      TO APPROVE: confirm the three surfaces feel finished or leave concrete product/visual notes.
      The Academy remains active until this acceptance and any resulting fixes are complete.
""",
        "- id: t-061",
    )


def reconcile_storefront() -> None:
    path = "projects/digital-storefront/roadmap.yaml"
    ensure_goal(
        path,
        "Finish the agreed Kind Robots storefront: every catalog item owned by this project is\n"
        "actually visible/orderable or intentionally delegated to its owning project, Stripe\n"
        "checkout/webhook/fulfillment paths work end-to-end, and the storefront passes a\n"
        "responsive visual/layout review before it is marked finished.",
    )
    append_milestones(
        path,
        """- id: m6
  title: "VERIFY & POLISH — catalog completeness, Stripe E2E, responsive storefront"
  weight: 20
  status: in-progress
""",
        "- id: m6",
    )
    append_tasks(
        path,
        """- id: t-037
  milestone: m6
  title: "Audit the live storefront against the agreed catalog and real implementation state"
  status: ready
  owner: null
  passes: 0
  stakes: reversible
  note: >
    Compare the actual /sanctuary giftshop/storefront with the agreed catalog: Mermaids PDF,
    KR-logo POD item, monthly supporter subscription, mana top-ups, direct Against Malaria giving,
    DLC unlocks, and coloring-book products where those are owned by their separate project.
    Distinguish built-and-visible, built-but-unreachable, placeholder/demo, delegated, and missing.
    Check current routes/components and production/test configuration rather than trusting old done notes.

- id: t-038
  milestone: m6
  title: "Implement every missing storefront-owned catalog item found by the reality audit"
  status: waiting
  owner: null
  passes: 0
  stakes: reversible
  depends_on: t-037
  note: >
    Close t-037's storefront-owned gaps. Do not duplicate products whose production is explicitly
    owned by coloring-book/packmaker/Mermaids; integrate their finished outputs instead. Remove demo
    products/placeholders once a real listing replaces them.

- id: t-039
  milestone: m6
  title: "Run and repair the Stripe checkout/webhook/fulfillment matrix end-to-end"
  status: waiting
  owner: null
  passes: 0
  stakes: reversible
  depends_on: t-037
  note: >
    Exercise test-mode purchase paths for PDF entitlement/download, supporter subscription,
    mana top-up, POD PrintJob creation, DLC Entitlement+Grant, and the general cart. Verify auth,
    idempotency, success/cancel returns, webhook fulfillment, and customer-visible post-purchase
    state. Fix code gaps found. Live keys/real charges remain a separate human gate.

- id: t-040
  milestone: m6
  title: "Resolve the first real POD fulfillment path rather than stopping at a pending PrintJob"
  status: waiting
  owner: null
  passes: 0
  stakes: outward-facing
  gate_human: true
  approved_by_human: false
  depends_on: [t-037, t-038]
  note: >
    The existing roadmap deliberately stopped before vendor submission because no POD account/API
    credentials were available. Determine whether the chosen provider account now exists. Agents may
    finish all reversible integration/test plumbing, but account creation, credentials, paid orders,
    and public listings require Silas. The KR-logo item should become genuinely orderable, not merely
    capable of creating a database PrintJob.

- id: t-041
  milestone: m6
  title: "Responsive storefront layout and visual polish pass"
  status: waiting
  owner: null
  passes: 0
  stakes: reversible
  depends_on: [t-038, t-039]
  note: >
    Apply Interface Vision rules specifically to the storefront: one clear hierarchy, useful product
    imagery, no nested-dashboard squeeze, clean cart/checkout states, and phone/tablet/desktop layouts
    with no hidden or unreachable controls. Verify through the deployed preview, not source alone.

- id: t-042
  milestone: m6
  title: "FOR SILAS: visually accept the completed storefront"
  status: waiting
  owner: silas
  passes: 0
  stakes: reversible
  gate_human: true
  approved_by_human: false
  depends_on: [t-039, t-041]
  note: >
    FOR SILAS: review the actual storefront at phone/tablet/desktop widths and confirm the agreed
    catalog is represented correctly. TO APPROVE: confirm the layout/product presentation feels
    finished or leave concrete notes. Storefront task-count exhaustion is not completion.
""",
        "- id: t-037",
    )


def reconcile_storybook() -> None:
    path = "projects/storybook/roadmap.yaml"
    ensure_goal(
        path,
        "Ship the collaborative Storybook experience as a polished story-first product: guided and\n"
        "limited-visibility play, reusable story state/artifacts, the in-progress casting/setup\n"
        "redesign, and a responsive front end that has been visually accepted on phone/tablet/desktop.",
    )
    set_milestone_field(path, "m1", "status", "done")
    set_milestone_field(path, "m2", "status", "in-progress")
    set_milestone_field(path, "m3", "status", "in-progress")
    set_milestone_field(path, "m4", "status", "in-progress")
    append_tasks(
        path,
        """- id: t-016
  milestone: m4
  title: "FOR SILAS: visually accept the redesigned Storybook setup and reading experience"
  status: waiting
  owner: silas
  passes: 0
  stakes: reversible
  gate_human: true
  approved_by_human: false
  depends_on: [t-011, t-012, t-013, t-014]
  note: >
    FOR SILAS: once the current casting-board/setup/deep-link redesign tasks are complete, review
    Storybook at phone/tablet/desktop widths with a real scenario/cast. TO APPROVE: confirm the
    front end feels like assembling and reading a story rather than nested admin panels, or leave
    concrete visual/interaction notes. This is separate from t-015's stage-role architecture choice.
""",
        "- id: t-016",
    )


def reconcile_lora_ingestion() -> None:
    path = "projects/lora-ingestion/roadmap.yaml"
    ensure_goal(
        path,
        "Keep LoRA/checkpoint files automatically represented as canonical Kind Robots Resource\n"
        "records, browsable/downloadable from the unified library, and prove Resource-localPath\n"
        "selection reaches real generation end-to-end before closing this now-nearly-complete project.",
    )
    set_milestone_field(path, "m2", "status", "done")
    set_task_field(path, "t-003", "title", '"Reconcile later Resource-backed generation evidence; run one current smoke only if proof is still missing"')
    set_task_field(path, "t-003", "gate_human", "false")
    set_task_field(path, "t-003", "approved_by_human", "false")
    set_task_field(path, "t-003", "status", "ready")
    add_task_field_block(
        path,
        "t-003",
        "outcome_note",
        "The original July 28 gate is stale in scope. Since then Kind Robots made Resource.localPath\n"
        "authoritative for LoRA resolution across image/video engines (including PR #1090), fixed\n"
        "art-styler path handling (#1136), unified the model library/download flow (#1152/#1166),\n"
        "and added retry-time Resource path refresh (#1163/#1164). This task now has one job: inspect\n"
        "later production/ArtJob evidence for a successful Resource-backed LoRA render. If that proof\n"
        "already exists, document it and finish the project. Only queue one fresh smoke render if the\n"
        "existing evidence is genuinely insufficient. No human product decision is required.",
    )


def reconcile_docs() -> None:
    replace_once(
        "projects/priority.yaml",
        "# Remaining projects retain their relative order; inactive entries are skipped via\n# project-overrides.yaml. Every active project should appear exactly once.",
        "# Remaining projects retain their relative order. Finite active projects are always\n# selected before continuous projects; paused/finished/retired entries are skipped.\n# Continuous is a fallback lifecycle, not a way to outrank unfinished product work.",
    )
    replace_once(
        "AGENTS.md",
        "3. **Check `project-overrides.yaml`** — skip any project where `status != active`. Paused,\n   retired, and finished projects are off-limits; do not claim tasks for them.\n4. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over\n   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)\n5. Within the chosen project, take the highest-priority task with `status: ready`.\n   If none anywhere, stop — do not invent work. (Exceptions: a proposal-kind project may\n   have a standing instruction to generate N pitches per cycle — follow its roadmap; and\n   `autonomous: true` projects follow the \"Autonomous projects — never idle\" rule below.)",
        "3. **Check `project-overrides.yaml`** — lifecycle is authoritative. Work finite\n   `status: active` projects first. Only when no active project has claimable ready work may\n   `status: continuous` projects run, in priority order. Paused, retired, and finished projects\n   are off-limits. Continuous is intentionally a fallback tier, not an equal-priority synonym\n   for active.\n4. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over\n   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)\n5. Within the selected lifecycle tier/project, take the highest-priority task with\n   `status: ready`. If a finite active project's list reaches zero open tasks, do NOT infer\n   completion from N/N. Reconcile its `goal` against the actual product and add missing work\n   or explicitly finish/pause it. A user-facing software project is not `finished` until its\n   live/preview front end has been checked at phone/tablet/desktop widths and Silas has either\n   accepted the visual state or explicitly waived that check in the current session. Proposal\n   projects may keep their documented pitch cadence. Never-idle work belongs to the continuous\n   lifecycle described below, not to an exhausted finite active roadmap.",
    )
    marker = "**Autonomous projects — never idle** (Silas, 2026-07-10):"
    text = read("AGENTS.md")
    if "**Lifecycle clarification (Silas, 2026-08-07):**" not in text:
        if marker not in text:
            raise RuntimeError("AGENTS autonomous marker missing")
        clarification = (
            "**Lifecycle clarification (Silas, 2026-08-07):** `continuous` now owns never-idle\n"
            "behavior. The historical autonomous rules below apply only when the project's override\n"
            "status is `continuous`. `autonomous: true` on a finite `active` roadmap may grant broad\n"
            "initiative while real ready tasks exist, but it may not invent endless polish/content work\n"
            "after the finite queue empties. AI Art Academy's test-run never-idle loop is explicitly\n"
            "ended; Animation Manager and Dream Cycle are the initial continuous programs.\n\n"
        )
        write("AGENTS.md", text.replace(marker, clarification + marker, 1))

    replace_once(
        "SOURCE_OF_TRUTH.md",
        "`active | paused | retired | finished`",
        "`active | continuous | paused | retired | finished`",
    )
    # CONTROL: clean stale finished projects out of the finite leading band and document the new tier.
    regex_once(
        "CONTROL.md",
        r"\*\*Priority order this week:\*\* interface-vision → challenge-center → ai-art-academy →\ncoloring-book → humboldt-scoop → humboldt-scoop-cms → digital-storefront → packmaker →\nmermaids-of-venice → kind-robots → kindrobots-unraid → global-ui\.",
        "**Priority order this week:** interface-vision → ai-art-academy → coloring-book →\n"
        "humboldt-scoop-cms → digital-storefront → mermaids-of-venice → kind-robots →\n"
        "kindrobots-unraid. Finite active work always outranks continuous programs; when the active\n"
        "queue is empty, animation-manager runs before dream-cycle (the final idle fallback).",
    )
    text = read("CONTROL.md")
    old = (
        "- Autonomous project initiative (2026-07-10): roadmaps may declare `autonomous: true`.\n"
        "  Those projects keep running without my input under the \"never idle\" rule in AGENTS.md\n"
        "  (style pass / roadmap upgrade / more inspirations / content expansion when nothing is\n"
        "  ready). ai-art-academy is the test run. Escalate only actual human gates."
    )
    new = (
        "- Continuous lifecycle (2026-08-07): `continuous` is the explicit never-idle program\n"
        "  status. Continuous projects run only after every finite `active` project has no claimable\n"
        "  ready work. Initial continuous programs: animation-manager and dream-cycle, with dream-cycle\n"
        "  always last. The AI Art Academy autonomous test is concluded; Academy is finite active work\n"
        "  and must stop inventing polish/content tasks when its real roadmap queue empties."
    )
    if old not in text:
        raise RuntimeError("CONTROL autonomous note not found")
    write("CONTROL.md", text.replace(old, new, 1))
    replace_once("CONTROL.md", "### ai-art-academy  (software, autonomous: true)", "### ai-art-academy  (software)")


def install_lifecycle_tooling() -> None:
    module = '''from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_LIFECYCLE_STATUSES = ("active", "continuous", "paused", "finished", "retired")
WORKABLE_PROJECT_STATUSES = ("active", "continuous")


def load_project_overrides(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = data.get("overrides") or []
    if isinstance(entries, dict):
        return {str(slug): cfg for slug, cfg in entries.items() if isinstance(cfg, dict)}
    if isinstance(entries, list):
        return {
            str(entry["slug"]): entry
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("slug"), str)
        }
    return {}


def lifecycle_status(overrides: dict[str, dict[str, Any]], slug: str) -> str:
    value = str(overrides.get(slug, {}).get("status", "active"))
    return value if value in PROJECT_LIFECYCLE_STATUSES else "active"


def ordered_workable_slugs(order: list[str], overrides: dict[str, dict[str, Any]]) -> list[str]:
    known = set(overrides)
    ordered = [slug for slug in order if slug in known]
    ordered += sorted(slug for slug in known if slug not in set(ordered))
    active = [slug for slug in ordered if lifecycle_status(overrides, slug) == "active"]
    continuous = [slug for slug in ordered if lifecycle_status(overrides, slug) == "continuous"]
    return [*active, *continuous]
'''
    write("scripts/project_lifecycle.py", module)

    next_ready = read("scripts/next_ready_task.py")
    next_ready = next_ready.replace(
        "from roadmap_deps import dependency_satisfied  # noqa: E402\n",
        "from roadmap_deps import dependency_satisfied  # noqa: E402\n"
        "from project_lifecycle import load_project_overrides, ordered_workable_slugs  # noqa: E402\n",
    )
    next_ready = re.sub(
        r"def load_active_overrides\(\) -> dict\[str, dict\[str, Any\]\]:\n.*?\n\n\ndef load_roadmap",
        "def load_workable_overrides() -> dict[str, dict[str, Any]]:\n"
        "    return load_project_overrides(OVERRIDES_FILE)\n\n\n"
        "def load_roadmap",
        next_ready,
        count=1,
        flags=re.DOTALL,
    )
    next_ready = next_ready.replace(
        "    ordered_slugs = [slug for slug in order if slug in active]\n    unordered_slugs = sorted(slug for slug in active if slug not in set(ordered_slugs))\n\n    for slug in [*ordered_slugs, *unordered_slugs]:",
        "    for slug in ordered_workable_slugs(order, active):",
    )
    next_ready = next_ready.replace(
        '    result = first_ready_task(load_priority_order(), load_active_overrides())',
        '    result = first_ready_task(load_priority_order(), load_workable_overrides())',
    )
    write("scripts/next_ready_task.py", next_ready)

    worker = read("scripts/run_worker.py")
    worker = worker.replace(
        "from roadmap_claims import remaining_scope_delegate_open  # noqa: E402\n",
        "from roadmap_claims import remaining_scope_delegate_open  # noqa: E402\n"
        "from project_lifecycle import (  # noqa: E402\n"
        "    WORKABLE_PROJECT_STATUSES,\n"
        "    lifecycle_status,\n"
        "    load_project_overrides,\n"
        "    ordered_workable_slugs,\n"
        ")\n",
    )
    worker = re.sub(
        r"def load_active_overrides\(\) -> dict\[str, dict\[str, Any\]\]:\n.*?\n\n\ndef load_roadmaps",
        "def load_overrides() -> dict[str, dict[str, Any]]:\n"
        "    return load_project_overrides(OVERRIDES_FILE)\n\n\n"
        "def load_roadmaps",
        worker,
        count=1,
        flags=re.DOTALL,
    )
    worker = worker.replace("    overrides = load_active_overrides()", "    overrides = load_overrides()")
    worker = worker.replace(
        "        if override.get('status', 'active') != 'active':\n            continue\n\n        roadmap['_path'] = str(path)",
        "        lifecycle = lifecycle_status(overrides, str(slug))\n"
        "        if lifecycle not in WORKABLE_PROJECT_STATUSES:\n"
        "            continue\n\n"
        "        roadmap['_lifecycle'] = lifecycle\n"
        "        roadmap['_path'] = str(path)",
    )
    worker = re.sub(
        r"    by_project = \{roadmap.get\('_project'\): roadmap for roadmap in roadmaps\}\n    ordered = \[by_project\[slug\] for slug in priority_order if slug in by_project\]\n    remaining = \[roadmap for roadmap in roadmaps if roadmap.get\('_project'\) not in priority_order\]\n\n    for roadmap in ordered \+ remaining:",
        "    by_project = {roadmap.get('_project'): roadmap for roadmap in roadmaps}\n"
        "    overrides = {str(slug): {'status': roadmap.get('_lifecycle', 'active')} for slug, roadmap in by_project.items()}\n"
        "    for slug in ordered_workable_slugs(priority_order, overrides):\n"
        "        roadmap = by_project[slug]",
        worker,
        count=1,
    )
    worker = worker.replace(
        "        'active_project_count': len(roadmaps),",
        "        'active_project_count': sum(1 for roadmap in roadmaps if roadmap.get('_lifecycle') == 'active'),\n"
        "        'continuous_project_count': sum(1 for roadmap in roadmaps if roadmap.get('_lifecycle') == 'continuous'),",
    )
    write("scripts/run_worker.py", worker)

    status = read("scripts/build_status.py")
    status = status.replace(
        "from pathlib import Path\n",
        "from pathlib import Path\n\nfrom project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides\n",
    )
    status = status.replace(
        'STATUS_FILE = REPO_ROOT / "STATUS.md"\n',
        'STATUS_FILE = REPO_ROOT / "STATUS.md"\nOVERRIDES_FILE = REPO_ROOT / "project-overrides.yaml"\n',
    )
    status = status.replace(
        "    project_rows = []\n    global_counts = {s: 0 for s in STATUS_COLS}\n    active_projects = 0\n",
        "    project_rows = []\n"
        "    global_counts = {s: 0 for s in STATUS_COLS}\n"
        "    overrides = load_project_overrides(OVERRIDES_FILE)\n"
        "    lifecycle_counts = {status: 0 for status in PROJECT_LIFECYCLE_STATUSES}\n",
    )
    status = status.replace(
        "        active_projects += 1\n        milestones = roadmap.get(\"milestones\") or []",
        "        lifecycle = lifecycle_status(overrides, project_dir.name)\n"
        "        lifecycle_counts[lifecycle] += 1\n"
        "        milestones = roadmap.get(\"milestones\") or []",
    )
    status = status.replace(
        '            f"| {project_dir.name} | {kind} | {progress}% "\n            f"| {counts[\'ready\']} | {counts[\'done\']} | {counts[\'blocked\']} |"',
        '            f"| {project_dir.name} | {lifecycle} | {kind} | {progress}% "\n            f"| {counts[\'ready\']} | {counts[\'done\']} | {counts[\'blocked\']} |"',
    )
    status = status.replace(
        '        f"| Active projects | {active_projects} |",',
        '        f"| Active projects | {lifecycle_counts[\'active\']} |",\n'
        '        f"| Continuous projects | {lifecycle_counts[\'continuous\']} |",\n'
        '        f"| Paused projects | {lifecycle_counts[\'paused\']} |",\n'
        '        f"| Finished projects | {lifecycle_counts[\'finished\']} |",\n'
        '        f"| Retired projects | {lifecycle_counts[\'retired\']} |",',
    )
    status = status.replace(
        '        "| Project | Kind | Progress | Ready | Done | Blocked |",\n        "|---|---|---|---|---|---|",',
        '        "| Project | Lifecycle | Kind | Progress | Ready | Done | Blocked |",\n'
        '        "|---|---|---|---|---|---|---|",',
    )
    write("scripts/build_status.py", status)

    validator = read("scripts/validate_roadmaps.py")
    validator = validator.replace(
        "import yaml\n\nROOT = Path(__file__).resolve().parents[1]\n",
        "import yaml\n\nfrom scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides\n\nROOT = Path(__file__).resolve().parents[1]\n",
    )
    validator = validator.replace(
        "def main() -> int:\n    ok = True\n",
        "def main() -> int:\n    ok = True\n"
        "    overrides_path = ROOT / 'project-overrides.yaml'\n"
        "    overrides = load_project_overrides(overrides_path) if overrides_path.exists() else {}\n"
        "    for slug, cfg in overrides.items():\n"
        "        status = str(cfg.get('status', 'active'))\n"
        "        if status not in PROJECT_LIFECYCLE_STATUSES:\n"
        "            print(f'invalid project lifecycle status for {slug}: {status}', file=sys.stderr)\n"
        "            ok = False\n",
    )
    validator = validator.replace(
        "        dupes = duplicate_task_ids(data[\"tasks\"])",
        "        slug = str(data.get('project') or path.parent.name)\n"
        "        lifecycle = str(overrides.get(slug, {}).get('status', 'active'))\n"
        "        if overrides and lifecycle == 'active':\n"
        "            open_tasks = [task for task in data['tasks'] if isinstance(task, dict) and task.get('status') != 'done']\n"
        "            if not open_tasks:\n"
        "                print(\n"
        "                    f'active project has no open tasks: {slug} -- reconcile its goal, add real work, or explicitly finish/pause it',\n"
        "                    file=sys.stderr,\n"
        "                )\n"
        "                ok = False\n\n"
        "        dupes = duplicate_task_ids(data[\"tasks\"])",
    )
    write("scripts/validate_roadmaps.py", validator)

    tests = read("tests/test_next_ready_task.py")
    tests = tests.replace("selector.load_active_overrides()", "selector.load_workable_overrides()")
    tests += '''\n\ndef test_continuous_project_waits_behind_any_active_ready_work(tmp_path: Path, monkeypatch) -> None:\n    projects_dir = configure_repo(tmp_path, monkeypatch)\n    write_yaml(projects_dir / "priority.yaml", "order:\\n  - forever\\n  - finite\\n")\n    write_yaml(\n        tmp_path / "project-overrides.yaml",\n        "overrides:\\n  - slug: forever\\n    status: continuous\\n  - slug: finite\\n    status: active\\n",\n    )\n    write_project(projects_dir, "forever", "- id: t-001\\n  title: Continuous task\\n  status: ready\\n  stakes: reversible\\n")\n    write_project(projects_dir, "finite", "- id: t-001\\n  title: Finite task\\n  status: ready\\n  stakes: reversible\\n")\n    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())\n    assert result is not None\n    assert result["project"] == "finite"\n\n\ndef test_continuous_project_runs_when_active_queue_is_empty(tmp_path: Path, monkeypatch) -> None:\n    projects_dir = configure_repo(tmp_path, monkeypatch)\n    write_yaml(projects_dir / "priority.yaml", "order:\\n  - forever\\n  - finite\\n")\n    write_yaml(\n        tmp_path / "project-overrides.yaml",\n        "overrides:\\n  - slug: forever\\n    status: continuous\\n  - slug: finite\\n    status: active\\n",\n    )\n    write_project(projects_dir, "forever", "- id: t-001\\n  title: Continuous task\\n  status: ready\\n  stakes: reversible\\n")\n    write_project(projects_dir, "finite", "- id: t-001\\n  title: Finite task\\n  status: done\\n  stakes: reversible\\n")\n    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())\n    assert result is not None\n    assert result["project"] == "forever"\n'''
    write("tests/test_next_ready_task.py", tests)

    validation_tests = read("tests/test_validate_roadmaps.py")
    validation_tests += '''\n\ndef test_active_project_with_no_open_tasks_fails_lifecycle_reconciliation(_isolate_root, capsys):\n    (_isolate_root / "project-overrides.yaml").write_text(\n        "overrides:\\n  - slug: demo\\n    status: active\\n", encoding="utf-8"\n    )\n    write_roadmap(_isolate_root, "demo", "project: demo\\ntasks:\\n- id: t-001\\n  status: done\\n")\n    assert validate_roadmaps.main() == 1\n    assert "active project has no open tasks" in capsys.readouterr().err\n\n\ndef test_continuous_project_may_have_only_recurring_done_history(_isolate_root, capsys):\n    (_isolate_root / "project-overrides.yaml").write_text(\n        "overrides:\\n  - slug: demo\\n    status: continuous\\n", encoding="utf-8"\n    )\n    write_roadmap(_isolate_root, "demo", "project: demo\\ntasks:\\n- id: t-001\\n  status: done\\n")\n    assert validate_roadmaps.main() == 0\n\n\ndef test_unknown_project_lifecycle_fails(_isolate_root, capsys):\n    (_isolate_root / "project-overrides.yaml").write_text(\n        "overrides:\\n  - slug: demo\\n    status: immortal\\n", encoding="utf-8"\n    )\n    write_roadmap(_isolate_root, "demo", "project: demo\\ntasks:\\n- id: t-001\\n  status: ready\\n")\n    assert validate_roadmaps.main() == 1\n    assert "invalid project lifecycle status" in capsys.readouterr().err\n'''
    write("tests/test_validate_roadmaps.py", validation_tests)

    build_status_tests = '''from pathlib import Path\n\nimport scripts.build_status as build_status\n\n\ndef test_status_counts_real_lifecycle_states(tmp_path: Path, monkeypatch) -> None:\n    projects = tmp_path / "projects"\n    projects.mkdir()\n    (tmp_path / "pitches").mkdir()\n    (tmp_path / "project-overrides.yaml").write_text(\n        "overrides:\\n"\n        "  - slug: finite\\n    status: active\\n"\n        "  - slug: forever\\n    status: continuous\\n"\n        "  - slug: shipped\\n    status: finished\\n",\n        encoding="utf-8",\n    )\n    for slug in ("finite", "forever", "shipped"):\n        path = projects / slug\n        path.mkdir()\n        (path / "roadmap.yaml").write_text(\n            f"project: {slug}\\nkind: software\\ntasks:\\n- id: t-001\\n  status: {'done' if slug == 'shipped' else 'ready'}\\n",\n            encoding="utf-8",\n        )\n    monkeypatch.setattr(build_status, "REPO_ROOT", tmp_path)\n    monkeypatch.setattr(build_status, "PROJECTS_DIR", projects)\n    monkeypatch.setattr(build_status, "PITCHES_DIR", tmp_path / "pitches")\n    monkeypatch.setattr(build_status, "STATUS_FILE", tmp_path / "STATUS.md")\n    monkeypatch.setattr(build_status, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")\n    build_status.build_status()\n    text = (tmp_path / "STATUS.md").read_text(encoding="utf-8")\n    assert "| Active projects | 1 |" in text\n    assert "| Continuous projects | 1 |" in text\n    assert "| Finished projects | 1 |" in text\n    assert "| forever | continuous | software |" in text\n'''
    write("tests/test_build_status.py", build_status_tests)

    # CI already runs the full pytest suite; add the real repository validator as a direct gate too.
    ci = read(".github/workflows/ci.yml")
    needle = "      - name: Validate project-overrides.yaml\n        run: |\n"
    if needle not in ci:
        raise RuntimeError("ci.yml lifecycle insertion point missing")
    insertion = (
        "      - name: Validate lifecycle and finite-project reconciliation\n"
        "        run: python scripts/validate_roadmaps.py\n\n"
    )
    # Put it after the existing project-overrides inline block by anchoring before the next job.
    job_marker = "\n  validate-task-events:\n"
    if insertion not in ci:
        index = ci.index(job_marker)
        ci = ci[:index] + "\n" + insertion + ci[index:]
    write(".github/workflows/ci.yml", ci)


def main() -> None:
    reconcile_overrides()
    reconcile_davinci()
    reconcile_interface_vision()
    reconcile_academy()
    reconcile_storefront()
    reconcile_storybook()
    reconcile_lora_ingestion()
    reconcile_docs()
    install_lifecycle_tooling()
    print("portfolio reconciliation transform applied")


if __name__ == "__main__":
    main()
