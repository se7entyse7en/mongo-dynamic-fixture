import string
import random
import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from mongo_dynamic_fixture.fields import BaseField
from mongo_dynamic_fixture.fields import IntegerField
from mongo_dynamic_fixture.fields import DoubleField
from mongo_dynamic_fixture.fields import BooleanField
from mongo_dynamic_fixture.fields import StringField
from mongo_dynamic_fixture.fields import ArrayField
from mongo_dynamic_fixture.fields import ObjectField
from mongo_dynamic_fixture.exceptions import NotGeneratedException


FIELDS_RANDOM_MODULE = 'mongo_dynamic_fixture.fields.random'


class BaseFieldTestCase(unittest.TestCase):

    def test_not_implemented(self):
        v = BaseField()
        with self.assertRaises(NotImplementedError):
            v.generate()


class IntegerFieldTestCase(unittest.TestCase):

    def test_default(self):
        v = IntegerField()
        self.assertTrue(0 <= v.generate() <= 100)

    def test_min_max_values(self):
        v = IntegerField(min_value=-100, max_value=0)
        self.assertTrue(-100 <= v.generate() <= 0)

        v = IntegerField(min_value=0, max_value=0)
        self.assertEqual(v.generate(), 0)

        v = IntegerField(min_value=100, max_value=0)
        with self.assertRaises(ValueError):
            v.generate()

    def test_not_required(self):
        v = IntegerField(required=False, not_present_prob=0)
        self.assertTrue(0 <= v.generate() <= 100)

        v = IntegerField(required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = IntegerField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = IntegerField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.randint = random.randint
            self.assertTrue(0 <= v.generate() <= 100)

    def test_nullable(self):
        v = IntegerField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.randint = random.randint
            self.assertTrue(0 <= v.generate() <= 100)

        v = IntegerField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

    def test_blankable(self):
        v = IntegerField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.randint = random.randint
            self.assertTrue(0 <= v.generate() <= 100)

        v = IntegerField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), 0)

    def test_choices(self):
        choices = [1, 5, 10]
        v = IntegerField(choices=choices)
        self.assertIn(v.generate(), choices)

    def test_nullable_blankable(self):
        v = IntegerField(null=True, null_prob=0.3,
                         blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), 0)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.randint = random.randint
            self.assertTrue(0 <= v.generate() <= 100)

    def test_nullable_blankable_choices(self):
        choices = [1, 5, 10]
        v = IntegerField(null=True, null_prob=0.3,
                         blank=True, blank_prob=0.3,
                         choices=choices)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            self.assertEqual(v.generate(), 0)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), choices)


class DoubleFieldTestCase(unittest.TestCase):

    def test_default(self):
        v = DoubleField()
        self.assertTrue(0 <= v.generate() <= 1)

    def test_min_max_values(self):
        v = DoubleField(min_value=-2.5, max_value=0)
        self.assertTrue(-2.5 <= v.generate() <= 0)

        v = DoubleField(min_value=0, max_value=0)
        self.assertEqual(v.generate(), 0)

        v = DoubleField(min_value=2.5, max_value=0)
        self.assertTrue(0 <= v.generate() <= 2.5)

    def test_not_required(self):
        v = DoubleField(required=False, not_present_prob=0)
        self.assertTrue(0 <= v.generate() <= 1)

        v = DoubleField(required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = DoubleField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = DoubleField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.uniform = random.uniform
            self.assertTrue(0 <= v.generate() <= 1)

    def test_nullable(self):
        v = DoubleField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.uniform = random.uniform
            self.assertTrue(0 <= v.generate() <= 1)

        v = DoubleField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.uniform = random.uniform
            self.assertIsNone(v.generate())

    def test_blankable(self):
        v = DoubleField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.uniform = random.uniform
            self.assertTrue(0 <= v.generate() <= 1)

        v = DoubleField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.uniform = random.uniform
            self.assertEqual(v.generate(), 0)

    def test_choices(self):
        choices = [1, 5, 10]
        v = DoubleField(choices=choices)
        self.assertIn(v.generate(), choices)

    def test_nullable_blankable(self):
        v = DoubleField(null=True, null_prob=0.3, blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.uniform = random.uniform
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.uniform = random.uniform
            self.assertEqual(v.generate(), 0)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.uniform = random.uniform
            self.assertTrue(0 <= v.generate() <= 1)

    def test_nullable_blankable_choices(self):
        choices = [1, 5, 10]
        v = DoubleField(null=True, null_prob=0.3, blank=True, blank_prob=0.3,
                        choices=choices)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            self.assertEqual(v.generate(), 0)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), choices)


