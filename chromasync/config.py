from pathlib import Path
import os


_CHROMASYNC_DIR_NAME = "chromasync"


_HOME_DIR      = Path(os.getenv("HOME", os.getenv("USERPROFILE")))
_XDG_CACHE_DIR = Path(os.getenv("XDG_CACHE_HOME",  _HOME_DIR / ".cache"))
_XDG_CONF_DIR  = Path(os.getenv("XDG_CONFIG_HOME", _HOME_DIR / ".config"))


# Configuration directories
CONF_DIR = Path(os.path.join(_XDG_CONF_DIR, _CHROMASYNC_DIR_NAME))
TEMPLATES_DIR = CONF_DIR / "templates"
PALETTES_DIR  = CONF_DIR / "palettes"
POST_SCRIPT_FILE = CONF_DIR / "chromasync-post.sh"
# CONF_FILE     = CONF_DIR / "chromasync.conf"


# Cache directories
CACHE_DIR  = Path(os.path.join(_XDG_CACHE_DIR, _CHROMASYNC_DIR_NAME))
OUTPUT_DIR = CACHE_DIR / "out"
LOG_FILE   = CACHE_DIR / "chromasync.log"




# Builds all the required files and directories
def build_environment():
    # Config files and directories
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    PALETTES_DIR.mkdir(parents=True, exist_ok=True)

    if not POST_SCRIPT_FILE.exists():
        POST_SCRIPT_FILE.touch()


    # Cache files and directories
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

