from .specialize_templates import build_templates
from .post_gen_script import run_post_gen_script
from .color import Palette

from .find_palette_file import find_palette_file

import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the load action")

    # Looks for a palette file
    file = find_palette_file(args=args)

    # Parses the input color palette
    palette = Palette.from_conf_file(file=file)

    # Generates all the templates
    build_templates(palette=palette, args=args)


    # Runs post-generation script
    run_post_gen_script()
