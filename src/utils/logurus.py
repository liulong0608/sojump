"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         logurus.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/9/5
"""
from loguru import logger
import sys


class LoguruLogger:
    def __init__(self, log_file_path, stream=0):
        """
        loguru二次封装
        :param log_file_path: 日志输出文件路径
        :param stream: 是否输出到控制台（0:否,1:是）
        """
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        if stream == 1:
            # 添加控制台输出的格式,sys.stdout为输出到屏幕
            self.logger.add(sys.stdout, level='DEBUG', enqueue=True, backtrace=True, diagnose=True,
                            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # 颜色>时间
                                   "{process.name} | "  # 进程名
                                   "{thread.name} | "  # 进程名
                                   "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                                   ":<cyan>{line}</cyan> | "  # 行号
                                   "<level>{level}</level>: "  # 等级
                                   "<level>{message}</level>",  # 日志内容
                            )
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(log_file_path, level='DEBUG', enqueue=True,
                        format='{time:YYYY-MM-DD HH:mm:ss} - '  # 时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} - {level} -{message}',  # 模块名.方法名:行号
                        rotation="10 MB")

    def get_logger(self):
        return self.logger
