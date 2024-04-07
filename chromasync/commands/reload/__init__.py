from ..load.specialize_templates import build_templates
from ..load.post_gen_script import run_post_gen_script
from ..load.color import Palette

from ...config.environment import CACHED_PALETTE_FILE

import argparse
import logging
import sys


logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace):
    logger.debug("Running the reload command")

    if not CACHED_PALETTE_FILE.exists():
        logger.critical("No previous loaded palette. Run the `load` command first")
        sys.exit(1)

    # Stores a json copy of thePalettepalette
    palette = Palette.from_conf_file(CACHED_PALETTE_FILE, args=args)

    # Generates all the templates
    build_templates(palette=palette, args=args)

    # Runs post-generation script
    run_post_gen_script()
