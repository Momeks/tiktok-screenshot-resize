#!/usr/bin/env python3
"""Resize images to vertical frame 1206×1670: fit inside frame with centered letterboxing."""

from __future__ import annotations

import argparse
import secrets
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

TARGET_W = 1206
TARGET_H = 1670
DEFAULT_JPEG_QUALITY = 95
LETTERBOX_RGB = (255, 255, 255)


def resize_contain_center(
    im: Image.Image,
    width: int,
    height: int,
    fill: tuple[int, int, int] = LETTERBOX_RGB,
) -> Image.Image:
    """Scale to fit entirely inside the frame; center on canvas with letterbox/pillarbox bars."""
    src_w, src_h = im.size
    scale = min(width / src_w, height / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height), fill)
    left = (width - new_w) // 2
    top = (height - new_h) // 2
    canvas.paste(resized, (left, top))
    return canvas


def save_jpeg(im: Image.Image, out_path: Path, quality: int) -> tuple[Path, int]:
    """Save JPEG at fixed quality; subsampling=0 (4:4:4) for sharper text and UI."""
    rgb = im.convert("RGB")
    path = out_path.with_suffix(".jpg")
    rgb.save(
        path,
        format="JPEG",
        quality=quality,
        subsampling=0,
        optimize=True,
    )
    size = path.stat().st_size
    return path, size


def save_png(im: Image.Image, out_path: Path) -> tuple[Path, int]:
    path = out_path.with_suffix(".png")
    im.save(path, format="PNG", optimize=True, compress_level=6)
    return path, path.stat().st_size


def unique_stem(out_dir: Path, prefix: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    short = secrets.token_hex(3)
    return out_dir / f"{prefix}_{ts}_{short}"


def process_one(
    src: Path,
    out_dir: Path,
    prefix: str,
    fmt: str,
    jpeg_quality: int,
) -> Path:
    if not src.is_file():
        raise FileNotFoundError(f"Not a file: {src}")

    out_dir.mkdir(parents=True, exist_ok=True)
    base = unique_stem(out_dir, prefix)

    with Image.open(src) as im:
        im_rgba = im.convert("RGBA")
        background = Image.new("RGB", im_rgba.size, (255, 255, 255))
        background.paste(im_rgba, mask=im_rgba.split()[-1])
        resized = resize_contain_center(background, TARGET_W, TARGET_H)

    if fmt == "png":
        path, size = save_png(resized, base)
    else:
        path, size = save_jpeg(resized, base, jpeg_quality)

    print(f"Wrote {path} ({size} bytes)")
    return path


def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            f"Resize images to {TARGET_W}×{TARGET_H} (fit inside frame, centered letterboxing); "
            "outputs get a unique timestamp+id suffix."
        ),
    )
    p.add_argument(
        "images",
        nargs="+",
        type=Path,
        help="Input image file(s)",
    )
    p.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("screenshots"),
        help="Output directory (default: ./screenshots)",
    )
    p.add_argument(
        "--prefix",
        default="tiktok",
        help="Filename prefix before timestamp (default: tiktok)",
    )
    p.add_argument(
        "--format",
        choices=("jpg", "png"),
        default="jpg",
        help="Output format (default: jpg)",
    )
    p.add_argument(
        "--jpeg-quality",
        type=int,
        default=DEFAULT_JPEG_QUALITY,
        metavar="Q",
        help=f"JPEG quality 1–100 (default: {DEFAULT_JPEG_QUALITY}; uses 4:4:4 chroma subsampling)",
    )
    args = p.parse_args()

    if not (1 <= args.jpeg_quality <= 100):
        print("error: --jpeg-quality must be between 1 and 100", file=sys.stderr)
        return 1

    try:
        for img in args.images:
            process_one(
                img.resolve(),
                args.output_dir.resolve(),
                args.prefix,
                args.format,
                args.jpeg_quality,
            )
    except (OSError, FileNotFoundError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
