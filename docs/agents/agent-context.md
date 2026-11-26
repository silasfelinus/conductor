# Read one task, not a roadmap

The existing Refresh Status workflow builds private advisory JSON locators at `ops/agent-context/<slug>.json`. No API, extra scheduler, or canonical copy of task notes.

1. Find a candidate in STATUS.md or accept an explicit assignment. Fetch only that project's JSON locator. The `ready` and `review` lists are bounded; `tasks` includes nonterminal tasks and exact source lines.
2. Fetch CONTROL.md global and selected project ranges, and the selected roadmap task range, using the recorded `source_commit` as ref. The Git blob hashes identify the precise source version. No notes or acceptance are summarized away.
3. Load the role hint's card once: [developer](roles/developer.md), [reviewer](roles/reviewer.md), [content](roles/content.md), [art](roles/art.md), [QA](roles/qa.md), [daily creative](roles/daily-creative.md). Hints are conservative, not authority or hard routing; override when actual scope calls for another role. Existing selector and medic roles remain valid.
4. Before writing, check current main lifecycle, task and dependencies; verify the claim through the connector protocol. The snapshot is not a claim or completion receipt. If source has moved, obtain fresh ranges or locate the task in the live source. Never use old line offsets against a different blob. If a locator is absent or stale, use direct GitHub reads or local show_task.py/show_control.py.
5. Do the work and close it under AGENTS.md. Use source links, not copied context, in handoffs.

Task events and the existing refresh workflow update the locators after canonical changes. No public publication or production-data write is added.
