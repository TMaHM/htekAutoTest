# -*- coding: utf-8 -*-

"""
phone.model
~~~~~~~~~~~~~~~~

This module contains the primary objects that abstract Phone.
"""

import sys
import datetime

import requests

from .log import log
from .typing import _type_check


class MSGController(object):
    """
    The :class:`MSGController <MSGController>` object is used to send cmd from :class:Phone to the real IP-Phone and
    judge the response.
    If it can't judge, it will query the :class:StatusChecker if the real phone actually in the correctly status.
    """
    from .action_url import url

    def send_cmd(self, cmd):
        self.url[cmd]

        pass

    def query_status(self):
        pass


class Phone(MSGController):
    """
    The :class:`Phone <Phone>` object, which define an IP-Phone and what it can do.

    :param ip:
    :param ext:
    :param line:
    :param web_usr:
    :param web_pwd:
    :param model:
    """

    def __init__(self,
                 ip=None, ext=None, line=None,
                 web_usr='admin', web_pwd='admin',
                 model=None):

        # 参数合法性校验
        ip = ip if _type_check(ip, 'ip') else sys.exit(-1)


        self.ip = ip
        self.ext = ext
        self.line = line
        self.usr = web_usr
        self.pwd = web_pwd
        self.model = model




    def dial(self):
        self.send_cmd()
        pass

    def press_key(self):

        pass


class StatusChecker(object):
    """
    The :class:`StatusChecker <StatusChecker>` object judge the status of real phone if it
    receives query from :class:MSGController.
    And return the result of judgment.
    """

    def query_parsing(self):
        pass

    def status_comparing(self):
        pass

    def query_answer(self):
        pass

    pass
