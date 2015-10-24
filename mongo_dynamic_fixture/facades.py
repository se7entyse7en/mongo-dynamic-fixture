from mongo_dynamic_fixture.fixture import Fixture


def N(*args, **kwargs):
    schema = args[0] if args else None
    extra = kwargs.pop('extra', {})
    kwargs.update(extra)
    data = schema.generate(**kwargs) if schema is not None else kwargs

    return data


def G(conn, *args, **kwargs):
    data = N(*args, **kwargs)
    fixture = Fixture(conn, data)
    fixture.insert()

    return data
