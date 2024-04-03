from ...config import TEMPLATES_DIR, PALETTES_DIR

from pathlib import Path
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the list action")

    if args.palette is True:
        # Palettes contained in the PALETTES_DIR
        content = ls_dir(PALETTES_DIR, remove_suffix=True)

        print(f"Found the following", end=" ")

        # Filters dark/light palettes only
        if args.dark is True:
            content = filter(lambda x: 'dark' in x, content)
            print("dark", end=" ")
        elif args.light is True:
            content = filter(lambda x: 'light' in x, content)
            print("light", end=" ")

        print(f"palettes in '{PALETTES_DIR}'")
        print("\t" + "\n\t".join(content))


    else:
        print(f"Found the following templates in '{TEMPLATES_DIR}'")
        # Templates contained in TEMPLATES_DIR
        content = ls_dir(TEMPLATES_DIR)
        print("\t" + "\n\t".join(content))





def ls_dir(path: Path, remove_suffix: bool=False) -> None:
    files = sorted({f for f in path.iterdir() if f.is_file()})

    if remove_suffix is True:
        names = map(lambda f: f.stem, files)
    else:
        names = map(lambda f: f.name, files)

    return names
