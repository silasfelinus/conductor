from pathlib import Path
import re

academy = Path('projects/ai-art-academy/roadmap.yaml')
text = academy.read_text(encoding='utf-8')
# Remove the stale trailing status key on t-017 that the duplicate-key audit surfaced.
text = text.replace("\n\n    status: done\n  - id: t-010\n", "\n\n  - id: t-010\n", 1)
# The former recurring task is historical completion now, not an in-flight review.
start = text.index('  - id: t-010\n')
end = text.index('\n  - id: ', start + 1)
block = text[start:end]
block = re.sub(r'(?m)^    status: .*$', '    status: done', block, count=1)
block = re.sub(r'(?m)^    owner: .*$', '    owner: null', block, count=1)
block = re.sub(r'(?m)^    claimed_by: .*$', '    claimed_by: null', block, count=1)
block = re.sub(r'(?m)^    claimed_at: .*$', '    claimed_at: null', block, count=1)
block = re.sub(
    r'(?ms)^    note: \|-\n.*?(?=^    continuous_improvement:)',
    '''    note: |-\n      ENDED 2026-08-07 by Silas direction. This was the Academy autonomous never-idle\n      experiment, not a permanent project mode. Its completed lane history remains in run_log,\n      including the final lane-3 ArtJob submission cycle (#1841), but this task no longer\n      rearms or invents more curriculum/polish work. The Academy now advances only through\n      finite product tasks, especially the web/iOS/Android shipping milestone.\n''',
    block,
    count=1,
)
text = text[:start] + block + text[end:]
academy.write_text(text, encoding='utf-8')

storybook = Path('projects/storybook/roadmap.yaml')
text = storybook.read_text(encoding='utf-8')
start = text.index('- id: t-015\n')
end = text.index('\n- id: t-016\n', start)
block = text[start:end]
if '  gate_human: true\n' not in block:
    block = block.replace('  stakes: reversible\n', '  stakes: reversible\n  gate_human: true\n  approved_by_human: false\n', 1)
block = block.replace(
    '  note: |-\n',
    '  note: |-\n    FOR SILAS: this is a subjective product-boundary decision, not an agent tooling block.\n    TO APPROVE: decide whether Stage presets become Storybook frames sharing narrative roles, or stay a separate system; record the choice here.\n\n',
    1,
)
text = text[:start] + block + text[end:]
storybook.write_text(text, encoding='utf-8')
