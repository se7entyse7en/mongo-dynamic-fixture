mongo-dynamic-fixture: easy testing by dynamically creating mongo fixtures
==========================================================================

.. image:: https://travis-ci.org/se7entyse7en/mongo-dynamic-fixture.svg?branch=master
  :target: https://travis-ci.org/se7entyse7en/mongo-dynamic-fixture

.. image:: https://coveralls.io/repos/se7entyse7en/mongo-dynamic-fixture/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/se7entyse7en/mongo-dynamic-fixture?branch=master


Motivation
----------

* Using static json fixtures can be a pain as they are hard to maintain if the data evolves
* Adding new tests usually require the addition of new static json fixtures
* If a static json fixture is used in more than one test case even a little change can break all test cases


Inspiration
-----------

This library is inspired from `django-dynamic-fixture <https://github.com/paulocheque/django-dynamic-fixture>`_.


Basic usage
-----------

The basic functions are ``N`` and ``G`` that stand for *New* and *Get* respectively.
First you have to define the schema of the data that you want to generate:
::

    from mongo_dynamic_fixture.schema import BaseSchema
    from mongo_dynamic_fixture.fields import IntegerField
    from mongo_dynamic_fixture.fields import DoubleField
    from mongo_dynamic_fixture.fields import BooleanField
    from mongo_dynamic_fixture.fields import StringField
    from mongo_dynamic_fixture.fields import ArrayField

    class SiteSchema(BaseSchema):

         schema = {
             'name': StringField(),
             'aliases': ArrayField(StringField()),
             'active': BooleanField(),
             'stats': {
                 'last_day_visits': IntegerField(),
                 'average_daily_visits': DoubleField()
             }
         }

After that you can already generate your fixtures!
::

    In [1]: from mongo_dynamic_fixture import N

    In [2]: N(SiteSchema)
    Out[2]:
    {'active': True,
     'aliases': ['kisxcp', 'lG', 'vH5', 'Q7oT1xi', 'RyooxkzB', 'FSFnP'],
     'name': 'oCmy0ZsGS',
     'stats': {'average_daily_visits': 0.02137056342099064, 'last_day_visits': 21}}

The function ``N`` takes an instance of ``BaseSchema`` as first argument and generates a fixture which is compliant with the schema provided.
Obviously sometimes we would like to have more control over the fixture that we want generate, for this reason the ``N`` function also takes ``**kwargs`` optional arguments to fix some specific fields:
::

    In [3]: N(SiteSchema, active=False, stats__last_day_visits=30)
    Out[3]:
    {'active': False,
     'aliases': ['Euheq6sRgF',
      '9ajFi',
      'xhCiZfxSsZ',
      'wf',
      'k9pkIXS',
      'kX10H5j4',
      'ZH',
      '142uYHlJvD'],
     'name': 'KEKasgW',
     'stats': {'average_daily_visits': 0.44985850259520865, 'last_day_visits': 30}}

As you can see both ``active`` and ``last_day_visits`` has been set to the values provided. If the key you want to fix is at the top level of the object then just use the variable name, otherwise list all its ancestors by separating them with ``_`` as for ``stats__last_day_visits``. If the resulting ``**kwargs`` key is not a valid python variable name, then pass it inside the ``extra`` argument:
::

    In [3]: N(MySchema, field1=False, extra={'field2__some-invalid-name!': 30})


The ``G`` function does the same thing of the ``N`` function but additionaly takes a ``pymongo`` connection to a mongo collection as first argument:
::

    In [4]: G(conn['test-db']['test-coll'], SiteSchema, active=False, stats__last_day_visits=30)
    Out[4]:
    {'active': False,
     'aliases': ['K8ae2uwdW',
      '8P1lkRBC6',
      'NUoyht',
      'YG',
      'BS9iV6Yy',
      'gHgRVCq'],
     'name': 'ihccMMs',
     'stats': {'average_daily_visits': 0.5553574439909581, 'last_day_visits': 30}}

we have just created a fixture and inserted it inside the collection 'test-coll' of the database 'test-db'.

The available fields that are all importable from ``mongo_dynamic_fixture.fields`` are the following:

- ``IntegerField``
- ``DoubleField``
- ``BooleanField``
- ``StringField``
- ``ArrayField``
- ``ObjectField``


A little more than basic usage
------------------------------

Each fields takes the following optional arguments:

- ``required`` (default: ``True``)
- ``null`` (default: ``False``)
- ``blank`` (default: ``False``)
- ``not_present_prob`` (default: ``0``)
- ``null_prob`` (default: ``0``)
- ``blank_prob`` (default: ``0``)

If ``required`` is ``False``, then with a probability given by ``not_present_prob`` the field will not be present in the document.

If ``null`` is ``True``, then with a probability given by ``null_prob`` the field will have a value of ``None``.

If ``blank`` is ``True``, then with a probability given by ``blank_prob`` the field will have a blank value which depends on the field.

The blank fields for each fields are the following:

- ``IntegerField`` -> ``0``
- ``DoubleField`` -> ``0.0``
- ``BooleanField`` -> ``False``
- ``StringField`` -> ``''``
- ``ArrayField`` -> ``[]``
- ``ObjectField`` -> ``{}``

``IntegerField`` and ``DoubleField`` also take ``min_value`` and ``max_value`` as optional arguments, and ``StringField`` and ``ArrayField`` also take ``min_length`` and ``max_length``.
``IntegerField``, ``DoubleField`` and ``StringField`` also take ``choices`` as optional argument which must be an iterable. In case that this argument is provided the generated value will one those present in the iterable.
With ``StringField`` it's also possible to specify the charset of the string to generate by passing it to the ``charset`` optional argument (default: ``string.ascii_letters + string.digits``).

Now you might ask "And what is the purpose of ``ObjectField``"? Suppose that you have a schema like the following:
::

    class SiteSchema(BaseSchema):

         schema = {
             'name': StringField(),
             'aliases': ArrayField(StringField()),
             'active': BooleanField(),
             'stats-hourly': {
                 'last_visits': IntegerField(),
                 'average_visits': DoubleField()
             },
             'stats-daily': {
                 'last_visits': IntegerField(),
                 'average_visits': DoubleField()
             },
             'stats-monthly': {
                 'last_visits': IntegerField(),
                 'average_visits': DoubleField()
             }
         }

you can use ``ObjectField`` to write it in a more concise way:
::

    from mongo_dynamic_fixture.fields import ObjectField

    obj_field = ObjectField({'last_visits': IntegerField(),
                             'average_visits': DoubleField()})

    class SiteSchema(BaseSchema):

         schema = {
             'name': StringField(),
             'aliases': ArrayField(StringField()),
             'active': BooleanField(),
             'stats-hourly': obj_field,
             'stats-daily': obj_field,
             'stats-monthly': obj_field
         }



Installation
------------

    pip install mongo-dynamic-fixture


Compatiblity
------------

Tested with:

- ``python2.7`` and ``pymongo>=2.0``
- ``python3.3``, ``python3.4`` and ``pymongo>=2.2``


Contributing
------------

For any suggestion, improvements, issues and bugs please open an Issue.
