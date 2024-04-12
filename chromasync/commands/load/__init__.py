from .specialize_templates import build_templates
from .post_gen_script import run_post_gen_script
from .color import Palette

from ...config.environment import CACHED_PALETTE_FILE
from ...util import smart_search_palette_file

from pathlib import Path
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the load command")

    # Looks for a palette file
    file = smart_search_palette_file(args=args)

    # Parses the input color palette
    palette = Palette.from_conf_file(file=file, args=args)

    # Generates all the templates
    build_templates(palette=palette, args=args)

    # Runs post-generation script
    run_post_gen_script()



