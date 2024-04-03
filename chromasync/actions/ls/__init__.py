from ...config import TEMPLATES_DIR, PALETTES_DIR

from pathlib import Path
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the list action")

    if args.palette is True:
        print(f"Found the following palettes in '{PALETTES_DIR}'")
        ls_dir(PALETTES_DIR, remove_suffix=True)
    else:
        print(f"Found the following templates in '{TEMPLATES_DIR}'")
        ls_dir(TEMPLATES_DIR)




def ls_dir(path: Path, remove_suffix: bool=False) -> None:
    files = sorted({f for f in path.iterdir() if f.is_file()})

    if remove_suffix is True:
        names = map(lambda f: f.stem, files)
    else:
        names = map(lambda f: f.name, files)

    print("\t" + "\n\t".join(names))
