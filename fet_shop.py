from selenium import webdriver
import numpy
import pandas as pd
import time, random, re
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
# import datetime
import threading
import queue

info_list_page = []


def get_id(str_page, end_page):
    info_list = []
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)
    # chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_opt)
    url_base = "https://order.jst-mfg.com/InternetShop/app/index.php?search_product=&select=a&page="

    for each in range(str_page, end_page):
        url = url_base + str(each) + '#showProductList'
        print(url)
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        if not driver.find_element_by_xpath("//hr[@class='p_line']"):
            print('{}未请求到页面，重新尝试'.format(url))
            driver.get(url)
        if not driver.find_elements_by_xpath("//button[@class='btn btn-link product_code_link']"):
            row_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

            print('{}未请求到表格数据，重新尝试'.format(url))
            print(row_html)
            driver.get(url)
        else:
            goods_ids = driver.find_elements_by_xpath("//button[@class='btn btn-link product_code_link']")
            goods_id_set = set(goods_ids)
            info_list.extend(i.get_attribute('value') or 'none' for i in goods_id_set)
            print(info_list)

    return info_list


def get_id_each(page):

    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)
    # chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_opt)
    url_base = "https://order.jst-mfg.com/InternetShop/app/index.php?search_product=&select=a&page="

    url = url_base + str(page) + '#showProductList'
    print(url)
    driver.get(url)
    time.sleep(random.uniform(3, 5))
    # if not driver.find_element_by_xpath("//hr[@class='p_line']"):
    #     print('{}未请求到页面，重新尝试'.format(url))
    #     driver.get(url)
    if not driver.find_elements_by_xpath("//button[@class='btn btn-link product_code_link']"):
        row_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

        print('{}未请求到表格数据，重新尝试'.format(url))
        print(row_html)
        driver.refresh()
    else:
        goods_ids = driver.find_elements_by_xpath("//button[@class='btn btn-link product_code_link']")
        goods_id_set = set(goods_ids)
        info_list_page.extend(i.get_attribute('value') or 'none' for i in goods_id_set)
        print(info_list_page)

    driver.quit()
    return info_list_page


def get_info_each(id):
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)
    # chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_opt)
    url_base = "https://order.jst-mfg.com/InternetShop/app/index.php?product="

    url = url_base + str(id) + '##showProductDetail'
    print(url)
    driver.get(url)
    time.sleep(random.uniform(3, 5))



def main(str_page=40, end_page=100):
    all_info = []
    for i in range(str_page, end_page, 5):
        info_list = get_id(i, i+5)
        all_info.extend(info_list)
    file_name = './info_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(all_info).to_excel(file_name)
    print(all_info)


def thread_main(str_page=150, end_page=170):
    page_queue = queue.Queue()
    for each in range(str_page, end_page):
        page_queue.put(each)

    while True:
        thread_list = [threading.Thread(target=get_id_each, args=(page_queue.get(),))
                       for i in range(18) if not page_queue.empty()]

        for each in thread_list:
            each.start()

        for each in thread_list:
            each.join()

        if page_queue.empty():
            break

    file_name = './info_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_page).to_excel(file_name)


if __name__ == '__main__':
    # main(150, 180)
    thread_main(600, 700)
