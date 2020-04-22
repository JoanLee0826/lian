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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

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

info_list_page = []
info_list_detail = []

def get_id(str_page, end_page):
    info_list = []
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('--no-sandbox')
    chrome_opt.add_argument('--incognito')   # 无缓存
    chrome_opt.add_argument('--headless ')  # 无头
    chrome_opt.add_argument('--disable-dev-shm-usage') # 设置代理服务器
    chrome_opt.add_argument('--proxy-server=https://117.88.4.124:3000')  #
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
    driver.set_page_load_timeout(20)
    url_base = "https://order.jst-mfg.com/InternetShop/app/index.php?product="

    url = url_base + str(id) + '#showProductDetail'
    print(url)
    driver.get(url)
    time.sleep(random.uniform(5, 7))
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


def id_thread_main(str_page=150, end_page=170):
    page_queue = queue.Queue()
    for each in range(str_page, end_page):
        page_queue.put(each)

    while True:
        thread_list = [threading.Thread(target=get_id_each, args=(page_queue.get(),))
                       for i in range(18) if not page_queue.empty()]

        for each in thread_list:
            each.start()
            time.sleep(random.random())

        for each in thread_list:
            each.join()

        if page_queue.empty():
            break

    file_name = './info_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_page).to_excel(file_name, engine='xlsxwriter')


def info_thread_main(str_page, end_page):
    info_page_queue = queue.Queue()
    id_df_all = pd.read_excel(r'all_id.xlsx')
    id_df_clean = pd.read_excel(r'jst_shop_clean.xlsx')
    id_list = id_df_all[-id_df_all['id'].isin(id_df_clean['id'])]['id']
    print(len(id_list))
    # for each in id_df['id'][str_page:end_page]:
    for each in id_list:
        info_page_queue.put(each)

    while True:
        thread_list = [threading.Thread(target=get_info_each, args=(info_page_queue.get(),))
                       for i in range(10) if not info_page_queue.empty()]

        for each in thread_list:
            each.start()

        for each in thread_list:
            each.join()

        if info_page_queue.empty():
            break

    file_name = './detail_list_' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_detail).to_excel(file_name, engine='xlsxwriter')


def get_dj_detail(keywords):
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('-–start-maximized')
    chrome_opt.add_argument('--no-sandbox')
    chrome_opt.add_argument('disable-popup-blocking')
    chrome_opt.add_argument('--incognito')   # 无缓存
    # chrome_opt.add_argument('--headless ')  # 无头
    chrome_opt.add_argument('--disable-dev-shm-usage')  # 设置代理服务器
    # chrome_opt.add_argument('--proxy-server=https://114.223.103.47:8118')  #
    prefs = {"profile.managed_default_content_settings.images": 2}  # 关闭图片，响应更快
    chrome_opt.add_experimental_option("prefs", prefs)

    # chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_opt)
    driver.maximize_window()
    driver.get('http://www.digikey.cn/')
    # time.sleep(300)

    # cookie 界面验证
    res_html_row = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    # print(res_html_row)

    # if is_visible(driver, "//div[@class='cookie-notice']//a[@class='secondary button']"):
    #     driver.find_element("//div[@class='cookie-notice']//a[@class='secondary button']").click()

    url = 'http://www.digikey.cn/products/zh?WT.z_header=search_go&keywords=' + keywords
    driver.get(url)
    # time.sleep(random.random())
    res_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    if is_visible(driver, "//tr[@class='exactPart']/td/a"):
        url = driver.find_element_by_xpath("//tr[@class='exactPart']/td/a").get_property('href')
        driver.get(url)
        # time.sleep(random.random())
        res_html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

    elif is_visible(driver, "//a[@id='digikeyPartNumberLnk']"):
        url_list = driver.find_elements_by_xpath("//a[@id='digikeyPartNumberLnk']")
        a_href_list = []
        for url in url_list:
            a_href = url.get_property('href')
            a_href_list.append(a_href)

        info_list_detail.append([keywords, a_href_list])
        print(info_list_detail[-1])
        driver.quit()
        return

    res_html_xpath = etree.HTML(res_html)
    # time.sleep(2)
    each_tr = res_html_xpath.xpath("//table[@class='product-details']/tbody/tr")
    goods_info = {}
    price_info = []
    for each in each_tr:
        try:
            each_key = each.xpath('string(./th)')
            each_key = re.sub('\n+|\t+', '', each_key)
            each_value = each.xpath('string(./td)')
            each_value = re.sub('\n+|\t+', '', each_value)
            goods_info[each_key] = each_value
        except:
            pass
    price_tr = res_html_xpath.xpath("//table[@id='pricing']//tr")
    for each_price in price_tr:
        try:
            each_price_info = each_price.xpath("string(.)")
            each_price_info = re.sub('\n+|\t+', ' ', each_price_info)
        except:
            each_price_info = None
        price_info.append(each_price_info)
    info_list_detail.append([keywords, goods_info, price_info])
    print(info_list_detail[-1])
    driver.quit()


def get_dj_thread(str_page, end_page):
    dj_queue = queue.Queue()
    df = pd.read_excel(r'新品资料搜集2492款-采购二部4.20.xlsx')
    for each in df['型号'][str_page: end_page]:
        dj_queue.put(str(each))

    while True:
        thread_list = [threading.Thread(target=get_dj_detail, args=(dj_queue.get(),))
                       for i in range(6) if not dj_queue.empty()]

        for each in thread_list:
            each.start()
            print(each.name)

        for each in thread_list:
            each.join()

        if dj_queue.empty():
            break

    file_name = './dj_detail' + str(str_page) + "_" + str(end_page) + '.xlsx'
    pd.DataFrame(info_list_detail).to_excel(file_name, engine='xlsxwriter')


if __name__ == '__main__':

    t1 = datetime.datetime.now()

    # get_dj_thread(str_page=630, end_page=700)
    # time.sleep(10)
    # get_dj_thread(str_page=700, end_page=800)
    # get_dj_thread(str_page=1200, end_page=1300)
    get_dj_thread(str_page=2000, end_page=2492)
    t2 = datetime.datetime.now()

    print((t2 - t1).seconds)

