from enum import Enum


class Directives(Enum):
    OUT_DIR      = "@dir:"
    COLOR_FORMAT = "@fmt:"


class ColorFmtSpecs(Enum):
    HEX_W_HASHTAG  = "#hex"
    HEX_WO_HASHTAG = "hex"