class BooleanFieldTestCase(unittest.TestCase):

    def test_default(self):
        v = BooleanField()
        self.assertIn(v.generate(), [True, False])

    def test_not_required(self):
        v = BooleanField(required=False, not_present_prob=0)
        self.assertIn(v.generate(), [True, False])

        v = BooleanField(required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = BooleanField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = BooleanField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), [True, False])

    def test_nullable(self):
        v = BooleanField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), [True, False])

        v = BooleanField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            self.assertIsNone(v.generate())

    def test_blankable(self):
        v = BooleanField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), [True, False])

        v = BooleanField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            self.assertFalse(v.generate())

    def test_nullable_blankable(self):
        v = BooleanField(null=True, null_prob=0.3, blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            self.assertFalse(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), [True, False])


class StringFieldTestCase(unittest.TestCase):

    def test_default(self):
        v = StringField()
        generated = v.generate()
        self.assertTrue(1 <= len(generated) <= 10)
        self.assertTrue(all([s in (string.ascii_letters + string.digits)
                             for s in generated]))

    def test_min_max_length(self):
        v = StringField(min_length=5, max_length=10)
        generated = v.generate()
        self.assertTrue(5 <= len(generated) <= 10)
        self.assertTrue(all([s in (string.ascii_letters + string.digits)
                             for s in generated]))

        v = StringField(min_length=0, max_length=0)
        generated = v.generate()
        self.assertEqual(generated, '')

        v = StringField(min_length=10, max_length=5)
        with self.assertRaises(ValueError):
            generated = v.generate()

    def test_charset(self):
        charset = '!@#$%^&*()_'
        v = StringField(charset=charset)
        generated = v.generate()
        self.assertTrue(1 <= len(generated) <= 10)
        self.assertTrue(all([s in charset for s in generated]))

    def test_not_required(self):
        v = StringField(required=False, not_present_prob=0)
        generated = v.generate()
        self.assertTrue(1 <= len(generated) <= 10)
        self.assertTrue(all([s in (string.ascii_letters + string.digits)
                             for s in generated]))

        v = StringField(required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = StringField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = StringField(required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([s in (string.ascii_letters + string.digits)
                                 for s in generated]))

    def test_nullable(self):
        v = StringField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([s in (string.ascii_letters + string.digits)
                                 for s in generated]))

        v = StringField(null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            generated = v.generate()
            self.assertIsNone(generated)

    def test_blankable(self):
        v = StringField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([s in (string.ascii_letters + string.digits)
                                 for s in generated]))

        v = StringField(blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            generated = v.generate()
            self.assertEqual(generated, '')

    def test_choices(self):
        choices = ['a', 'b', 'c']
        v = StringField(choices=choices)
        self.assertIn(v.generate(), choices)

    def test_nullable_blankable(self):
        v = StringField(null=True, null_prob=0.3, blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            generated = v.generate()
            self.assertIsNone(generated)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            generated = v.generate()
            self.assertEqual(generated, '')

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([s in (string.ascii_letters + string.digits)
                                 for s in generated]))

    def test_nullable_blankable_choices(self):
        choices = ['a', 'b', 'c']
        v = StringField(null=True, null_prob=0.3, blank=True, blank_prob=0.3,
                        choices=choices)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            generated = v.generate()
            self.assertIsNone(generated)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            self.assertEqual(v.generate(), '')

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            self.assertIn(v.generate(), choices)


class ArrayFieldTestCase(unittest.TestCase):

    def test_default(self):
        v = ArrayField(IntegerField())
        generated = v.generate()
        self.assertTrue(1 <= len(generated) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in generated]))

        int_field = mock.Mock(wraps=IntegerField())
        int_field.generate = lambda: 0
        str_field = mock.Mock(wraps=StringField())
        str_field.generate = lambda: 'string'
        v = ArrayField([int_field, str_field])
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.randint.return_value = 2

            mocked_random.choice.side_effect = [int_field, str_field]
            generated = v.generate()

            self.assertEqual(len(generated), 2)
            self.assertEqual(generated[0], 0)
            self.assertTrue(generated[1], 'string')

    def test_min_max_length(self):
        v = ArrayField(IntegerField(), min_length=5, max_length=10)
        generated = v.generate()
        self.assertTrue(5 <= len(generated) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in generated]))

        v = ArrayField(IntegerField(), min_length=0, max_length=0)
        generated = v.generate()
        self.assertEqual(generated, [])

        v = ArrayField(IntegerField(), min_length=10, max_length=5)
        with self.assertRaises(ValueError):
            generated = v.generate()

    def test_not_required(self):
        v = ArrayField(IntegerField(), required=False, not_present_prob=0)
        generated = v.generate()
        self.assertTrue(1 <= len(generated) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in generated]))

        v = ArrayField(IntegerField(), required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = ArrayField(IntegerField(), required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = ArrayField(IntegerField(), required=False, not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in generated]))

    def test_nullable(self):
        v = ArrayField(IntegerField(), null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in generated]))

        v = ArrayField(IntegerField(), null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

    def test_blankable(self):
        v = ArrayField(IntegerField(), blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in generated]))

        v = ArrayField(IntegerField(), blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), [])

    def test_nullable_blankable(self):
        v = ArrayField(IntegerField(), null=True, null_prob=0.3,
                       blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), [])

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            generated = v.generate()
            self.assertTrue(1 <= len(generated) <= 10)
            self.assertTrue(all([isinstance(i, int) for i in generated]))


