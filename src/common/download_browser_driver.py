# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         download_browser_driver.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/8/24 23:07
# @Software:        PyCharm
# ====/******/=====
import os
import requests
from bs4 import BeautifulSoup


def get_chrome_version():
    # 获取当前Chrome浏览器的版本号
    from subprocess import check_output
    version = check_output(['google-chrome', '--version']).decode('utf-8').split(' ')[2]
    return version


def download_driver():
    # 获取Chrome浏览器版本
    version = get_chrome_version()

    # 构建下载链接
    url = f"https://chromedriver.chromium.org/home/downloads/version-selection/?min=80.0.3987.16&max={version}"

    # 发送HTTP请求，获取页面内容
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析页面，获取驱动下载链接
    download_link = soup.find('a', {'class': 'download-link'})['href']

    # 下载驱动文件
    driver_path = os.path.join(os.getcwd(), 'chromedriver')
    response = requests.get(download_link)
    with open(driver_path, 'wb') as file:
        file.write(response.content)

    print(f"驱动已下载至 {driver_path}")