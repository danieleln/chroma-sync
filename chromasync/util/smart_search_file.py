from pathlib import Path
import argparse

from ..config.environment import PALETTES_DIR, TEMPLATES_DIR

import logging

logger = logging.getLogger("chromasync")


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




def smart_search_palette_file(palette: str) -> Path:
    file = smart_search_file(
        file=Path(palette),
        dir=PALETTES_DIR,
        ext=".conf"
    )

    if file is None:
        # Unable to find the specified palette
        logger.critical(f"Unable to find palette '{palette}'")
        sys.exit(1)

    return file




def smart_search_template_file(template: str) -> Path:
    file = smart_search_file(
        file=Path(template),
        dir=TEMPLATES_DIR,
        ext=".conf"
    )

    if file is None:
        logger.error(f"Unable to find template '{template}'")

    return file
