# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-27

import pytest

from htekAutoTest.request_get import Requests


class TestRequests:

    def test_get_access_token(self):
        method = 'new'
        request = Requests()
        assert request.get_access_token(method) is not None
