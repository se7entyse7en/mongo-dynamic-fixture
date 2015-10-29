from mongo_dynamic_fixture.fixture import Fixture


def N(*args, **kwargs):
    schema_cls = args[0] if args else None
    extra = kwargs.pop('extra', {})
    kwargs.update(extra)
    if schema_cls is not None:
        data = schema_cls().generate(**kwargs)
    else:
        data = kwargs

    return data


def G(conn, *args, **kwargs):
    data = N(*args, **kwargs)
    fixture = Fixture(conn, data)
    fixture.insert()

    return data
