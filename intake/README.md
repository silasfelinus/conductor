# intake/

Drop new project requests here as Markdown files before running the intake script.

## Format

Create a file named `YYYY-MM-DD-<slug>.md` with:

```markdown
# Project Request: <Project Name>

slug: <kebab-case-slug>
kind: software | content | proposal
repo: owner/repo  (or omit if no external repo)

## Description
One paragraph.

## Why now
Why is this worth picking up at this point.

## Rough scope
What done looks like.
```

## Processing

Run `python scripts/intake.py <slug> --kind <kind>` to scaffold the project directory
from `projects/_template/`. The intake file can be archived or deleted after processing.

## Status

| File | Status |
|---|---|
| (none yet) | — |
