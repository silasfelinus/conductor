#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import shutil
import tarfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PART_DIR = ROOT / 'projects' / 'coloring-book' / '.surgery-payload'
MONSTER_WORKFLOW = ROOT / '.github' / 'workflows' / 'monster-recast-art-jobs.yml'


def main() -> None:
    if not PART_DIR.exists():
        print('Coloring surgery payload already materialized.')
        return

    previous_monster_workflow = MONSTER_WORKFLOW.read_bytes()
    encoded = ''.join(
        path.read_text(encoding='utf-8').strip()
        for path in sorted(PART_DIR.glob('part-*'))
    )
    payload = base64.b64decode(encoded)
    with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
        archive.extractall(ROOT, filter='data')
    # The Actions token may write normal repository files but should not rewrite
    # workflows. GitHub applies the final workflow update directly after this commit.
    MONSTER_WORKFLOW.write_bytes(previous_monster_workflow)

    roadmap_path = ROOT / 'projects' / 'coloring-book' / 'roadmap.yaml'
    roadmap = yaml.safe_load(roadmap_path.read_text(encoding='utf-8'))
    roadmap['notes_from_silas'] = (
        'Canonical book order and scope, clarified 2026-07-17: book 1 is Monster Recast, '
        'book 2 is Hollywood Recast (never “Hollywood Recast 2”), and book 3 is Kind Robots. '
        'Each book tracks exactly 36 interior illustration proposals and begins with a complete '
        'set of 36 COLOR design prompts. Prompt writing, ArtJob submission, render retrieval, and '
        'same-stage review advance in batches of up to 18 images (half a book), not 1-6. Design '
        'iterations are color-first. Early BW studies may be retained as inspiration, but a faithful '
        'BW coloring-page counterpart is generated only after its color composition is accepted. '
        'Each proposal ultimately finishes as one confirmed final color file and one faithful final '
        'BW file. Covers are separate. Accepted is not final. Use MR, HWR, and KR prefixes. Internal '
        'art generation and curation are authorized; publishing, POD accounts/listings, spend, and '
        'public Character release remain human-gated.'
    )
    task_notes = {
        't-022': (
            'CURRENT COLOR-FIRST DIRECTION 2026-07-17: use the canonical color-art-jobs.yaml queue. '
            'A Worker generation/submission/review pass handles up to 18 Monster Recast color '
            'proposals at one stage. Do not generate new BW variants until the corresponding color '
            'composition is accepted; then derive a faithful BW counterpart in an 18-image pass. '
        ),
        't-023': (
            'Hollywood Recast already has 36 named color proposals and queued color ArtJobs. '
            'It may collect/render color proposals while Monster Recast remains editorially first. '
            'Use batches of up to 18 at one stage. The canonical title is Hollywood Recast, never '
            'Hollywood Recast 2. BW follows accepted color composition. '
        ),
        't-024': (
            'Kind Robots already has 36 named color proposals and queued color ArtJobs, including '
            'kr-001 as a variation on the supplied/canonical Kind Robots logo. Use batches of up to '
            '18 at one stage. Existing art and early BW are inspiration until accepted; BW production '
            'follows accepted color composition. '
        ),
    }
    for task in roadmap.get('tasks', []):
        task_id = task.get('id')
        if task_id in task_notes:
            old = str(task.get('note') or '')
            if not old.startswith(task_notes[task_id]):
                task['note'] = task_notes[task_id] + old
    roadmap_path.write_text(
        yaml.safe_dump(roadmap, sort_keys=False, allow_unicode=True, width=110),
        encoding='utf-8',
    )

    shutil.rmtree(PART_DIR)


if __name__ == '__main__':
    main()
