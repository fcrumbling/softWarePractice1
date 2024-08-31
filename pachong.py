#! /usr/local/bin/python3
import requests
import bs4
import pandas as pd
import os
import sys
import re

def restart():
    os.system("python ./pachong.py")# 当前程序所在位置
    sys.exit() # 结束当前程序

def get_area_page(soup):
    page = str(soup.find_all("div","page-box house-lst-page-box")[0])
    # 使用正则表达式提取totalPage的值
    match = re.search(r'"totalPage":(\d+)', page)
    if match:
        total_page = match.group(1)
        return total_page
    else:
        print("\033[4;31m该地区没有房源\033[0m")
        return 0

area_dict = {
    "浦东" : "pudong" , "闵行" : "minxing" , "宝山" : "baoshan" ,"徐汇" : "xuhui" ,
    "普陀" : "putuo" ,"洋浦" : "yangpu" ,"长宁" : "changning" ,"松江" : "songjiang" ,
    "嘉定" : "jiading" ,"黄浦" : "huangpu" ,"静安" : "jingan" ,"虹口" : "hongkou" ,
    "青浦" : "qingpu" ,"奉贤" : "fengxian" ,"金山" : "jinshan" ,"崇明" : "chongming" }

print("              \033[1;36m欢迎来到上海地区二手房分析预测系统！！\033[0m")
print("                    \033[0;30m请选择您想购买二手房地区\033[0m")
print("""
                      \033[1;30m浦东 \033[0m\033[1;30m闵行 \033[0m\033[1;30m宝山 \033[0m\033[1;30m徐汇\033[0m
                      \033[1;30m普陀 \033[0m\033[1;30m洋浦 \033[0m\033[1;30m长宁 \033[0m\033[1;30m松江\033[0m
                      \033[1;30m嘉定 \033[0m\033[1;30m黄浦 \033[0m\033[1;30m静安 \033[0m\033[1;30m虹口\033[0m
                      \033[1;30m青浦 \033[0m\033[1;30m奉贤 \033[0m\033[1;30m金山 \033[0m\033[1;30m崇明\033[0m
      """)

area_choose = input("在此输入要查询区域：")

try:
    area_pingyin = area_dict[area_choose]
except:
    print("\033[4;31m警告:该区域不在查询范围内\033[0m")
    restart()

url = r'https://sh.lianjia.com/ershoufang/' + area_dict[area_choose] + '/'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
          'Cookie' : 'lianjia_ssid=b9337e6f-4652-48e7-980d-bfff190430a7; lianjia_uuid=3a4a985b-b799-4bca-854a-4f63e3b01476; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1725092624; HMACCOUNT=92987F33D63C5269; _jzqa=1.1218652899013096200.1725092624.1725092624.1725092624.1; _jzqc=1; _jzqckmp=1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22191a788761523c-03379530102999-4c657b58-1327104-191a7887616e2b%22%2C%22%24device_id%22%3A%22191a788761523c-03379530102999-4c657b58-1327104-191a7887616e2b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.1844623798.1725092634; _gid=GA1.2.1270040898.1725092634; select_city=310000; crosSdkDT2019DeviceId=-d786w8--xzzpb2-sot7yfstdrlv2lr-91gk9yp9c; login_ucid=2000000441868421; lianjia_token=2.0014e90678441c0b1105442f495a7db50b; lianjia_token_secure=2.0014e90678441c0b1105442f495a7db50b; security_ticket=kvzvkKgbJpmjYvF+wNIRylJsegwcOdLdJrVld6OFcIMGsJzJnVIbADUSWdUJAk3iEzaX/d76y3vaGMABHlMRkpV9WnYt/kpuUFBwHbw0zUEa8t2cz0o/Q6tmEB0uVozhwFoqBxF/08tDhCG6484ur42bE+b4+bxisEgYchqxA2g=; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1725093969; _jzqb=1.15.10.1725092624.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _ga_LRLL77SF11=GS1.2.1725093905.1.1.1725093979.0.0.0; _ga_GVYN2J1PCG=GS1.2.1725093905.1.1.1725093979.0.0.0'}

response = requests.get(url,headers=header).text
soup = bs4.BeautifulSoup(response,'html.parser')

totalPages = get_area_page(soup)
assert totalPages != 0

table = pd.DataFrame(columns=('地址','户型','面积','朝向','装修','楼层','购买时间','总价','单价','关注度','发布时间','链接'))

for page in range(int(totalPages)):
    url = url  + 'pg%s/' % (page + 1)
    name = [i.text.strip() for i in soup.findAll(name = 'a', attrs = {'data-el':'region'})]
    Type = [i.text.split('|')[0].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    size = [float(i.text.split('|')[1].strip()[:-2]) for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    direction = [i.text.split('|')[2].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    ZX = [i.text.split('|')[3].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    flool = [i.text.split('|')[4].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    year = [i.text.split('|')[5].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
    total = [float(i.text[:-1]) for i in soup.findAll(name = 'div', attrs = {'class':'totalPrice'})] 
    price_text = [i.text for i in soup.findAll(name = 'div', attrs = {'class':'unitPrice'})]
    price = [int(re.sub(r'[^\d]', '', price)) for price in price_text]
    attention_text = [i.text.split('/')[0] for i in soup.findAll(name="div",attrs={'class':'followInfo'})]
    attention = [int(re.sub(r'[^\d]', '', attention)) for attention in attention_text]
    pubTime = [i.text.split('/')[1] for i in soup.findAll(name="div",attrs={'class':'followInfo'})]
    superUrl = [i.get("href") for i in soup.find_all("a",attrs={'data-el':"ershoufang"})][::2]
    new_table=pd.DataFrame({'地址':name,'户型':Type,'面积':size,'朝向':direction,'装修':ZX,'楼层':flool,'购买时间':year,'总价':total,'单价':price,'关注度':attention,'发布时间':pubTime,'链接':superUrl})
    table = pd.concat([table,new_table])
    maxOfHourse = table.shape[0]
    if maxOfHourse >= 3000 :
        break

numOfHourse = table.shape[0]
table.to_csv("./" + area_dict[area_choose] + ".csv")