from pathlib import Path
import os


_CHROMASYNC_DIR_NAME = "chromasync"
_CHROMASYNC_CONF_DIR_ENV_VAR  = "CHROMASYNC_CONFIG_DIR"
_CHROMASYNC_CACHE_DIR_ENV_VAR = "CHROMASYNC_CACHE_DIR"


# System directories
_HOME_DIR      = Path(os.getenv("HOME", os.getenv("USERPROFILE")))
_XDG_CACHE_DIR = Path(os.getenv("XDG_CACHE_HOME",  _HOME_DIR / ".cache"))
_XDG_CONF_DIR  = Path(os.getenv("XDG_CONFIG_HOME", _HOME_DIR / ".config"))


# Default config and cache directories
_DEFAULT_CONF_DIR  = os.path.join(_XDG_CONF_DIR,  _CHROMASYNC_DIR_NAME)
_DEFAULT_CACHE_DIR = os.path.join(_XDG_CACHE_DIR, _CHROMASYNC_DIR_NAME)


# Configuration dirs/files
CONF_DIR = Path(os.getenv(_CHROMASYNC_CONF_DIR_ENV_VAR, _DEFAULT_CONF_DIR))
TEMPLATES_DIR = CONF_DIR / "templates"
PALETTES_DIR  = CONF_DIR / "palettes"
POST_SCRIPT_FILE = CONF_DIR / "chromasync-post.sh"
# CONF_FILE     = CONF_DIR / "chromasync.conf"


# Cache dirs/files
CACHE_DIR  = Path(os.getenv(_CHROMASYNC_CACHE_DIR_ENV_VAR, _DEFAULT_CACHE_DIR))
OUTPUT_DIR = CACHE_DIR / "out"
LOG_FILE   = CACHE_DIR / "chromasync.log"
CACHED_PALETTE_FILE = CACHE_DIR / "palette.conf"


# Builds all the required files and directories
def build_environment():
    # Builds config dirs/files
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    PALETTES_DIR.mkdir(parents=True, exist_ok=True)

    if not POST_SCRIPT_FILE.exists():
        POST_SCRIPT_FILE.touch()


    # Builds cache dirs/files
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

