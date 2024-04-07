from pathlib import Path
import configparser
import argparse
import logging
import sys

from ....config.confspecs import DARK_VARIANT, LIGHT_VARIANT, METADATA_HEADER
from ....config.environment import PALETTES_DIR, CACHED_PALETTE_FILE
from ....config.colors import BaseColors, get_os_colors

from .hexcolor import HexColor





logger = logging.getLogger("chromasync")



class Palette:
    def __init__(self, palette: dict) -> "Palette":
        # Actual palette
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

        # loads the palette file
        config = load_palette_conf_file(file=file, args=args)

        # Selects which of the light/dark variant to load
        variant = select_variant(config=config, args=args, file=file)

        # Stores a copy of the palette file
        write_palette_conf_file(config=config, variant=variant, path=CACHED_PALETTE_FILE)

        # Retreives color informations
        palette = { }
        color_hex_string = None

        for color in BaseColors:
            # Gets the string contained by the enum
            color = color.value

            try:
                color_hex_string = config.get(variant, color)

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





def load_palette_conf_file(file: Path, args: argparse.Namespace) -> configparser.ConfigParser:
    logger.debug(f"Parsing '{file}'")

    config = configparser.ConfigParser()

    try:
        config.read(file)

    except configparser.MissingSectionHeaderError:
        logger.critical(
            f"Missing section variant in '{file}'." + \
            f"Expected at least one of `[{DARK_VARIANT}]`, " + \
            f"`[{LIGHT_VARIANT}]` before color definition"
        )
        sys.exit(1)

    except Exception as e:
        logger.critical(f"An error occurred while parsing palette '{file}': {e}")
        sys.exit(1)


    return config


def write_palette_conf_file(config: configparser.ConfigParser, variant: str, path: Path) -> None:
    logger.debug("Caching palette file")

    # Adds the variant specification
    if not config.has_section(METADATA_HEADER):
        config[METADATA_HEADER] = {}

    config[METADATA_HEADER]["variant"] = variant

    try:
        with open(path, "w") as f:
            config.write(f)
    except Exception as e:
        logger.error(f"An error occurred while writing cache file '{path}': {e}")



# Finds which variant (dark/light) to load
def select_variant(config: configparser.ConfigParser, args: argparse.Namespace, file: Path) -> str:
    logger.debug("Selecting dark/light variant")

    has_dark = config.has_section(DARK_VARIANT)
    has_light = config.has_section(LIGHT_VARIANT)


    # Requested dark theme
    if args.dark is True:
        if not has_dark:
            logger.critical(f"Palette '{file}' has no variant `[{DARK_VARIANT}]`")
            sys.exit(1)

        logger.debug("Selected dark variant from --dark option")
        return DARK_VARIANT


    # Requested light theme
    if args.light is True:
        if not has_light:
            logger.critical(f"Palette '{file}' has no variant `[{LIGHT_VARIANT}]`")
            sys.exit(1)

        logger.debug("Selected light variant from --light option")
        return LIGHT_VARIANT


    # No variant was explicitly requested

    # Looks for a metadata tag
    if config.has_option(METADATA_HEADER, "variant"):
        variant = config.get(METADATA_HEADER, "variant")

        if variant in (DARK_VARIANT, LIGHT_VARIANT):
            logger.debug(f"Selected {variant} variant from metadata section")
            return variant

        logger.critical(
            f"Invalid variant specification `{variant}` in palette file '{file}'. " + \
            f"Valid values are `{DARK_VARIANT}`, " + \
            f"`{LIGHT_VARIANT}`"
        )
        sys.exit(1)


    # Looks for available variants
    if has_dark and has_light:
        # Palette has both variants and no variant was specified
        # in the arguments => can't decide which one to load
        logger.critical(
            f"Palette '{file}' has both a light and a dark variant. " + \
            f"Specify which one to load by adding either of the " + \
            f"options `--dark`, `--light`"
        )
        sys.exit(1)

    if has_dark:
        logger.debug(f"Selected dark variant. It's the only one available")
        return DARK_VARIANT

    if has_light:
        logger.debug(f"Selected light variant. It's the only one available")
        return LIGHT_VARIANT


    # Palette has no variant specification
    logger.critical(
        f"Missing section variant in '{file}'." + \
        f"Expected at least one of `[{DARK_VARIANT}]`, " + \
        f"`[{LIGHT_VARIANT}]` before color definition"
    )
    sys.exit(1)
