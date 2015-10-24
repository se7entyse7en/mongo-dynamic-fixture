import atexit

from mongobox import MongoBox
from mongobox import unittest


class MongoTemporaryInstance(object):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            atexit.register(cls._instance.shutdown)

        return cls._instance

    def __init__(self):
        self._box = MongoBox()
        self._box.start()

    @property
    def conn(self):
        return self._box.client

    def shutdown(self):  # pragma: no cover
        self._box.stop()


class MongoTestCase(unittest.MongoTestCase):

    def __init__(self, *args, **kwargs):
        super(MongoTestCase, self).__init__(*args, **kwargs)
        mongo_temp_instance = MongoTemporaryInstance.get_instance()
        self._conn = mongo_temp_instance.conn()

    @property
    def mongo_client(self):
        return self._conn

    def tearDown(self):
        super(MongoTestCase, self).tearDown()
        self.purge_database()
