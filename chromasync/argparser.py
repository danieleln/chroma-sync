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

    ld_group = parser.add_mutually_exclusive_group(required=False)

    ld_group.add_argument(
        "-d", "--dark",
        action="store_true",
        help="loads the dark variant"
    )

    ld_group.add_argument(
        "-l", "--light",
        action="store_true",
        help="loads the light variant"
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


    ld_group = parser.add_mutually_exclusive_group(required=False)

    ld_group.add_argument(
        "-d", "--dark",
        action="store_true",
        help="lists dark palettes only"
    )

    ld_group.add_argument(
        "-l", "--light",
        action="store_true",
        help="lists light palettes only"
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




