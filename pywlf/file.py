import os
import json
import xlrd
import shutil
import chardet
import openpyxl


def mod_encoding(file: str, dst_encoding: str):
    """修改文件编码
    :param file: 文件路径
    :param dst_encoding: 目标编码
    """
    src_encoding = get_encoding(file)
    file_data = ""
    with open(file, "r", encoding=src_encoding) as f:
        for line in f:
            file_data += line
    with open(file, "w", encoding=dst_encoding) as f:
        f.write(file_data)


def get_encoding(file: str):
    """获取文件编码
    :param file: 文件路径
    :return: 文件编码
    """
    with open(file, "rb") as fp:
        return chardet.detect(fp.read(1024 * 1024))["encoding"]


def mod_str(file: str, lns: list, old_str: str, new_str: str):
    """替换文件指定的行的字符
    param file: 文件名
    param lns: 行号，指定的所有行都替换
    param old_str: 旧字符串
    param new_str: 新字符串
    """
    encoding = get_encoding(file)
    file_data, ln = "", 0
    with open(file, "r", encoding=encoding) as f:
        for line in f:
            ln += 1
            if ln in lns:
                if old_str in line:
                    line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding=encoding) as f:
        f.write(file_data)


def list_dir(filepath, contains: str = None):
    """列出目录下的所有文件
    :param filepath: 路径
    :param contains: 文件路径包含的字符
    """
    res = []
    for file in os.listdir(filepath):
        fp = f'{filepath}/{file}'
        if contains:
            if contains in file:
                res.append(fp)
        else:
            res.append(fp)
    res.sort()
    return res


def new_dir_ifn(dst_dir: str):
    """创建目录，不存在则创建，存在无操作
    :param dst_dir: 要创建的目录
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)


def del_fd(dst_dir: str):
    """删除文件或目录
    :param dst_dir: 要删除的目录或文件
    """
    if os.path.isdir(dst_dir):
        shutil.rmtree(dst_dir)
    elif os.path.isfile(dst_dir):
        os.remove(dst_dir)


def file_size(filepath: str):
    """获取文件或文件夹的大小
    :param filepath: 路径
    :warn: TB级别以及超过TB的数据就别用了，需要考虑性能了
    """
    res = 0
    # 判断输入是文件夹还是文件
    if os.path.isdir(filepath):
        # 如果是文件夹则统计文件夹下所有文件的大小
        for file in os.listdir(filepath):
            res += os.path.getsize(f'{filepath}/{file}')
    elif os.path.isfile(filepath):
        # 如果是文件则直接统计文件的大小
        res += os.path.getsize(filepath)
    # 格式化返回大小
    bu = 1024
    if res < bu:
        res = f'{bu}B'
    elif bu <= res < bu**2:
        res = f'{round(res / bu, 3)}KB'
    elif bu**2 <= res < bu**3:
        res = f'{round(res / bu**2, 3)}MB'
    elif bu**3 <= res < bu**4:
        res = f'{round(res / bu**3, 3)}GB'
    elif bu**4 <= res < bu**5:
        res = f'{round(res / bu**4, 3)}TB'
    else:
        res = 'NaN'
    return res


def cls_dir(filepath: str):
    """清空文件夹下的所有文件，先删除文件夹再创建
    :param filepath: 路径
    """
    if os.path.exists(filepath):
        shutil.rmtree(filepath)
    os.mkdir(filepath)


def from_json(filepath, k1: str = None, k2: str = None, k3: str = None):
    """读json文件，返回字典结构数据
    :param filepath: 路径
    :param k1: 一级深度key
    :param k2: 二级深度key
    :param k3: 三级深度key
    """
    with open(filepath, "r", encoding='utf-8') as fr:
        data = json.load(fr)
    data = eval(data) if type(data) is str else data
    res = {}
    if k1:
        if k2:
            if k3:
                v1 = get_key(data, k1)
                v2 = get_key(v1, k2)
                res = get_key(v2, k3)
            else:
                v1 = get_key(data, k1)
                res = get_key(v1, k2)
        else:
            res = get_key(data, k1)
    else:
        res = data
    return res


def get_key(data: any, key: str):
    """从json数据中获取指定的key

    Args:
        data (any): json数据
        key (str): key

    Returns:
        dict|list|NaN: 返回key的值
    """
    if type(data) is dict:
        res = data.get(key)
    elif type(data) is list:
        res = [e.get(key) for e in data]
    else:
        res = None
    return res


def to_json(filepath: str, data: dict, cn=True, encoding='utf8'):
    """把数据写入到json文件中
    :param filepath: 路径
    """
    json_data = json.dumps(data, ensure_ascii=not cn)
    with open(filepath, "w", encoding=encoding) as fw:
        fw.write(json_data)


def to_xlsx(filepath: str, data: list, autoh=False, headers: list = None):
    """把数据写入到excel文件中
    :param filepath: 路径
    """
    wk = openpyxl.Workbook()
    sheet = wk.active
    if type(data[0]) is list:
        if headers:
            data.insert(0, headers)
        for i, lv in enumerate(data):
            for j, v in enumerate(lv):
                sheet.cell(row=i + 1, column=j + 1).value = v
    elif type(data[0]) is dict:
        if headers:
            rc = {k: k for k in headers}
            data.insert(0, rc)
        if autoh and not headers:
            rc = {k: k for k in data[0]}
            data.insert(0, rc)
        for i, rc in enumerate(data):
            for j, k in enumerate(rc):
                sheet.cell(row=i + 1, column=j + 1).value = rc[k]
    wk.save(filepath)
