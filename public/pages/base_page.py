# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         base_page.py  
# @version          bate1.2.3
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 23:17
# @Software:        PyCharm
# ====/******/=====
from typing import Text, Tuple, List, Any

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logurus import LoguruLogger
from src.utils.read_config import read_ini_file
from src.utils.driver_options import driver_options

log = LoguruLogger(r"/src/common/logs/sojump.log", stream=1).get_logger()


class BasePage:

    def __init__(self):
        self.driver = self.new_driver()
        self.wait: WebDriverWait = WebDriverWait(self.driver, timeout=20, poll_frequency=0.8)

    @staticmethod
    def new_driver() -> WebDriver:
        service = Service(read_ini_file("chromeDriver", "path"))
        driver = webdriver.Chrome(service=service,
                                  options=driver_options(is_wx=read_ini_file("environment", "is_wx")))
        driver.maximize_window()
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        return driver

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def open_url(self, url: Text) -> None:
        """
        打开url网址
        :param url: 网址
        :return: None
        """
        self.driver.get(url)

    def __wait_visible(self, locator: Tuple[Text, Text]) -> None:
        """
        等待元素可见
        :param locator: 元素定位路径
        :return: None
        """
        self.wait.until(EC.visibility_of_element_located(locator))

    def get_element(self, by: Text, value: Text) -> WebElement:
        """
        获取网页元素
        :param by: 定位方式
        :param value: 元素路径
        :return:
        """
        selector_map = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR
        }
        try:
            locator = (selector_map[by], value)  # 元素定位表达式
            self.__wait_visible(locator)    # 等待元素可见
            element = self.driver.find_element(*locator)    # 获取元素
            return element
        except NoSuchElementException:
            log.error(f"Element not found by {by}: {value}")

    def get_elements(self, by: Text, value: Text) -> List[WebElement]:
        """
        获取网页一组元素
        :param by: 定位方式
        :param value: 元素路径
        :return: 返回一组的元素
        """
        selector_map = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR
        }
        try:
            locator = (selector_map[by], value)  # 元素定位表达式
            self.__wait_visible(locator)    # 等待元素可见
            elements = self.driver.find_elements(*locator)    # 获取元素
            return elements
        except NoSuchElementException:
            log.error(f"Element not found by {by}: {value}")

    def click(self, by: Text, value: Text) -> None:
        """
        点击元素
        :param by: 定位方式
        :param value: 元素路径
        :return: None
        """
        element = self.get_element(by, value)
        element.click()

    def fillIn(self, by: Text, value: Text, text: Any) -> None:
        """
        输入文本内容
        :param by: 定位方式
        :param value: 元素路径
        :param text: 输入的文本
        :return: None
        """
        element = self.get_element(by, value)
        element.send_keys(text)

    def executeJsScript(self, script: Text) -> None:
        """
        执行js脚本
        :param script: 脚本内容
        :return: None
        """
        self.driver.execute_script(script)

    def getAttribute(self, by: Text, value: Text, attribute: Text) -> Text:
        """
        获取元素属性值
        :param by: 定位方式
        :param value: 元素路径
        :param attribute: 属性名称
        :return: 属性值
        """
        element = self.get_element(by, value)
        return element.get_attribute(attribute)

    def get_url(self) -> Text:
        """
        获取当前网址
        :return: 网址内容
        """
        return self.driver.current_url

    def upload_file(self, by: Text, value: Text, file_path: Text) -> None:
        """
        上传文件
        :param by: 定位方式
        :param value: 元素路径
        :param file_path: 文件路径
        :return: None
        """
        element = self.get_element(by, value)
        element.send_keys(file_path)
