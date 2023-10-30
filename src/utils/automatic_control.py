# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         automatic_control.py  
# @version          v1.0.2
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/23 0:03
# @Software:        PyCharm
# ====/******/=====
import textwrap
from typing import Text

from config.setting import ensure_path_sep


class AutomaticControl:

    @staticmethod
    def yaml_data_path() -> Text:
        """ 返回yaml配置文件路径 """
        return ensure_path_sep("\\src\\conf")

    @staticmethod
    def conf_path() -> Text:
        """ 存放配置文件路径 """
        return ensure_path_sep("\\src\\common")


def auto_test():
    import yaml

    # 读取 YAML 文件
    with open(r'D:\sojump\src\conf\questionTypeConfiguration.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # 从 YAML 数据中提取信息
    url = data.get('url', '')
    type = data.get('type', '')
    ccc = data.get('ccc', 0)
    bili = data.get('bili', [])

    # 生成 Python 代码
    python_code = textwrap.dedent(f"""
    bili = {bili}
    ops = driver.find_elements(By.CSS_SELECTOR, lists[{ccc}-1])
    element = driver.find_element(By.CSS_SELECTOR, ops[danxuan(bili)])
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()
""")

    # 将生成的 Python 代码写入文件
    with open('auto_test.py', 'w') as output_file:
        output_file.write(python_code)

    # 打印成功消息
    print("生成的代码已写入 auto_test.py 文件。")


auto_test()