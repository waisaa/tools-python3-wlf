import locale
from enum import Enum
from core import sys_type, SysType
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DateFormat(Enum):
    STD_MIC = '%Y-%m-%d %H:%M:%S.%f'
    STD_SEC = '%Y-%m-%d %H:%M:%S'
    STD_DAY = '%Y-%m-%d'
    TRIM_SEC = '%Y%m%d%H%M%S'
    TRIM_DAY = '%Y%m%d'
    TRIM_MON = '%Y%m'
    CHN_DAY = '%Y年%m月%d日'
    CHN_MON = '%Y年%m月'
    CUS_MIN = '%Y_%m%d_%H%M'
    INFLUX = '%Y-%m-%dT%H:%M:%S.%fZ'


class DateUnit(Enum):
    SEC = 'sec'
    MIN = 'min'
    HOUR = 'hour'
    DAY = 'day'
    YEAR = 'year'


class DateAbbr(Enum):
    SEC = 's'
    MIN = 'm'
    HOUR = 'h'
    DAY = 'd'


if sys_type() == SysType.WIN:
    locale.setlocale(locale.LC_CTYPE, 'chinese')


def fsecs(secs: int) -> str:
    """格式化秒，（日d，时h，分m，秒s）

    Args:
        secs (int): 秒数

    Returns:
        str: 格式化后的字符串
    """
    if secs < 60:
        res = f'{secs}s'
    elif 60 <= secs < 60 * 60:
        min, sec = divmod(secs, 60)
        res = f'{int(min)}m{int(sec)}s'
    elif 60 * 60 <= secs < 24 * 60 * 60:
        hou, secs = divmod(secs, 60 * 60)
        res = f'{int(hou)}h{fsecs(secs)}'
    elif secs >= 24 * 60 * 60:
        day, secs = divmod(secs, 24 * 60 * 60)
        res = f'{int(day)}d{fsecs(secs)}'
    else:
        res = secs
    return res


def ndt(src_ts_ms: int = None) -> datetime:
    """获取当前日期或传入毫秒时间戳对应的日期

    Args:
        src_ts_ms (int): 毫秒时间戳

    Returns:
        datetime: 日期
    """
    return ts2date(src_ts_ms)


def nts(src_dt: datetime = None) -> int:
    """获取当前毫秒时间戳（13位毫秒级）

    Args:
        src_dt (datetime): 日期

    Returns:
        int: 毫秒时间戳
    """
    return date2ts(src_dt)


def ts2date(src_ts_ms: int = None) -> datetime:
    """获取当前日期或传入毫秒时间戳对应的日期

    Args:
        src_ts_ms (int): 毫秒时间戳

    Returns:
        datetime: 日期
    """
    return datetime.fromtimestamp(src_ts_ms / 1000) if src_ts_ms else datetime.now()


def date2ts(src_dt: datetime = None) -> int:
    """获取当前毫秒时间戳（13位毫秒级）

    Args:
        src_dt (datetime): 日期

    Returns:
        int: 毫秒时间戳
    """
    src_dt = src_dt if src_dt else ndt()
    return int(src_dt.timestamp() * 1000)


def str2ts(src_dt_str: str, src_df: str = DateFormat.STD_SEC) -> int:
    """把日期字符串转成13位毫秒级时间戳

    Args:
        src_dt_str (str): 源日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.

    Returns:
        int: 毫秒级时间戳
    """
    return date2ts(str2date(src_dt_str, src_df))


def str2str(src_dt_str: str, src_df: str = DateFormat.STD_SEC, dst_df: str = DateFormat.CHN_DAY) -> str:
    """把日期字符串格式化成其他格式的日期字符串

    Args:
        src_dt_str (str): 源日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.
        dst_df (str, optional): 目标日期字符串格式. Defaults to DateFormat.CHN_DAY.

    Returns:
        str: 目标日期字符串
    """
    return date2str(str2date(src_dt_str, src_df), dst_df)


def date2str(src_dt: datetime = None, dst_df: str = DateFormat.STD_SEC) -> str:
    """把日期格式化成指定格式的字符串

    Args:
        src_dt (datetime, optional): 源日期. Defaults to now.
        dst_df (str, optional): 目标日期字符串格式. Defaults to DateFormat.STD_SEC.

    Returns:
        str: 字符串
    """
    src_dt = src_dt if src_dt else ndt()
    src_dt = src_dt + relativedelta(hours=-8) if dst_df == DateFormat.INFLUX else src_dt
    res = datetime.strftime(src_dt, dst_df)
    if dst_df == DateFormat.INFLUX:
        m1 = res.split('.')[0]
        m2 = str(src_dt.timestamp()).split('.')[1][:3]
        m22 = eval(m2)
        m3 = 'Z' if m22 == 0 else f'.{m2}Z'
        res = f'{m1}{m3}'
    elif dst_df == DateFormat.STD_MIC:
        res = res[:-3]
    return res


