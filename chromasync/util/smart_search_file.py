from pathlib import Path
import argparse

from ..config.environment import PALETTES_DIR


def smart_search_file(file: Path, dir: Path=None, ext: str=None) -> Path:
    file = file.expanduser()

    # Looks for a file in the whole file system
    if file.exists():
        return file


    # Looks for `file` inside the specified `dir`
    if dir is not None:
        file = dir / file

        if file.exists():
            return file


    # Looks for `file` inside `dir` with extension `ext`
    if ext is not None:
        file = file.with_suffix(ext)

        if file.exists():
            return file


    return None




def smart_search_palette_file(args: argparse.Namespace) -> Path:
    # Looks for a file in the whole file system
    # e.g.: `chromasync load "path/to/my/palette.conf"`
    file = smart_search_file(
        file=Path(args.palette),
        dir=PALETTES_DIR,
        ext=".conf"
    )


    if file is None:
        # Unable to find the specified palette
        logger.critical(f"Unable to find file/palette '{args.palette}'")
        sys.exit(1)

    return file
