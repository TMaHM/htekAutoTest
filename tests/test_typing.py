# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-24
"""
Test for typing.model
"""

from htekAutoTest.typing import _format_check


def test_typing_ip():
    _test_box = {
        'valid': ('10.3.0.1', '192.168.0.254',),
        'invalid': ('0.0.0.0', '10.10.3.-1', 'test', ['10.2.3.120'], None, 1,)
    }
    for value in _test_box['valid']:
        assert _format_check(value, arg_type='ip') is True
    for value in _test_box['invalid']:
        assert _format_check(value, arg_type='ip') is False


def test_type_ext():
    _test_box = {
        'valid': ('8724', '10.3.0.70@htekvoip.3cx.asia'),
        'invalid': (None,)
    }
    for value in _test_box['valid']:
        assert _format_check(value, arg_type='ext') is True
    for value in _test_box['invalid']:
        assert _format_check(value, arg_type='ext') is False


def test_type_line():
    _test_box = {
        'valid': ((1, 2), (4, 4), (16, 16), [2, 6], [16, None]),
        'invalid': ((3, 2), (0, 2), (1, 0), (255, 16), (), None, 1, [-1], [0, -254], 'te')
    }
    for value in _test_box['valid']:
        assert _format_check(value, arg_type='line') is True

    for value in _test_box['invalid']:
        assert _format_check(value, arg_type='line') is False
