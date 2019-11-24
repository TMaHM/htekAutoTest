# -*- coding: utf-8 -*-
"""
Test for typing.model
"""

import pytest
from htekAutoTest.typing import _type_check


def test_typing_ip():
    ip = '10.3.0.0'
    result = _type_check(ip, 'ip')
    assert result is True


test_typing_ip()