class ObjectFieldTestCase(unittest.TestCase):

    simple_schema = {
        'integer': IntegerField(),
        'string': StringField(),
        'boolean': BooleanField()
    }

    complex_schema = {
        'array': ArrayField(IntegerField()),
        'nest-1': {
            'nest-2': {
                'string': StringField()
            },
            'integer': IntegerField()
        }
    }

    nested_schema = {
        'simple': ObjectField(simple_schema),
        'complex': ObjectField(complex_schema)
    }

    def assertEqualSimpleSchema(self, value):
        self.assertEqual(set(value.keys()), set(self.simple_schema.keys()))
        self.assertTrue(0 <= value['integer'] <= 100)
        self.assertTrue(0 <= len(value['string']) <= 10)
        self.assertTrue(all([s in (string.ascii_letters + string.digits)
                             for s in value['string']]))
        self.assertTrue(isinstance(value['boolean'], bool))

    def assertEqualComplexSchema(self, value):
        self.assertEqual(set(value.keys()), set(self.complex_schema.keys()))
        self.assertTrue(0 <= len(value['array']) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in value['array']]))

        self.assertEqual(set(value['nest-1'].keys()),
                         set(self.complex_schema['nest-1'].keys()))
        self.assertTrue(0 <= value['nest-1']['integer'] <= 100)

        self.assertEqual(set(value['nest-1']['nest-2'].keys()),
                         set(self.complex_schema['nest-1']['nest-2'].keys()))
        self.assertTrue(0 <= len(value['nest-1']['nest-2']['string']) <= 10)
        self.assertTrue(all([s in (string.ascii_letters + string.digits)
                             for s in value['nest-1']['nest-2']['string']]))

    def test_default_simple_schema(self):
        v = ObjectField(self.simple_schema)
        self.assertEqualSimpleSchema(v.generate())

    def test_default_complex_schema(self):
        v = ObjectField(self.complex_schema)
        self.assertEqualComplexSchema(v.generate())

    def test_default_nested_schema(self):
        v = ObjectField(self.nested_schema)
        generated = v.generate()
        self.assertEqual(set(generated.keys()), set(self.nested_schema.keys()))
        self.assertEqualSimpleSchema(generated['simple'])
        self.assertEqualComplexSchema(generated['complex'])

    def test_not_required(self):
        v = ObjectField(self.simple_schema, required=False, not_present_prob=0)
        self.assertEqualSimpleSchema(v.generate())

        v = ObjectField(self.simple_schema, required=False, not_present_prob=1)
        with self.assertRaises(NotGeneratedException):
            v.generate()

        v = ObjectField(self.simple_schema, required=False,
                        not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            with self.assertRaises(NotGeneratedException):
                v.generate()

        v = ObjectField(self.simple_schema, required=False,
                        not_present_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqualSimpleSchema(v.generate())

    def test_nullable(self):
        v = ObjectField(self.simple_schema, null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqualSimpleSchema(v.generate())

        v = ObjectField(self.simple_schema, null=True, null_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

    def test_blankable(self):
        v = ObjectField(self.simple_schema, blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqualSimpleSchema(v.generate())

        v = ObjectField(self.simple_schema, blank=True, blank_prob=0.5)
        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), {})

    def test_nullable_blankable(self):
        v = ObjectField(self.simple_schema, null=True, null_prob=0.3,
                        blank=True, blank_prob=0.3)

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertIsNone(v.generate())

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 0.5
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqual(v.generate(), {})

        with mock.patch(FIELDS_RANDOM_MODULE) as mocked_random:
            mocked_random.random.return_value = 1
            mocked_random.choice = random.choice
            mocked_random.randint = random.randint
            self.assertEqualSimpleSchema(v.generate())
