from pathlib import Path
import configparser
import argparse
import logging
import sys

from ....config import PALETTES_DIR

from .color_names import BaseColors
from .os_colors import get_os_colors
from .hexcolor import HexColor


CONF_FILE_DARK_SECTION_HEADER  = "Dark"
CONF_FILE_LIGHT_SECTION_HEADER = "Light"



logger = logging.getLogger("chromasync")



class Palette:
    def __init__(self, palette: dict) -> "Palette":
        self._palette = palette


    # Retrieves the HexColor from its name
    def get(self, color_name: str) -> HexColor:
        logger.debug(f"Retrieving color '{color_name}'")

        if color_name in self._palette.keys():
            return self._palette[color_name]

        logger.critical(
            f"Invalid color '{color_name}'. " + \
            f"Valid colors are {self._palette.keys()}"
        )
        sys.exit(1)


    # Retrieves a composite color (like RED:30:GRN)
    def get_composite(self, color_name1: str, percentage: int, color_name2: str) -> HexColor:
        composite_color_name = f"{color_name1}:{percentage}:{color_name2}"
        logger.debug(f"Retrieving color '{composite_color_name}'")

        # Uses cached values when possible
        if composite_color_name in self._palette.keys():
            return self._palette[composite_color_name]

        # Creates the composite color
        color1 = self.get(color_name1)
        color2 = self.get(color_name2)

        composite_color = color1.blend(color2, percentage/100)

        # Caches the composite color
        self._palette[composite_color_name] = composite_color

        return composite_color


    # Creates a new palette from a file
    @classmethod
    def from_conf_file(cls, file: Path, args: argparse.Namespace) -> "Palette":
        logger.info(f"Parsing palette from file '{file}'")

        # Parses the palette '.conf' file
        config = configparser.ConfigParser()
        try:
            config.read(file)

        except configparser.MissingSectionHeaderError:
            logger.critical(
                f"Missing section header in '{file}'." + \
                f"Expected at least one of `[{CONF_FILE_DARK_SECTION_HEADER}]`, " + \
                f"`[{CONF_FILE_LIGHT_SECTION_HEADER}]` before color definition"
            )
            sys.exit(1)

        except Exception as e:
            logger.critical(f"An error occurred while parsing palette '{path}': {e}")
            sys.exit(1)


        # Checks if at least one variant is present
        has_dark = config.has_section(CONF_FILE_DARK_SECTION_HEADER)
        has_light = config.has_section(CONF_FILE_LIGHT_SECTION_HEADER)

        if not (has_dark or has_light):
            logger.critical(
                f"Missing section header in '{file}'." + \
                f"Expected at least one of `[{CONF_FILE_DARK_SECTION_HEADER}]`, " + \
                f"`[{CONF_FILE_LIGHT_SECTION_HEADER}]` before color definition"
            )
            sys.exit(1)


        # Finds which variant (dark/light) to load
        header = None
        if args.dark is True:
            header = CONF_FILE_DARK_SECTION_HEADER
        elif args.light is True:
            header = CONF_FILE_LIGHT_SECTION_HEADER
        else:
            # Palette has both variants and no variant was specified
            # in the arguments => can't decide which one to load
            if has_dark and has_light:
                logger.critical(
                    f"Specify which variant to load by adding either " + \
                    f"`--dark` or `--light`. Palette '{file}' has both variants"
                )
                sys.exit(1)

            if has_dark:
                header = CONF_FILE_DARK_SECTION_HEADER
            elif has_light:
                header = CONF_FILE_LIGHT_SECTION_HEADER


        # Checks if the required header is available
        if not config.has_section(header):
            logger.critical(f"Palette '{file}' has no header `[{header}]`")
            sys.exit(1)


        # Retreives color informations
        palette = { }
        color_hex_string = None

        for color in BaseColors:
            # Gets the string contained by the enum
            color = color.value

            try:
                # TODO: add support for light theme
                color_hex_string = config.get(header, color)

            except configparser.NoOptionError:
                logger.critical(f"Missing color '{color}' in '{file}'")
                sys.exit(1)


            # Adds the color to the palette dict
            palette[color] = HexColor(name=color, hex_string=color_hex_string)


        # Sets OS colors
        os_colors = get_os_colors(palette)
        palette = palette | os_colors

        logger.debug(f"Parsed palette: {palette}")


        # Wraps the palette
        return cls(palette=palette)





