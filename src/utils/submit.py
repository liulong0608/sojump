"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         submit.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/10/30
"""
import time

from config.globalparam import log


def submit(driver, s_time):
    """
    提交执行函数
    Args:
        driver:  Selenium浏览器实例
        s_time:  提交时间

    Returns:

    """
    time.sleep(s_time)
    driver.click("xpath", "//*[@id='ctlNext']")
