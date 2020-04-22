import requests
import pandas as pd
import numpy as np
import random
from lxml import etree
import time
import datetime

normal_user_agent = [
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
ip_get_url = 'https://www.xicidaili.com/wn/'
s = requests.Session()

row_headers = {
    'User-Agent': random.choice(normal_user_agent),
}

res = s.get(ip_get_url, headers=row_headers)
print(res.status_code)
res_html = etree.HTML(res.text)
all_list = []

print(res_html)
for each in res_html.xpath('//table[@id="ip_list"]//tr'):
    each_ip = each.xpath('./td[2]/text()')
    each_port = each.xpath('./td[3]/text()')
    each_city = each.xpath('./td[4]/a/text()')
    each_hide = each.xpath('./td[5]/text()')
    each_http = each.xpath('./td[6]/text()')
    each_speed = each.xpath('./td[7]/div/@title')
    each_con = each.xpath('./td[8]/div/@title')
    each_live = each.xpath('./td[9]/text()')
    each_time = each.xpath('./td[10]/text()')

    each_list = [each_ip, each_port, each_city, each_hide, each_http,
                 each_speed, each_con, each_live, each_time]
    print(each_list)
    all_list.append(each_list)

df = pd.DataFrame(all_list)

def get_first(x):
    try:
        s = x[0]
    except:
        s = None
    return s

for each in df.columns:
    df[each] = df[each].map(get_first)

df.columns = ['ip', 'port', 'city', 'hide', 'http', 'speed', 'con', 'live', 'time']
df.dropna(subset=['ip','port'], inplace=True)
df['speed'] = df['speed'].str.strip('秒')
df['con'] = df['con'].str.strip('秒')
df['proxies'] = df['http'] + '://' + df['ip'] + ':' + df['port']

aft = datetime.datetime.now().strftime('%m_%d_%H_%M')
file_name = './ip_list/ip_list_wn' + aft + '.xlsx'
df.to_excel(file_name, index=False)