import requests
from hashlib import md5
import datetime
import json
import xlwt

secretKey="17711607-3619-432d-aaf8-aa0f0106dadb"
hl = md5()
hl.update((secretKey + datetime.datetime.now().strftime('%Y%m%d')).encode(encoding='utf-8'))
myProductSecretKey = hl.hexdigest().upper()
#response=requests.get("http://127.0.0.1:7878/queryProductStock?store=01&authcode="+myProductSecretKey)
response=requests.get("http://106.15.224.141:7878/queryProductStock?store=04&authcode="+myProductSecretKey)   #全量
#response=requests.get("http://106.15.224.141:7878/queryProductStock?store=01&update=20190429161903&authcode="+myProductSecretKey)  #变量
#print(response.text)
result=json.loads(response.text)
print("总条数："+str(len(result)))
#print(myProductSecretKey)

# 创建excel工作表
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('sheet1')

# 设置表头
worksheet.write(0, 0, label='PN')
worksheet.write(0, 1, label='QTY')
worksheet.write(0, 2, label='MOQ')
worksheet.write(0, 3, label='PRICE')
worksheet.write(0, 4, label='BRAND')
worksheet.write(0, 5, label='TYPE')
# 将json字典写入excel
# 变量用来循环时控制写入单元格，感觉有更好的表达方式
val = 1
for item in result:
    worksheet.write(val, 0, item["PN"])
    worksheet.write(val, 1, item["QTY"])
    worksheet.write(val, 2, item["MOQ"])
    worksheet.write(val, 3, item["PRICE"])
    worksheet.write(val, 4, item["BRAND"])
    worksheet.write(val, 5, item["TYPE"])
    val += 1
# 保存
workbook.save('04174.xls')