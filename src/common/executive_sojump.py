"""         ==Coding: UTF-8==
**    @Project :        Sojump
**    @fileName         executive_sojump.py
**    @version          v1.3
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/8/12
"""
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import math
import os
import random
import re
import time

import threading
from config import globalparam
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.common.DaiLiIp import DaiLiIP

"""
## 重构问卷星脚本代码
    * v0.1
        * 面向过程的方式
        1、先写配置读取JSON配置文件
        2、循环遍历JSON题型（判断题型，执行该题型的执行函数）
            1. v0.1版本完善了单选、多选、填空的执行函数
    * v0.2
        * 面向过程的方式
        1、增加代理ip
    * v0.3
        * 面向过程的方式
        1、增加题型（下拉框、多选题（至少选择几项））
    * v0.4
        * 面向过程的方式
        1、增加题型（单选矩形题）
    * v0.5
        * 面向过程的方式
        1、增加题型（排序题（随机排序））
        2、优化验证函数和提交函数
    * v0.6
        * 面向过程的方式
        1、优化获取页面元素的函数
    * v0.7
        * 面向过程的方式
        1、增加题型（单选量表题）    
    * v0.8
        * 面向过程的方式
        1、增加题型（多级下拉题-随机、多级下拉题-不随机）
    * v0.8.2
        * 面向过程的方式
        1、完善多级下拉题-不随机
        2、增加清除cookie缓存机制
    * v0.9
        * 面向过程的方式
        1、增加题型（多项填空）
    * v1.0
        * 面向过程的方式
        1、优化单选矩阵题执行函数的逻辑
        2、优化多级下拉题执行函数
        3、优化元素定位增加显式等待，异常处理
        4、优化多选填空题执行函数
        5、优化提交函数，增加提交等待时间
        6、优化判断题型执行相关题型函数逻辑
        7、优化(多级下拉框执行函数-选项随机)执行函数的逻辑
        8、增加多线程方式执行脚本（todo）
    * v1.1
        * 面向过程的方式
        1、优化多级下拉框题执行速度
        2、新增题型（矩阵填空题）
        3、暂时关闭多线程执行方式
    * v1.2
        * 面向过程的方式
        1、修复一些问题
        2、通过读取配置文件决定提交时间，是否修改userAgent
        3、回滚到多线程之前的版本
    * v1.3
        * 面向过程的方式
        1、新增题型（矩阵滑块题）
"""


