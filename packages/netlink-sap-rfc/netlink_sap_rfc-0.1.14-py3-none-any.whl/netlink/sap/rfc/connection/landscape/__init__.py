"""Get system information from the SAPGUI landscape configuration

For the time being, this works on Windows only, and expects that SAPGUI is installed and configured.
"""

from netlink.logging import logger

try:
    import winreg
except ModuleNotFoundError:
    logger.verbose('winreg not found, no GUI Landscape support.')
    from .landscape import LandscapeBase as Landscape
else:
    from .landscape import Landscape

