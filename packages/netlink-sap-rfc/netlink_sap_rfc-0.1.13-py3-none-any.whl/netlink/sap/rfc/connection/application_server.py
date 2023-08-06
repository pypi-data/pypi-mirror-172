from netlink.sap.rfc.connection import Server


class ApplicationServer:
    def __init__(self, name, server: Server, connection):
        self.name = name
        self._server = server
        self._connection = connection

    def connect(self):
        return self._connection.clone(server=self._server)

    open = connect
