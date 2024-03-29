import logging

class ColorFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        level = ""
        match record.levelname:
            case "DEBUG":
                level = "\033[1;36mDBG\033[0m"
            case "INFO":
                level = "\033[1;32mNFO\033[0m"
            case "WARNING":
                level = "\033[1;33mWRN\033[0m"
            case "ERROR":
                level = "\033[1;31mERR\033[0m"
            case "CRITICAL":
                level = "\033[1;31mCRT\033[0m"
                # level = "\033[41;97mC\033[0m"

        return "[{}] {}".format(level, record.getMessage())
