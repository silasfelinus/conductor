# Production operator guide

The existing `scripts/build_music_video.py` is the renderer/exporter; `scripts/dead_air_produce.py` is Dead Air's short-film authoring adapter. Kind Robots owns MusicVideo runtime data and private ArtJobs. Conductor owns dated editorial scripts and review.

## Run a pilot, without writing anything

```bash
cd conductor
python scripts/dead_air_produce.py --episode projects/dead-air/episodes/2026-11-12-sorry-farm.yaml --dry-run
```

## Start a private production (only when authenticated)

```bash
cd conductor
KR_BASE_URL=https://kind-robots.vercel.app python scripts/dead_air_produce.py --episode projects/dead-air/episodes/2026-11-12-sorry-farm.yaml --start
```

The tool prints a MusicVideo ID. **Record it as production evidence in a PR or episode tracking note**; for retries, pass that ID instead of starting over:

```bash
cd conductor
KR_BASE_URL=https://kind-robots.vercel.app python scripts/dead_air_produce.py --episode projects/dead-air/episodes/2026-11-12-sorry-farm.yaml --video-id YOUR_EXISTING_ID --resume
```

`--resume` is intentionally non-blocking: it may return "rendering" with the *same* ArtJob IDs. Run again later. The private final upload is part of production, not public release.

## Archival / clearance

Keep an episode's script, rejected versions, pop-culture reference analysis, human direction, source-rights notes, shot continuity bible, generation prompt/ArtJob provenance and final quality report in the repository. The project `TRANSMISSIONS.md` stores explicit human-supplied mission and public editorial notes, never imaginary access to private model thoughts. Git history is durable, but not a promise of eternal memory. Published cuts need separate human approval and rights clearance.

## Known integration limits

- The code-backed MusicVideo scenes can hold exact shots, duration, style and prompts. Generic `scenes/plan` would overwrite the comic timing; the adapter writes the scene plan itself before render.
- The music-video pipeline can synthesize a song with ACE-Step, but a 15-second commercial needs authored dialogue. The adapter creates local espeak/FFmpeg provisional VO and a restrained tone bed; voice acting and sound design deserve a human/artistic pass before publication.
- LTX/WAN hero animation is slow on a 12 GB GPU. The adapter requests clips on the nominated scenes; it does not fabricate clips or accept Ken Burns as verified animation.
- Run in a Python environment with `pyyaml`, FFmpeg, FFprobe and espeak available. Never print KR_API_TOKEN.
- `--start` is only for authorized private drafts. Never set `isPublic=true`, deploy, email or externally publish from this script.
