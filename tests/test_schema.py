import string
import unittest

from tests import SimpleTestSchema


class SchemaTestCase(unittest.TestCase):

    def test_default(self):
        v = SimpleTestSchema()
        generated = v.generate()
        self.assertEqual(set(generated.keys()),
                         set(SimpleTestSchema.schema.keys()))
        self.assertTrue(0 <= len(generated['array']) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in generated['array']]))

        self.assertEqual(set(generated['nest-1'].keys()),
                         set(SimpleTestSchema.schema['nest-1'].keys()))
        self.assertTrue(0 <= generated['nest-1']['integer'] <= 100)

        self.assertEqual(
            set(generated['nest-1']['nest-2'].keys()),
            set(SimpleTestSchema.schema['nest-1']['nest-2'].keys()))
        self.assertTrue(
            0 <= len(generated['nest-1']['nest-2']['string']) <= 10)
        self.assertTrue(
            all([s in (string.ascii_letters + string.digits)
                 for s in generated['nest-1']['nest-2']['string']]))
        self.assertTrue(0 <= generated['nest_3']['double'] <= 1)

    def test_with_overrider(self):
        overrider = {
            'nest-1__integer': 10000,
            'nest-1__nest-2__string': 'abcdef'
        }
        v = SimpleTestSchema()
        generated = v.generate(nest_3__double=999.999, extra=overrider)
        self.assertEqual(set(generated.keys()),
                         set(SimpleTestSchema.schema.keys()))
        self.assertTrue(0 <= len(generated['array']) <= 10)
        self.assertTrue(all([isinstance(i, int) for i in generated['array']]))

        self.assertEqual(set(generated['nest-1'].keys()),
                         set(SimpleTestSchema.schema['nest-1'].keys()))
        self.assertEqual(generated['nest-1']['integer'], 10000)

        self.assertEqual(
            set(generated['nest-1']['nest-2'].keys()),
            set(SimpleTestSchema.schema['nest-1']['nest-2'].keys()))
        self.assertEqual(generated['nest-1']['nest-2']['string'], 'abcdef')
        self.assertEqual(generated['nest_3']['double'], 999.999)
