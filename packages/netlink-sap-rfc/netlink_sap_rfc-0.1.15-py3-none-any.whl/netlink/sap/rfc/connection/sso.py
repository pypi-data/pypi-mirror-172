import getpass

from .connection import Connection
from .landscape import Landscape
from .server import Server

from netlink.logging import logger

default_landscape = Landscape()


def sso(sysid: str, client: str, user: str = None, language="EN", raw: bool = False):
    """
    Connect to SAP using Single-Sign-On

    :param sysid: System ID (<sid>)
    :param client: SAP Client
    :param user: User ID, defaults currently user
    :param language: Default: EN
    :param raw: Default: False
    :return: sap.rfc.Connection
    """
    sysid = sysid.upper()
    if user is None:
        user = getpass.getuser()
    user = user.upper()

    login_info = default_landscape[sysid].copy()
    if not login_info.get("sncname"):
        msg = f"SNC Name for {sysid} not found."
        logger.error(msg)
        raise AttributeError(msg)

    kwargs=Server.from_landscape(sysid).kwargs()
    logger.info(f"Connecting using SSO to {sysid}/{client} with {user}")
    return Connection(client=client,
                      user=user,
                      snc_qop='9',
                      snc_partnername=login_info["sncname"],
                      language=language,
                      raw=raw, **kwargs)
