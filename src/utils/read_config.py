# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         read_config.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 23:26
# @Software:        PyCharm
# ====/******/=====
import configparser
from typing import Text, Union


def read_ini_file(section: Text, option: Text, file_path: Text = None) -> Union[Text, bool, None]:
    """
    读取 INI 配置文件
    :param file_path: ini配置文件路径
    :param section: 节
    :param option: 选项
    :return: 配置项的值
    """
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取 INI 文件
    config.read(file_path, encoding="utf-8")

    # 检查 INI 文件中是否存在指定的节和选项
    if config.has_section(section) and config.has_option(section, option):
        # 获取配置项的值
        value = config.get(section, option)
        return value
    else:
        # 处理节或选项不存在的情况
        return None


