class Fixture(object):

    def __init__(self, conn, data):
        self._conn = conn
        self._data = data

    @property
    def conn(self):
        return self._conn

    @property
    def data(self):
        return self._data

    def insert(self):
        self.conn.insert(self.data)
