from mongo_dynamic_fixture.schema import BaseSchema
from mongo_dynamic_fixture.fields import IntegerField
from mongo_dynamic_fixture.fields import DoubleField
from mongo_dynamic_fixture.fields import StringField
from mongo_dynamic_fixture.fields import ArrayField


class SimpleTestSchema(BaseSchema):

    schema = {
        'array': ArrayField(IntegerField()),
        'nest-1': {
            'nest-2': {
                'string': StringField()
            },
            'integer': IntegerField()
        },
        'nest_3': {
            'double': DoubleField()
        }
    }
