from enum import Enum


class Directives(Enum):
    # TODO: change @out to @dir (or add @dir) to specify the output
    #       directory. The output file name is the template file name
    OUT_FILE     = "@out:"
    COLOR_FORMAT = "@fmt:"


class ColorFmtSpecs(Enum):
    HEX_W_HASHTAG  = "#hex"
    HEX_WO_HASHTAG = "hex"
