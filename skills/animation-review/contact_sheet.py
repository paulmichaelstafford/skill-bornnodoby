#!/usr/bin/env python3
"""Make a labelled contact sheet from video frames: 4 across, one label each."""
import glob
import os
import sys

from PIL import Image, ImageDraw

def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit("usage: contact_sheet.py FRAME... OUT.png")
    out = args[-1]
    paths = []
    for a in args[:-1]:
        paths.extend(sorted(glob.glob(a)) if any(c in a for c in "*?[") else [a])
    if not paths:
        raise SystemExit("no frames")
    cols = 4
    thumb_w, thumb_h = 400, 250
    label_h = 22
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (18, 18, 22))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w, thumb_h))
        x = (i % cols) * thumb_w + (thumb_w - img.width) // 2
        y = (i // cols) * (thumb_h + label_h) + label_h
        sheet.paste(img, (x, y))
        draw.text(((i % cols) * thumb_w + 6, (i // cols) * (thumb_h + label_h) + 4),
                  os.path.basename(path), fill=(230, 230, 230))
    sheet.save(out)
    print(out)

if __name__ == "__main__":
    main()
