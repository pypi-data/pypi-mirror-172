import collections.abc

from netlink.logging import logger
from .landscape import Landscape

default_landscape = Landscape()


class Server(collections.abc.Mapping):
    PARAMETER_NAMES = ('ashost', 'sysnr', 'mshost', 'msserv', 'sysid', 'group')

    def __init__(self,
                 ashost: str = None, sysnr: str = None,  # direct Application Host
                 mshost: str = None, msserv: str = None, sysid: str = None, group: str = None,  # via message server
                 **kwargs,  # dummy to catch unsupported
                 ):
        """

        :param ashost:
        :param sysnr:
        :param mshost:
        :param msserv:
        :param sysid:
        :param group:
        """
        self.ashost = ashost
        self.sysnr = sysnr
        self.mshost = mshost
        self.msserv = msserv
        self.sysid = sysid
        self.group = group

    def __getitem__(self, item):
        if item.lower() in self.PARAMETER_NAMES:
            return self.__dict__[item.lower()]
        raise KeyError(item)

    def __getattr__(self, item):
        if item.lower() in self.PARAMETER_NAMES:
            return self[item]
        raise AttributeError(item)

    def __len__(self):
        return len([i for i in self.PARAMETER_NAMES if self[i]])

    def __iter__(self):
        return iter([i for i in self.PARAMETER_NAMES if self[i]])

    def kwargs(self):
        return {k: v for k, v in self.items()}

    def __str__(self):
        if self.ashost is not None:
            return f'{self.ashost}:32{self.sysnr}'
        else:
            return f"{self.mshost}:{self.msserv} ({self.sysid}-{self.group})"

    @property
    def is_valid(self) -> bool:
        if self.ashost is not None:
            if self.sysnr is None or (
            self.mshost is not None or self.msserv is not None or self.group is not None):
                return False
        else:
            if self.sysnr is not None or self.mshost is None or self.msserv is None or self.sysid is None or self.group is None:
                return False
        return True

    @classmethod
    def from_landscape(cls,
                       sysid: str,
                       landscape: Landscape = None) -> 'Server':
        """
        Get server info from Landscape xml

        :param sysid:
        :param landscape:
        """
        if landscape is None:
            landscape = default_landscape
        try:
            entry = landscape[sysid.upper()]
        except KeyError:
            msg = f"System ID '{sysid.upper()}' not found in Landscape."
            logger.error(msg)
            raise KeyError(msg) from None
        kwargs = {k: v for k, v in entry.items() if k in cls.PARAMETER_NAMES}
        return cls(**kwargs)