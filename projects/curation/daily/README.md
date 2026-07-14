# Daily art scoring reports

One file per day: `<YYYY-MM-DD>.yaml`, written by
`scripts/curate_art.py --daily` during the daily-digest workflow.

Each report scores the art the pipeline generated in the last ~24h against
`AESTHETIC-GUIDELINES.md` (the steerable aesthetic bar), so the digest can
feature the day's highest-scored renders in its "Top-scored art today" gallery.

Shape:

```yaml
date: 2026-01-01
model: claude-opus-4-8      # null when scored objective-only (no ANTHROPIC_API_KEY)
since: 24 hours ago
scored: <count with a numeric score>
results:                   # sorted highest score first
  - image: projects/images/<file>.webp
    public_url: https://raw.githubusercontent.com/silasfelinus/conductor/main/...
    source: images | process
    variant: color | bw
    scored_at: <iso>
    stage: vision | floor
    score: 0-100 | null
    verdict: promote | revise | reject | needs-vision
    one_liner: short caption for the gallery
    reasons: [...]
```

Regenerated each run; safe to delete old reports.
