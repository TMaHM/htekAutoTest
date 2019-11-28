# -*- coding: utf-8 -*-

"""
phone.model
~~~~~~~~~~~~~~~~

This module contains the primary objects that abstract Phone.
"""

import re
import time
import math
import operator
import base64
from functools import reduce

from PIL import Image

from htekAutoTest.log import log
from htekAutoTest.typing import _format_check
from htekAutoTest.typing import _path_check
from htekAutoTest.model import get_phone_attr
from htekAutoTest.model import get_phone_pixel
from htekAutoTest.exceptions import *
from htekAutoTest.action_url import prepare_url
from htekAutoTest.action_url import status_code
from htekAutoTest.request_get import Requests

IMG_DIR = r'../ext/'


class StatusChecker(Requests):
    """
    The :class:`StatusChecker <StatusChecker>` object judge the status of real phone if it
    receives query from :class:MSGController.
    And return the result of judgment.
    """

    def _query_status(self, param, status, *args):
        print(param)
        self.ip = param['ip']
        self.web_usr = param['web_usr']
        self.web_pwd = param['web_pwd']
        self.model = param['model']
        self.status = status

        if self.model is None:
            log.error('Model of {} is None, cannot comparing...'.format(self.ip))
            return False
        else:
            self.path = self._prepare_img()
            if self.path is not None:
                if self._query_parsing(self.status, self.model, self.path, args) is True:
                    return True
                else:
                    return False
            else:
                log.error('Capture screen failed on {}.'.format(self.ip))

    def _query_parsing(self, status, model, path, *args):
        """
        Query baidu OCR or Query img comparing.
        :param status: status for query
        :return: True or False
        """
        import random

        self.status = status
        self.model = model
        tmp_path = IMG_DIR + r'cropped/tmp-{}{}.bmp'.format(self.status, random.randint(1, 1000))
        _path_check(IMG_DIR + 'cropped')

        # crop img according to query status
        # if status is 'outgoing', compare result of ocr with dst.ext
        if self.status == 'outgoing':
            pixel_tuple = get_phone_pixel(self.model, 'outgoing')
            crop_img = Image.open(path)
            try:
                cropped = crop_img.crop(pixel_tuple)
                cropped.save(tmp_path)
                log.info('Pixel tuple is ({})'.format(pixel_tuple))
            except ValueError:
                log.error('Value Error: Pixel tuple need 4 elements.')
                return False
        # if status is 'ringing', compare img ringing with specification model
        elif self.status == 'ringing':
            pass
        # if status is 'talking', compare img talking with specification model
        elif self.status == 'talking':
            pass

        # query ocr and compare if there is returning a result
        if self.status in ('outgoing',):
            log.info('Query OCR using img at {}...'.format(tmp_path))
            ocr = self._query_ocr(tmp_path)
            print(ocr)
            for item in args:
                if item in ocr:
                    log.info('OCR comparing [{}] with [{}]success.'.format(item, ocr))
                    return True
                else:
                    return False

    def _query_ocr(self, img):
        """
        Crop img according to status, and query ocr service from Baidu
        :return:
        """
        f = open(img, 'rb')
        f_base64 = base64.b64encode(f.read())
        ocr = self.query_ocr(f_base64)
        return ocr

    def _prepare_img(self):

        self.capture_url = 'http://{}:{}@{}/download_screen'.format(self.web_usr, self.web_pwd, self.ip)
        parsing_time = time.ctime().split(' ')[3].replace(':', '-')

        _path_check(IMG_DIR + r'/temp_img/')
        self.img_path = IMG_DIR + r'/temp_img/{}{}.bmp'.format(parsing_time, self.status)

        r = self.download_img(self.capture_url)
        if r[0] != 200:
            self.img_path = None
        else:
            with open(self.img_path, 'wb') as f:
                f.write(r[1])

        return self.img_path

    def _status_comparing(self, model, status):

        self.model = model
        self.status = status

        _path_check(IMG_DIR + r'status/')
        original_img = IMG_DIR + r'status/{}-{}.bmp'.format(self.model, self.status)
        compare_img = self.img_path

        if compare_img is None:
            return False

        try:
            img_new = Image.open(compare_img)
            img_ori = Image.open(original_img)
        except FileNotFoundError:
            log.error('Image File Not Exist')
            log.debug(traceback.format_exc())
            return False

        h_new = img_new.histogram()
        h_ori = img_ori.histogram()

        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h_new, h_ori))) / len(h_ori))
        if 0 <= result <= 10:
            return True
        else:
            return False


