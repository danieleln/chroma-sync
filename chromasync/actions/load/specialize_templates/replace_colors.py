from ..color import Palette, HexColor, ColorFmtSpecs

from .parse_directive import Directives

import logging
import re


logger = logging.getLogger("chromasync")


# Matches expressions of the form {RED}, {RED:60:YLW}
COLOR_REGEX = r"\{([^:}]+)(?:(?::(\d+))(?::([^:}]+)))?\}"


def replace_colors(template: str, palette: Palette, directives: dict) -> str:
    logger.debug(f"Replacing color definitions")

    # Required color format (hex with/without leading #)
    fmt_spec = directives.get(Directives.COLOR_FORMAT, ColorFmtSpecs.HEX_W_HASHTAG)



    # Converts the regular expression match to the corresponding HexColor
    @HexColor.format_decorator(fmt_spec)
    def match2color(match: re.Match) -> HexColor:
        color1 = match.group(1)
        color2 = match.group(3)

        if color2 is not None:
            # Returns the composite color
            percentage = int(match.group(2))
            return palette.get_composite(color1, percentage, color2)

        # Returns just the first color
        return palette.get(color1)




    # Returns the replaced string
    return re.sub(COLOR_REGEX, match2color, template)


