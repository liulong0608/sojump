# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         random_bili.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/28 20:35
# @Software:        PyCharm
# ====/******/=====
def random_bili(num):
    a = 100 // num
    yu = 100 - a * num
    result = []
    for i in range(num):
        result.append(a)
    for i in range(yu):
        result[i] += 1
    return result