class MSGController(StatusChecker):
    """
    The :class:`MSGController <MSGController>` object is used to send cmd from :class:Phone to the real IP-Phone and
    judge the response.
    If it can't judge, it will query the :class:StatusChecker if the real phone actually in the correctly status.
    """

    def __init__(self):
        self.ip = None
        self.ext = None
        self.line = None
        self.web_usr = None
        self.web_pwd = None
        self.model = None

        self.prefix = 'http://{}:{}@{}'
        self.url = None

    def _send_cmd(self, cmd, *args):
        """
        Receive args from :class:`Phone`, call the corresponding method splice them to a completed URL, and
        call :class:`Request` to send requests.get().

        :param cmd: command :str: which action the phone want to call
        :param *args: given by :class:`Phone` :method:`send_cmd`,
                      contains two part:
                      => obj :obj: it depends on the cmd.
                         For method dial, it is the destination Phone; for method press_key, it is the key will press.
                      => param :dict: phone's property.
                      they all used to splice the HTTP GET URL
        :return: Return the response of HTTP GET
                 200 -> success
                 403 -> Auth Failed
                 404 -> Not Found
                 480 -> Local Error
                 481 -> Remote Error
                 500 -> Connection Error
        """

        if len(args) == 2:
            self._prepare_prefix(args[1])
        elif len(args) == 1:
            self._prepare_prefix(args[0])
            print(args[0])

        if cmd == 'dial':
            self._prepare_dial(args[0], args[1])
        elif cmd == 'press':
            self._prepare_press(args[0].upper(), args[1])
        else:
            self.url = None

        r = self.request_get(self.url)[0]
        if r == 200:
            log.debug('Send cmd({}) [{}] successfully.'.format(cmd.title(), self.url))
            return 200
        elif r == 403:
            log.error('{} Auth Failed, please check if web_usr and web_pwd are wrong.'.format(self.ip))
            return 403
        elif r == 404:
            log.error('{} Web page not found, please check if url is wrong => [{}]'.format(self.ip, self.url))
        elif r == 500:
            if not self.ping(self.ip):
                log.error('{} Connection Error. Maybe it is dead.'.format(self.ip))
                return 500
            else:
                log.error('{} Web service error, although the ip can still connect, please check.'.format(self.ip))
                return 480
        else:
            log.error('Undefined Return Code [{}]'.format(r))
            return r

    def _check_status(self, status, param, *args):
        self.status = status
        self._prepare_check_status(self.status, param)

        r = self.request_get(self.url)
        print(self.url)

        if r[0] == 200:
            pat_return_result = r'(?<=<Return>)(\d)(?=</Return>)'
            check_result = re.findall(pat_return_result, r[1])

            if check_result[0] == '0':
                log.info('{} Status [{}] check passed by Action URL.'.format(self.ip, self.status))
                return True

            elif check_result[0] == '1':
                log.error('{} Status [{}] check failed by Action URL. '
                          'Will try to query OCR'.format(self.ip, self.status))
                if self._query_status(param, self.status, args):
                    log.info('{} Status [{}] check passed by OCR.'.format(self.ip, self.status))
                    return True
                else:
                    log.error('{} Status [{}] check failed by OCR.'.format(self.ip, self.status))
                    return False
            else:
                log.error('Unknown Event [{}]'.format(check_result))
                return False
        else:
            log.error('Check Status [{}] Error, return code [{}], reason [{}].'.format(self.status, r[0], r[1]))
            return r[0]

    def _prepare_prefix(self, arg):
        self.ip = arg['ip']
        self.web_usr = arg['web_usr']
        self.web_pwd = arg['web_pwd']
        self.prefix = prepare_url('prefix').format(
            ip=self.ip, web_usr=self.web_usr, web_pwd=self.web_pwd)
        return self.prefix

    def _prepare_dial(self, dst, param):

        self.ext = param['ext']
        self.line = param['line']
        self._prepare_prefix(param)

        self.url = self.prefix + prepare_url('dial').format(ext=dst.ext, line=self.line)
        return self.url

    def _prepare_press(self, key, param):

        self._prepare_prefix(param)

        self.url = self.prefix + prepare_url('press').format(key=key)
        return self.url

    def _prepare_check_status(self, status, param):

        self._prepare_prefix(param)
        self.status_code = status_code[status]

        self.url = self.prefix + prepare_url('check_status').format(status=self.status_code)
        print(self.prefix)
        return self.url


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
                log.war('Model {} has not defined in :dict:`_model`, '
                        'so some functions of {} will be unavailable.'.format(model, ip))
                lines, dsskeys, hardkeys, lcd_size = None, None, None, None
                pass
        else:
            log.war(
                'Model ({}) has not defined in :dict:`_model`, '
                'so some functions of {} will be unavailable.'.format(model, ip))
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
        """
        Splice the property of phone as a dict to avoid inconsistent.
        :return: :dict:`_param_dir`
        """
        _param_dir = {
            'ip': self.ip,
            'ext': self.ext,
            'line': self.line,
            'model': self.model,
            'web_usr': self.web_usr,
            'web_pwd': self.web_pwd,
        }
        return _param_dir

    def dial(self, dst):
        log.info('%s trying to dial %s...' % (self.ext, dst.ext))
        r = self.send_cmd('dial', dst)
        if r == 200:
            # sleep for 1s to wait for the phone finished the last operation
            time.sleep(1)
            r_status = self.check_status('outgoing')
            if r_status is True:
                log.info('%s dial %s completed.' % (self.ext, dst.ext))
                return 200
            else:
                log.error('%s dial %s failed.' % (self.ext, dst.ext))
                return 480
        else:
            return r

    def press_key(self, key):
        self.send_cmd('press', key)

    def answer(self, key: str = 'ok'):

        r_status = self.check_status('ringing')
        if r_status is True:
            r = self.send_cmd('press', key)
            if r == 200:
                __ = self.check_status('talking')
            return 200
        else:
            log.error('There is no call incoming at %s' % self.ip)
            return 480

    def send_cmd(self, cmd, obj):
        """
        The method is used to avoid call `param` in every method.
        :param cmd: command :str: that pass to `_send_cmd`
        :param obj: needed argument, like dial() need a dst phone
        :return: Return the response of HTTP GET
                 200 -> success
                 403 -> Auth Failed
                 404 -> Not Found
                 480 -> Local Error
                 481 -> Remote Error
        """

        return self._send_cmd(cmd, obj, self.param)

    def check_status(self, status, *args):

        return self._check_status(status, self.param, args)
