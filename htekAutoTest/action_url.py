# -*- coding: utf-8 -*-
"""
The dict ``url`` defines a mapping from common names for phone's action to their action url.
It is case insensitive.

Now it only used in :class:MSGController
"""

url = {

    'prefix': 'http://{web_usr}:{web_pwd}@{ip}',
    'dial': '/Phone_ActionURL&Command=1&Number={ext}&Account={line}',
    'press': '/AutoTest&keyboard={key}',
    'check_status': '/AutoTest&autoverify=STATE={status}',
    'capture_screen': '/download_screen'
}

status_code = {

    'speaker': 1,
    'outgoing': 2,
    'talking': 3,
    'ringing': 4,
    'hold': 5,
    'new_initiate': 6,
    'new_talking': 7,
    'conference': 8,
    'conf_hold': 9,
}


# x = _url['dial'].format(usr='admin', pwd='admin', ip='10.3.3.191', ext='2055', line='1')
# print(x)


def prepare_url(action):
    return url[action]
