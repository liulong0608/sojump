# == Coding: UTF-8 ==
# @Project :        wjx
# @fileName         DaiLiIp.py  
# @version          v0.1
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/8/13 15:53
# @Software:        PyCharm
# ====/******/=====
from lxml import etree
import requests


class DaiLiIP:
    def __init__(self):
        self.url_temp = "http://www.89ip.cn/index_{}.html"
        self.headers = {
            'Host': 'www.89ip.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cookie': 'waf_cookie=b75a2f4a-8cec-4f70ffb03b44475d7362e5d7eb11704d46b8; '
                      'Hm_lvt_f9e56acddd5155c92b9b5499ff966848=1594153585; '
                      'Hm_lpvt_f9e56acddd5155c92b9b5499ff966848=1594153585',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
            }

    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1, 51)]
        return url_list

    def parse_url(self, url):
        # print("now url:", url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):
        data = etree.HTML(html_str)
        url_list = data.xpath("//table[@class='layui-table']/tbody/tr/td[1]/text()")
        # print(url_list)

        dk_list = data.xpath("//table[@class='layui-table']/tbody/tr/td[2]/text()")
        # print(dk_list)

        i = 0
        newip_list = []
        while i < len(url_list):
            url = url_list[i].replace('\n', '').replace('\t', '')
            dk = dk_list[i].replace('\n', '').replace('\t', '')
            newip = url + ':' + dk
            newip_list.append(newip)
            i += 1
        return newip_list

    def save_content_list(self, newip_list):
        with open('ip.txt', 'a+', encoding='utf8') as f:
            for newip in newip_list:
                f.write(newip + '\n')

    def run(self):
        # 1、根据url地址规律构造url_list
        url_list = self.get_url_list()
        # 2、发送请求，获取响应
        for url in url_list:
            html_str = self.parse_url(url)
            # 3、提取数据
            content_list = self.get_content_list(html_str)
            # 4、保存
            self.save_content_list(content_list)