# 读取JSON配置文件
def readJsonConfig(file=globalparam.question_config_path):
    with open(file, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


json_data = readJsonConfig()


def get_ip(ip_num=1):
    if json_data['ip_proxy'] != 0:
        proxyPool = f'http://http.tiqu.alibabaapi.com/getip?num={ip_num}&type=1&pack=你的id&port=1&lb=1&pb=45&regions='
        ips = []
        ip_port = requests.get(proxyPool).text
        pools = re.findall(r"(\d+\.\d+\.\d+\.\d+):(\d+)", ip_port)
        for pool in pools:
            ip = pool[0]
            port = pool[1]
            dict = {
                "ip": ip,
                "port": port
            }
            ips.append(dict)
        print(f"提取到ip：{ips}")
        return ips
    return '本地IP'


def get_ip_file(ip_num=1):  # 获取指定ip个数
    """
    通过文件获取代理ip,获取指定ip个数
    :return:
    """
    with open('ip.txt', 'r') as f:
        lines = f.readlines()
        selected_lines = lines[:ip_num]
        return selected_lines


_ips = get_ip()


def driver():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # 随机获取某个代理值
    if json_data['ip_proxy'] == 0:
        # 如果配置的0，则不需要ip代理
        pass
    elif json_data['ip_proxy'] == 1:
        match = random.randint(0, len(_ips) - 1)
        ip = _ips[match]['ip']
        port = _ips[match]['port']
        option.add_argument(f'--proxy-server={ip}:{port}')
    if json_data['wx_respond'] == 1:
        # 添加user-agent
        option.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.105 Mobile Safari/537.36 MicroMessenger/8.0.0.1841(0x2800005C) "
            "Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN")
    service = Service('../../python/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=option)
    driver.maximize_window()
    # driver.set_window_size(512, 1440)
    # driver.set_window_position(x, y)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return driver


def single_selection(qid: int, bili: list):
    """
    单选题处理函数
    :param qid: 题号
    :param bili: 比例
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.ui-radio')
    options[danxuan(bili)].click()
    print(f"第{qid}题【单选题】的比例分布为：{bili}")


def multiple_selection(qid: int, bili: list):
    """
    多选题处理函数
    :param qid: 题号
    :param bili: 比例
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.ui-checkbox')
    flag = False
    while not flag:
        for count in range(len(bili)):
            if duoxuan(bili[count]):
                options[count].click()
                flag = True
    print(f"第{qid}题【多选题】的比例分布为：{bili}")


def select_options(qid, min_options, bili):
    temp_flag = 0
    ops = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.ui-checkbox')
    while temp_flag < min_options:
        temp_answer = []
        for count in range(len(bili)):
            if duoxuan(bili[count]):
                temp_answer.append(count)
                temp_flag += 1
            if count == len(bili) - 1 and temp_flag < min_options:
                temp_flag = 0
            elif count == len(bili) - 1 and temp_flag >= min_options:
                for count in range(len(temp_answer)):
                    # ops列表，包含了需要点击的元素
                    ops[temp_answer[count]].click()
    print(f"第{qid}题【多选题】（至少{min_options}个选项）的比例分布为：{bili}")


def fill_in_the_blank(qid: int, bili: list, value: list):
    """
    填空题执行函数
    :param qid: 题号
    :param bili: 比例
    :param value: 待填空的值
    :return:
    """
    fill_value = value[danxuan(bili)]
    get_all_blocks()[qid - 1].find_element(By.CSS_SELECTOR, f'#q{qid}').send_keys(fill_value)
    print(f'第{qid}题【填空题】的比例分布为：{bili}')


# 下拉框执行函数
def select_drop_down(qid: int, bili: list):
    """
    下拉框执行函数
    :param qid: 题号
    :param bili: 比例
    :return:
    """
    get_all_blocks()[qid - 1].find_element(By.CSS_SELECTOR, '.select2-selection.select2-selection--single').click()

    options = get_elements_by_css(f'#select2-q{qid}-results li')
    options = options[1:]  # 去掉第一个选项
    options[danxuan(bili)].click()
    print(f'第{qid}题【下拉框】的比例分布为：{bili}')


def matrix_problem(qid: int):
    """
    单选矩阵题执行函数
    :param qid:
    :return:
    """
    matrix_options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, 'tbody tr[tp="d"]')
    items = json_data['deploy']
    subkeys_lists = items[qid - 1]['subkeys']
    for index in range(len(subkeys_lists)):
        options = matrix_options[index].find_elements(By.CSS_SELECTOR, 'td:not(.scalerowtitletd)')
        options[danxuan(subkeys_lists[index]['bili'])].click()
        print(
            f'第{str(qid)}-{subkeys_lists[index]["subkeys_qid"]}题【单选矩阵题】的比例分布为：{subkeys_lists[index]["bili"]}')


def JMix(qid: int, bili: list):
    """
    排序题执行函数
    :param qid:
    :param bili:
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, f"#div{qid} ul li")

    # 按照比例对选项进行排序
    # def map_list_to_indices(lst):
    #     array_list = []
    #     for item in lst:
    #         array_list.append(item)
    #
    #     array_list.sort(reverse=True)
    #     map_dict = {}
    #     for i in range(len(array_list)):
    #         map_dict[array_list[i]] = i
    #
    #     a = np.zeros(len(lst), dtype=int)
    #     for i in range(len(lst)):
    #         a[i] = map_dict.get(lst[i])
    #         del map_dict[lst[i]]
    #
    #     return list(a)
    #
    # sorted_indices = map_list_to_indices(bili)
    q_lists = get_elements_by_css(f'#div{qid} > ul > li')
    for index in bili:
        # driver.find_element(By.CSS_SELECTOR, f'#div{qid} > ul > li:nth-child({index+1})').click()
        q_lists[index - 1].click()
        time.sleep(0.5)
    print(f'第{qid}题【排序题】的比例分布为：{bili}')
    # todo
    # 因为按照指定的比例进行排序在vm网址不太好实现，对于排序题暂时只用随机排序random_JMix()方法


def random_JMix(qid: int):
    """
    排序题执行函数
    :param qid:
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, f"#div{qid} ul li")
    for i in range(1, len(options) + 1):
        index = random.randint(i, len(options))
        get_element_by_css(f'#div{qid} > ul > li:nth-child({index})').click()
        time.sleep(0.5)
    print(f'第{qid}题【排序题】的比例分布为：随机排序')


