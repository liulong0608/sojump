# == Coding: UTF-8 ==
# @Project :        sojump
# @fileName         base_page.py  
# @version          bate1.2.3
# @author           LIULONG
# @GiteeWarehouse   https://gitee.com/liu-long068/
# @WritingTime      2023/10/21 23:17
# @Software:        PyCharm
# ====/******/=====
import random
import time
from typing import Text, Tuple, List, Any

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.globalparam import CHROMEDRIVER_PATH, linear_config_path, log_path
from src.utils.logurus import LoguruLogger
from src.utils.read_config import read_ini_file
from src.utils.driver_options import driver_options

log = LoguruLogger(log_file_path=log_path, stream=False).get_logger()


class BasePage:

    def __init__(self, x_axi=None, y_axi=None):
        self.driver = self.new_driver(x_axi, y_axi)
        self.wait: WebDriverWait = WebDriverWait(self.driver, timeout=20, poll_frequency=0.8)

    @staticmethod
    def new_driver(x_axi, y_axi) -> WebDriver:
        service = Service(CHROMEDRIVER_PATH)
        wx = read_ini_file("environment", "USE_WX", file_path=linear_config_path)
        proxy = read_ini_file("proxy", "USE_IP_PROXY", file_path=linear_config_path)
        driver = webdriver.Chrome(service=service,
                                  options=driver_options(wx, proxy))
        if x_axi is None and y_axi is None:
            driver.maximize_window()
        else:
            driver.set_window_size(970, 1440)
            driver.set_window_position(x_axi, y_axi)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        return driver

    def clear_cookies(self) -> None:
        """
        清除Selenium中的cookie
        """
        CLEAR_COOKIES = r"""
        function clearCookie() {
                var keys = document.cookie.match(/[^ =;]+(?=\=)/g);
                if (keys) {
                    for (var i = keys.length; i--;) {
                        document.cookie = keys[i] + '=0;path=/;expires=' + new Date(0).toUTCString();
                        document.cookie = keys[i] + '=0;path=/;domain=' + document.domain + ';expires=' + new Date(0).toUTCString();
                        document.cookie = keys[i] + '=0;path=/;domain=kevis.com;expires=' + new Date(0).toUTCString();
                    }
                }
            }
        clearCookie();
        """
        self.driver.execute_script(CLEAR_COOKIES)

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
            "css": By.CSS_SELECTOR,
            "tag": By.TAG_NAME
        }
        try:
            locator = (selector_map[by], value)  # 元素定位表达式
            self.__wait_visible(locator)  # 等待元素可见
            element = self.driver.find_element(*locator)  # 获取元素
            return element
        except NoSuchElementException:
            log.error(f"Element not found by {by}: {value}")
        except TimeoutException:
            log.error(f"Elment finding timeout by {by}: {value}")

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
            self.__wait_visible(locator)  # 等待元素可见
            elements = self.driver.find_elements(*locator)  # 获取元素
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

    def fillIn(self, by: Text, value: Text | WebElement, text: Any) -> None:
        """
        输入文本内容
        :param by: 定位方式
        :param value: 元素路径
        :param text: 输入的文本
        :return: None
        """
        element = self.get_element(by, value)
        element.send_keys(text)

    def switch_to_frame(self, by: Text, value: Text) -> None:
        """
        切换到iframe
        :param by: 定位方式
        :param value: 元素路径
        :return: None
        """
        element = self.get_element(by, value)
        self.driver.switch_to.frame(element)

    def switch_to_default_content(self) -> None:
        """
        切换到默认iframe
        :return: None
        """
        self.driver.switch_to.default_content()

    def executeJsScript(self, script: Text, args: Any) -> None:
        """
        执行js脚本
        :param script: 脚本内容
        :param args: 执行脚本的参数
        :return: None
        """
        self.driver.execute_script(script, args)

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

    def get_textContent(self, by: Text, value: Text) -> Text:
        """
        获取元素文本内容
        :param by: 定位方式
        :param value: 元素路径
        :return: 文本内容
        """
        try:
            element = self.get_element(by, value)
            return element.text
        except AttributeError:
            return ""

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

    def select_option(self, select_element: WebElement, options_list: List[Text]) -> None:
        """
        选择元素
        :param select_element: 元素
        :param options_list: 选项列表
        :return: None
        """
        try:
            locator = (By.CSS_SELECTOR, 'option')
            self.__wait_visible(locator)
            options = [option.text for option in select_element.find_elements(By.CSS_SELECTOR, 'option')]
            if len(options) > 0:
                options.pop(0)  # 排除第一个
                selected_option = random.choice(options)
                self.executeJsScript(f"arguments[0].value='{selected_option}';", select_element)
                self.executeJsScript("arguments[0].dispatchEvent(new Event('change'));", select_element)
            else:
                log.error("No options found in select element")
                return
        except IndexError:
            log.error("No options found in select element")
        except Exception as e:
            log.error(f"Error selecting random option: {e}")

    def drag_element_horizontally(self, element: WebElement, x: int) -> None:
        """
        拖动元素
        :param element: 元素
        :param x: 拖动的距离
        :return: None
        """
        ActionChains(self.driver).drag_and_drop_by_offset(element, x, 0).perform()

    def verify(self):
        """ 处理验证函数 """
        try:
            # 出现点击验证码验证
            time.sleep(1)
            try:
                # 点击对话框的确认按钮
                self.driver.find_element(By.XPATH, '.layui-layer.layui-layer-dialog div a').click()
                time.sleep(1)
                # 点击智能检测按钮
                self.driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
            except:
                # 点击智能检测按钮
                self.driver.find_element(By.CSS_SELECTOR, '#rectMask').click()
                # self.click("css", "#rectMask")
            time.sleep(3)
        except:
            log.info("无验证")
            # 滑块验证
        try:
            slider = self.driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
            if str(slider.text).startswith("请按住滑块"):
                width = slider.size.get('width')
                ActionChains(self.driver).drag_and_drop_by_offset(slider, width, 0).perform()
        except:
            pass
