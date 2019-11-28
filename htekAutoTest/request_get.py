# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-25

"""
The request_get.model is one of the fundamentals of this Automatic Testing framework.
"""

import os
import json
import requests

from htekAutoTest.log import log


class Requests(object):

    @staticmethod
    def request_get(url):
        try:
            r = requests.get(url)
            if r.status_code == 401:
                requests.get(url)
                if r.status_code == 401:
                    return 403, r.text
                else:
                    return r.status_code, r.text
            else:
                return r.status_code, r.text

        except requests.exceptions.ConnectionError:
            return 500, ConnectionError

    @staticmethod
    def download_img(url):
        try:
            r = requests.get(url)
            if r.status_code == 401:
                requests.get(url)
                if r.status_code == 401:
                    return 403, r.content
                elif r.status_code == 200:
                    return 200, r.content
            elif r.status_code == 200:
                return 200, r.content
            else:
                return 480, r.content

        except requests.exceptions.ConnectionError:
            return 500, ConnectionError

    def query_ocr(self, img_b64):

        ocr_list = []
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
        params = {"image": img_b64}
        access_token = self.get_access_token()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        def post_ocr(url, data, header, token):
            url = url + "?access_token=" + token
            response = requests.post(url, data=data, headers=header)
            if response:
                r = response.json()
                print(r)
                try:
                    for __ in r['words_result']:
                        ocr_list.append(__['words'])
                    return ocr_list

                except KeyError:
                    for k, v in r.items():
                        if k == 'error_code':
                            if v == 110:
                                log.error('Access token invalid or no longer valid.')
                                log.error('Try to update Access token.')
                                return None
                    return None

        result = post_ocr(request_url, params, headers, access_token)
        if result is None:
            access_token = self.get_access_token('new')
            if access_token is not None:
                return post_ocr(request_url, params, headers, access_token)
            else:
                return None
        else:
            return result

    @staticmethod
    def get_access_token(*method):

        access_token = None
        if len(method) != 0:
            if method[0] == 'new':
                ak = 'ljwII9uBaQDdQ3aDfygoywRX'
                sk = '4iqvryHIdQhOZMtfiAIM27xwjxO0ErlZ'
                host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=' \
                       'client_credentials&client_id=%s&client_secret=%s' % (ak, sk)
                with open(r'../ext/access_token.json', 'w', encoding='utf-8') as f:
                    response = requests.get(host)
                    if response:
                        json.dump(response.json(), f)

        with open('../ext/access_token.json', 'r', encoding='utf-8') as f:
            r = json.load(f)
            for k, v in r.items():
                if k == 'access_token':
                    access_token = v
                    log.info('Access Token found => [{}]'.format(v))
                    break
                elif k == 'error_description' or k == 'Client authentication failed':
                    log.error('Access Token Error [{}}]'.format(v))
                    return None
                else:
                    continue
            else:
                log.error('Access Token or Expires not found, need to check.')

            if access_token is not None:
                return access_token
            else:
                log.error('Access Token not found, need to check.')
                return None

    @staticmethod
    def ping(ip):
        return_code = os.system('ping -c 1 -w 1 %s' % ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        ex_int = int('{:016b}'.format(return_code)[0:-8], 2)
        print(ex_int)
        if ex_int:
            return False
        else:
            return True
