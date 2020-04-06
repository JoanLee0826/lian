import requests
import random
import pandas as pd
from lxml import etree
import time
import threading, queue


class GoodDetail:
    def __init__(self):
        self.all_info = []
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
        self.url_base = 'http://erp.jst-e.com/qjdzd/top_utl.page_show?p_pk_no=1010&p1=&p2='

        self.row_headers = {
            'User-Agent': random.choice(self.head_user_agent),
            #         'sec-fetch-dest': 'document',
            #         'sec-fetch-mode': 'navigate',
            #         'sec-fetch-site': 'same-origin',
            #         'sec-fetch-user': '?1',
            'Host': 'erp.jst-e.com',
            'upgrade-insecure-requests': '1',
        }
        self.s = requests.Session()

    def get_detail(self, page):
        # print(self.s)
        self.s.headers.update(self.row_headers)

        res = self.s.get(url=self.url_base + str(page), timeout=20)
        print(page, res.status_code)
        res_row_html = etree.HTML(res.text)
        tbody = res_row_html.xpath('//tbody/tr')
        for each in tbody:
            try:
                style = each.xpath('./td/a/text()')[0]
            except :
                style = None

            try:
                a = each.xpath('./td[2]/text()')[0]
            except:
                a = None
            try:
                b = each.xpath('./td[3]/text()')[0]
            except:
                b = None

            try:
                c = each.xpath('./td[4]/text()')[0]
            except:
                c = None
            try:

                d = each.xpath('./td[5]/text()')[0]
            except:
                d = None

            each_info = [style, a, b, c, d]
            self.all_info.append(each_info)

    def run(self, start_page, end_page):

        for i in range(start_page, end_page):
            self.get_detail(i)
            time.sleep(random.random())

        time.sleep(5)
        df = pd.DataFrame(self.all_info, columns=['型号', '最小包装', '整箱包装', '价格', '库存'])
        df.to_excel('./info_1000_1069.xlsx', index=None)


if __name__ == '__main__':
    qj = GoodDetail()
    qj.run(1000, 1069)




