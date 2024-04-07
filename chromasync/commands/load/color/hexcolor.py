import logging
import sys
import re

from ....config.directives import ColorFmtSpecs

logger = logging.getLogger("chromasync")



class HexColor:
    def __init__(self, name: str, hex_string: str) -> None:
        # Checks whether the hex_string is a valid hex string
        if not re.match(r"^#[0-9a-fA-F]{6}$", hex_string):
            logger.critical(
                f"Invalid HEX color '{color}'. "
                f"Colors must be of the form '#1a2b3c'"
            )
            sys.exit(1)

        self.name = name
        self.hex_string = hex_string


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, color={self.hex_string})"


    # Blends the current color to a given one
    def blend(self, color: "HexColor", percentage: float) -> "HexColor":
        if percentage < 0 or percentage > 1:
            logger.error(f"Invalid percentage {percentage}. Using value 1")
            percentage = 1

        r1, g1, b1 = self.to_RGB()
        r2, g2, b2 = color.to_RGB()


        # Blends two integer values
        def _blend(c1: int, c2: int, perc: float):
            return int(c1 * perc + c2 * (1 - perc))

        return HexColor.from_RGB(
            f"{self.name}{int(percentage*100)}{color.name}",
            _blend(r1, r2, percentage),
            _blend(g1, g2, percentage),
            _blend(b1, b2, percentage),
        )


    # Returns the hex string with/without the initial hashtag
    def to_hex(self, hashtag: bool=True) -> str:
        if hashtag is True:
            return self.hex_string

        return self.hex_string[1:]


    # Converts the hex_string into R,G,B integers
    def to_RGB(self) -> tuple[int]:
        return (
            int(self.hex_string[1:3], 16),
            int(self.hex_string[3:5], 16),
            int(self.hex_string[5:7], 16)
        )


    # Formats the color according to a format specification
    def format(self, fmt_spec: str) -> str:
        match fmt_spec:
            case ColorFmtSpecs.HEX_W_HASHTAG | ColorFmtSpecs.HEX_W_HASHTAG.value:
                return self.to_hex(hashtag=True)

            case ColorFmtSpecs.HEX_WO_HASHTAG | ColorFmtSpecs.HEX_WO_HASHTAG.value:
                return self.to_hex(hashtag=False)

            case _:
                valid_specs = [f"'{spec.value}'" for spec in ColorFmtSpecs]
                logger.critical(
                    f"Invalid color format specification '{fmt_spec}'. " + \
                    f"Valid format specs are {', '.join(valid_specs)}"
                )
                sys.exit(1)


    # Makes the method "format" into a decorator
    @staticmethod
    def format_decorator(fmt_spec: str):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).format(fmt_spec)
            return wrapper
        return decorator



    @classmethod
    def from_RGB(cls, name: str, r: int, g: int, b: int) -> "HexColor":
        # Checks if color components are valid
        for c in (r, g, b):
            if c < 0 or c > 255:
                logger.critical(
                    f"Invalid RGB value '{c}'. " + \
                    "Expected an integer from 0 to 255"
                )
                sys.exit(1)

        R = hex(r)[2:].zfill(2)
        G = hex(g)[2:].zfill(2)
        B = hex(b)[2:].zfill(2)

        return cls(name=name, hex_string=f"#{R}{G}{B}")


