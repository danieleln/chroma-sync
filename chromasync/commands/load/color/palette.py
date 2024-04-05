from pathlib import Path
import configparser
import logging
import sys

from ....config import PALETTES_DIR

from .color_names import BaseColors, CONF_FILE_SECTION_NAME
from .os_colors import get_os_colors
from .hexcolor import HexColor



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
    def from_conf_file(cls, file: Path) -> "Palette":
        logger.info(f"Parsing palette from file '{file}'")

        # Parses the palette '.conf' file
        config = configparser.ConfigParser()
        try:
            config.read(file)

        except configparser.MissingSectionHeaderError:
            logger.critical(f"Missing section header [{CONF_FILE_SECTION_NAME}] in '{file}'")
            sys.exit(1)

        except Exception as e:
            logger.critical(f"An error occurred while parsing palette '{path}': {e}")
            sys.exit(1)


        # Retreives color informations
        palette = { }
        color_hex_string = None

        for color in BaseColors:
            # Gets the string contained by the enum
            color = color.value

            try:
                color_hex_string = config.get(CONF_FILE_SECTION_NAME, color)

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





