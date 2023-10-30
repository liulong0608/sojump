# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         ActionWJX.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 22:52
# @Software:        PyCharm
# ====/******/=====
"""
Python version： 3.10.9
Chrome version： 118.0.5993.89
chromedriver version： 118.0.5993.88

代码采用线性结构
"""
import random
import time
from typing import List, Text

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from public.pages.base_page import BasePage
from src.common.executive_sojump import randomBili
from src.utils.danxuan_duoxuan import danxuan, duoxuan
from src.utils.obtain_all_blocks import get_all_blocks
from src.utils.querySelector import querySelectorAll

# ####################################################################
# 全局变量
WJX_URL = "https://www.wjx.cn/vm/hIVIpS7.aspx"
USE_IP_PROXY = False  # 是否使用IP代理
driver = BasePage()
# ####################################################################
driver.open_url(WJX_URL)  # 打开问卷
# driver.clear_cookies(driver)    # 清除cookies
blocks = get_all_blocks(driver)  # 获取问卷所有题块
# ####################################################################
# 1 单选
SerialNumber = querySelectorAll(blocks[0], ".ui-radio")
# bili = randomBili(2)  # 生成随机比例
bili = [0, 100]
values = ["填0", "填1", "填2"]  # 有填空待填的内容
index = danxuan(bili)
SerialNumber[index].click()
if index == 1:  # 如果第一个选项有填空，则==0，第二个选项有填空，==1 ...
    temp_loc: WebElement = SerialNumber[index].find_element(By.CSS_SELECTOR, "input.OtherRadioText")
    temp_loc.send_keys(random.choices(values))

# 2 多选
SerialNumber = querySelectorAll(blocks[1], ".ui-checkbox")
bili = [100, 100, 20, 30, 50, 20]
values = ["填0", "填1", "填2"]  # 有填空待填的内容

flag = False
while not flag:
    for count in range(len(bili)):
        index = duoxuan(bili[count])
        if index:
            SerialNumber[count].click()
            if count == 0:  # 如果第一个选项有填空，则==0，第二个选项有填空，==1 ...
                temp_loc: WebElement = SerialNumber[count].find_element(By.CSS_SELECTOR, "input.OtherText")
                temp_loc.send_keys(random.choices(values))
            elif count == 1:
                temp_loc: WebElement = SerialNumber[count].find_element(By.CSS_SELECTOR, "input.OtherText")
                temp_loc.send_keys(random.choices(values))
            flag = True

# 3 填空题

time.sleep(10)
