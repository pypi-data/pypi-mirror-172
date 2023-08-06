from .login import login
from .server import Server


def _get_keepass_entry(keepass_database, **kwargs):
    entries = keepass_database.find_entries(**kwargs)
    if entries:  # found at least one
        if len(entries) > 1:  # not unique -> error
            raise Exception
        return entries[0]
    return None


def keepass(keepass_database, sysid: str, client: str, user: str = None, language: str = None, raw: bool = False, landscape=None):
    """
    Connect to SAP using information from KeePass Database

    In addition to the password, any other setting might be stored (e.g. ashost)

    :param keepass_database: Opened Keepass Database
    :param sysid: Used to search  - first looks for this value in property 'logical_system'
    :param client: Used to search
    :param user: Used to search
    :param language: override possible entry
    :param raw:
    :param landscape: Used to determine connection information if not in KeePass
    :return:
    """

    # try if sysid a logical_system
    entry = _get_keepass_entry(keepass_database=keepass_database,
                               string=dict(logical_system=sysid))
    if not entry:  # search for sysid, client, user
        entry = _get_keepass_entry(keepass_database=keepass_database,
                                   username=user.upper(),
                                   string=dict(sysid=sysid.upper(),
                                               client=client))
        if not entry:
            raise Exception

    # try to create a server from the data in keepass
    server = Server(**entry.custom_properties)
    if not server.is_valid:  # no valid config
        server = Server.from_landscape(sysid, landscape=landscape)
    if language is None:
        language = entry.custom_properties.get('language', 'EN')

    return login(server=server,
                 client=entry.get_custom_property('client'),
                 user=entry.username,
                 passwd=entry.password,
                 language=language,
                 raw=raw)
