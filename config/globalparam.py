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
config_file_path = os.path.split(os.path.realpath(__file__))[0]
# 项目根目录
prj_path = os.path.dirname(config_file_path)
# 线性结构题型配置文件路径
linear_config_path = os.path.join(prj_path, 'main', '线性结构脚本配置.ini')
# 题型配置文件路径
question_config_path = os.path.join(prj_path, 'config', 'question_config.json')
# 浏览器驱动路径, 默认使用谷歌浏览器
CHROMEDRIVER_PATH = os.path.join(prj_path, 'config', 'chromedriver.exe')  # Chrome浏览器驱动路径
EDGEDRIVER_PATH = os.path.join(prj_path, 'config', 'edgedriver.exe')  # Edge浏览器驱动路径
FIXEDDRIVER_PATH = os.path.join(prj_path, 'config', 'geckodriver.exe')  # Firefox浏览器驱动路径
# 日志文件路径
log_path = os.path.join(prj_path, 'main', 'logs', 'WJX.log')
log = LoguruLogger(log_path, stream=True).get_logger()
