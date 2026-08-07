from pathlib import Path

path = Path('SOURCE_OF_TRUTH.md')
text = path.read_text(encoding='utf-8')
old = '- project lifecycle: active, paused, finished, retired;'
new = '- project lifecycle: `active | paused | retired | finished`;'
if old in text:
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
elif new not in text and '`active | continuous | paused | retired | finished`' not in text:
    raise SystemExit('SOURCE_OF_TRUTH lifecycle wording is in an unexpected state')
