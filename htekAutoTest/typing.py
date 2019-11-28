# -*- coding: utf-8 -*-
"""
The ``typing`` model will check the legality of the arguments.
"""

import os

from htekAutoTest.log import log


def _format_check(*arg, arg_type, ):
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
        if len(arg) == 1:
            if arg[0] is None:
                log.error('Argument should be a number or a SIP URI, not %s' % arg)
                return False
            else:
                # TODO: judgment for URI format
                return True
        else:
            log.error('Too many Argument.')
            return False

    elif arg_type.upper() == 'LINE':
        # Compare line to lines, the line should less than or equal to lines
        # It is ok if lines is int, although it should less than 17 for now, but
        # it maybe change to larger further.

        if len(arg) != 2:
            if (isinstance(arg[0], tuple) or isinstance(arg[0], list)) and len(arg) == 1:
                if len(arg[0]) != 2:
                    log.error('Line checking accept line(which line) and lines(total number of line), \n\t'
                              'you can use a tuple or a list to recognize them, or use them 2 directly like:\n\t'
                              '_format_check(line, lines, arg_type=\'line\').')
                    return False
                else:
                    _line, _lines = arg[0]
            else:
                log.error('Line checking only accept a tuple or list contain line and lines, or just them 2.')
                return False
        else:
            _line, _lines = arg

        if isinstance(_line, int) and isinstance(_lines, int):
            # _line > 0 and _line <= _lines => _lines > 0
            if (_line <= _lines) and _line > 0:
                return True
            else:
                log.error(
                    'Value of argument `line` must larger than 0 and less than lines({}), '
                    'but you give {}.'.format(_lines, _line))
                return False
        elif isinstance(_line, int) and isinstance(_lines, type(None)):
            # It is ok if _lines is None (if model is not defined, it is None)
            if 0 < _line <= 16:
                return True
            else:
                log.error(
                    'Value of argument `line` must larger than 0 and less than or equal to 16, '
                    'but you give {}'.format(_line))
                return False
        else:
            log.error('Type of argument `line` should be :int:, but you give {}'.format(type(_line)))
            return False


def _path_check(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass
