from ...config import TEMPLATES_DIR, PALETTES_DIR
from ..load.color.palette import CONF_FILE_DARK_SECTION_HEADER, CONF_FILE_LIGHT_SECTION_HEADER
from ..load.color.palette import Palette

from pathlib import Path
import configparser
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the list command")

    if args.palette is True:
        # Palettes contained in the PALETTES_DIR
        palettes = ls_dir(PALETTES_DIR, remove_suffix=True)

        print(f"Found the following", end=" ")

        # Filters dark/light palettes only
        if args.dark is True:
            palettes = filter_palettes(palettes, CONF_FILE_DARK_SECTION_HEADER)
            print("dark", end=" ")
        elif args.light is True:
            palettes = filter_palettes(palettes, CONF_FILE_LIGHT_SECTION_HEADER)
            print("light", end=" ")

        print(f"palettes in '{PALETTES_DIR}'")
        print("\t" + "\n\t".join(palettes))


    else:
        print(f"Found the following templates in '{TEMPLATES_DIR}'")
        # Templates contained in TEMPLATES_DIR
        templates = ls_dir(TEMPLATES_DIR)
        print("\t" + "\n\t".join(templates))





def ls_dir(path: Path, remove_suffix: bool=False) -> None:
    files = sorted({f for f in path.iterdir() if f.is_file()})

    if remove_suffix is True:
        names = map(lambda f: f.stem, files)
    else:
        names = map(lambda f: f.name, files)

    return names



# Selects palettes that have the specified (light/dark) header
def filter_palettes(palettes: list, header: str) -> list:

    def palette_has_section(palette: Palette) -> bool:
        path = (PALETTES_DIR / palette).with_suffix(".conf")

        config = configparser.ConfigParser()
        try:
            config.read(path)
        except:
            return False

        return config.has_section(header)

        # NOTE: it could be faster just to open each file and look
        #       for the header without using configparser
        # try:
        #     with open(path) as f:
        #         for line in f.readlines():
        #             if line.startswith(f"[{header}]"):
        #                 return True
        # except:
        #     pass
        #
        #     return False


    return filter(palette_has_section, palettes)
