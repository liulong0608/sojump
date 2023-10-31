# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         driver_options.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 23:21
# @Software:        PyCharm
# ====/******/=====
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.globalparam import log
from src.utils.obtain_ip import get_ip
from src.utils.read_config import read_ini_file


def driver_options(is_wx: bool, is_ip_proxy: bool) -> Options:
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    if is_wx == "True" or is_wx == "true":
        option.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.105 Mobile Safari/537.36 MicroMessenger/8.0.0.1841(0x2800005C) "
            "Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN"
        )
    if is_ip_proxy == "True" or is_ip_proxy == "true":
        try:
            _ips = get_ip(proxy_url=read_ini_file("proxy", "PROXY_URL", file_path=r"D:\sojump\main\线性结构脚本配置.ini"))
            match = random.randint(0, len(_ips) - 1)
            ip = _ips[match]['ip']
            port = _ips[match]['port']
            option.add_argument(f'--proxy-server={ip}:{port}')
        except Exception as e:
            log.error(f"Error occurred while getting IP.")
    else:
        log.warning("未使用代理")
    return option
