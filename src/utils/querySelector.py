# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         querySelector.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/28 21:30
# @Software:        PyCharm
# ====/******/=====
from typing import List, Text

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def querySelectorAll(element_list: List[WebElement], loc: Text) -> WebElement:
    """
    查询元素
    :param element_list: 元素列表
    :param loc: 查找的元素路径
    :return:
    """
    return element_list.find_elements(By.CSS_SELECTOR, loc)

