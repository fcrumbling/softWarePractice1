#! /usr/local/bin/python3
import requests
import bs4
import os
import re
import csv
from time import sleep

def get_area_page(soup):
    #print(soup.find_all("div","page-box house-lst-page-box"))
    page = str(soup.find_all("div","page-box house-lst-page-box")[0])
    #使用正则表达式提取totalPage的值
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
    "嘉定" : "jiading" ,
    "黄浦" : "huangpu" ,"静安" : "jingan" ,"虹口" : "hongkou" ,
    "青浦" : "qingpu" ,"奉贤" : "fengxian" ,"金山" : "jinshan" ,"崇明" : "chongming" }
folder_path = './ShangHai'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
for _,area_choose in area_dict.items(): 
    url_init = r'https://sh.lianjia.com/ershoufang/' + area_choose + '/'
    headers = { 'Host': "bj.lianjia.com",
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
                'Accept-Encoding': "gzip, deflate, sdch",
                'Accept-Language': "zh-CN,zh;q=0.8", 
                'User-Agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50", 'Connection': "keep-alive", }
    response = requests.get(url_init,headers=headers).text
    soup = bs4.BeautifulSoup(response,'html.parser')

    totalPages = get_area_page(soup)
    assert totalPages != 0

    f = open(f'{folder_path}/{area_choose}.csv', mode='a', encoding='utf-8', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=['地址','户型','面积','朝向','装修','楼层','购买时间','总价','单价','关注度','发布时间','链接'])
    csv_writer.writeheader()

    maxOfHourse = 0
    for page in range(int(totalPages)):
        url = url_init  + 'pg%s/' % (page + 1)
        response = requests.get(url,headers=headers).text
        soup = bs4.BeautifulSoup(response,'html.parser')
        names = [i.text.strip() for i in soup.findAll(name = 'a', attrs = {'data-el':'region'})]
        Types = [i.text.split('|')[0].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        sizes = [float(i.text.split('|')[1].strip()[:-2]) for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        directions = [i.text.split('|')[2].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        ZXs = [i.text.split('|')[3].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        flools = [i.text.split('|')[4].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        years = [i.text.split('|')[5].strip() for i in soup.findAll(name = 'div', attrs = {'class':'houseInfo'})]
        totals = [float(i.text[:-1]) for i in soup.findAll(name = 'div', attrs = {'class':'totalPrice'})] 
        price_text = [i.text for i in soup.findAll(name = 'div', attrs = {'class':'unitPrice'})]
        prices = [int(re.sub(r'[^\d]', '', price)) for price in price_text]
        attention_text = [i.text.split('/')[0] for i in soup.findAll(name="div",attrs={'class':'followInfo'})]
        attentions = [int(re.sub(r'[^\d]', '', attention)) for attention in attention_text]
        pubTimes = [i.text.split('/')[1] for i in soup.findAll(name="div",attrs={'class':'followInfo'})]
        superUrls = [i.get("href") for i in soup.find_all("a",attrs={'data-el':"ershoufang",'class' : "noresultRecommend img LOGCLICKDATA"})][::2]

        for name,Type,size,direction,ZX,flool,year,total,price,attention,pubTime,superUrl in zip(names,Types,sizes,directions,ZXs,flools,years,totals,prices,attentions,pubTimes,superUrls):
            dic = {'地址':name,'户型':Type,'面积':size,'朝向':direction,'装修':ZX,'楼层':flool,'购买时间':year,'总价':total,'单价':price,'关注度':attention,'发布时间':pubTime,'链接':superUrl}
            csv_writer.writerow(dic)
            maxOfHourse += 1

        if maxOfHourse >= 200 :
            break

        sleep(1)




