from ..load.specialize_templates import build_templates
from ..load.post_gen_script import run_post_gen_script
from ..load.color import Colorscheme

from ...config.environment import CACHED_COLORSCHEME_FILE

import argparse
import logging
import sys


logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace):
    logger.debug("Running the reload command")

    if not CACHED_COLORSCHEME_FILE.exists():
        logger.critical("No previous loaded colorscheme. Run the `load` command first")
        sys.exit(1)

    # Stores a json copy of the colorscheme
    colorscheme = Colorscheme.from_conf_file(CACHED_COLORSCHEME_FILE, args=args)

    # Generates all the templates
    build_templates(colorscheme=colorscheme, args=args)

    # Runs post-generation script
    if not args.no_script:
        run_post_gen_script()
