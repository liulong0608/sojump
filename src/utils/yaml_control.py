# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         yaml_control.py  
# @version          v1.0.2
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/22 23:54
# @Software:        PyCharm
# ====/******/=====
import os
from typing import Text, Dict

import yaml


class GetYamlData:
    """
    获取yaml文件中的数据
    """

    def __init__(self, file_dir: Text):
        self.file_dir = str(file_dir)

    def get_yaml_data(self) -> Dict:
        """
        获取yaml中的数据
        :return:
        """
        # 判断文件是否存在
        if not os.path.exists(self.file_dir):
            data = open(self.file_dir, "r", encoding="utf-8")
            res = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("文件路径不存在")
        return res

