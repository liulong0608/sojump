"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         next_page.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/10/30
"""
import time


def next_page(driver):
    """
    下一页
    :param driver:
    :return:
    """
    driver.click("css", "div#divNext a")
    time.sleep(1)

