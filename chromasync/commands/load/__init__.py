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

    # Parses the input color palette
    palette = Palette.from_conf_file(file=file, args=args)

    # Stores a copy of the palette
    palette.to_conf_file(path=CACHED_PALETTE_FILE)

    # Generates all the templates
    build_templates(palette=palette, args=args)

    # Runs post-generation script
    run_post_gen_script()
