import collections
from collections import defaultdict

import six

from mongo_dynamic_fixture import fields


class BaseSchema(fields.ObjectField):

    schema = {}

    def __init__(self):
        super(BaseSchema, self).__init__(self.schema)

    def generate(self, **kwargs):
        generated = super(BaseSchema, self).generate()
        extra = kwargs.pop('extra', {})
        extra.update(kwargs)
        overrider = self._build_overrider(extra)

        return self._override(generated, overrider)

    def _build_overrider(self, overrider_kwargs):
        infinite_defaultdict = lambda: defaultdict(infinite_defaultdict)
        overrider = infinite_defaultdict()
        keys_values = [(k.split('__'), v)
                       for k, v in six.iteritems(overrider_kwargs)]

        for keys, value in keys_values:
            cd = overrider
            for k in keys[:-1]:
                cd = cd[k]

            cd[keys[-1]] = value

        return dict(overrider)

    def _override(self, generated, overrider):
        for k, v in six.iteritems(overrider):
            if isinstance(v, collections.Mapping):
                r = self._override(generated.get(k, {}), v)
                generated[k] = r
            else:
                generated[k] = overrider[k]

        return generated
