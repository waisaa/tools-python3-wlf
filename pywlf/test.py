from pydate import fsecs, start_of_day, end_of_day, shift


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
    

freq, start_time, end_time = 5, '2023-10-20 17:00:00', '2023-10-20 17:05:00'
mt = date_partition(freq, start_time, end_time)
print(mt)
