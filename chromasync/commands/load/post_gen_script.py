from ...config.environment import POST_SCRIPT_FILE

import subprocess
import logging
import sys


logger = logging.getLogger("chromasync")


def run_post_gen_script() -> None:
    # Generates a warning if the script is not defined
    if not POST_SCRIPT_FILE.exists():
        logger.warning(f"Post generation script '{POST_SCRIPT_FILE}' was not found")
        return 


    logger.debug(f"Running post generation script '{POST_SCRIPT_FILE}'")

    try:
        subprocess.run([POST_SCRIPT_FILE], check=True)

    except PermissionError:
        logger.error(
            f"Post generation script '{POST_SCRIPT_FILE}' has no execution permission!\n" + \
            f"Run `chmod u+x '{POST_SCRIPT_FILE}'` in your shell"
        )
        sys.exit(1)

    except Exception as e:
    # except subprocess.CalledProcessError as e:
        logger.critical(
            f"An error occurred while executing '{POST_SCRIPT_FILE}': {e}")
        sys.exit(1)
