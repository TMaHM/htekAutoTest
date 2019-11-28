# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-25

"""
Test for phone.model
"""

import pytest

from htekAutoTest.phone import Phone
from htekAutoTest.phone import MSGController
from htekAutoTest.phone import StatusChecker
from htekAutoTest.exceptions import *

device = Phone('10.3.3.191', '2057', 1)


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

    def test_prepare_prefix(self):
        param_dir = {
            'ip': '10.3.3.191',
            'web_usr': 'admin',
            'web_pwd': 'admin',
        }

        expected = 'http://admin:admin@10.3.3.191'
        controller = MSGController()

        assert expected == controller._prepare_prefix(param_dir)

    def test_prepare_dial(self, ):
        param_dir = {
            'ext': '2057',
            'line': 1,
            'ip': '10.3.3.191',
            'web_usr': 'admin',
            'web_pwd': 'admin',
        }

        expected = 'http://admin:admin@10.3.3.191/Phone_ActionURL&Command=1&Number=2054&Account=1'
        controller = MSGController()
        controller._prepare_prefix(param_dir)
        assert expected == controller._prepare_dial(device, param_dir)

    def test_prepare_press(self):
        param_dir = {
            'ext': '2057',
            'line': 1,
            'ip': '10.3.3.191',
            'web_usr': 'admin',
            'web_pwd': 'admin',
        }
        key = '1'

        expected = 'http://admin:admin@10.3.3.191/AutoTest&keyboard=1'
        controller = MSGController()
        controller._prepare_prefix(param_dir)
        assert expected == controller._prepare_press(key)

    def test_prepare_check_status(self):
        param_dir = {
            'ip': '10.3.3.191',
            'web_usr': 'admin',
            'web_pwd': 'admin'
        }

        expected = 'http://admin:admin@10.3.3.191/AutoTest&autoverify=STATE=2'

        controller = MSGController()
        controller._prepare_prefix(param_dir)
        assert expected == controller._prepare_check_status('outgoing')

    def test_send_cmd(self):
        cmd = 'dial'
        obj = device
        param_dir = {
            'ip': '10.3.3.192',
            'ext': '2054',
            'web_usr': 'admin',
            'web_pwd': 'admin',
            'line': 3
        }

        controller = MSGController()
        controller._prepare_prefix(param_dir)
        controller._send_cmd(cmd, obj, param_dir)


class TestStatusChecker:

    def test_query_parsing(self):
        status = 'outgoing'
        model = 'uc912'
        img = '../ext/temp_img/test_outgoing.bmp'
        dst_number = '2054'

        status_checker = StatusChecker()
        assert status_checker._query_parsing(status, model, img, dst_number) is True
