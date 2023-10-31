# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         obtain_ip.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/28 20:36
# @Software:        PyCharm
# ====/******/=====
import re
from typing import Text, List

from config.globalparam import log
import requests


def get_ip(proxy_url: Text) -> List:
    """
    通过api获取代理ip,获取指定ip个数
    :param proxy_url: 代理url地址
    :return: List

    Usage:
        [{'ip': '117.31.87.23', 'port': '43351'}]
    """
    ips = []
    try:
        ip_port = requests.get(proxy_url).text
        pools = re.findall(r"(\d+\.\d+\.\d+\.\d+):(\d+)", ip_port)
        ips = [{"ip": ip, "port": port} for ip, port in pools]
        if len(ips) != 0:
            log.info(f"提取到ip：{ips}")
            return ips
        else:
            log.error(f"未提取到ip，默认使用本地ip")
    except requests.exceptions.RequestException as e:
        log.error(f"Error occurred while getting IP: {str(e)}")
    except Exception as e:
        log.error(f"提取ip发生异常，默认使用本地ip：{str(e)}")


