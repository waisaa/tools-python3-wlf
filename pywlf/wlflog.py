import logging
from logging import handlers
from inspect import currentframe
import colorlog
from pywlf.wlffile import new_dir_ifn


class WlfLog:
    """日志工具类"""
    logger = None
    format = '%(asctime)s %(levelname)s: %(message)s'
    colors = {
        'DEBUG': 'cyan',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    # 颜色格式
    fmt_colored, fmt_colorless = None, None
    # 日志输出端
    console_handler, file_handler = None, None
    # 默认日志输入目录
    log_dir = 'logs'

    @classmethod
    def init(cls, logname: str, console: bool = False, retention: int = 7):
        """使用前需要初始化，输入生成的日志文件名
        注意：默认按天生成日志，且保留最近一周的日志文件
        """
        if not cls.logger:
            new_dir_ifn(cls.log_dir)
            logfile = f'{cls.log_dir}/{logname}'
            cls.logger = logging.getLogger(logfile)
            cls.logger.setLevel(logging.DEBUG)
            cls.fmt_colored = colorlog.ColoredFormatter(f'%(log_color)s{cls.format}', datefmt=None, reset=True, log_colors=cls.colors)
            cls.fmt_colorless = logging.Formatter(cls.format)
            if console:
                cls.console_handler = logging.StreamHandler()
            cls.file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', backupCount=retention, encoding='utf-8')

    @classmethod
    def open(cls):
        if cls.logger:
            if cls.console_handler:
                cls.console_handler.setFormatter(cls.fmt_colored)
                cls.logger.addHandler(cls.console_handler)
            if cls.file_handler:
                cls.file_handler.setFormatter(cls.fmt_colored)
                cls.logger.addHandler(cls.file_handler)
        else:
            print('Please init LogUtil first!')

    @classmethod
    def close(cls):
        if cls.console_handler:
            cls.logger.removeHandler(cls.console_handler)
        cls.logger.removeHandler(cls.file_handler)

    @classmethod
    def debug(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        cls.logger.debug("< {} >".format(title).center(100, "-"))
        cls.logger.debug(f'< {filepath} - {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.debug(msg)
        cls.logger.debug("")
        cls.close()

    @classmethod
    def info(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.info("< {} >".format(title).center(100, "-"))
            cls.logger.info(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.info(msg)
        cls.logger.info("")
        cls.close()

    @classmethod
    def warn(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.warn("< {} >".format(title).center(100, "-"))
            cls.logger.warn(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.warn(msg)
        cls.logger.warn("")
        cls.close()

    @classmethod
    def error(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.error("< {} >".format(title).center(120, "#"))
            cls.logger.error(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.error(msg)
        cls.logger.error("")
        cls.close()

    @classmethod
    def critical(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.critical("< {} >".format(title).center(120, "#"))
            cls.logger.critical(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.critical(msg)
        cls.logger.critical("")
        cls.close()