def str2date(src_dt_str: str, src_df: str = DateFormat.STD_SEC) -> datetime:
    """把日期字符串格式化成日期

    Args:
        src_dt_str (str): 源日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.

    Returns:
        datetime: 日期
    """
    if src_df == DateFormat.INFLUX:
        src_dt_str = src_dt_str if '.' in src_dt_str else src_dt_str.replace('Z', '.0Z')
        res = datetime.strptime(src_dt_str, src_df)
        res += relativedelta(hours=8)
    else:
        res = datetime.strptime(src_dt_str, src_df)
    return res


def shift(src_dt: datetime = None, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
    """把日期根据传入的偏移量偏移

    Args:
        src_dt (datetime, optional): 源日期. Defaults to now.
        years (int, optional): 年偏移量. Defaults to 0.
        months (int, optional): 月偏移量. Defaults to 0.
        days (int, optional): 日偏移量. Defaults to 0.
        hours (int, optional): 时偏移量. Defaults to 0.
        minutes (int, optional): 分偏移量. Defaults to 0.
        seconds (int, optional): 秒偏移量. Defaults to 0.

    Returns:
        datetime: 偏移后的日期
    """
    src_dt = src_dt if src_dt else ndt()
    return src_dt + relativedelta(years=years) + relativedelta(months=months) + relativedelta(days=days) + relativedelta(hours == hours) + relativedelta(minutes=minutes) + relativedelta(
        seconds=seconds)


def diff(src_dt_str1: str, src_dt_str2: str, src_df: str = DateFormat.STD_SEC, diff_unit: DateUnit = DateUnit.SEC) -> int:
    """获取两个日期字符串的时间差，默认单位秒

    Args:
        src_dt_str1 (str): 日期字符串
        src_dt_str2 (str): 日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.
        diff_unit (DateUnit, optional): 时间差值单位. Defaults to DateUnit.SEC.

    Returns:
        int: 正值代表第二个比第一个晚几秒，负值则相反
    """
    ts1 = str2date(src_dt_str1, src_df).timestamp()
    ts2 = str2date(src_dt_str2, src_df).timestamp()
    diff_secs = int(ts2 - ts1)
    if diff_unit == DateUnit.SEC:
        return diff_secs
    elif diff_unit == DateUnit.MIN:
        return round(diff_secs / 60, 1)
    elif diff_unit == DateUnit.HOUR:
        return round(diff_secs / (60 * 60), 1)
    elif diff_unit == DateUnit.DAY:
        return round(diff_secs / (60 * 60 * 24), 1)
    elif diff_unit == DateUnit.YEAR:
        return round(diff_secs / (60 * 60 * 24 * 365), 1)


def start_of_day(src_dt_str: str, src_df: str = DateFormat.STD_SEC) -> datetime:
    """获取某一天的起始时间

    Args:
        src_dt_str (str): 源日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.

    Returns:
        datetime: 某一天的起始时间
    """
    return str2date(date2str(str2date(src_dt_str, src_df), DateFormat.STD_DAY), DateFormat.STD_DAY)


def end_of_day(src_dt_str: str, src_df: str = DateFormat.STD_SEC) -> datetime:
    """获取某一天的结束时间，即第二天的开始时间

    Args:
        src_dt_str (str): 源日期字符串
        src_df (str, optional): 源日期字符串格式. Defaults to DateFormat.STD_SEC.

    Returns:
        datetime: 某一天的结束时间
    """
    return str2date(date2str(str2date(src_dt_str, src_df) + relativedelta(days=1), DateFormat.STD_DAY), DateFormat.STD_DAY)


def over_shift(src_dt1: datetime, src_dt2: datetime, shift_secs: int) -> bool:
    """判断两个时间是否相差是否超过偏移量

    Args:
        src_dt1 (datetime): 源日期
        src_dt2 (datetime): 源日期
        shift_secs (int): 偏移量，单位秒

    Returns:
        bool: 返回 True | False
    """
    return abs((src_dt1 - src_dt2).total_seconds()) > shift_secs
