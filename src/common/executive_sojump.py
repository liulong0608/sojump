"""         ==Coding: UTF-8==
**    @Project :        Sojump
**    @fileName         executive_sojump.py
**    @version          v0.4
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/8/12
"""
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

"""
import json
import math
import os
import random
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import DaiLiIp

# 读取JSON配置文件
current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'

print(current_path)


def readJsonConfig(file="../../config/题型配置.json"):
    with open(file, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


json_data = readJsonConfig()


def get_ip(ip_num=1):
    if json_data['ip_proxy'] != 0:
        proxyPool = f'http://http.tiqu.alibabaapi.com/getip?num={ip_num}&type=1&pack=118557&port=1&lb=1&pb=45&regions='
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
        # 如果配置的1，需要ip代理
        # daili = DaiLiIp.DaiLiIP()
        # daili.run()
        # matchs = get_ip_file()
        # for match in matchs:
        #     ip, port = match.strip().split(':')
        #     print('代理ip：{0}:{1}'.format(ip, port))
        match = random.randint(0, len(_ips) - 1)
        ip = _ips[match]['ip']
        port = _ips[match]['port']
        option.add_argument(f'--proxy-server={ip}:{port}')
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    # driver.set_window_size(600, 400)
    # driver.set_window_position(50, 50)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return driver


# driver = driver()


def single_selection(qid: int, bili: list):
    """
    单选题处理函数
    :param qid: 题号
    :param bili: 比例
    :return:
    """
    options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.ui-radio')
    options[danxuan(bili)].click()
    print(f"第{qid}单选题的比例分布为：{bili}")


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
    print(f"第{qid}多选题的比例分布为：{bili}")


def select_options(qid, min_options, bili):
    temp_flag = 0
    ops = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, '.ui-checkbox')
    while temp_flag < min_options:
        temp_answer = []
        for count in range(len(bili)):
            # 这里假设duoxuan是一个函数，需要您自己实现
            if duoxuan(bili[count]):
                temp_answer.append(count)
                temp_flag += 1
            if count == len(bili) - 1 and temp_flag < min_options:
                temp_flag = 0
            elif count == len(bili) - 1 and temp_flag >= min_options:
                for count in range(len(temp_answer)):
                    # 这里假设ops是一个列表，包含了需要点击的元素
                    ops[temp_answer[count]].click()
    print(f"第{qid}多选题（至少{min_options}个选项）的比例分布为：{bili}")


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

    options = driver.find_elements(By.CSS_SELECTOR, f'#select2-q{qid}-results li')
    options = options[1:]  # 去掉第一个选项
    options[danxuan(bili)].click()
    print(f'第{qid}题【下拉框】的比例分布为：{bili}')


def matrix_problem(qid: int, bili: list, subkeys_qid):
    """
    单选矩阵题执行函数
    :param qid:
    :param bili:
    :return:
    """
    matrix_options = get_all_blocks()[qid - 1].find_elements(By.CSS_SELECTOR, 'tbody tr[tp="d"]')
    items = json_data['deploy']
    subkeys_num = items[qid - 1]['subkeys']
    # for i in range(len(subkeys_num)):
    #     options = matrix_options[i].find_elements(By.CSS_SELECTOR, 'td:not(.scalerowtitletd)')
    #     options[danxuan(bili)].click()
    options = matrix_options[subkeys_qid-1].find_elements(By.CSS_SELECTOR, 'td:not(.scalerowtitletd)')
    options[danxuan(bili)].click()
    print(f'第{str(qid)+"1"}题【单选矩阵题】的比例分布为：{bili}')


def get_all_blocks():
    """
    获取所有题块
    :return: 所有题块的元素
    """
    return driver.find_elements(By.CSS_SELECTOR, '.fieldset>div[class="field ui-field-contain"]')


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


def submit():
    try:
        # 出现点击验证码验证
        time.sleep(1)
        # 点击对话框的确认按钮
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        # 点击智能检测按钮
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
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


def main():
    # 遍历 deploy 数组，根据不同类型的题目执行相应的函数
    for item in json_data['deploy']:
        if item['type'] == '单选':
            single_selection(item['qid'], item['bili'])
        elif item['type'] == '多选':
            multiple_selection(item['qid'], item['bili'])
        elif item['type'] == '多选-至少选择几项':
            select_options(item['qid'], item['min_options'], item['bili'])
        elif item['type'] == '填空':
            fill_in_the_blank(item['qid'], item['bili'], item['value'])
        elif item['type'] == '下拉框':
            select_drop_down(item['qid'], item['bili'])
        elif item['type'] == '矩形单选':
            # id = item['subkeys']['subkeys_qid' - 1]
            for i in range(len(item['subkeys'])):
                matrix_problem(item['qid'], item['subkeys'][i]['bili'], item['subkeys'][i]['subkeys_qid'])
    # 提交
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    submit()


def run():
    while True:
        global count
        driver.get(json_data['url'])
        url = driver.current_url
        main()
        time.sleep(4)
        url_ = driver.current_url
        if url != url_:
            count += 1
            print(f"提交时间：{time.strftime('%H:%M:%S', time.localtime(time.time()))}，已提交{count}份！提交IP：{_ips}")
            print("*" * 100)
            driver.get(json_data['url'])
        else:
            time.sleep(2)


if __name__ == '__main__':
    count = 0
    driver = driver()
    run()
