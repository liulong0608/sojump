"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         select_option.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/10/30
"""
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.globalparam import log


def select_option(driver, select_element, options_lsit):
    try:
        # 等待元素可见
        wait = WebDriverWait(driver, 30)
        options_visible = EC.visibility_of_element_located((By.CSS_SELECTOR, 'option'))
        wait.until(options_visible)
        # 获取选项元素列表
        options = [option.text for option in select_element.find_elements(By.CSS_SELECTOR, 'option')]
        if len(options) > 0:
            options.pop(0)  # 排除第一个
            selected_option = random.choice(options)
            driver.execute_script(f"arguments[0].value='{selected_option}';", select_element)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
        else:
            log.error("No options found in select element")
            return
    except IndexError:
        log.error("select_option failed: options list index out of range")
    except Exception as e:
        log.error(f"Error selecting random option: {e}")