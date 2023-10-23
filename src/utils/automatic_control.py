# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         automatic_control.py  
# @version          v1.0.2
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/23 0:03
# @Software:        PyCharm
# ====/******/=====
from typing import Text

from config.setting import ensure_path_sep


class AutomaticControl:

    @staticmethod
    def yaml_data_path() -> Text:
        """ 返回yaml配置文件路径 """
        return ensure_path_sep("\\src\\conf")

    @staticmethod
    def conf_path() -> Text:
        """ 存放配置文件路径 """
        return ensure_path_sep("\\src\\common")
