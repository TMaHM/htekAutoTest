# -*- coding: utf-8 -*-
"""
The ``typing`` model will check the legality of the arguments.
"""

import traceback

from .log import log


def _type_check(arg, arg_type):
    """
    Check the legality of the arg according to the arg_type

    :param arg:
    :param arg_type:
    :return: True of False
    """
    if arg_type.upper() == 'IP':
        try:
            _ip = arg.split(r'.')
            if len(_ip) == 4:
                pass
            else:
                return False
            if 0 < int(_ip[0]) < 255:
                pass
            else:
                return False
            for __ in _ip[1:]:
                if 0 <= int(__) < 255:
                    return True
                else:
                    return False
        except AttributeError:
            log.error('Argument should be <str `ip`>, not %s' % type(arg))
            return False

    elif arg_type.upper() == 'EXT':
        # extension should be number or SIP URI, so there is currently no too strict check.
        if arg is None:
            log.error('Argument should be a number or a SIP URI, not %s' % arg)
            return False
        else:
            return True
