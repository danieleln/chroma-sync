from .config import PALETTES_DIR
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
        help="available sub-commands"
    )

    add_load_subcommand(subp)
    add_list_subcommand(subp)


    return parser




# Load sub command options
def add_load_subcommand(subparser):
    parser = subparser.add_parser("load", help="loads a new theme")

    parser.add_argument(
        "palette",
        help=f"sources a palette either from '{PALETTES_DIR}' (file" + \
             f"extension can be omitted) or from a  file anywhere in" + \
             f"the file system (as long as it's readable)"
    )

    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="backups existing templates before overwriting them"
    )




# List sub command options
def add_list_subcommand(subparser):
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




