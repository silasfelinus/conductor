# Manuscript drop folder

Silas: put the **Mermaids of Venice** PDF here (any filename is fine —
`mermaids-of-venice.pdf` suggested). This is the third-printing file: the text you
hand-edited, with the minor word-choice and pacing edits in the first two chapters.

Committing it here unblocks two things:

1. **Editorial pipeline** (this project, tasks t-004..t-007). Agents read the
   manuscript and produce four separate files in `../editorial/`:
   - `general-impressions.md` — honest reader-level reactions
   - `editorial-notes.md` — structural and line-level notes (described, never rewritten)
   - `cultural-awareness.md` — gaze/privilege gaps, handled with care
   - `VERY-IMPORTANT.md` — actual typos and grammar errors only, with page/line
     context so you can fix them in your own hand

   Also set `approved_by_human: true` and `status: done` on task t-003 in
   `../roadmap.yaml` so the dependency resolver releases those tasks.

2. **The store's first product** (digital-storefront t-010) — add your price note
   there when you're ready.

## Ground rules for agents

- The prose is Silas's alone. Advise as an editor; **never** draft replacement
  prose intended for the book.
- This PDF is a **sale product**. If/when it is wired for delivery in
  kind_robots, it is served from authenticated server-side storage — it must
  never be copied into `public/`, a public repo path, or any URL reachable
  without purchase.