# 单选量表题执行函数
def single_scale(qid: int, bili: list):
    """
    单选量表题执行函数
    :param qid: 题号
    :param bili: 比例
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, 'ul[tp="d"] li')
    options[danxuan(bili)].click()
    print(f'第{qid}题【单选量表题】的比例分布为：{bili}')


def multilevel_pulldown_nonrandom(qid: int):
    """
    多级下拉框执行函数-选项不随机
    :param qid: 题号
    :return:
    """
    get_all_blocks()[qid - 1].find_element(By.CSS_SELECTOR,
                                           f"#div{qid} input#q{qid}").click()
    time.sleep(1)
    items = json_data['deploy']  # all question list
    subkeys_list = items[qid - 1]['subkeys']
    for index in range(len(subkeys_list)):
        select_element = get_element_by_css(
            f'#divFrameData div.ui-select:nth-child({subkeys_list[index]["subkeys_qid"]}) select')
        # time.sleep(1)
        if select_element:
            driver.execute_script(f"arguments[0].value='{subkeys_list[index]['value']}';",
                                  select_element)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
            time.sleep(0.5)
            print(
                f"第{qid}题【多级下拉框】的第{subkeys_list[index]['subkeys_qid']}个select选择为：{subkeys_list[index]['value']}")
    click(".layer_save_btn a")


def multilevel_pulldown_random(qid: int):
    """
    多级下拉框执行函数-选项随机
    :param qid: 题号
    :return:
    """
    items = json_data['deploy']
    list_num = items[qid - 1]['Drop-downNumber']
    options = {}
    for i in range(1, list_num + 1):
        # 创建i个空列表
        options[f"options_{i}"] = []
    # options["options_1"]
    get_all_blocks()[qid - 1].find_element(By.CSS_SELECTOR, f'#div{qid} input#q{qid}').click()
    time.sleep(1)
    # 获取有多少个select
    select_list = get_elements_by_css(f'#divFrameData div.ui-select')
    # select_num = len(select_list)
    for index in range(list_num):
        select_element = get_element_by_css(
            f'#divFrameData div.ui-select:nth-child({index + 1}) select')
        if select_element:
            options[f"options_{index + 1}"].append(select_element)
            select_option(select_element, options[f"options_{index + 1}"])
            time.sleep(0.2)
            print(
                f"第{qid}题【多级下拉框】的第{index + 1}个select选择为：随机选项")
    time.sleep(0.5)
    click(".layer_save_btn a")


def multinomial_filling(qid: int):
    """
    多项填空题执行函数
    :param qid: 题号
    :return:
    """
    items = json_data['deploy']
    subkeys_list = items[qid - 1]['subkeys']
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.topictext span.textCont')
    for index in range(len(subkeys_list)):
        fill_value = subkeys_list[index]['value'][danxuan(subkeys_list[index]['bili'])]
        options[index].send_keys(fill_value)
        print(
            f'第{str(qid)}-{subkeys_list[index]["subkeys_qid"]}题【多项填空题】的比例分布为：{subkeys_list[index]["bili"]}')


def matrix_filling(qid: int):
    """
    矩阵填空题执行函数
    :param qid: 题号
    :return:
    """
    items = json_data['deploy']
    subkeys_list = items[qid - 1]['subkeys']
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, 'div.ui-input-text textarea')
    for index in range(len(subkeys_list)):
        fill_value = subkeys_list[index]['value'][danxuan(subkeys_list[index]['bili'])]
        options[index].send_keys(fill_value)
        print(
            f'第{str(qid)}-{subkeys_list[index]["subkeys_qid"]}题【矩阵填空题】的比例分布为：{subkeys_list[index]["bili"]}')


def matrix_slider_problem(qid: int):
    """
    矩阵滑块题执行函数
    :return:
    """
    items = json_data['deploy']
    subkeys_list = items[qid - 1]['subkeys']
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, 'input.ui-slider-input')
    for index in range(len(subkeys_list)):
        if subkeys_list[index]['value_random']:
            fill_value = random.randint(subkeys_list[index]['value_random']['min'], subkeys_list[index]['value_random']['max'])
            options[index].send_keys(fill_value)
        else:
            fill_value = subkeys_list[index]['value']
            options[index].send_keys(fill_value)
        print(
            f'第{str(qid)}-{subkeys_list[index]["subkeys_qid"]}题【矩阵滑块题】的选项值为：{fill_value}')


def get_all_blocks():
    """
    获取所有题块
    :return: 所有题块的元素
    """
    return get_elements_by_css('.fieldset>div[class="field ui-field-contain"]')


def danxuan(proportion):
    """
    单选执行函数
    :param proportion: 比例
    :return: 选项的索引值
    """
    total = sum(proportion)  # 计算总比例
    random_num = math.floor(random.random() * total) + 1  # 生成随机数
    for index in range(len(proportion)):
        random_num -= proportion[index]  # 减去当前选项的比例值
        if random_num <= 0:
            return index


def duoxuan(probability):
    """
    多选题执行函数
    :param probability: 比例
    :return:
    """
    flag = False
    i = random.randint(1, 100)
    if i <= probability:
        flag = True
    return flag


def randomBili(num):
    a = 100 // num
    yu = 100 - a * num
    result = []
    for i in range(num):
        result.append(a)
    for i in range(yu):
        result[i] += 1
    return result


def submit(s_time):
    """
    提交执行函数
    :param s_time: 提交等待时间(秒)
    :return:
    """
    time.sleep(s_time)
    click('//*[@id="ctlNext"]', 'xpath')
    errorMessage = get_element_by_css('.errorMessage').text
    if errorMessage == "请选择选项":
        print("提交失败，存在未选择的题，请检查...")


# 封装元素定位
def get_element_by_css(loc, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, loc))
        )
        return element
    except Exception as e:
        print(f"Failed to find element by CSS: {loc}")
        return None


def get_elements_by_css(loc, timeout=10):
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, loc))
        )
        return elements
    except Exception as e:
        print(f"Failed to find elements by CSS: {loc}")
        return []


def get_element_by_xpath(loc, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, loc))
        )
        return element
    except Exception as e:
        print(f"Failed to find element by CSS: {loc}")
        return None


def get_elements_by_xpath(loc, timeout=10):
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, loc))
        )
        return elements
    except Exception as e:
        print(f"Failed to find elements by CSS: {loc}")
        return []


def click(loc, locator_type='css', timeout=10):
    try:
        if locator_type == 'id':
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, loc))
            )
            element.click()
        elif locator_type == 'name':
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.NAME, loc))
            )
            element.click()
        elif locator_type == 'xpath':
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, loc))
            )
            element.click()
        elif locator_type == 'css':
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, loc))
            )
            element.click()
    except NoSuchElementException:
        print(f"Element not found by {locator_type}: {loc}")
    except Exception as e:
        print(f"Failed to click element: {e}")


def select_option(select_element, options):
    # 将下拉列表的元素放置在列表中
    options = [option.text for option in select_element.find_elements(By.CSS_SELECTOR, 'option')]
    options.pop(0)  # 排除第一个
    selected_option = random.choice(options)
    driver.execute_script(f"arguments[0].value='{selected_option}';", select_element)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)


# 封装通过题块获取子题块
def get_child_blocks(qid, loc):
    return get_all_blocks()[qid].find_elements(By.CSS_SELECTOR, loc)


def verify():
    try:
        # 出现点击验证码验证
        time.sleep(1)
        try:
            # 点击对话框的确认按钮
            driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
            # 点击智能检测按钮
            driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]/div[1]/div[3]').click()
        except:
            # 点击智能检测按钮
            driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]/div[1]/div[3]').click()
        time.sleep(3)
    except:
        print("无验证")
        # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass


def handle_single_selection(item):  # 单选
    single_selection(item['qid'], item['bili'])


def handle_multiple_selection(item):  # 多选
    multiple_selection(item['qid'], item['bili'])


def handle_select_option(item):  # 多选-至少选择几项
    select_options(item['qid'], item['min_options'], item['bili'])


def handle_fill_blank(item):  # 填空
    fill_in_the_blank(item['qid'], item['bili'], item['value'])


def handle_multinomial_filling(item):  # 多项填空
    multinomial_filling(item['qid'])


def handle_matrix_filling(item):  # 矩阵填空
    matrix_filling(item['qid'])


def handle_select_drop_down(item):  # 下拉框
    select_drop_down(item['qid'], item['bili'])


def handle_multilevel_pulldown_nonrandom(item):  # 多级下拉框-不随机
    multilevel_pulldown_nonrandom(item['qid'])


def handle_multilevel_pulldown_random(item):  # 多级下拉框-随机
    multilevel_pulldown_random(item['qid'])


def handle_random_JM(item):  # 随机排序题  JMix
    random_JMix(item['qid'])


def handle_matrix_problem(item):  # 单选矩阵题
    matrix_problem(item['qid'])


def handle_matrix_multiSelect(item):  # 多选矩阵题
    pass


def handle_single_scale(item):  # 单选量表题
    single_scale(item['qid'], item['bili'])


def handle_multi_scale(item):  # 多选量表题
    pass


def handle_matrix_slider_problem(item):  # 矩阵滑块题
    matrix_slider_problem(item['qid'])


def main():
    handler_mapping = {
        '单选题': handle_single_selection,
        '多选题': handle_multiple_selection,
        '多选题-至少选择几项': handle_select_option,
        '填空题': handle_fill_blank,
        '多项填空题': handle_multinomial_filling,
        '矩阵填空题': handle_matrix_filling,
        '下拉题': handle_select_drop_down,
        '多级下拉题-不随机': handle_multilevel_pulldown_nonrandom,
        '多级下拉题-随机': handle_multilevel_pulldown_random,
        '排序题': handle_random_JM,
        '单选矩阵题': handle_matrix_problem,
        '多选矩阵题': handle_matrix_multiSelect,
        '单选量表题': handle_single_scale,
        '多选量表题': handle_multi_scale,
        '矩阵滑块题': handle_matrix_slider_problem
    }
    for item in json_data['deploy']:
        item_type = item['type']
        handler = handler_mapping.get(item_type)
        if handler:
            handler(item)
        else:
            print(f"Unsupported item type:{item_type}")
    # 提交
    time.sleep(1)
    if json_data['submit_random_time']['flag']:
        submit(random.randint(json_data['submit_random_time']['min'], json_data['submit_random_time']['max']))
    else:
        submit(json_data['submit_time'])  # 等待设定的秒数后提交
    verify()


def run():
    while True:
        global count
        driver.delete_all_cookies()
        driver.get(json_data['url'])
        time.sleep(2)
        main()
        time.sleep(4)
        url_ = driver.current_url
        if 'https://www.wjx.cn/wjx/join/completemobile2.aspx?' in url_:
            count += 1
            print(f"提交时间：{time.strftime('%H:%M:%S', time.localtime(time.time()))}，已提交{count}份！提交IP：{_ips}")
            print("*" * 100)
            driver.get(json_data['url'])
        else:
            time.sleep(2)
            return "提交时遇到错误，程序终止."


if __name__ == '__main__':
    count = 0  # 初始提交份数
    driver = driver()
    run()
