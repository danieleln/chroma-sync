from ...config import PALETTES_DIR

from pathlib import Path
import argparse
import logging
import sys

logger = logging.getLogger("chromasync")



def find_palette_file(args: argparse.Namespace) -> Path:
    # Looks for a file in the whole file system
    # e.g.: `chromasync load "path/to/my/palette.conf"`
    file = Path(args.palette).expanduser()

    if file.exists():
        return file


    # Looks inside PALETTES_DIR
    # e.g.: `chromasync load "palette.conf"`
    file = PALETTES_DIR / args.palette

    if file.exists():
        return file


    # Looks inside PALETTES_DIR, this time adding also the extension
    # e.g.: `chromasync load "palette.conf"`
    file = file.with_suffix(".conf")

    if file.exists():
        return file


    # Unable to find the specified palette
    logger.critical(f"Unable to find file/palette '{args.palette}'")
    sys.exit(1)
