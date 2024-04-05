from .. import load

from ...config import CACHED_PALETTE_FILE

import argparse
import logging
import sys


logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace):
    logger.debug("Running the reload command")

    if not CACHED_PALETTE_FILE.exists():
        logger.critical("No previous loaded palette. Run the `load` command first")
        sys.exit(1)

    load.load_palette_from_file(CACHED_PALETTE_FILE, args)
