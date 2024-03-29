from .color_names import OSColors, BaseColors

import logging
logger = logging.getLogger("chromasync")


# The two main colors per each distro
# TODO: add all the distros!!
OS_COLORS = {
    "Arch":        [BaseColors.CYN, BaseColors.WHT],
    "Debian":      [BaseColors.RED, BaseColors.WHT],
    "EndeavourOS": [BaseColors.MAG, BaseColors.BLU],
    "Manjaro":     [BaseColors.GRN, BaseColors.WHT],
    "PopOS":       [BaseColors.CYN, BaseColors.WHT],
    "Ubuntu":      [BaseColors.RED, BaseColors.WHT],
}




def get_os_colors(palette: dict):
    distro_name = get_linux_distro()

    if distro_name in OS_COLORS:
        color1, color2 = OS_COLORS[distro_name]
        color1 = color1.value
        color2 = color2.value

        return {
            OSColors.OS1.value : palette[color1],
            OSColors.OS2.value : palette[color2],

            OSColors.OS1H.value : palette[color1 + "H"],
            OSColors.OS2H.value : palette[color2 + "H"],
        }


    logger.error(f"No OS colors definition for distro '{distro_name}'")

    # Fallback: just returns the foreground
    fg_color = palette["FG"]
    return {
        OSColors.OS1.value : fg_color,
        OSColors.OS2.value : fg_color,

        OSColors.OS1H.value : fg_color,
        OSColors.OS2H.value : fg_color,
    }




# Retrieves the current distro by reading file /etc/os-release
def get_linux_distro():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('NAME='):
                    return line.split('=')[1].strip().strip('"')

    except FileNotFoundError:
        logger.error("Can't find file /etc/os-release")
        return "?"
