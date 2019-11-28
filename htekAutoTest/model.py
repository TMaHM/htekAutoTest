# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-25

"""
Defined all the necessary configuration info for IP-Phone, and
setup a mapping for these info to model.

Model: it determines the number of Lines, DSSKeys, HardKeys, size of LCD, Images of the phone
"""

# Pixel: left, top, right, bottom
_model = {
    ('UC912E', 'UC912', 'UC912G', 'UC912'): {
        'lines': 4,
        'dsskeys': 12,
        'hardkeys': ('mute', 'headset', 'vm', 'tsf', 'redial', 'speaker'),
        'lcd_size': (192, 64),
        'outgoing': (49, 30, 143, 46),

    },
}


def get_phone_attr(model):
    for k, v in _model.items():
        if model.upper() in k:
            return v['lines'], v['dsskeys'], v['hardkeys'], v['lcd_size']
        else:
            continue
    else:
        return None


def get_phone_pixel(model, status):
    for k, v in _model.items():
        if model.upper() in k:
            return v[status]
        else:
            continue
    else:
        return None

# line, dsskeys, hardkeys, lcd_size = get_phone_attr('uc9132')
# print(line, dsskeys, hardkeys, lcd_size)
