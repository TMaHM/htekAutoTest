# -*- coding: utf-8 -*-

"""
phone.model
~~~~~~~~~~~~~~~~

This module contains the primary objects that abstract Phone.
"""

from htekAutoTest.log import log
from htekAutoTest.typing import _format_check
from htekAutoTest.model import get_phone_attr
from htekAutoTest.exceptions import *
from htekAutoTest.action_url import prepare_url
from htekAutoTest.request_get import Requests


class MSGController(Requests):
    """
    The :class:`MSGController <MSGController>` object is used to send cmd from :class:Phone to the real IP-Phone and
    judge the response.
    If it can't judge, it will query the :class:StatusChecker if the real phone actually in the correctly status.
    """

    def __init__(self):
        Requests.__init__(self)
        self.ip = None
        self.ext = None
        self.line = None
        self.web_usr = None
        self.web_pwd = None
        self.model = None

        self.prefix = 'http://{}:{}@{}'
        self.url = None

    def _send_cmd(self, cmd, *args):
        self.ip = args[1]['ip']
        self.web_usr = args[1]['web_usr']
        self.web_pwd = args[1]['web_pwd']
        self._prepare_prefix(self.ip, self.web_usr, self.web_pwd)

        if cmd == 'dial':
            self._prepare_dial(args[0], args[1])
            # return self.url
        elif cmd == 'press':
            self._prepare_press(args[0])
        else:
            # return 'None'
            self.url = None
        r = self._send(self.url)
        print(r)

    def query_status(self):
        pass

    def _send(self, url):
        self.url = url
        r = self.request_get(self.url)
        if r == 200:
            log.info('Send cmd [{}] successfully.'.format(self.url))
            return 200

    def _prepare_prefix(self, ip, web_usr, web_pwd):
        self.ip = ip
        self.web_usr = web_usr
        self.web_pwd = web_pwd
        self.prefix = prepare_url('prefix').format(
            ip=self.ip, web_usr=self.web_usr, web_pwd=self.web_pwd)
        return self.prefix

    def _prepare_dial(self, dst, param):

        self.ext = param['ext']
        self.line = param['line']

        self.url = self.prefix + prepare_url('dial').format(ext=dst.ext, line=self.line)
        return self.url

    def _prepare_press(self, key):

        self.url = self.prefix + prepare_url('press').format(key=key)
        print(self.url)
        return self.url

    # def _prepare_check_status(self, status):
    #
    #     self.url = self.prefix +


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
                 ip: str = None, ext: str = None, line: int = None,
                 web_usr='admin', web_pwd='admin',
                 model=None):
        MSGController.__init__(self)

        # 参数合法性校验
        ip = ip if _format_check(ip, arg_type='ip') else wrong_ip()
        ext = ext if _format_check(ext, arg_type='ext') else wrong_ext()
        if model is not None:
            model = model
            try:
                lines, dsskeys, hardkeys, lcd_size = get_phone_attr(model)
            except TypeError:
                log.war('This model {} has not defined in :dict:`_model`, '
                        'thus some functions will not be used.'.format(model))
                lines, dsskeys, hardkeys, lcd_size = None, None, None, None
                pass
        else:
            log.war(
                'This model {} has not defined in :dict:`_model`, '
                'thus some functions will not be used.'.format(model))
            lines, dsskeys, hardkeys, lcd_size = None, None, None, None
        line = line if _format_check(line, lines, arg_type='line') else wrong_line()

        self.ip = ip
        self.ext = ext
        self.line = line
        self.web_usr = web_usr
        self.web_pwd = web_pwd
        self.model = model

    @property
    def param(self):
        _param_dir = {
            'ip': self.ip,
            'ext': self.ext,
            'line': self.line,
            'web_usr': self.web_usr,
            'web_pwd': self.web_pwd,
        }
        return _param_dir

    def dial(self, dst):
        self._send_cmd('dial', dst, self.param)
        pass

    def press_key(self, key):
        self._send_cmd('press', key, self.param)
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
