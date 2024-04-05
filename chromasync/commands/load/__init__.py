from .specialize_templates import build_templates
from .post_gen_script import run_post_gen_script
from .find_palette_file import find_palette_file
from .color import Palette

from ...config import CACHED_PALETTE_FILE

from pathlib import Path
import argparse
import logging
import shutil

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the load command")

    # Looks for a palette file
    file = find_palette_file(args=args)

    # Stores a copy of the palette
    shutil.copy2(file, CACHED_PALETTE_FILE)

    # Loads the palette
    load_palette_from_file(file, args)



# Loads a palette from a file
def load_palette_from_file(file: Path, args: argparse.Namespace):

    # Parses the input color palette
    palette = Palette.from_conf_file(file=file, args=args)

    # Generates all the templates
    build_templates(palette=palette, args=args)


    # Runs post-generation script
    run_post_gen_script()
