# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         setting.py  
# @version          v1.0.2
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/22 23:41
# @Software:        PyCharm
# ====/******/=====
import os


def root_path():
    """ 获取 根路径 """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path):
    """
    兼容 windows 和 linux 不同环境的操作系统路径
    :param path:
    :return:
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() + path

