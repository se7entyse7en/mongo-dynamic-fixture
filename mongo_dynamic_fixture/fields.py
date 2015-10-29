import string
import random
import collections

import six

from mongo_dynamic_fixture.exceptions import NotGeneratedException


class BaseField(object):

    blank_value = ''

    def __init__(self, required=True, null=False, blank=False,
                 not_present_prob=0, null_prob=0, blank_prob=0):
        self._required = required
        self._null = null
        self._blank = blank
        self._not_present_prob = not_present_prob
        self._null_prob = null_prob
        self._blank_prob = blank_prob

    @property
    def required(self):
        return self._required

    @property
    def null(self):
        return self._null

    @property
    def blank(self):
        return self._blank

    @property
    def not_present_prob(self):
        return self._not_present_prob

    @property
    def null_prob(self):
        return self._null_prob

    @property
    def blank_prob(self):
        return self._blank_prob

    def generate(self):
        r1 = random.random()
        if not self.required and r1 < self.not_present_prob:
            raise NotGeneratedException

        r2 = random.random()
        if self.null and r2 < self.null_prob:
            value = None
        elif self.blank and r2 < self.null_prob + self.blank_prob:
            value = self.blank_value
        else:
            value = self._generate_value()

        return value

    def generate_value(self):
        raise NotImplementedError

    def _generate_value(self):
        return self.generate_value()


class ChoosableBaseField(BaseField):

    def __init__(self, choices=None, **kwargs):
        super(ChoosableBaseField, self).__init__(**kwargs)
        self._choices = choices

    @property
    def choices(self):
        return self._choices

    def _generate_value(self):
        if self.choices is not None:
            value = random.choice(self.choices)
        else:
            value = self.generate_value()

        return value


class NumericalField(ChoosableBaseField):

    def __init__(self, min_value, max_value, **kwargs):
        super(NumericalField, self).__init__(**kwargs)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value


class IntegerField(NumericalField):

    blank_value = 0

    def __init__(self, min_value=0, max_value=100, **kwargs):
        super(IntegerField, self).__init__(min_value, max_value, **kwargs)

    def generate_value(self):
        return random.randint(self.min_value, self.max_value)


class DoubleField(NumericalField):

    blank_value = 0.0

    def __init__(self, min_value=0.0, max_value=1.0, **kwargs):
        super(DoubleField, self).__init__(min_value, max_value, **kwargs)

    def generate_value(self):
        return random.uniform(self.min_value, self.max_value)


class BooleanField(BaseField):

    blank_value = False

    def generate_value(self):
        return random.choice([True, False])


class StringField(ChoosableBaseField):

    blank_value = ''

    def __init__(self, min_length=1, max_length=10, charset=None, **kwargs):
        super(StringField, self).__init__(**kwargs)
        self._min_length = min_length
        self._max_length = max_length
        self._charset = charset or (string.ascii_letters + string.digits)

    @property
    def min_length(self):
        return self._min_length

    @property
    def max_length(self):
        return self._max_length

    @property
    def charset(self):
        return self._charset

    def generate_value(self):
        return ''.join([
            random.choice(self.charset) for _ in range(random.randint(
                self.min_length, self.max_length))])


class ArrayField(BaseField):

    blank_value = []

    def __init__(self, content_fields, min_length=1, max_length=10, **kwargs):
        super(ArrayField, self).__init__(**kwargs)
        self._min_length = min_length
        self._max_length = max_length
        if not isinstance(content_fields, collections.Iterable):
            content_fields = [content_fields]
        self._content_fields = content_fields

    @property
    def min_length(self):
        return self._min_length

    @property
    def max_length(self):
        return self._max_length

    @property
    def content_fields(self):
        return self._content_fields

    def generate_value(self):
        return [random.choice(self.content_fields).generate() for _ in range(
            random.randint(self.min_length, self.max_length))]


class ObjectField(BaseField):

    blank_value = {}

    def __init__(self, schema, **kwargs):
        super(ObjectField, self).__init__(**kwargs)
        self._schema = schema

    @property
    def schema(self):
        return self._schema

    def generate_value(self):

        def _generate_value(schema):
            generated = {}
            for k, v in six.iteritems(schema):
                if isinstance(v, BaseField):
                    generated[k] = v.generate()
                else:
                    sub_generated = {}
                    for sub_k, sub_v in six.iteritems(v):
                        sub_generated[sub_k] = _generate_value({
                            sub_k: sub_v})[sub_k]

                    generated[k] = sub_generated

            return generated

        return _generate_value(self.schema)
