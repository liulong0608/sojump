"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         verify.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/10/30
"""
import time

from selenium.webdriver import ActionChains

from config.globalparam import log


def verify(driver):
    """
    处理验证函数
    Args:
        driver: Selenium浏览器实例

    Returns:

    """
    # 出现点击验证码验证
    time.sleep(1)
    try:
        try:
            # 点击对话框的确认按钮
            driver.click("xpath", '//*[@id="layui-layer1"]/div[3]/a')
            # 点击智能检测按钮
            driver.click("xpath", '//*[@id="SM_BTN_1"]/div[1]/div[3]')
        except:
            # 点击智能检测按钮
            driver.click("xpath", '//*[@id="SM_BTN_1"]/div[1]/div[3]')
        time.sleep(3)
    except:
        log.info("无验证")
    # 滑块验证
    try:
        slider = driver.get_element("xpath", '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            driver.drag_element_horizontally(slider, width)
    except:
        pass
