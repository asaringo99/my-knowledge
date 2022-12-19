""" logger(python)のdecorator

"""

import os
from logging import getLogger, Logger, StreamHandler, FileHandler, Formatter, Filter, DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET
from functools import wraps
import inspect
import time
from logger import Logging

ABSPATH = os.path.abspath(".")

superlogger = Logging()

def defaultlog(logger:Logger=superlogger.create_require(logname="default")):

    def logdec(func):

        @wraps(func)
        def printlog(*arg, **kwargs):

            funcname = func.__name__

            extra = {
                'real_filename': inspect.getfile(func).replace(ABSPATH,""),
                'real_funcname': funcname,
                'real_lineno'  : inspect.currentframe().f_back.f_lineno
            }

            start_time = time.process_time()
            logger.info("{}: START".format(funcname), extra=extra)

            try:
                response = func(*arg, **kwargs)
            except Exception as e:
                end_time = time.process_time()
                logger.error("{}: KILL(process time : {:3g})".format(funcname, end_time - start_time), extra=extra)
                logger.error(e)
                raise e
            else:
                end_time = time.process_time()
                logger.info("{}: END(process time : {:3g})".format(funcname, end_time - start_time), extra=extra)

            return response
        
        return printlog

    return logdec
