from netlink.core import Singleton, Mapping
from netlink.sap.rfc.connection import Connection


class RfcDestinationMap(Singleton, Mapping):
    def __init__(self):
        if '_data' not in self.__dict__:
            self._data = {}
            try:
                with open('sapnwrfc.ini', 'r', encoding='utf-8-sig') as f:
                    record = {}
                    dest = ""
                    for line in f:
                        if line.startswith('#') or line.startswith('/*') or line.startswith('//'):
                            continue
                        line = line.strip()
                        # empty line completes a 'dest' section (if open)
                        if not line:
                            if dest:
                                self._data[dest] = record
                                self._data[dest]['dest'] = dest
                                record = {}
                                dest = ''
                            continue
                        try:
                            key, value = line.split('=', maxsplit=1)
                        except ValueError:
                            continue
                        key = key.strip().lower()
                        value = value.strip()
                        if key == 'dest':
                            dest = value.upper()
                            continue
                        record[key] = value
                    if dest:
                        self._data[dest] = record
                        self._data[dest]['dest'] = dest
            except FileNotFoundError:
                pass


rfc_destination_map = RfcDestinationMap()


def dest(destination: str):
    return Connection(**rfc_destination_map[destination.upper()])
