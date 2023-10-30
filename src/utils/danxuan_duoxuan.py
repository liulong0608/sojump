# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         danxuan_duoxuan.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/28 21:41
# @Software:        PyCharm
# ====/******/=====
import math
import random


def danxuan(proportion):
    """
    单选执行函数
    :param proportion: 比例
    :return: 选项的索引值
    """
    total = sum(proportion)  # 计算总比例
    random_num = math.floor(random.random() * total) + 1  # 生成随机数
    for index in range(len(proportion)):
        random_num -= proportion[index]  # 减去当前选项的比例值
        if random_num <= 0:
            return index


def duoxuan(probability):
    """
    多选题执行函数
    :param probability: 比例
    :return:
    """
    flag = False
    i = random.randint(1, 100)
    if i <= probability:
        flag = True
    return flag
