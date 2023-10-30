# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         obtain_all_blocks.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/28 21:16
# @Software:        PyCharm
# ====/******/=====
from config.globalparam import log


def get_all_blocks(driver):
    """
    获取所有题块
    :return: 所有题块的元素
    """
    try:
        return driver.get_elements("css", '.fieldset>div[class="field ui-field-contain"]')
    except Exception as e:
        log.error(f"Error occurred while getting all blocks: {str(e)}")
