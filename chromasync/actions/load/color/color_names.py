from enum import Enum

CONF_FILE_SECTION_NAME = "Palette"


class BaseColors(Enum):
    BG = "BG"
    FG = "FG"

    BLK = "BLK"
    RED = "RED"
    GRN = "GRN"
    YLW = "YLW"
    BLU = "BLU"
    MAG = "MAG"
    CYN = "CYN"
    WHT = "WHT"

    BLKH = "BLKH"
    REDH = "REDH"
    GRNH = "GRNH"
    YLWH = "YLWH"
    BLUH = "BLUH"
    MAGH = "MAGH"
    CYNH = "CYNH"
    WHTH = "WHTH"



class OSColors(Enum):
    OS1 = "OS1"
    OS2 = "OS2"

    OS1H = "OS1H"
    OS2H = "OS2H"
