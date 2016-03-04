from sqlalchemy.inspection import inspect


def to_dict(inst, cls):
    """
    Dictify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    thing_relations = inspect(cls).relationships
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    # This for is to dictify relationships too, since a relationship is not a column
    # Probably not neccesary
    # for rel in thing_relations:
    #     d[rel.key] = str(getattr(inst, rel.key))
    return d
