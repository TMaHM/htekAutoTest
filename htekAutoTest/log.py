import logging
import os
import time
import platform


if platform.system() == 'Windows':
    LOG_DIR = r'C:\\Documents\\htekPhoneLog\\'
elif platform.system() == 'Linux':
    LOG_DIR = '/tmp/htekPhoneLog/'
now_month = time.ctime().split(' ')[1]
now_date = time.ctime().split(' ')[2]
now_time = time.ctime().split(' ')[3].replace(':', '')


class Logger:

    def __init__(self, echo: bool = False, clevel=logging.DEBUG, flevel=logging.DEBUG):
        # log及截屏文件存放目录
        log_dir = LOG_DIR + r'log/'
        log_backup = log_dir + r'backup/'
        self.screen_dir = log_dir + r'screenShot'
        # log文件绝对路径
        info_path = log_dir + r'info.log'
        debug_path = log_dir + r'debug.log'
        # screen_file = self.screen_dir  # 不知道为什么存在，先隐掉

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            os.makedirs(log_backup)
            open(info_path, 'w').close()
            open(debug_path, 'w').close()
        else:
            if not os.path.exists(info_path):
                open(info_path, 'w').close()
                open(debug_path, 'w').close()
            else:
                if not os.path.exists(log_backup):
                    os.makedirs(log_backup)
                else:
                    pass
                info_size = os.path.getsize(info_path)
                debug_size = os.path.getsize(debug_path)
                if info_size / 1024 ** 2 > 5:
                    print('---Backup info.log because large than 5M.----')
                    os.rename(info_path,
                              '{dir}info_bak_{month}{date}{time}.log'.format(dir=log_backup, month=now_month,
                                                                             date=now_date, time=now_time))
                    open(info_path, 'w').close()
                else:
                    pass
                if debug_size / 1024 ** 2 > 5:
                    print('---Backup debug.log because large than 5M---')
                    os.rename(debug_path,
                              '{dir}debug_bak_{month}{date}{time}.log'.format(dir=log_backup, month=now_month,
                                                                              date=now_date, time=now_time))
                    open(debug_path, 'w').close()
                else:
                    pass

        if not os.path.exists(self.screen_dir):
            os.makedirs(self.screen_dir)

        self.logger_debug = logging.getLogger(info_path)
        self.logger_info = logging.getLogger(debug_path)
        self.logger_debug.setLevel(logging.DEBUG)
        self.logger_info.setLevel(logging.INFO)
        fmt_info = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt_debug = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置终端日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt_info)
        sh.setFormatter(fmt_debug)
        sh.setLevel(clevel)
        # 设置文件日志
        fh_info = logging.FileHandler(info_path)
        fh_debug = logging.FileHandler(debug_path)
        fh_info.setFormatter(fmt_info)
        fh_debug.setFormatter(fmt_debug)
        fh_info.setLevel(flevel)
        fh_debug.setLevel(flevel)
        if echo:
            self.logger_info.addHandler(sh)
            self.logger_debug.addHandler(sh)
        self.logger_info.addHandler(fh_info)
        self.logger_debug.addHandler(fh_debug)

    def debug(self, message):
        self.logger_debug.debug(message)

    def info(self, message):
        self.logger_info.info(message)

    def war(self, message):
        self.logger_info.warning(message)

    def error(self, message):
        self.logger_info.error(message)


log = Logger()
