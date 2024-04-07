import logging.config
import argparse

from .color_formatter import ColorFormatter
from ...config.environment import LOG_FILE

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": ColorFormatter,
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno",
                "thread_name": "threadName"
            }
        },
        "detailed": {
            "format": "%(levelname)s from %(filename)s @ %(asctime)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "color",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": LOG_FILE,
            "maxBytes": 500_000,
            "backupCount": 2
        }
    },
    "loggers": {
        "chromasync": {
            "level": "DEBUG",
            "handlers": ["stdout", "file"]
        }
    }
}






def setup_logging(args: argparse.Namespace) -> None:

    # Sets the verbosity of the logger
    if args.quiet is True:
        # Disables logging to stdout
        try:
            log_config["loggers"]["chromasync"]["handlers"].remove("stdout")
        except:
            pass

    elif args.verbose is True:
        # Logs also info to stdout
        log_config["handlers"]["stdout"]["level"] = "INFO"


    # Configs logging
    logging.config.dictConfig(config=log_config)
