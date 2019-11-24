# -*- coding: utf-8 -*-
"""
Test for typing.model
"""

from htekAutoTest.typing import _type_check


def test_typing_ip():
    _test_box = {
        'valid': ('10.3.0.1', '192.168.0.254',),
        'invalid': ('0.0.0.0', '10.10.3.-1', 'test', ['1', '2'], None, 1,)
    }
    for value in _test_box['valid']:
        assert _type_check(value, arg_type='ip') is True
    for value in _test_box['invalid']:
        assert _type_check(value, arg_type='ip') is False
