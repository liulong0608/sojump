# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         ActionWJX.py  
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 22:52
# @Software:        PyCharm
# ====/******/=====
"""
Python version： 3.10.9
Chrome version： 119.0.6045.124
chromedriver version： 119.0.6045.105

代码采用线性结构
"""
import os
import random
import threading
import time
from typing import List, Text

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.globalparam import log, linear_config_path
from public.pages.base_page import BasePage
from src.common.executive_sojump import randomBili
from src.utils.danxuan_duoxuan import danxuan, duoxuan
from src.utils.next_page import next_page
from src.utils.read_config import read_ini_file
from src.utils.submit import submit

lock = threading.Lock()
_count = 0

WJX_URL = "https://www.wjx.cn/vm/hIVIpS7.aspx"  # 问卷地址


# ####################################################################

def handle_wjx(driver):
    # ####################################################################
    try:
        driver.driver.find_element(By.CSS_SELECTOR, ".slideChunkWord").click()
    except:
        pass
    # 1 单选
    SerialNumber = driver.get_elements("css", "#div1 div.ui-radio")  # 第一题，就是div1
    # bili = randomBili(2)  # 生成随机比例
    bili = [0, 100]
    values = ["填0", "填1", "填2"]  # 有填空待填的内容
    index = danxuan(bili)
    SerialNumber[index].click()
    if index == 1:  # 如果第一个选项有填空，则==0，第二个选项有填空，==1 ...
        temp_loc: WebElement = SerialNumber[index].find_element(By.CSS_SELECTOR, "input.OtherRadioText")
        temp_loc.send_keys(random.choices(values))

    # 2 多选
    SerialNumber = driver.get_elements("css", "#div2 div.ui-checkbox")
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
    SerialNumber = driver.get_element("css", "#div3 div.ui-input-text input")
    bili = randomBili(3)
    values = ["填0", "填1", "填2"]
    SerialNumber.send_keys(values[danxuan(bili)])

    # 4 下拉框题
    driver.click("css", "#div4 .select2-selection.select2-selection--single")
    options = driver.get_elements("css", "#select2-q4-results li")  # 第4题，就是q4
    options = options[1:]  # 去掉第一个选项
    time.sleep(0.3)
    options[danxuan(bili)].click()

    # 5 多选题-至少选3项
    SerialNumber = driver.get_elements("css", "#div5 div.ui-checkbox")
    bili = randomBili(4)
    min_option = 3
    selected_answers = []
    temp_flag = 0
    while len(selected_answers) < min_option:
        for count in range(len(bili)):
            if duoxuan(bili[count]):
                selected_answers.append(count)
                selected_answers = list(set(selected_answers))
                temp_flag += 1
        if len(selected_answers) < min_option:
            temp_flag = 0
    for idx in selected_answers:
        SerialNumber[idx].click()

    # 6 单选矩形题、矩阵量表题
    matrix_options = driver.get_elements("css", "#div6 tbody tr[tp='d']")
    subkeys_length = len(matrix_options)
    for index in range(len(matrix_options)):
        bili = randomBili(4)
        options = matrix_options[index].find_elements(By.CSS_SELECTOR, "td:not(.scalerowtitletd)")
        options[danxuan(bili)].click()

    # 7 排序题
    jmix_options = driver.get_elements("css", "#div7 ul li")
    for i in range(1, len(jmix_options) + 1):
        index = random.randint(i, len(jmix_options))
        if index != 5:
            driver.get_element("css", f"#div7 > ul > li:nth-child({index})").click()
            time.sleep(0.5)

    # 8 量表题
    SerialNumber = driver.get_elements("css", '#div8 ul[tp="d"] li')
    # bili = randomBili(2)  # 生成随机比例
    bili = [20, 20, 20, 20]
    index = danxuan(bili)
    SerialNumber[index].click()

    # 9 多项填空
    SerialNumber = driver.get_elements("css", "#div9 .topictext span.textCont")
    # 第一个空
    bili = randomBili(3)
    values = ["张三", "李四", "王五"]
    SerialNumber[0].send_keys(values[danxuan(bili)])
    # 第二个空
    bili = randomBili(3)
    values = [23, 24, 30]
    SerialNumber[1].send_keys(values[danxuan(bili)])
    # 第三个空
    bili = randomBili(3)
    values = ["135000000", "151000000", "198000000"]
    SerialNumber[2].send_keys(values[danxuan(bili)])

    # 10 多级下拉题-选项不随机
    subkeys_list = [
        {
            "subkeys_qid": 1,
            "value": "华北地区"
        },
        {
            "subkeys_qid": 2,
            "value": "山东省"
        },
        {
            "subkeys_qid": 3,
            "value": "青岛市"
        },
        {
            "subkeys_qid": 4,
            "value": "黄岛区"
        }
    ]
    driver.click("css", "#div10 input#q10")  # 第10题，就是div0, q10
    for i in range(len(subkeys_list)):
        select_element = driver.get_element("css",
                                            f'#divFrameData div.ui-select:nth-child({subkeys_list[i]["subkeys_qid"]}) select')
        if select_element:
            driver.executeJsScript(f"arguments[0].value='{subkeys_list[i]['value']}';", select_element)
            driver.executeJsScript("arguments[0].dispatchEvent(new Event('change'));", select_element)
        time.sleep(0.8)
    driver.click("css", ".layer_save_btn a")

    # ###############################################
    # 点击下一页
    next_page(driver)
    # ###############################################

    # 11 多级下拉题-选项随机
    try:
        numberOfDropDownBoxes = 3  # 下拉框个数
        driver.click("css", "#div11 input#q11")  # 第11题，就是div11, q11
        option_list = []
        select_elements = driver.get_elements("css", "#divFrameData .layer_content select")
        for index in range(1, int(numberOfDropDownBoxes) + 1):
            select_element = select_elements[index - 1]
            if select_element:
                __option = select_element.find_elements(By.CSS_SELECTOR, "option")  # 获取所有下拉选项
                if len(__option) > 0:
                    __option.pop(0)  # 排除第一个
                    selected_option = random.choice(__option)
                    option_list.append(selected_option)
                    driver.executeJsScript(f"arguments[0].value='{selected_option.text}';", select_element)
                    driver.executeJsScript("arguments[0].dispatchEvent(new Event('change'));", select_element)
                    time.sleep(0.5)
                else:
                    log.error("未找到下拉框中的内容！")
    except Exception as e:
        log.warning({str(e)})
    time.sleep(0.5)
    driver.click("css", ".layer_save_btn a")

    # 12 矩阵填空题
    subkeys_list = [
        {
            "subkeys_qid": 1,
            "value": ["差", "一般", "好", "极好"],
            "bili": [25, 25, 25, 25]
        },
        {
            "subkeys_qid": 2,
            "value": ["差", "一般", "好", "极好"],
            "bili": [25, 25, 25, 25]
        },
        {
            "subkeys_qid": 3,
            "value": ["差", "一般", "好", "极好"],
            "bili": [25, 25, 25, 25]
        }
    ]
    options = driver.get_elements("css", "#div12 div.ui-input-text textarea")
    for index in range(len(subkeys_list)):
        options[index].send_keys(subkeys_list[index]["value"][danxuan(subkeys_list[index]["bili"])])
        time.sleep(0.3)

    # 13 矩阵滑条题
    subkeys_list = [
        {
            "subkeys_qid": 1,
            "value_random": {
                "flag": True,
                "min": 0,
                "max": 100
            },
            "value": [10, 22, 23, 80]
        },
        {
            "subkeys_qid": 2,
            "value_random": {
                "flag": True,
                "min": 0,
                "max": 100
            },
            "value": [50, 70, 88, 93]
        }
    ]
    options = driver.get_elements("css", "#div13 input.ui-slider-input")
    for index in range(len(subkeys_list)):
        if subkeys_list[index]['value_random']:
            fill_value = random.randint(subkeys_list[index]['value_random']['min'],
                                        subkeys_list[index]['value_random']['max'])
            options[index].send_keys(fill_value)
            time.sleep(0.3)
        else:
            fill_value = subkeys_list[index]['value']
            options[index].send_keys(fill_value)
            time.sleep(0.3)

    # 14 矩阵量表题
    matrix_options = driver.get_elements("css", "#div14 tbody tr[tp='d']")
    subkeys_list = [
        {
            "subkeys_qid": 1,
            "bili": [0, 0, 0, 0, 100]
        },
        {
            "subkeys_qid": 2,
            "bili": [0, 0, 0, 0, 100]
        },
        {
            "subkeys_qid": 3,
            "bili": [100, 0, 0, 0, 0]
        }
    ]
    for index in range(len(matrix_options)):
        bili = subkeys_list[index]["bili"]
        options = matrix_options[index].find_elements(By.CSS_SELECTOR, "td:not(.scalerowtitletd)")
        options[danxuan(bili)].click()

    # 15 多选矩阵题
    subkeys_list = [
        {
            "subkeys_qid": 1,
            "bili": [25, 25, 25, 25]
        },
        {
            "subkeys_qid": 2,
            "bili": [25, 25, 25, 25]
        },
        {
            "subkeys_qid": 3,
            "bili": [25, 25, 25, 25]
        },
        {
            "subkeys_qid": 4,
            "bili": [25, 25, 25, 25]
        }
    ]
    matrix_options = driver.get_elements("css", "#div15 tbody tr[tp='d']")
    for index in range(len(matrix_options)):
        options = matrix_options[index].find_elements(By.CSS_SELECTOR, "td:not(.scalerowtitletd)")
        flag = False
        while not flag:
            for count in range(len(subkeys_list[index]['bili'])):
                index = duoxuan(subkeys_list[index]['bili'][count])
                if index:
                    options[count].click()
                    time.sleep(0.3)
                    flag = True

    # 16 多选题-最多选择3项
    SerialNumber = driver.get_elements("css", "#div16 div.ui-checkbox")
    bili = randomBili(5)
    max_option = 3  # 最多选择3项
    selected_answers = []
    while True:
        for count in range(len(bili)):
            if len(selected_answers) < max_option:
                if duoxuan(bili[count]):
                    selected_answers.append(count)
                    selected_answers = list(set(selected_answers))
                    continue
            else:
                break
        if len(selected_answers) != 0:
            break
    for idx in selected_answers:
        SerialNumber[idx].click()

    """
        # 地理位置题
        try:
        address = "安徽省安庆市潜山市龙潭乡龙潭乡人民政府"
        driver.executeJsScript("arguments[0].value='{}'".format(address),
                               driver.driver.find_element(By.CSS_SELECTOR, "input#q题号"))  # 第2题，就是q2
        driver.click("css", ".getLocalBtn")
        driver.switch_to_frame("tag", "iframe")
        driver.click("css", ".lbs-list div.localres_wrap.divCurLoc a")
    except Exception as e:
        log.warning({str(e)})
    finally:
        driver.switch_to_default_content()
    """
