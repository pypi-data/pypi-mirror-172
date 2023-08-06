import getpass

from netlink.logging import logger
from .connection import Connection


def login(server, client: str, passwd: str, user: str = None, language="EN", raw: bool = False):
    """
    Connect to SAP

    :param server:
    :param client:
    :param passwd:
    :param user:
    :param language:
    :param raw:
    :return:
    """
    if user is None:
        user = getpass.getuser()
    user = user.upper()

    kwargs=server.kwargs()
    logger.verbose(f"Connecting to {server} with {user}")
    return Connection(client=client,
                      user=user,
                      passwd=passwd,
                      language=language,
                      raw=raw,
                      **kwargs)
