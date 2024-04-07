from ....config.directives import Directives

import logging

logger = logging.getLogger("chromasync")


def parse_directives(lines: list[str]) -> tuple[str, dict]:
    logger.debug(f"Parsing directives")

    template = ""
    directives = {}

    for line in lines:
        # Tries to parse directive from the current line
        for directive in Directives:
            if line.startswith(directive.value):
                # Removes the directive header
                value = line[len(directive.value):].strip()
                directives[directive] = value
                break
        else:
            # No directive was found on this line
            template += line



    pretty_print_directives = {d.name: v for d,v in directives.items()}
    logger.debug(f"Found directives {pretty_print_directives}")
    # logger.debug(f"Found template {template}")

    return template, directives


