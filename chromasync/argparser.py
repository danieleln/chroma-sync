from .config.environment import PALETTES_DIR
import argparse


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="chromasync",
        description="Theme synchroniser"
    )

    # Global options
    add_verbosity_opts(parser)


    # Sub commands
    subp = parser.add_subparsers(
        dest="action",
        required=True,
        help="available commands"
    )

    add_load_command(subp)
    add_reload_command(subp)
    add_list_command(subp)


    return parser




# Load sub command options
def add_load_command(subparser):
    parser = subparser.add_parser("load", help="loads a new theme")

    parser.add_argument(
        "palette",
        help=f"loads a palette either from the filesystem (by specifying " + \
             f"a path) or from '{PALETTES_DIR}'. In the latter case, " + \
             f"file extension might be omitted"
    )

    add_light_dark_group(
        parser=parser,
        required=False,
        light_help="loads the light variant",
        dark_help="loads the dark variant",
    )

    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="backups existing templates before overwriting them"
    )





# Reload sub command options
def add_reload_command(subparser):
    parser = subparser.add_parser("reload", help="reloads the last theme")

    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="backups existing templates before overwriting them"
    )

    add_light_dark_group(
        parser=parser,
        required=False,
        light_help="reloads the light variant theme",
        dark_help="reloads the dark variant of the current theme",
    )




# List sub command options
def add_list_command(subparser):
    parser = subparser.add_parser("list", help="lists available palettes/templates")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-p", "--palette",
        action="store_true",
        help=f"shows available palettes"
    )

    group.add_argument(
        "-t", "--template",
        action="store_false",
        help=f"shows available templates"
    )

    add_light_dark_group(
        parser=parser,
        required=False,
        light_help="lists light palettes only",
        dark_help="lists dark palettes only",
    )




# Global verbosity options
def add_verbosity_opts(parser):
    verbosity_group = parser.add_mutually_exclusive_group(required=False)

    verbosity_group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="logs on the terminal are disabled"
    )

    verbosity_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="all logs are printed also on the terminal"
    )



# Adds --light/--dark option pair
def add_light_dark_group(parser, required: bool, light_help: str, dark_help: str):
    ld_group = parser.add_mutually_exclusive_group(required=False)

    ld_group.add_argument(
        "-d", "--dark",
        action="store_true",
        help=dark_help,
    )

    ld_group.add_argument(
        "-l", "--light",
        action="store_true",
        help=light_help,
    )
