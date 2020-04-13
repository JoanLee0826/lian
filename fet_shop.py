from selenium import webdriver
import numpy
import pandas as pd
import time, random, re
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
import datetime
import threading
import queue
from lxml import etree

info_list_page = []
info_list_detail = []

def get_id(str_page, end_page):
    info_list = []
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('--no-sandbox')
    chrome_opt.add_argument('--incognito')   # 无缓存
    chrome_opt.add_argument('--headless ')  # 无头
    chrome_opt.add_argument('--disable-dev-shm-usage')
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
    chrome_opt.add_argument('--incognito')  # 无缓存
    chrome_opt.add_argument('--headless ')  # 无头
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
    info_each_list = [id]
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('--incognito')  # 无缓存
    chrome_opt.add_argument('--headless ')  # 无头
    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)
    # chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_opt)
    url_base = "https://order.jst-mfg.com/InternetShop/app/index.php?product="

    url = url_base + str(id) + '#showProductDetail'
    print(url)
    driver.get(url)
    time.sleep(random.uniform(1, 2))
    if not driver.find_elements_by_xpath("//div[@class='col-md-12']"):
        row_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

        print('{}未请求到表格数据，重新尝试'.format(url))
        print(row_html)
        driver.refresh()
    else:
        goods_sku = driver.find_element_by_xpath("//div[@class='col-md-12']").text
        try:
            goods_pdf = driver.find_element_by_xpath("//a[@class='link001']").get_attribute('href')
        except:
            goods_pdf = None
        goods_status = driver.find_element_by_xpath("//div[@class='t_align_r']").text
        price_items = {}
        detail_items = {}
        row_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        etree_html = etree.HTML(row_html)
        for each in etree_html.xpath("//table[@class='tanka_tbl_cb']//tr"):
            # print(each)
            keys = each.xpath('./td[1]/text()')
            values = each.xpath('./td[2]/text()')
            try:
                price_items[keys[0]] = values[0]
            except:
                print(keys, keys, values)
        # print('price:', price_items)
        for each in etree_html.xpath("//table[@class='detail_tbl_cb']//tr"):
            keys = each.xpath("./th/text()")
            values = each.xpath("./td/text()")
            try:
                detail_items[keys[0]] = values[0]
            except:
                print(keys, values)
        # print('detail:', detail_items)
        info_each_list = [id, goods_sku, goods_pdf, goods_status, price_items, detail_items]
        print(info_each_list)
        info_list_detail.append(info_each_list)
    driver.quit()
    return info_each_list


def main(str_page=40, end_page=100):
    all_info = []
    for i in range(str_page, end_page, 5):
        info_list = get_id(i, i+5)
        all_info.extend(info_list)
    file_name = './info_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(all_info).to_excel(file_name)
    print(all_info)


def id_thread_main(str_page=150, end_page=170):
    page_queue = queue.Queue()
    for each in range(str_page, end_page):
        page_queue.put(each)

    while True:
        thread_list = [threading.Thread(target=get_id_each, args=(page_queue.get(),))
                       for i in range(15) if not page_queue.empty()]

        for each in thread_list:
            each.start()

        for each in thread_list:
            each.join()

        if page_queue.empty():
            break

    file_name = './info_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_page).to_excel(file_name, engine='xlsxwriter')


def info_thread_main(str_page, end_page):
    info_page_queue = queue.Queue()
    id_df = pd.read_excel(r'F:\DEDE\lian\all_id.xlsx')

    for each in id_df['id'][str_page:end_page]:
        info_page_queue.put(each)

    while True:
        thread_list = [threading.Thread(target=get_info_each, args=(info_page_queue.get(),))
                       for i in range(15) if not info_page_queue.empty()]

        for each in thread_list:
            each.start()

        for each in thread_list:
            each.join()

        if info_page_queue.empty():
            break

    file_name = './detail_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_detail).to_excel(file_name, engine='xlsxwriter')


if __name__ == '__main__':

    t1 = datetime.datetime.now()
    info_thread_main(1000, 1050)
    t2 = datetime.datetime.now()
    print((t2 - t1).seconds)
    # main(150, 180)
    # id_thread_main(200, 220)
