import requests
import random
import pandas as pd
from lxml import etree
import time
import threading, queue
import datetime
import re


class Lian:
    def __init__(self):
        self.cate_info = []
        self.all_info = []
        self.cate_error = []
        self.detail_error = []

        self.repair_queue = queue.Queue()
        self.size_queue = queue.Queue()
        self.id_page_queue = queue.Queue()

        self.head_user_agent = [
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
            'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
            'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
            'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
        ]
        self.url_base = 'http://www.vanlinkon.com/'
        self.detail_base = 'http://www.vanlinkon.com/search?title='

        self.row_headers = {
            'User-Agent': random.choice(self.head_user_agent),
            #         'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            # 'Host': 'www.vanlinkon.com',
            'upgrade-insecure-requests': '1',
        }
        self.s = requests.Session()
        self.s.proxies = {
            # "http": "http://121.237.148.110:3000",
            "https": "HTTPS://117.88.4.124:3000",
        }

    def get_ip_test(self):
        ip_test_url = 'http://www.ip-api.com/json'
        res = self.s.get(ip_test_url, headers=self.row_headers, verify=False)
        print(res.json())

    def get_category(self, category, page):
        self.s.headers.update(self.row_headers)
        url_cate = self.url_base + 'category/' + str(category) + '?per_page='
        try:
            print('page:', page)
            res = self.s.get(url=url_cate + str(page), timeout=30, verify=False)
        except Exception as e:
            print(e)
            self.cate_error.append([category, page])
            print(page)
            return

        print('类目：', category, res.status_code)
        res_row_html = etree.HTML(res.text)
        each_body = res_row_html.xpath("//div[@class='col-xs-6 col-mo-4']")
        for each in each_body:
            try:
                product_manufacturer = each.xpath(".//h6[@class='product-manufacturer']/a/text()")[0].strip()
                print(product_manufacturer.strip())
                # 加入商品型号id表格
                self.cate_info.append(product_manufacturer)
            except Exception as e:
                print(e)
                pass

    def get_detail(self, manufacturer):
        try:
            res = self.s.get(url=self.detail_base + manufacturer, timeout=30)
        except Exception as e:
            print(e)
            self.detail_error.append(manufacturer)
            print(manufacturer)
            return

        print('型号', manufacturer, res.status_code)
        res_row_html = etree.HTML(res.text)
        each_body = res_row_html.xpath("//tr[@class='single-product']")
        for each in each_body:
            try:
                brand = each.xpath(".//td[2]/text()")[0]
            except:
                brand = None

            try:
                size = each.xpath(".//td[3]/text()")[0]
            except:
                size = None

            try:
                stock = each.xpath(".//td[4]/text()")[0]
                stock = int(stock.replace(',',''))
            except:
                stock = None

            try:
                min_shop = each.xpath(".//td[5]/text()")[0]
            except:
                min_shop = None

            try:
                min_package = each.xpath(".//td[6]/text()")[0]
                min_package = int(min_package.replace(',', ''))
            except:
                min_package = None

            try:
                price_all = each.xpath("string(.//ul[@class='list-unstyled'])")
                price_all = re.sub('[  ]+', '', price_all).strip().split('\n')
            except:
                price_all = None
            each_list = [brand, size, stock, min_shop, min_package, price_all]
            print(each_list)
            self.all_info.append(each_list)

    #  多线程获取某类目的商品型号id
    def get_id_thread(self, category, start_page, end_page):

        for each in range(start_page, end_page+1):
            self.id_page_queue.put((category, each))

        while True:
            try:
                thread_list = [threading.Thread(target=self.get_category, args=(self.id_page_queue.get()))
                               for i in range(20) if not self.id_page_queue.empty()]
                for each in thread_list:
                    self.s.headers.update({'User-Agent': random.choice(self.head_user_agent)})
                    try:
                        time.sleep(random.random())
                        each.start()
                        print('thread_name', each.name)
                    except Exception as e:
                        print(e)

                for each in thread_list:
                    each.join()

            except Exception as e:
                print(e)

            # 页面队列完成时 退出
            if self.id_page_queue.empty():
                break

        aft = datetime.datetime.now().strftime('%m_%d_')
        file_name = './data/new/商品型号列表' + aft + str(category) + '_' + str(start_page or 'str') + '_' \
                    + str(end_page or 'end') + '.xlsx'
        pd.DataFrame(self.cate_info).to_excel(file_name, index=None)
        if self.cate_error:
            pd.DataFrame(self.cate_error).to_excel(file_name.replace('商品型号', '遗漏页面'))

    #  多线程获取商品详情，
    def get_detail_thread(self, file_path, start_page, end_page):

        df = pd.read_excel(file_path)
        for each in df['型号'][start_page: end_page+1]:
            self.size_queue.put(each)
        time.sleep(2)

        while True:
            try:
                thread_list = [threading.Thread(target=self.get_detail, args=(self.size_queue.get(),))
                               for i in range(20) if not self.size_queue.empty()]
                for each in thread_list:
                    self.s.headers.update({'User-Agent': random.choice(self.head_user_agent)})
                    try:
                        time.sleep(random.random())
                        each.start()
                        print('thread_name:', each.name)
                    except Exception as e:
                        print(e)

                for each in thread_list:
                    each.join()

            except Exception as e:
                print(e)

            if self.size_queue.empty():
                break

        aft = datetime.datetime.now().strftime('%m_%d_')
        file_name = './data/商品详情' + aft + str(start_page) + '_' + str(end_page) + '.xlsx'
        pd.DataFrame(self.all_info).to_excel(file_name,
                                             index=None)
                                             # columns=['品牌', '型号', '库存', '最小起订', '最小包装', '区间价格'])
        if self.detail_error:
            pd.DataFrame(self.detail_error).to_excel(file_name.replace('商品详情', '商品详情遗漏型号'))

    def get_repair(self, file_path):
        data = pd.read_excel(file_path)

        for cate, page in zip(data['品牌代码'], data['页面']):
            print(int(cate), page)
            self.repair_queue.put((int(cate), page))

        time.sleep(2)
        while True:
            try:
                thread_list = [threading.Thread(target=self.get_category, args=(self.repair_queue.get()))
                               for i in range(20) if not self.repair_queue.empty()]
                for each in thread_list:
                    self.s.headers.update({'User-Agent': random.choice(self.head_user_agent)})
                    try:
                        time.sleep(random.random())
                        each.start()
                        print('thread_name', each.name)
                    except Exception as e:
                        print(e)

                for each in thread_list:
                    each.join()

                time.sleep(5)

            except Exception as e:
                print(e)

            # 页面队列完成时 退出
            if self.repair_queue.empty():
                break

        aft = datetime.datetime.now().strftime('%m_%d_%H_%M')
        file_name = './data/商品型号获取_repair' + aft + '_.xlsx'
        pd.DataFrame(self.cate_info).to_excel(file_name)


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    lian = Lian()

    # 0, ip测试
    lian.get_ip_test()
    # 1, 获取给个品牌的产品id
    # lian.get_id_thread(category=3, start_page=1, end_page=20)

    # 2, 获取部分没得到的页面
    # lian.get_repair(file_path=r'F:\DEDE\lian\data\new\连可连_TE_遗漏汇总.xlsx')

    # 3, 获取商品详情，遗漏部分更改路径即可
    # lian.get_detail_thread(file_path=r'data/new/品牌汇总/连可连_molex_品牌型号.xlsx', start_page=2, end_page=3)
    t2 = datetime.datetime.now()

    print('运行时间: {}秒,'.format((t2 - t1).seconds))
