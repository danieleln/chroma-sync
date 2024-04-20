from .specialize_templates import build_templates
from .post_gen_script import run_post_gen_script
from .color import Colorscheme

from ...config.environment import CACHED_COLORSCHEME_FILE
from ...util import smart_search_colorscheme_file

from pathlib import Path
import argparse
import logging

logger = logging.getLogger("chromasync")


def run(args: argparse.Namespace) -> None:
    logger.debug("Running the load command")

    # Looks for a colorscheme file
    file = smart_search_colorscheme_file(colorscheme=args.colorscheme)

    # Parses the input color colorscheme
    colorscheme = Colorscheme.from_conf_file(file=file, args=args)

    # Generates all the templates
    build_templates(colorscheme=colorscheme, args=args)

    # Runs post-generation script
    run_post_gen_script()



