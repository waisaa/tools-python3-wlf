from enum import Enum
import platform
import uuid
import time
from pydate import fsecs, start_of_day, end_of_day, shift


class SysType(Enum):
    LIN = 'Linux'
    WIN = 'Windows'


class Tight(Enum):
    YES = True
    NO = False


def uid(param: str = None, tight: bool = False) -> str:
    """获取uuid字符串

    Args:
        param (str, optional): 自定义参数. Defaults to None.
        tight (bool, optional): 紧凑型的. Defaults to False.

    Returns:
        str: uuid字符串
    """
    res = str(uuid.uuid3(uuid.NAMESPACE_OID, str(param))) if param else str(uuid.uuid1())
    res = res.replace('-', '') if tight else res
    return res


def time_cost(fn: function):
    """这个装饰器用于统计函数运行耗时

    Args:
        fn (function): 被统计函数
    """

    def _timer(*args, **kwargs):
        func_name = fn.__name__
        print(f'{func_name} start')
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        cost = fsecs(end - start)
        print(f'{func_name} end')
        print(f'{func_name} cost {cost}')
        return result

    return _timer


def section(max: float, count: int = 10, min: float = 0) -> list:
    """根据数据范围划分区间

    Args:
        max (float): 最大值
        count (int, optional): 划分的区间数. Defaults to 10.
        min (float, optional): 最小值. Defaults to 0.

    Returns:
        list: 返回划分后的区间集合 ['区间1', '区间2', '区间3', ...]
        eg: ['0.0 ~ 3.3', '3.3 ~ 6.7', '>= 6.7']
    """
    res = []
    interval = max / count
    while len(res) < count:
        start, end = min, min + interval
        res.append(f'{start:.1f} ~ {end:.1f}') if end < max else res.append(f'>= {min:.1f}')
        min += interval
    return res


def date_partition(freq, start_time, end_time):
    """根据数据频率划分时间区间
    :param freq 数据频率
    :return 返回划分后的时间区间集合 {}
    """
    res = {}
    begin = start_of_day(start_time)
    end = end_of_day(end_time)
    while begin < end:
        res[begin] = None
        begin = shift(begin, seconds=freq)
    return res


def del_none(li):
    """删除list中None"""
    return [e for e in li if e]


def sys_type() -> str:
    """获取当前操作系统

    Returns:
        str: 系统名称
    """
    return platform.system()


def to_str(bytes_or_str):
    """
    把byte类型转换为str
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value
