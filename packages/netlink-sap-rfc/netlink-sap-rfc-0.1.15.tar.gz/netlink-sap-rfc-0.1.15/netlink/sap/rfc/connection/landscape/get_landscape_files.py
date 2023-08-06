import winreg

from netlink.logging import logger

def get_landscape_files():
    registry_key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                                  r"Software\SAP\SAPLogon\LandscapeFilesLastUsed")
    result = []
    try:
        path = winreg.QueryValueEx(registry_key, "LandscapeFileOnServer")[0]
        logger.trace(f'Found SAPGUI Landscape Server File {path}')
        result.append(path)
    except FileNotFoundError:
        logger.verbose('No entry for SAPgui Landscape Server File found.')
    try:
        path = winreg.QueryValueEx(registry_key, "LandscapeFile")[0]
        logger.trace(f'Found local SAPGUI Landscape File {path}')
        result.append(path)
    except FileNotFoundError:
        logger.verbose('No entry for local SAPgui Landscape File found.')
    return tuple(result)