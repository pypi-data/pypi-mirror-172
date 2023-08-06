import datetime
import re

import pyrfc

from netlink.logging import logger

from .server import Server
from .util import make_date_time_converters
from ..function import Function
from ..table import select
from ..exception import LogonError, CommunicationError

DATETIME_RE = re.compile(r"Date:\s(\d{4})(\d{2})(\d{2}).*?Time:\s(\d{2})(\d{2})(\d{2})")


class Connection:
    def __init__(self, raw: bool = False, **kwargs):
        if 'config' not in kwargs:
            kwargs['config'] = {}
        kwargs['config']['dtime'] = not raw
        self._clone_data = kwargs.copy()
        logger.debug("Connecting to SAP: %s" % str({k: v for k, v in kwargs.items() if k.upper() not in ('PASSWD', 'X509CERT')}))
        try:
            self._connection = pyrfc.Connection(**kwargs)
        except pyrfc.LogonError as e:
            logger.error(e.message)
            raise LogonError from None
        except pyrfc.CommunicationError as e:
            logger.error(e.message)
            raise CommunicationError from None

        self.connection_attributes = self._connection.get_connection_attributes()
        self._functions = {}
        self._application_servers = None
        self._converters = None

    def clone(self, **kwargs):
        clone_args = self._clone_data.copy()
        clone_args.update(kwargs)
        return self.__class__(**clone_args)

    @property
    def datetime(self):
        """Current (local) time reported by connection"""
        response = self.stfc_connection(requtext='0')
        m = DATETIME_RE.search(response.resptext)
        return datetime.datetime(*[int(m.group(i+1)) for i in range(6)])

    def to_date(self, value):
        """convert formatted datestring to datetime.date using connecton date-format"""
        if self._converters is None:
            self._set_converters()
        return self._converters['date'](value)

    def to_time(self, value):
        """convert formatted timestring to datetime.date using connecton date-format"""
        if self._converters is None:
            self._set_converters()
        return self._converters['time'](value)

    def datetime_system_to_user(self, value):
        """convert datetime from system time to user time"""
        if self._converters is None:
            self._set_converters()
        return self._converters['system_to_user'](value)

    def datetime_user_to_system(self, value):
        """convert datetime from user time to system time"""
        if self._converters is None:
            self._set_converters()
        return self._converters['user_to_system'](value)


    def _set_converters(self):
        user = self.bapi_user_get_detail(username=self.user)
        date_converter, time_converter = make_date_time_converters(user.defaults.datfm, user.defaults.timefm)
        self._converters = dict(date=date_converter, time=time_converter)
        user_timezone = user.logondata.tzone
        system_timezone = self.select('TTZCU', 'TZONESYS')[0].tzonesys
        if user_timezone == system_timezone:
            offset = 0
        else:
            user_time_rule = self.select('TTZZ', 'ZONERULE', tzone=user_timezone)[0].zonerule
            user_delta = int(user_time_rule[1:3])*60 + int(user_time_rule[3:5])
            if user_time_rule[0] == 'M':
                user_delta = -user_delta
            system_time_rule = self.select('TTZZ', 'ZONERULE', tzone=system_timezone)[0].zonerule
            system_delta = int(system_time_rule[1:3])*60 + int(system_time_rule[3:5])
            if system_time_rule[0] == 'M':
                system_delta = -system_delta
            offset = datetime.timedelta(seconds=user_delta-system_delta)
        if not offset:
            self._converters['system_to_user'] = lambda x: x
            self._converters['user_to_system'] = lambda x: x
        else:
            self._converters['system_to_user'] = lambda x: x+offset
            self._converters['user_to_system'] = lambda x: x-offset

    def __getattr__(self, item):
        if item == "call":
            return self._connection.call
        if item == "get_function_description":
            return self._connection.get_function_description
        if item.upper() not in self._functions and item in self.connection_attributes:
            return self.connection_attributes[item]
        return self[item]

    def __getitem__(self, item):
        item = item.upper()
        if item not in self._functions:
            logger.debug(f"Initializing function '{item}'")
            self._functions[item] = Function(self, item)
        return self._functions[item]

    @property
    def sid(self):
        return self.sysId

    @property
    def sysid(self):
        return self.sysId

    def __str__(self):
        return f"{self.sysId}/{self.client} ({self.user})"

    def close(self):
        self._connection.close()

    def __del__(self):
        self.close()

    def select(self, table, *args, **kwargs):
        return select(self, table, *args, **kwargs)

    @property
    def application_servers(self):
        if self._application_servers is None:
            response = self.th_server_list()
            self._application_servers = {i.name: self.ApplicationServer(
                i.name, server=Server(ashost=i.host, sysnr=str(int.from_bytes(i.servno, 'big'))[-2:]), connection=self) for i in response.list}
        return self._application_servers
