import requests
import random
import pandas as pd
from lxml import etree
import time
import threading, queue


class Lian:
    def __init__(self):
        self.all_info = []
        self.size_queue = queue.Queue()
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
        self.url_base = 'https://www.vanlinkon.com/'
        self.detail_base = 'https://www.vanlinkon.com/search?title='

        self.row_headers = {
            'User-Agent': random.choice(self.head_user_agent),
            #         'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'Host': 'www.vanlinkon.com',
            'upgrade-insecure-requests': '1',
        }
        self.s = requests.Session()

    def get_category(self, category, start_page, end_page):
        self.s.headers.update(self.row_headers)
        url_cate = self.url_base + 'category/' + str(category) + '?per_page='
        for i in range(start_page, end_page+1):
            time.sleep(random.random())
            self.s.headers.update(self.row_headers)
            res = self.s.get(url=url_cate + str(start_page), timeout=20)
            print(category, res.status_code)
            res_row_html = etree.HTML(res.text)
            each_body = res_row_html.xpath("//div[@class='col-xs-6 col-mo-4']")
            for each in each_body:
                product_manufacturer = each.xpath(".//h6[@class='product-manufacturer']/a/text()")
                self.size_queue.put(product_manufacturer)

    def get_detail(self, manufacturer):

        res = self.s.get(url=self.detail_base + manufacturer, timeout=20)
        print(manufacturer, res.status_code)
        res_row_html = etree.HTML(res.text)
        each_body = res_row_html.xpath("//tr[@class='single-product']")
        for each in each_body:
            brand = each.xpath(".//td[2]/text()")
            size = each.xpath(".//td[3]/text()")
            stock = each.xpath(".//td[4]/text()")
            min_shop = each.xpath(".//td[5]/text()")
            min_package = each.xpath(".//td[6]/text()")
            price_all = each.xpath("string(.//ul[@class='list-unstyled'])")
            each_list = [brand, size, stock, min_shop, min_package, price_all]
            self.all_info.append(each_list)

    def run(self, category, start_page=1, end_page=20):
        self.get_category(category=category, start_page=start_page, end_page=end_page)
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
                        print(each.name)
                    except Exception as e:
                        print(e)

                for each in thread_list:
                    each.join()

            except Exception as e:
                print(e)

            if self.size_queue.empty():
                break

