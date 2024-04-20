from ..load.color.colorscheme import DARK_VARIANT, LIGHT_VARIANT
from ..load.color.colorscheme import Colorscheme

from ...config.environment import TEMPLATES_DIR, COLORSCHEMES_DIR

from ...util import list_dir_content

from pathlib import Path
import configparser
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the list command")

    # Prints available templates
    if args.template is True:
        print(f"Found the following templates in '{TEMPLATES_DIR}'")
        # Templates contained in TEMPLATES_DIR
        templates = list_dir_content(TEMPLATES_DIR)
        print("\t" + "\n\t".join(templates))
        return None


    # Prints available colorschemes

    # Colorschemes contained in the COLORSCHEMES_DIR
    colorschemes = list_dir_content(COLORSCHEMES_DIR, remove_suffix=True)

    print(f"Found the following", end=" ")

    # Filters dark/light colorschemes only
    if args.dark is True:
        colorschemes = filter_colorschemes(colorschemes, DARK_VARIANT)
        print("dark", end=" ")
    elif args.light is True:
        colorschemes = filter_colorschemes(colorschemes, LIGHT_VARIANT)
        print("light", end=" ")

    print(f"colorschemes in '{COLORSCHEMES_DIR}'")
    print("\t" + "\n\t".join(colorschemes))




# Selects colorschemes that have the specified (light/dark) header
def filter_colorschemes(colorschemes: list, header: str) -> list:

    def colorscheme_has_section(colorscheme: Colorscheme) -> bool:
        path = (COLORSCHEMES_DIR / colorscheme).with_suffix(".conf")

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


    return filter(colorscheme_has_section, colorschemes)
