import logging
from logging import handlers
from inspect import currentframe
import colorlog
from pywlf.wlffile import new_dir_ifn


class Log():
    log = None
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
    
    def __init__(self, name: str, console: bool = False, retention: int = 7):
        """
        Initialize the log with a name and an optional level.
        """
        new_dir_ifn(self.log_dir)
        logfile = f'{self.log_dir}/{name}'
        self.log = logging.getLogger(logfile)
        self.log.setLevel(logging.DEBUG)
        self.fmt_colored = colorlog.ColoredFormatter(f'%(log_color)s{self.format}', datefmt=None, reset=True, log_colors=self.colors)
        self.fmt_colorless = logging.Formatter(self.format)
        if console:
            self.console_handler = logging.StreamHandler()
        self.file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', backupCount=retention, encoding='utf-8')

    def open(self):
        if self.log:
            if self.console_handler:
                self.console_handler.setFormatter(self.fmt_colored)
                self.log.addHandler(self.console_handler)
            if self.file_handler:
                self.file_handler.setFormatter(self.fmt_colored)
                self.log.addHandler(self.file_handler)
        else:
            print('Please init LogUtil first!')

    def close(self):
        if self.console_handler:
            self.log.removeHandler(self.console_handler)
        self.log.removeHandler(self.file_handler)

    def debug(self, title: str = None, *msg):
        self.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        self.log.debug("< {} >".format(title).center(100, "-"))
        self.log.debug(f'< {filepath} - {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            self.log.debug(msg)
        self.log.debug("")
        self.close()

    def info(self, title: str = None, *msg):
        self.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            self.log.info("< {} >".format(title).center(100, "-"))
            self.log.info(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                self.log.info(msg)
        self.log.info("")
        self.close()

    def warn(self, title: str = None, *msg):
        self.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            self.log.warn("< {} >".format(title).center(100, "-"))
            self.log.warn(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                self.log.warn(msg)
        self.log.warn("")
        self.close()

    def error(self, title: str = None, *msg):
        self.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            self.log.error("< {} >".format(title).center(120, "#"))
            self.log.error(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                self.log.error(msg)
        self.log.error("")
        self.close()

    def critical(self, title: str = None, *msg):
        self.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            self.log.critical("< {} >".format(title).center(120, "#"))
            self.log.critical(f'< {filepath} - {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                self.log.critical(msg)
        self.log.critical("")
        self.close()
