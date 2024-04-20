from pathlib import Path
import argparse
import sys

from ..config.environment import COLORSCHEMES_DIR, TEMPLATES_DIR

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




def smart_search_colorscheme_file(colorscheme: str) -> Path:
    file = smart_search_file(
        file=Path(colorscheme),
        dir=COLORSCHEMES_DIR,
        ext=".conf"
    )

    if file is None:
        # Unable to find the specified colorscheme
        logger.critical(
            f"Unable to find colorscheme '{colorscheme}'. " + \
            f"Type `chromasync list -p` to see the available colorschemes."
        )
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
