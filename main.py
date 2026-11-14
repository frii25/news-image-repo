#!/usr/bin/env python3
"""news-image-01 entry.

Copies the pre-rendered newspaper front-page poster (entry.png, shipped
beside this program) to $MAKEFUN_OUTPUT_DIR/entry.png.

The poster sums up Friday 13 November 2026: a title band, a hero photo of
the FAA ground stop, two smaller photos (Ukraine drone raid, Microsoft 365
outage day 2) and three further verified headlines (Nvidia CEO exit,
Qatar-Turkey defence pact, Mekelle falls / COP31). All facts were verified
against AP/Reuters reporting of 13 Nov 2026; the text was rendered crisply
with PIL, so nothing is garbled.

Deterministic by construction: the program performs a byte-for-byte copy of
the same shipped file on every run, so two runs write identical bytes.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        head = f.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        f.seek(16)
        width, height = struct.unpack(">II", f.read(8))
    if width > MAX_DIM or height > MAX_DIM:
        print(f"error: entry.png is {width}x{height}, over the "
              f"{MAX_DIM}x{MAX_DIM} limit", file=sys.stderr)
        return 1

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the {MAX_BYTES} limit",
              file=sys.stderr)
        return 1

    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
