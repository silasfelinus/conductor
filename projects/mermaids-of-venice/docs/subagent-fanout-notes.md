# Subagent fan-out-to-single-file workaround

Kaizen task from Reviewer review of PR #229 (mermaids-of-venice/t-011). Notes the
pattern used for the t-004..t-007/t-010 editorial pass so a future large-document
pass doesn't rediscover it from scratch.

## The harness limitation

Subagents launched via the Agent tool cannot write files directly in a way that
lands reliably in the parent session's working tree for the parent to commit.
Whatever a subagent tries to persist to disk is not guaranteed to be visible or
committable by the orchestrating session once the subagent returns. Only the
**parent session's own return text** from each subagent call is reliably usable.

This means "spin up N subagents, each writes its own output file, then commit
all N files" does not work. The subagents' file-write side effects can't be
trusted as the source of truth.

## The workaround

1. **Split the source into sections** sized to fit comfortably in one subagent's
   context (for the manuscript pass: ~13 sections across a 338pp / ~86k-word PDF).
2. **Fan out one subagent per section**, each with a narrow, well-scoped prompt
   (e.g. "read pages X-Y and report typos/grammar issues with page+quote+fix" or
   "read pages X-Y and report tonal/structural observations"). Ask each subagent
   to return its findings as **plain text in its final reply**, not as a file it
   claims to have written.
3. **The parent session collects every subagent's returned text** and holds it
   in the conversation/working context — this is the actual data transfer point.
4. **The parent session itself writes the final output file(s)**, synthesizing
   across all the collected subagent text into the target document(s). The
   parent is the only actor that reliably persists to disk.

## Practical guidance for the next large pass

- Prefer many narrow subagent prompts over few broad ones — narrower prompts
  produce more directly usable text (less summarization loss) and are easier
  to merge in step 4.
- If the output needs to be a single coherent document (not just a concatenation
  of section notes), plan for a synthesis pass: either the parent does the
  synthesis itself after collecting all sections, or a final subagent is given
  all prior subagents' returned text as input and asked to produce the merged
  draft — but even then, the parent session is the one that writes the file.
- Don't rely on a subagent's own claim that it "wrote" or "saved" a file as
  confirmation that the file exists in the working tree. Verify with a direct
  Read/Glob from the parent after the fact if a subagent's tool use suggests it
  attempted a write.
- This applies to any large fan-out read/synthesis task, not just manuscripts:
  large codebases, long PDFs, big log dumps, etc.

## Reference

Original occurrence: the mermaids-of-venice manuscript editorial pass
(t-004..t-007, t-010), producing `editorial/general-impressions.md`,
`editorial/editorial-notes.md`, `editorial/cultural-awareness.md`,
`editorial/VERY-IMPORTANT.md`, and `editorial/guest-reviews.md` from a 13-way
sectional subagent fan-out over the second-edition manuscript PDF. See
`TALKBACK.md` (2026-07-06 entries) for the original process note.
