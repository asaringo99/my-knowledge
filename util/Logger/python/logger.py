""" logger(python)のexample

    __launch(): ロガー開始の合図
    __mkdirs(): logsがない場合log directoryを作成
    create_require(): loggerを作成する

"""

import os
import sys
from logging import getLogger, Logger, StreamHandler, FileHandler, Formatter, Filter, DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET
from datetime import datetime

LOGLEVEL = DEBUG
ABSPATH = os.path.abspath(".")
LOG_PATH = ABSPATH + "/logs/"
FILE_PATH = LOG_PATH + "{}.log".format(datetime.now().strftime('%Y%m%d'))

class CustomFilter(Filter):
    """任意に定義することのできるフィルター"""

    def filter(self, record):
        """ファイル名、関数名、行番号が出力されるようにフィルタを設定
        rtype: boolean: Trueで常にフィルターをパス
        """
        record.real_filename = getattr(record,'real_filename',record.filename)
        record.real_funcname = getattr(record,'real_funcname',record.funcName)
        record.real_lineno   = getattr(record,'real_lineno',  record.lineno)
        return True

class Logging():

    def __new__(cls, *args, **kargs):
        """Singleon pattern"""
        if not hasattr(cls, "_instance"):
            cls._instance = super(Logging, cls).__new__(cls)
            cls._instance.__mkdirs()
            cls._instance.__launch()
        return cls._instance

    def __launch(cls):
        startlogger = getLogger("start-logger")
        logger = getLogger("server-logger")
        logger.setLevel(LOGLEVEL)

        sh = StreamHandler(sys.stdout)
        fh = FileHandler(FILE_PATH)
        sh.setLevel(LOGLEVEL)
        fh.setLevel(LOGLEVEL)
        startlogger.addHandler(fh)
        startlogger.addHandler(sh)
        startlogger.critical('\n------------ START LOGGER [{}] ------------'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def __mkdirs(cls):
        print(LOG_PATH)
        try: os.makedirs(LOG_PATH)
        except: pass

    def __init__(self):
        self.fmt_default = Formatter(fmt="%(asctime)s.%(msecs)03d [%(levelname)s]\t%(real_filename)s - %(real_funcname)s:%(real_lineno)s -> %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.fmt_debug   = Formatter(fmt="%(asctime)s.%(msecs)03d [%(levelname)s]\t%(real_filename)s - %(real_funcname)s:%(real_lineno)s -> %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.fmt_start   = Formatter(fmt="%(asctime)s.%(msecs)03d %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.greet = "default"

    def create_require(self, logname="default", fmt_type="default", loglevel=DEBUG, filepath=FILE_PATH, custom_filter=True):
        """loggerの生成
        
        :param str     logname  : loggerの名前
        :param str     fmt_type : フォーマッターの指定
        :param int     loglevel : ログレベル
        :param str     filepath : 出力ファイルパス
        :param boolean loglevel : カスタムフィルタを利用するか
        :return: loggerを返す
        :rtype : Logging
        """

        logger = getLogger(logname)
        logger.setLevel(loglevel)

        if logger.hasHandlers(): return logger

        fmt = self.fmt_default
        if fmt_type == "start": fmt = self.fmt_start
        if fmt_type == "debug": fmt = self.fmt_debug
        if loglevel == DEBUG  : fmt = self.fmt_debug

        sh = StreamHandler(sys.stdout)
        sh.setLevel(loglevel)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

        if filepath is not None:
            fh = FileHandler(filepath)
            fh.setLevel(loglevel)
            fh.setFormatter(fmt)
            logger.addHandler(fh)

        if custom_filter: logger.addFilter(CustomFilter())

        return logger

