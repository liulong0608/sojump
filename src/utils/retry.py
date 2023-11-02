"""         ==Coding: UTF-8==
**    @Project :        sojump
**    @fileName         retry.py
**    @version          v0.1
**    @author           Echo
**    @Warehouse        https://gitee.com/liu-long068/
**    @EditTime         2023/11/2
"""
from config.globalparam import log


# 重试装饰器
def retry(retry_times=3):
    def wrapper(func):
        def inner(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.error("执行发生错误，开始重试！")
                    # 发生异常时重新打开浏览器
                    # driver = BasePage(970, 0)

        return inner

    return wrapper
