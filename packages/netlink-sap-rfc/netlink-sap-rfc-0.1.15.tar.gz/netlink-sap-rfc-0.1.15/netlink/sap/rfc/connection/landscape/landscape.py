import pathlib

from netlink.core import Mapping
from netlink.logging import logger
from .get_landscape_files import get_landscape_files
from .process_landscape_xml import process_landscape_xml


class LandscapeBase(Mapping):
    def __init__(self):
        self._data = {}

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)


class Landscape(LandscapeBase):
    """SAP System information from GUI Landscape XML files"""

    def __init__(self, landscape_file=None):
        super(Landscape, self).__init__()
        sysids = {}
        message_servers = {}
        if landscape_file is None:
            for landscape_file in get_landscape_files():
                logger.verbose(f"Processing {landscape_file}")
                with open(landscape_file, "r", encoding="utf-8-sig") as file_handle:
                    t_sysids, t_message_servers = process_landscape_xml(file_handle)
                sysids.update({i: t_sysids[i] for i in t_sysids})
                message_servers.update(t_message_servers)
        else:
            if isinstance(landscape_file, str):
                file_handle = open(landscape_file, "r", encoding="utf-8-sig")
            elif isinstance(landscape_file, pathlib.Path):
                file_handle = landscape_file.open("r", encoding="utf-8-sig")
            else:
                file_handle = landscape_file
            t_sysids, t_message_servers = process_landscape_xml(file_handle)
            if file_handle != landscape_file:
                file_handle.close()
            sysids.update({i: t_sysids[i] for i in t_sysids})
            message_servers.update(t_message_servers)
        for sysid in sysids:
            if sysids[sysid].get("msid"):
                sysids[sysid].update(message_servers[sysids[sysid].pop("msid")])
                sysids[sysid]["sysid"] = sysid
            logger.trace(f"Landscape Entry {sysid}: {sysids[sysid]}")
            self._data[sysid] = sysids[sysid]

    def __getitem__(self, item):
        return self._data[item.upper()]
