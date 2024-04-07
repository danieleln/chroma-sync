from enum import Enum


class Directives(Enum):
    OUT_FILE     = "@out:"
    COLOR_FORMAT = "@fmt:"


class ColorFmtSpecs(Enum):
    HEX_W_HASHTAG  = "#hex"
    HEX_WO_HASHTAG = "hex"
