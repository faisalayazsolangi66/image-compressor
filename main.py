#!/usr/bin/env python3
"""Compress JPEG images by lowering quality.

Re-saves JPEG files at a lower quality setting (and optionally a
smaller width) and reports how much space each file saved.
"""
import argparse
import os
import sys

IMAGE_EXTS = {".jpg", ".jpeg"}


def collect_images(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        return [os.path.join(path, name) for name in sorted(os.listdir(path))
                if os.path.isfile(os.path.join(path, name))
                and os.path.splitext(name)[1].lower() in IMAGE_EXTS]
    return []


def human_kb(size_bytes):
    return f"{size_bytes / 1024:.1f} KB"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compress JPEG images by lowering quality."
    )
    parser.add_argument("input", help="JPEG file or folder of JPEGs")
    parser.add_argument("--quality", type=int, default=75,
                        help="JPEG quality 1-95 (default: 75, lower = smaller)")
    parser.add_argument("--output", default="compressed",
                        help="output folder (default: compressed)")
    parser.add_argument("--max-width", type=int, default=0,
                        help="also shrink images wider than this (0 = keep size)")
    parser.add_argument("--in-place", action="store_true",
                        help="overwrite the original files instead of writing to --output")
    args = parser.parse_args(argv)

    if not 1 <= args.quality <= 95:
        parser.error("--quality must be between 1 and 95")
    if args.max_width < 0:
        parser.error("--max-width must be 0 or more")

    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is not installed. Install it with: pip install Pillow",
              file=sys.stderr)
        return 1

    images = collect_images(args.input)
    if not images:
        print(f"No JPEG images found in: {args.input}", file=sys.stderr)
        return 1

    if not args.in_place:
        os.makedirs(args.output, exist_ok=True)

    total_before = total_after = 0
    done = 0
    for src in images:
        dest = src if args.in_place else os.path.join(
            args.output, os.path.basename(src))
        before = os.path.getsize(src)
        try:
            with Image.open(src) as image:
                image = image.convert("RGB")
                if args.max_width and image.width > args.max_width:
                    ratio = args.max_width / image.width
                    image = image.resize(
                        (args.max_width, int(image.height * ratio)))
                image.save(dest, "JPEG", quality=args.quality, optimize=True)
        except Exception as exc:
            print(f"Failed: {src}: {exc}", file=sys.stderr)
            continue
        after = os.path.getsize(dest)
        saved = 100 * (before - after) / before if before else 0
        total_before += before
        total_after += after
        done += 1
        print(f"{src} -> {dest}: {human_kb(before)} -> {human_kb(after)} "
              f"({saved:.0f}% smaller)")

    if total_before:
        overall = 100 * (total_before - total_after) / total_before
        print(f"Done: {done} file(s), {human_kb(total_before)} -> "
              f"{human_kb(total_after)} ({overall:.0f}% smaller overall).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
