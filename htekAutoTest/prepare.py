# -*- coding: utf-8 -*-
# Written by Stephen.Yu
# Original Date: 2019-11-27

import os
import platform

if platform.system() == 'Windows':
    LOG_DIR = r'C:\\Documents\\htekPhoneLog\\'
    IMG_DIR = r'./ext/status/'

elif platform.system() == 'Linux':
    LOG_DIR = r'/tmp/htekPhoneLog/'
    IMG_DIR = r'./ext/status/'

else:
    LOG_DIR = r'./tmp/htekPhoneLog/'
    IMG_DIR = r'./ext/status/'

if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