########################################################################################################################

    try:
        # 提交
        s_time: int = 5  # 等待5秒后提交
        # submit(driver, s_time)
        submit(driver, random.randint(5, 10))  # 随机等待5-10秒提交
    except:
        pass


def run(x_axi, y_axi):
    global _count
    _WJX_URL = WJX_URL
    driver = BasePage(x_axi, y_axi)
    num = read_ini_file("copies", "num", file_path=linear_config_path)  # 读取配置文件中的份数
    while _count < int(num):
        try:
            driver.open_url(_WJX_URL)
            driver.clear_cookies()  # 清除cookie
            star_time = time.time()
            try:
                msg = driver.driver.find_element(By.CSS_SELECTOR, ".layui-layer-content").text
                if str(msg).startswith("您之前已经回答了部分题目，是否继续上次回答"):
                    driver.click("css", ".layui-layer-btn.layui-layer-btn- a.layui-layer-btn1")
            except:
                pass
            # driver.clear_cookies()
        except Exception as e:
            log.error(f"Error occurred while opening url: {str(e)}")
            driver.quit()
            driver = BasePage(x_axi, y_axi)
            continue

        before_url = driver.get_url()
        wj_flag = driver.getAttribute("css", "#divPowerBy a", "title")
        if driver.driver.execute_script(
                "return document.readyState;") == "complete" and wj_flag == "问卷星_不止问卷调查/在线考试" and time.time() - star_time < 60:  # 判断页面是否加载完
            log.info("问卷加载完毕，开始执行刷题")
            handle_wjx(driver)
        else:
            log.warning("60s内页面未加载完，重新打开浏览器")
            driver.quit()
            driver = BasePage(x_axi, y_axi)
            continue
        driver.verify()
        # time.sleep(1)
        success_msg = driver.get_textContent("css", "div.ValError .submit_tip_color")
        if "提交成功" in success_msg or before_url in "https://www.wjx.cn/wjx/join/completemobile2.aspx?":
            with lock:
                _count += 1
            log.success(
                "\033[35m" + f"提交时间：{time.strftime('%H:%M:%S', time.localtime(time.time()))}，已提交{_count}份！" + "\033[0m")
            if read_ini_file("proxy", "USE_IP_PROXY", file_path=linear_config_path) == "True":
                driver.quit()
                if _count == int(num):
                    break
                time.sleep(1)
                driver = BasePage(x_axi, y_axi)

        else:
            log.error("提交失败,大概有题目未完成或验证未通过，重新打开浏览器")
            driver.quit()
            driver = BasePage(x_axi, y_axi)


if __name__ == "__main__":
    try:
        if read_ini_file("proxy", "USE_IP_PROXY", file_path=linear_config_path) == "False":
            threads = []
            for i in range(2):
                x_axi = i * 970
                t = threading.Thread(target=run, args=(x_axi, 0))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        else:
            run(x_axi=-10, y_axi=0)
    except KeyboardInterrupt:
        exit()
