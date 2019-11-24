# -*- coding: utf-8 -*-
"""
The ``typing`` model will check the legality of the arguments.
"""

import traceback
from htekAutoTest.log import log


def _type_check(*arg, arg_type, ):
    """
    Check the legality of the arg according to the arg_type

    :param *arg: the argument need to be checked
    :param arg_type: the type of the argument
    :return: True or False
    """

    if arg_type.upper() == 'IP':
        if len(arg) != 1:
            log.error('IP checking accept only 1 ip address.')
            return False
        else:
            _arg = arg[0]

        try:
            _ip = _arg.split(r'.')
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
                    continue
                else:
                    return False
            else:
                return True
        except AttributeError:
            log.error('Argument should be <str `ip`>, not %s' % type(_arg))
            return False

    elif arg_type.upper() == 'EXT':
        # Extension should be number or SIP URI, so there is currently no too strict check.
        # But it is still need to protect this argument not to be None
        if arg is None:
            log.error('Argument should be a number or a SIP URI, not %s' % arg)
            return False
        else:
            return True
