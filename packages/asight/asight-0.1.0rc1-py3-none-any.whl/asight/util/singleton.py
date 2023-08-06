"""
singleton module
"""


def singleton(cls):
    """
    :param cls: any class
    :return: singleton handle
    """
    _instance = {}

    def _singleton(*args: any, **kw: any) -> any:
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance.get(cls)

    return _singleton
