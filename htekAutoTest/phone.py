# -*- coding: utf-8 -*-

"""
phone.model
~~~~~~~~~~~~~~~~

This module contains the primary objects that abstract Phone.
"""

import sys
import datetime

import requests

from htekAutoTest.log import log
from htekAutoTest.typing import _type_check
from htekAutoTest.model import get_phone_attr


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
                 ip: str = None, ext: str = None, line=None,
                 web_usr='admin', web_pwd='admin',
                 model=None):
        # 参数合法性校验
        ip = ip if _type_check(ip, 'ip') else sys.exit(-1)
        ext = ext if _type_check(ext, 'ext') else sys.exit(-1)
        if model is not None:
            model = model
            try:
                lines, dsskeys, hardkeys, lcd_size = get_phone_attr(model)
            except TypeError:
                log.war('This model {} has not defined in :dict:`_model`, thus some functions will not be used.')
                lines, dsskeys, hardkeys, lcd_size = None, None, None, None
                pass
        else:
            log.war('This model {} has not defined in :dict:`_model`, thus some functions will not be used.')
            lines, dsskeys, hardkeys, lcd_size = None, None, None, None
        line = line if _type_check(line, 'line') else 1

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
