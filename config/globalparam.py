"""         ==Coding: UTF-8==
**    @Project :        Sojump
**    @fileName         globalparam.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/8/16
"""
import os

# 读取配置文件
config_file_path = os.path.split(os.path.realpath(__file__))[0] + '\\'  # D:\Sojump\config

# 题型配置文件路径
question_config_path = config_file_path + '题型配置.json'

# 浏览器驱动路径
driver_path = '../python/chromedriver.exe'
