from ....config.environment import TEMPLATES_DIR, OUTPUT_DIR
from ....config.directives import ColorFmtSpecs
from ....util import smart_search_template_file

from ..color import Colorscheme, HexColor

from .parse_directive import parse_directives, Directives
from .replace_colors import replace_colors

from argparse import Namespace
from pathlib import Path
import logging
import shutil
import sys


logger = logging.getLogger("chromasync")


def build_templates(colorscheme: Colorscheme, args: Namespace) -> None:
    logger.debug(f"Specializing templates")

    # The `reload` command can have templates passed as arguments
    if hasattr(args, "template") and args.template is not None:
        for template in args.template:
            # Looks for the specified templates
            file = smart_search_template_file(template)

            # Builds the templates
            if file is not None:
                build_template(
                    template_path=file, colorscheme=colorscheme, args=args)

        return


    # If no template is specified, looks for all templates
    for template_path in TEMPLATES_DIR.iterdir():

        # Ignores directories
        # NOTE: build_templates can be made recursive to build all
        #       templates nested within TEMPLATES_DIR
        if template_path.is_file():
            build_template(
                template_path=template_path, colorscheme=colorscheme, args=args)




def build_template(template_path: str, colorscheme: Colorscheme, args: Namespace) -> None:
    logger.debug(f"Specializing template '{template_path}'")

    # Reads the content of the template file
    lines = []
    try:
        with open(template_path, "r") as template_file:
            lines = template_file.readlines()
    except Exception as e:
        logger.critical(f"An error occured while reading file '{template_path}': {e}")
        sys.exit(1)


    # Parses directives and removes them from the template
    template, directives = parse_directives(lines=lines)

    # Replaces colors in the template
    specialized_template = replace_colors(
        template=template, colorscheme=colorscheme, directives=directives)

    # Looks for the OUT_DIR directive. If it doesn't find it, just
    # use the default output directory
    out_dir = Path(directives.get(
        Directives.OUT_DIR,
        OUTPUT_DIR
    )).expanduser()

    # Concats the filename to the output directory
    out_file = out_dir / template_path.name


    store_template(
        out_file=out_file,
        specialized_template=specialized_template,
        template_path=template_path,
        args=args,
    )





def store_template(out_file: Path, specialized_template: str, template_path: str, args: Namespace) -> None:
    logger.debug(f"Storing specialized template '{template_path}' to '{out_file}'")

    # Checks if the file already exists
    if out_file.exists():
        if args.backup is True:
            logger.info(f"File '{out_file}' already exists. Creating a backup copy")

            # Backs-up the file
            try:
                bak_file = out_file.with_name(f"{out_file.name}.bak")
                shutil.copy2(out_file, bak_file)
            except:
                logger.critical(f"Unable to backup '{out_file}' as '{bak_file}'")
                sys.exit(1)

        else:
            logger.warning(
                f"File '{out_file}' already exists. " + \
                f"No backup copy was created cause option --backup is missing"
            )


    # Makes sure that the base directory exists
    elif not out_file.parent.exists():
        logger.warning(
            f"Directory '{out_file.parent}' doesn't exists. Creating it.")
        try:
            out_file.parent.mkdir(parents=True)
        except:
            logger.error(f"Unable to create directory '{out_file.parent}'")
            sys.exit(1)



    # Stores the specialized template
    try:
        with open(out_file, "w") as file:
            file.write(specialized_template)
    except Exception as e:
        logger.error(
            f"An error occurred while saving the specialized template " + \
            f"'{template_path}' to '{output_file}': {e}"
        )

    else:
        logger.debug(f"Correctly saved the specialized template to '{out_file}'")



