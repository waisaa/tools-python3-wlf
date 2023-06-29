import logging
from logging import handlers
import colorlog

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


def init(cls, logname: str, console: bool = False):
    """使用前需要初始化，输入生成的日志文件名
    注意：默认按天生成日志，且保留最近一周的日志文件
    """
    if not cls.logger:
        pdir = '/'.join(logname.split('/')[:-1])
        if pdir:
            FileUtil.create_dir_if_not_exist(pdir)
        cls.logger = logging.getLogger(logname)
        cls.logger.setLevel(logging.DEBUG)
        # 有颜色格式
        cls.fmt_colored = colorlog.ColoredFormatter(f'%(log_color)s{cls.format}', datefmt=None, reset=True, log_colors=cls.colors)
        # 无颜色格式
        cls.fmt_colorless = logging.Formatter(cls.format)
        # 输出到控制台和文件
        if console:
            cls.console_handler = logging.StreamHandler()
        cls.file_handler = handlers.TimedRotatingFileHandler(filename=logname, when='D', backupCount=3, encoding='utf-8')


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


def close(cls):
    if cls.console_handler:
        cls.logger.removeHandler(cls.console_handler)
    cls.logger.removeHandler(cls.file_handler)


def debug(cls, title: str = None, *msg):
    cls.open()
    lastframe = currentframe().f_back
    filepath = lastframe.f_code.co_filename
    funcn = lastframe.f_code.co_name
    lineo = lastframe.f_lineno
    cls.logger.debug("< {} >".format(title).center(100, "-"))
    cls.logger.debug(f'< {funcn} - {lineo} >')
    if msg or msg == 0 or msg is False:
        cls.logger.debug(msg)
    cls.logger.debug("")
    cls.close()


def info(cls, title: str = None, *msg):
    cls.open()
    lastframe = currentframe().f_back
    filepath = lastframe.f_code.co_filename
    funcn = lastframe.f_code.co_name
    lineo = lastframe.f_lineno
    if title:
        cls.logger.info("< {} >".format(title).center(100, "-"))
        cls.logger.info(f'< {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.info(msg)
    cls.logger.info("")
    cls.close()


def warn(cls, title: str = None, *msg):
    cls.open()
    lastframe = currentframe().f_back
    filepath = lastframe.f_code.co_filename
    funcn = lastframe.f_code.co_name
    lineo = lastframe.f_lineno
    if title:
        cls.logger.warn("< {} >".format(title).center(100, "-"))
        cls.logger.warn(f'< {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.warn(msg)
    cls.logger.warn("")
    cls.close()


def error(cls, title: str = None, *msg):
    cls.open()
    lastframe = currentframe().f_back
    filepath = lastframe.f_code.co_filename
    funcn = lastframe.f_code.co_name
    lineo = lastframe.f_lineno
    if title:
        cls.logger.error("< {} >".format(title).center(120, "#"))
        cls.logger.error(f'< {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.error(msg)
    cls.logger.error("")
    cls.close()


def critical(cls, title: str = None, *msg):
    cls.open()
    lastframe = currentframe().f_back
    filepath = lastframe.f_code.co_filename
    funcn = lastframe.f_code.co_name
    lineo = lastframe.f_lineno
    if title:
        cls.logger.critical("< {} >".format(title).center(120, "#"))
        cls.logger.critical(f'< {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.critical(msg)
    cls.logger.critical("")
    cls.close()
