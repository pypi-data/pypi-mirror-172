import collections

from netlink.logging import logger
from lxml import etree


def process_landscape_xml(file_handle):
    root = etree.parse(file_handle).getroot()
    if root.tag != "Landscape":
        msg = f"Wrong root tag: <{root.tag}> - expected <Landscape>"
        logger.error(msg)
        raise ValueError(msg)
    sysids = collections.defaultdict(dict)
    message_servers = {}
    for element in root:
        if element.tag == "Services":
            for child in element:
                # noinspection PyProtectedMember
                if type(child) == etree._Comment:
                    continue
                if child.tag != "Service":
                    logger.warning(f"Wrong tag: <{child.tag}> - expected <Service>")
                    continue
                if child.get("type") == "SAPGUI":
                    sid = child.get("systemid")
                    if child.get("sncname"):
                        sysids[sid]["sncname"] = child.get("sncname")
                    if child.get("mode") == "1":
                        sysids[sid]["ashost"], sysids[sid]["sysnr"] = child.get("server").split(":", 1)
                        sysids[sid]["sysnr"] = sysids[sid]["sysnr"][-2:]
                    else:
                        sysids[sid]["msid"] = child.get("msid")
                        sysids[sid]["group"] = child.get("server")
        elif element.tag == "Messageservers":
            for child in element:
                # noinspection PyProtectedMember
                if type(child) == etree._Comment:
                    continue
                if child.tag != "Messageserver":
                    logger.warning(f"Wrong tag: <{child.tag}> - expected <Messageserver>")
                    continue
                message_servers[child.get("uuid")] = {"mshost": child.get("host"), "msserv": child.get("port")}
    return sysids, message_servers