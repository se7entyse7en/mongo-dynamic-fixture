from mongo_dynamic_fixture.test import MongoTestCase
from mongo_dynamic_fixture.fixture import Fixture


class FixtureTestCase(MongoTestCase):

    def test_fixture(self):
        data = {'_id': '123',
                'key': 'value'}
        db_name = 'db_test'
        coll_name = 'coll_test'
        conn = self.mongo_client[db_name][coll_name]
        fixture = Fixture(conn, data)
        fixture.insert()

        documents = list(conn.find())
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], data)
