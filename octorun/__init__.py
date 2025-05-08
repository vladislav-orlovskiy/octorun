import logging
from importlib.metadata import PackageNotFoundError, version

logging.basicConfig(level=logging.DEBUG)
try:
    __version__ = version("octorun")
except PackageNotFoundError:
    try:
        with open("VERSION", "r") as version_file:
            __version__ = version_file.read().strip()
    except FileNotFoundError:
        logging.error("Version file not found. Setting version to 0.0.0.")
        __version__ = "0.0.0"
