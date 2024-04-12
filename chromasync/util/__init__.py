from . import logging_config
from .smart_search_file import smart_search_file, smart_search_palette_file

from pathlib import Path


# Retrieves the current distro by reading file /etc/os-release
def get_linux_distro():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('NAME='):
                    return line.split('=')[1].strip().strip('"')

    except FileNotFoundError:
        logger.error("Can't find file /etc/os-release")
        return "?"


# Lists the content of a directory
def list_dir_content(path: Path, remove_suffix: bool=False) -> None:
    files = sorted({f for f in path.iterdir() if f.is_file()})

    if remove_suffix is True:
        names = map(lambda f: f.stem, files)
    else:
        names = map(lambda f: f.name, files)

    return names
