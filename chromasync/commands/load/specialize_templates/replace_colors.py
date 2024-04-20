from ..color import Colorscheme, HexColor
from ....config.directives import ColorFmtSpecs

from .parse_directive import Directives

import logging
import re


logger = logging.getLogger("chromasync")


# Matches expressions of the form {RED}, {RED:60:YLW}
COLOR_REGEX = r"\{(\w+)(?::(\d+):(\w+))?\}"

def replace_colors(template: str, colorscheme: Colorscheme, directives: dict) -> str:
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
            return colorscheme.get_composite(color1, percentage, color2)

        # Returns just the first color
        return colorscheme.get(color1)




    # Returns the replaced string
    return re.sub(COLOR_REGEX, match2color, template)


