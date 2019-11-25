import traceback


class WrongIP(ValueError):
    """Wrong IP Address"""


class WrongExt(ValueError):
    """Wrong Extension"""


class WrongLine(ValueError):
    """Wrong Line"""


def wrong_ip():
    raise WrongIP


def wrong_ext():
    raise WrongExt


def wrong_line():
    raise WrongLine
