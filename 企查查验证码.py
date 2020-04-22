
from selenium import webdriver
import numpy
import pandas as pd
import time, random, re
# from selenium.webdriver.support.ui import Select  # 下拉框
# from selenium.webdriver.common.keys import Keys   # 键盘操作

import datetime
import threading
import queue
from lxml import etree

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options

def is_visible(driver, locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

# 一直等待某个元素消失，默认超时10秒
def is_not_visible(driver, locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

qcc_row = 'https://qcc.com'

chrome_opt = webdriver.ChromeOptions()
    # chrome_opt = Options()
chrome_opt.add_argument('-–start-maximized')  # 最大化 响应式网站不最大化 某些元素不展示
chrome_opt.add_argument('--no-sandbox')  # 非沙盒启动
# chrome_opt.add_argument('--incognito')  # 无缓存
# chrome_opt.add_argument('--headless ')  # 无头

prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
chrome_opt.add_experimental_option("prefs", prefs)
# chrome_opt.add_argument('--headless')  # 无头模式
driver = webdriver.Chrome(executable_path='chromdriver.exe', chrome_options=chrome_opt)
driver.maximize_window()


#

driver.get(qcc_row)

if is_visible(driver, "//a[@class='navi-btn']"):
    driver.find_element_by_xpath("//a[@class='navi-btn']").click()

time.sleep(random.random)

if is_visible(driver, "")