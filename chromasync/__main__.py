from .argparser import build_arg_parser
from .config.environment import build_environment
from . import commands
from . import util

import logging




def main():
    # Builds chromasync files and directories
    build_environment()


    # Parses commandline arguments
    parser = build_arg_parser()
    args = parser.parse_args()


    # Sets up logging
    logger = logging.getLogger("chromasync")
    util.logging_config.setup_logging(args=args)

    logger.debug(f"Running chromasync")


    # Executes the required action
    match args.action:
        case "load":
            commands.load.run(args=args)

        case "reload":
            commands.reload.run(args=args)

        case "list":
            commands.ls.run(args=args)








if __name__ == "__main__":
    main()




