#!/usr/bin/env python3
"""Copy the pre-rendered front page into the make.fun output folder.

Stdlib only. The image itself is produced by gen_image.py; this script
just places a copy where the platform expects it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "entry.png"
DEFAULT_DEST = "/output"


def resolve_destination():
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_DEST
    return os.path.join(chosen, SOURCE_NAME)


def main():
    source = os.path.join(HERE, SOURCE_NAME)
    if not os.path.isfile(source):
        print("missing source image: " + source, file=sys.stderr)
        print("run: python3 gen_image.py", file=sys.stderr)
        return 1
    target = resolve_destination()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    print("copied " + source + " -> " + target + " (" + str(size) + " bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
