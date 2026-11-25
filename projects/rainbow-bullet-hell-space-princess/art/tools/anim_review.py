import importlib.util
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/home/user/conductor/scripts")
spec = importlib.util.spec_from_file_location(
    "op", "/home/user/conductor/scripts/export_rainbow_opening.py"
)
op = importlib.util.module_from_spec(spec)
spec.loader.exec_module(op)
from PIL import Image

out = Path(".")
for arg in sys.argv[1:]:
    name, iid = arg.split("=")
    mp4 = out / f"{name}.mp4"
    if not mp4.exists():
        mp4.write_bytes(op.download(int(iid)))
    info = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=width,height,nb_frames,r_frame_rate",
            "-of",
            "csv=p=0",
            str(mp4),
        ],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    d = out / name
    d.mkdir(exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-i",
            str(mp4),
            "-vf",
            "select=not(mod(n\\,10))",
            "-vsync",
            "vfr",
            str(d / "f%03d.png"),
        ],
        check=True,
    )
    frames = sorted(d.glob("f*.png"))[:8]
    ims = [Image.open(f) for f in frames]
    w, h = ims[0].size
    s = 240 / h
    strip = Image.new("RGB", (int(w * s) * len(ims), 240))
    for i, im in enumerate(ims):
        strip.paste(im.resize((int(w * s), 240)), (i * int(w * s), 0))
    strip.save(out / f"{name}-strip.png")
    print(name, info, len(list(d.glob("f*.png"))))
