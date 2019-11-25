# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-25

"""
Test for phone.model
"""

import pytest

from htekAutoTest.phone import Phone
from htekAutoTest.phone import MSGController
from htekAutoTest.exceptions import *

device = Phone('10.3.3.191', '2054', 1)


@pytest.fixture
def error_fixture():
    assert 0


class TestPhone:

    @pytest.mark.parametrize(
        'exception, ip', (
                (WrongIP, '10.3.09'),
                (WrongIP, None),
                (WrongIP, '255.0.0.0'),
                (WrongIP, '0.1.3.2'),
                (WrongIP, 1),
        )
    )
    def test_invalid_ip(self, exception, ip):
        with pytest.raises(exception):
            Phone(ip)

    @pytest.mark.parametrize(
        'exception, ext', (
                (WrongExt, None),
        )
    )
    def test_invalid_ext(self, exception, ext):
        with pytest.raises(exception):
            Phone('10.3.3.191', ext, 1)

    @pytest.mark.parametrize(
        'exception, line', (
                (WrongLine, None),
                (WrongLine, 0),
                (WrongLine, -1),
                (WrongLine, 'test'),
                (WrongLine, 17),
                (WrongLine, ())
        )
    )
    def test_invalid_line_without_model(self, exception, line):
        with pytest.raises(exception):
            Phone('10.3.3.191', '000', line)

    @pytest.mark.parametrize(
        'exception, line', (
                (WrongLine, None),
                (WrongLine, 16),
                (WrongLine, 0),
                (WrongLine, 5)
        )
    )
    def test_invalid_line_with_model(self, exception, line):
        with pytest.raises(exception):
            Phone('10.3.3.191', '000', line, model='uc912')


class TestMSGController:

    def test_prepare_dial(self, ):
        ip = '10.3.3.191'
        ext = '2057'
        line = 1
        web_usr = 'admin'
        web_pwd = 'admin'

        param_dir = {
            'ext': ext,
            'line': line,
        }

        expected = 'http://admin:admin@10.3.3.191/Phone_ActionURL&Command=1&Number=2054&Account=1'
        controller = MSGController()
        controller._prepare_prefix(ip, web_usr, web_pwd)
        assert expected == controller._prepare_dial(device, param_dir)

    def test_prepare_press(self):
        ip = '10.3.3.191'
        web_usr = 'admin'
        web_pwd = 'admin'
        key = '1'

        expected = 'http://admin:admin@10.3.3.191/AutoTest&keyboard=1'
        controller = MSGController()
        controller._prepare_prefix(ip, web_usr, web_pwd)
        assert expected == controller._prepare_press(key)

    def test_send(self):
        url = 'http://admin:admin@10.3.3.191/AutoTest&keyboard=1'
        expected = 200

        controller = MSGController()
        assert expected == controller._send(url)
