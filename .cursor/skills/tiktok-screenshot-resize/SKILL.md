---
name: tiktok-screenshot-resize
description: Resizes attached or local screenshots to vertical 1206×1670 with fit-inside framing and centered letterboxing; high-quality JPEG (default Q95, 4:4:4). Writes uniquely named files under screenshots/. Use when the user attaches screenshots for TikTok, asks to resize for TikTok, or mentions TikTok export dimensions.
---

# TikTok screenshot resize

## When to use

Apply when the user shares screenshot paths, attaches images meant for TikTok, or asks for TikTok-sized exports.

## Spec (encode in behavior, not repetition)

- Output frame: **1206 × 1670** (vertical; works better for some TikTok layouts than strict 1080×1920). **Contain + centered**: full image scales to fit; **letterbox/pillarbox** bars (default **white**) fill the rest—no cropping.
- **JPEG:** high quality by default (**quality 95**, chroma **subsampling 0** / 4:4:4 for sharper text). Optionally `--jpeg-quality 1–100`.
- **PNG** via `--format png` (lossless; larger files).
- Filenames: `{prefix}_{YYYYMMDD_HHMMSS}_{6-char-hex}.jpg` so nothing overwrites prior runs.

## What to run

From the **project root**:

1. Ensure dependency: `python3 -m pip install -r requirements.txt` (needs Pillow).
2. Resize one or more files:

```bash
python3 resize_tiktok.py "/path/to/screen.png"
```

Higher JPEG quality (e.g. 98):

```bash
python3 resize_tiktok.py shot.png --jpeg-quality 98
```

Or call the script directly:

```bash
python3 .cursor/skills/tiktok-screenshot-resize/scripts/resize_for_tiktok.py "/path/to/screen.png"
```

Multiple inputs:

```bash
python3 resize_tiktok.py a.png b.jpg
```

Custom output folder or PNG:

```bash
python3 resize_tiktok.py shot.png -o ./screenshots --format png
```

## Agent checklist

- [ ] Use **absolute paths** for inputs when the user attaches files outside the repo.
- [ ] Default **output dir** is `./screenshots` under the project root unless the user specifies otherwise.
- [ ] Report the written paths and file sizes.

Utility script: [scripts/resize_for_tiktok.py](scripts/resize_for_tiktok.py)
