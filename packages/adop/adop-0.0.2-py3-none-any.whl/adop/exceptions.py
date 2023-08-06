class Fail(Exception):
    pass


class CommandFail(Exception):
    pass


class CacheNotFound(Fail):
    pass
