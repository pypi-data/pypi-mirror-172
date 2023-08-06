from .server import Server
from .login import login


def login_sid(sysid: str, client: str, passwd: str, user: str = None, language="EN", raw: bool = False, landscape=None):
    """

    :param sysid:
    :param client:
    :param passwd:
    :param user:
    :param language:
    :param raw:
    :param landscape:
    :return:
    """
    sysid = sysid.upper()
    return login(server=Server.from_landscape(sysid, landscape=landscape),
                 client=client,
                 user=user,
                 passwd=passwd,
                 language=language,
                 raw=raw)
