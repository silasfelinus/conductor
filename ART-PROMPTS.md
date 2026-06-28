# Image Requests

Canonical project image requests now live in `projects/art-prompts.yaml` so `scripts/build_workspace.py` can render and prune them automatically.

Pending project asset sets currently queued there:

- `sketchy` — icon, card, hero
- `art-generator-connect` — icon, card, hero
- `storymaker` — icon, card, hero
- `media-watchlist` — icon, card, hero
- `conductor-app` — icon, card, hero
- `alexa-integration` — icon, card, hero

Save generated files to `projects/images/{slug}-{type}.webp`, then run:

```bash
python scripts/build_workspace.py
```
