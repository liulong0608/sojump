"""         ==Coding: UTF-8==
**    @Project :        Sojump
**    @fileName         globalparam.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/8/16
"""
import os

from src.utils.logurus import LoguruLogger

# 读取配置文件
config_file_path = os.path.split(os.path.realpath(__file__))[0] + '\\'  # D:\Sojump\config

# 题型配置文件路径
question_config_path = config_file_path + 'test.json'

# 浏览器驱动路径, 默认使用谷歌浏览器
CHROMEDRIVER_PATH = r" D:\sojump\config\chromedriver.exe"  # Chrome浏览器驱动路径
EDGEDRIVER_PATH = r"D:\sojump\config\msedgedriver.exe"  # Edge浏览器驱动路径
FIXEDDRIVER_PATH = r"D:\sojump\config\firefoxdriver.exe"  # Firefox浏览器驱动路径

# 日志文件路径
log = LoguruLogger(r"D:\sojump\src\common\logs\WJX.log", stream=1).get_logger()
