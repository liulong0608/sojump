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
from typing import Text

import requests
from bs4 import BeautifulSoup

import subprocess


def add_chrome_to_path(chrome_path: Text) -> None:
    # 获取当前的PATH环境变量
    path = os.environ.get('PATH', '')
    user_name = os.getlogin()
    appdata_path = os.path.join('C:\\Users', user_name, 'AppData')

    # 检查Chrome路径是否已经在PATH中
    if chrome_path not in path:
        # 将Chrome路径添加到PATH中
        os.environ['PATH'] = f"{path};{appdata_path}{chrome_path}"


def get_chrome_version():
    try:
        # 使用命令行运行 "chrome.exe" 命令并捕获输出
        result = subprocess.run([r"C:\Users\wendaye\AppData\Local\Google\Chrome\Application\chrome.exe", "--version"],
                                capture_output=True, text=True, check=True)

        # 输出包含版本信息，例如 "Google Chrome 98.0.4758.102"
        output = result.stdout.strip()

        # 从输出中提取版本号
        version = output.split()[-1]

        return version
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except FileNotFoundError:
        add_chrome_to_path(r"\\Local\\Google\\Chrome\\Application")


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


if __name__ == '__main__':
    print(get_chrome_version())
