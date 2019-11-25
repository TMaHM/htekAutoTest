# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-25

"""
The request_get.model is one of the fundamentals of this Automatic Testing framework.
"""

import requests
from htekAutoTest.log import log


class Requests(object):

    @staticmethod
    def request_get(url):
        try:
            r = requests.get(url)
            return r.status_code

        except requests.exceptions.ConnectionError:
            return 500

