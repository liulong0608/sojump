# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         driver_options.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 23:21
# @Software:        PyCharm
# ====/******/=====
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def driver_options(is_wx: bool) -> Options:
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    if is_wx == "True" or is_wx == "true":
        option.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.105 Mobile Safari/537.36 MicroMessenger/8.0.0.1841(0x2800005C) "
            "Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN"
        )
    return option
