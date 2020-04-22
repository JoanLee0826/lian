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


# 一直等待某元素可见，默认超时10秒
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

# 初始化
all_info = []

def get_driver(driver_path):
    chrome_opt = webdriver.ChromeOptions()
    # chrome_opt = Options()
    chrome_opt.add_argument('-–start-maximized')  # 最大化 响应式网站不最大化 某些元素不展示
    chrome_opt.add_argument('--no-sandbox')  # 非沙盒启动
    chrome_opt.add_argument('--incognito')  # 无缓存
    # chrome_opt.add_argument('--headless ')  # 无头

    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)
    # chrome_opt.add_argument('--headless')  # 无头模式
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_opt)
    driver.maximize_window()
    return driver


def get_html(key_words):
    driver = get_driver('chromedriver.exe')
    driver.maximize_window()
    driver.get('https://www.qcc.com/')
    time.sleep(random.uniform(1, 2))
    url = 'https://www.qcc.com/search?key=' + key_words.replace(' ', '+')
    print(url)
    driver.get(url)
    time.sleep(random.uniform(2, 3))

    if is_visible(driver, "//table[@class='m_srchList']/tbody"):

        info_tbody = driver.find_elements_by_xpath("//table[@class='m_srchList']/tbody/tr")
        for each in info_tbody:
            p_text = []
            try:
                title = each.find_element_by_xpath("./td/a[@class='ma_h1']").get_property()
            except:
                title = None
            p_text_ele = each.find_elements_by_xpath("./td/p")

            for each in p_text_ele:
                try:
                    print(each.text)
                    p_text.append(each.text)
                except:
                    pass
            try:
                status = each.find_element_by_xpath("./td[@class='statustd']/span").text
            except:
                status = None

            try:
                com_id = each.find_element_by_xpath("./td[@class='statustd']/a").get_property('data-keyno')
            except:
                com_id = None

            each_list= [key_words, title, p_text, status, com_id]
            all_info.append([each_list])
            print(all_info[-1])

    else:
        all_info.append([key_words, 'None'])
        print(all_info[-1])
    driver.quit()


def qcc_main(start_cot, end_cot):
    # driver = get_driver(driver_path='chromedriver.exe')
    page_queue = queue.Queue()
    key_words_df = pd.read_excel(r'F:\DEDE\clean\output\中国地区查找.xlsx')
    for each in key_words_df['sea_com'][start_cot: end_cot]:
        # page_queue.put(each)
        get_html(each)

    # while True:
    #     thread_list = [threading.Thread(target=get_html, args=(page_queue.get(),))
    #                    for i in range(5) if not page_queue.empty()]
    #
    #     for each in thread_list:
    #         each.start()
    #         time.sleep(random.random())
    #
    #     for each in thread_list:
    #         each.join()
    #
    #     if page_queue.empty():
    #         break

    file_name = './com_info_list_' + str(start_cot) + "_" + str(end_cot) + '.xlsx'
    pd.DataFrame(all_info).to_excel(file_name, engine='xlsxwriter')


if __name__ == '__main__':
    qcc_main(20, 30)
