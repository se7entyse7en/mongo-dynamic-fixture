import string

from tests import SimpleTestSchema
from mongo_dynamic_fixture import N
from mongo_dynamic_fixture import G
from mongo_dynamic_fixture.test import MongoTestCase


class FacadesTestCase(MongoTestCase):

    def setUp(self):
        super(FacadesTestCase, self).setUp()
        db_name = 'db_test'
        coll_name = 'coll_test'
        self.conn = self.mongo_client[db_name][coll_name]

    def test_N_no_schema_no_extra(self):
        actual_data = N(_id='123', key_1='value-1', key_2='value-2')
        expected_data = {
            '_id': '123',
            'key_1': 'value-1',
            'key_2': 'value-2'
        }
        self.assertEqual(actual_data, expected_data)

    def test_N_no_schema(self):
        actual_data = N(_id='123', key_1='value-1', key_2='value-2',
                        extra={'key-3': 'value-3'})
        expected_data = {
            '_id': '123',
            'key_1': 'value-1',
            'key_2': 'value-2',
            'key-3': 'value-3'
        }
        self.assertEqual(actual_data, expected_data)

    def test_N_with_schema_no_extra(self):
        actual_data = N(SimpleTestSchema, _id='123', nest_3__double=999.999)

        self.assertEqual(
            set(actual_data.keys()),
            set(SimpleTestSchema.schema.keys()).union(set(['_id'])))
        self.assertEqual(actual_data['_id'], '123')
        self.assertTrue(0 <= len(actual_data['array']) <= 10)
        self.assertTrue(all([isinstance(i, int)
                             for i in actual_data['array']]))

        self.assertEqual(set(actual_data['nest-1'].keys()),
                         set(SimpleTestSchema.schema['nest-1'].keys()))
        self.assertTrue(0 <= actual_data['nest-1']['integer'] <= 100)

        self.assertTrue(
            0 <= len(actual_data['nest-1']['nest-2']['string']) <= 10)
        self.assertTrue(
            all([s in (string.ascii_letters + string.digits)
                 for s in actual_data['nest-1']['nest-2']['string']]))
        self.assertEqual(actual_data['nest_3']['double'], 999.999)

    def test_N_with_schema(self):
        actual_data = N(SimpleTestSchema, _id='123', nest_3__double=999.999,
                        extra={'nest-1__nest-2__string': 'abcdef',
                               'nest-1__integer': 10000})

        self.assertEqual(
            set(actual_data.keys()),
            set(SimpleTestSchema.schema.keys()).union(set(['_id'])))
        self.assertEqual(actual_data['_id'], '123')
        self.assertTrue(0 <= len(actual_data['array']) <= 10)
        self.assertTrue(all([isinstance(i, int)
                             for i in actual_data['array']]))

        self.assertEqual(set(actual_data['nest-1'].keys()),
                         set(SimpleTestSchema.schema['nest-1'].keys()))
        self.assertEqual(actual_data['nest-1']['integer'], 10000)

        self.assertEqual(
            set(actual_data['nest-1']['nest-2'].keys()),
            set(SimpleTestSchema.schema['nest-1']['nest-2'].keys()))
        self.assertEqual(actual_data['nest-1']['nest-2']['string'], 'abcdef')
        self.assertEqual(actual_data['nest_3']['double'], 999.999)

    def test_G_no_schema_no_extra(self):
        actual_data = G(self.conn, _id='123', key_1='value-1', key_2='value-2')
        expected_data = {
            '_id': '123',
            'key_1': 'value-1',
            'key_2': 'value-2'
        }
        self.assertEqual(actual_data, expected_data)

        documents = list(self.conn.find())
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], expected_data)

    def test_G_no_schema(self):
        actual_data = G(self.conn, _id='123', key_1='value-1', key_2='value-2',
                        extra={'key-3': 'value-3'})
        expected_data = {
            '_id': '123',
            'key_1': 'value-1',
            'key_2': 'value-2',
            'key-3': 'value-3'
        }
        self.assertEqual(actual_data, expected_data)

        documents = list(self.conn.find())
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], expected_data)

    def test_G_with_schema_no_extra(self):
        actual_data = G(self.conn, SimpleTestSchema, _id='123',
                        nest_3__double=999.999)

        documents = list(self.conn.find())
        self.assertEqual(len(documents), 1)

        for data in [actual_data, documents[0]]:
            self.assertEqual(
                set(data.keys()),
                set(SimpleTestSchema.schema.keys()).union(set(['_id'])))
            self.assertEqual(data['_id'], '123')
            self.assertTrue(0 <= len(data['array']) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in data['array']]))

            self.assertEqual(set(data['nest-1'].keys()),
                             set(SimpleTestSchema.schema['nest-1'].keys()))
            self.assertTrue(0 <= actual_data['nest-1']['integer'] <= 100)

            self.assertTrue(0 <= len(data['nest-1']['nest-2']['string']) <= 10)
            self.assertTrue(
                all([s in (string.ascii_letters + string.digits)
                     for s in data['nest-1']['nest-2']['string']]))
            self.assertEqual(data['nest_3']['double'], 999.999)

    def test_G_with_schema(self):
        actual_data = G(self.conn, SimpleTestSchema, _id='123',
                        nest_3__double=999.999,
                        extra={'nest-1__nest-2__string': 'abcdef',
                               'nest-1__integer': 10000})

        documents = list(self.conn.find())
        self.assertEqual(len(documents), 1)

        for data in [actual_data, documents[0]]:
            self.assertEqual(
                set(data.keys()),
                set(SimpleTestSchema.schema.keys()).union(set(['_id'])))
            self.assertEqual(data['_id'], '123')
            self.assertTrue(0 <= len(data['array']) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in data['array']]))

            self.assertEqual(set(data['nest-1'].keys()),
                             set(SimpleTestSchema.schema['nest-1'].keys()))
            self.assertEqual(data['nest-1']['integer'], 10000)

            self.assertEqual(
                set(data['nest-1']['nest-2'].keys()),
                set(SimpleTestSchema.schema['nest-1']['nest-2'].keys()))
            self.assertEqual(data['nest-1']['nest-2']['string'], 'abcdef')
            self.assertEqual(data['nest_3']['double'], 999.999)
