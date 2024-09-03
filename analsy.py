import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from time import sleep
# 设置字体为 SimHei (黑体) 或你已安装的其他支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
class Analsy:
    def __init__(self,target):
        self.area_dict = {
            "pudong": "浦东", "minxing": "闵行", "baoshan": "宝山", "xuhui": "徐汇",
            "putuo": "普陀", "yangpu": "洋浦", "changning": "长宁", "songjiang": "松江",
            "jiading": "嘉定",
            "huangpu": "黄浦", "jingan": "静安", "hongkou": "虹口",
            "qingpu": "青浦", "fengxian": "奉贤", "jinshan": "金山", "chongming": "崇明"
        }
        self.all_data = pd.DataFrame()
        folder_path = './Shanghai/'
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # 读取文件并添加一个新列 '区域'，根据文件名填充
                    temp_data = pd.read_csv(file_path, sep=',', header=0, encoding='utf-8')
                    area_name = file_name.replace('.csv', '')  # 假设文件名格式为“区域.csv”
                    temp_data['区域'] = self.area_dict[area_name]  # 添加新列并填入区域值

                    # 合并数据
                    self.all_data = pd.concat([self.all_data, temp_data], ignore_index=True)
                except Exception as e:
                    print(f"读取文件 {file_name} 时发生错误: {e}")
        self.all_data = self.all_data.apply(pd.to_numeric, errors='ignore')

        self.area_dict = {
        "浦东" : 100 , "闵行" : 100 , "宝山" :100 ,"徐汇" : 100,
        "普陀" : 100 ,"洋浦" : 100 ,"长宁" : 100 ,"松江" :100 ,
        "嘉定" : 100 ,
        "黄浦" : 90 ,"静安" : 100 ,"虹口" : 100 ,
        "青浦" : 100 ,"奉贤" : 100 ,"金山" : 88 ,"崇明" : 52 }

    #均价
    def avg_price(self):
        Price = pd.to_numeric(self.data['总价'], errors='coerce')
        avgPrice = Price.dropna()
        return np.average(avgPrice)
    # 各区均价与总均价的可视化
    def avg_price_all(self):
        self.all_data['总价'] = pd.to_numeric(self.all_data['总价'], errors='coerce')
        self.all_data = self.all_data.dropna(subset=['总价'])

        # 计算各个区域的平均价格
        avg_prices_by_area = self.all_data.groupby('区域')['总价'].mean()

        # 计算总均价
        total_avg_price = self.all_data['总价'].mean()
        plt.figure(figsize=(12, 6))
        sns.barplot(x=avg_prices_by_area.index, y=avg_prices_by_area.values, palette="viridis")
        plt.axhline(total_avg_price, color='red', linestyle='--', label=f'总均价: {total_avg_price:.2f}')
        # 设置图表标题和标签
        plt.title('各区均价与总均价对比', fontsize=16)
        plt.xlabel('区域', fontsize=14)
        plt.ylabel('平均总价 (元)', fontsize=14)
        plt.xticks(rotation=45)
        plt.legend()
        # 保存图表
        plt.savefig('./analysis_result/avg_price_comparison.png', dpi=300)  # 保存为PNG格式，dpi=300保证清晰度

        # 显示图表
        plt.tight_layout()
        plt.show()
        plt.close()
    #精装比和简装比
    def decorated_percent(self):
        decorated = self.data['装修'].tolist()
        # mpCount = decorated.count('毛坯')
        jianzCount = decorated.count('简装')
        jingzCount = decorated.count('精装')
        return jianzCount * 1.0 / len(decorated) * 100,jingzCount * 1.0 / len(decorated) * 100
    # 全市二手房装修程度分析
    def decorated_percent_all(self):
        # 统计每种装修类型的数量
        decorated_counts = self.all_data['装修'].value_counts()

        # 生成饼图
        plt.figure(figsize=(8, 8))
        plt.pie(decorated_counts, labels=decorated_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
        plt.title('全市二手房装修程度分析', fontsize=16)
        # 保存图表
        plt.savefig('./analysis_result/decorated_percent_all.png', dpi=300) 
        # 显示图表
        plt.show()
        plt.close()
    #单价与关注度
    def price_popularity(self):
        # 将“单价”和“关注度”转换为数值类型，并移除无效值
        self.data['单价'] = pd.to_numeric(self.data['单价'], errors='coerce')
        self.data['关注度'] = pd.to_numeric(self.data['关注度'], errors='coerce')
        valid_data = self.data.dropna(subset=['单价', '关注度'])
        # 计算单价和关注度的相关性,线性相关性，1为完全正相关（即一个变量增加，另一个变量也增加）。
        correlation = valid_data['单价'].corr(valid_data['关注度'])
        return correlation
    # 全市单价与关注度分析
    def price_popularity_all(self):
        self.all_data['单价'] = pd.to_numeric(self.all_data['单价'], errors='coerce')
        self.all_data['关注度'] = pd.to_numeric(self.all_data['关注度'], errors='coerce')
        valid_data = self.all_data.dropna(subset=['单价', '关注度'])

        correlation = valid_data['单价'].corr(valid_data['关注度'])
        
        # 绘制散点图和回归线
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=valid_data, x='单价', y='关注度', alpha=0.6)
        sns.regplot(data=valid_data, x='单价', y='关注度', scatter=False, color='red')
        plt.title(f'全市单价与关注度分析 (相关性: {correlation:.2f})', fontsize=16)
        plt.xlabel('单价 (元)', fontsize=14)
        plt.ylabel('关注度', fontsize=14)
        plt.grid(True)
        
        # 保存图表
        plt.savefig('./analysis_result/price_popularity_all.png', dpi=300)
        plt.tight_layout()
        plt.show()
        plt.close()
        return correlation
    #总价与关注度
    def total_price_popularity(self):
        self.data['总价'] = pd.to_numeric(self.data['总价'], errors='coerce')
        self.data['关注度'] = pd.to_numeric(self.data['关注度'], errors='coerce')
        valid_data = self.data.dropna(subset=['总价', '关注度'])
        correlation = valid_data['总价'].corr(valid_data['关注度'])
        return correlation
    #全市总价与关注度分析
    def total_price_popularity_all(self):
        self.all_data['总价'] = pd.to_numeric(self.all_data['总价'], errors='coerce')
        self.all_data['关注度'] = pd.to_numeric(self.all_data['关注度'], errors='coerce')
        valid_data = self.all_data.dropna(subset=['总价', '关注度'])

        correlation = valid_data['总价'].corr(valid_data['关注度'])
        
        # 绘制散点图和回归线
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=valid_data, x='总价', y='关注度', alpha=0.6)
        sns.regplot(data=valid_data, x='总价', y='关注度', scatter=False, color='red')
        plt.title(f'全市总价与关注度分析 (相关性: {correlation:.2f})', fontsize=16)
        plt.xlabel('总价 (元)', fontsize=14)
        plt.ylabel('关注度', fontsize=14)
        plt.grid(True)
        
        # 保存图表
        plt.savefig('./analysis_result/total_price_popularity_all.png', dpi=300)
        plt.tight_layout()
        plt.show()
        plt.close()
        return correlation

    #平均关注度较高即为热门户型
    def top3_popularity_type(self):
        self.data['关注度'] = pd.to_numeric(self.data['关注度'], errors='coerce')
        self.data['户型'] = self.data['户型'].astype(str)
        valid_data = self.data.dropna(subset=['户型', '关注度'])
        # 计算每个户型的平均关注度
        avg_popularity = valid_data.groupby('户型')['关注度'].mean()
        # 获取平均关注度最高的前三个户型
        top3_types = avg_popularity.nlargest(3).index.tolist()
        # 筛选出这些热门户型的数据
        top3_data = valid_data[valid_data['户型'].isin(top3_types)]
        # 计算每个热门户型的均价
        top3_avg_prices = top3_data.groupby('户型')['总价'].mean()
        # 打印热门户型及其均价
        for hx, price in top3_avg_prices.items():
            print(f"热门户型: {hx} - 平均总价: {price:.2f} 万元")
        
        return top3_avg_prices
    # 全市热门户型均价分析
    def top3_popularity_type_all(self):
        self.all_data['关注度'] = pd.to_numeric(self.all_data['关注度'], errors='coerce')
        self.all_data['户型'] = self.all_data['户型'].astype(str)
        valid_data = self.all_data.dropna(subset=['户型', '关注度'])
        avg_popularity = valid_data.groupby('户型')['关注度'].mean()
        
        top3_types = avg_popularity.nlargest(3).index.tolist()
        top3_data = valid_data[valid_data['户型'].isin(top3_types)]
        
        top3_avg_prices = top3_data.groupby('户型')['总价'].mean()

        # 绘制图表
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top3_avg_prices.index, y=top3_avg_prices.values, palette='viridis')
        plt.title('全市热门户型均价分析', fontsize=16)
        plt.xlabel('户型', fontsize=14)
        plt.ylabel('平均总价 (万元)', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 保存图表
        plt.savefig('./analysis_result/top3_popularity_type_avg_price.png', dpi=300)  # 保存为PNG格式，dpi=300保证清晰度
        plt.show()
    def get_analysis_result(self):
        self.avg_price_all()
        self.decorated_percent_all()
        self.total_price_popularity_all()
        self.price_popularity_all()
        self.top3_popularity_type_all()
    #二手房数量(用于计算各区二手房占比)
    #这边需要爬取全部的数据才行,暂时用页面查看到的数据替代一下
    def second_house_count(self):
        return len(self.data)
    # def huxing_percent():
    #     data=pd.read_csv('./chongming.csv',sep=',',header=0,encoding='utf-8')
    #     huxingErshoufang = np.array(data['户型'])
    #     huxing_types = np.unique(huxingErshoufang)
    #     print("该地区包含以下户型:",end=" ")

    #     for huxing_type in huxing_types:
    #         print(huxing_type ,end = ' ')
    #     print("\n请选择您感兴趣的户型:",end=" ")
    #     huxingChoose = input()
    #     print("您是否需要知晓装修信息:(若是请输入是,否则输入否)",end = " ")
    #     ZXFlag = input()

    #     assert ZXFlag == '是' or ZXFlag == '否'
    #     assert np.isin(huxingChoose,huxing_types)

    #     if ZXFlag == '是':
    #         hxCount,mpCount,jianzCount,jingzCount = zhuangxiu_percent(huxingChoose,huxingErshoufang)
    #         print(f"该户型在该地区共有{hxCount}套,其中毛坯房有{mpCount}套,简装房有{jianzCount}套,精装房有{jingzCount}套")

    #     huxingErshoufang[huxingErshoufang != huxingChoose] = 0
    #     huxingErshoufang[huxingErshoufang == huxingChoose] = 1 
    #     percent = np.sum(huxingErshoufang,keepdims=False) * 1.0 / huxingErshoufang.shape[0]
    #     return percent

   

# def ershoufang_top10_url_print(hxChoose,data):
#     dataHxs = data["户型"]
#     dataAttentions = data["关注度"]
#     dataUrls = data["链接"]

#     attentions = []
#     Urls = [] 
#     topUrls = []

#     for hx,attention,url in zip(dataHxs,dataAttentions,dataUrls):
#         if hx == hxChoose:
#             attentions.append(attention)
#             Urls.append(url)

#     iters = 10 if len(Urls) >= 10 else len(Urls)

#     for iter in range(iters):
#         index = attentions.index(max(attentions))
#         topUrls.append(Urls[index])
#         attentions.pop(index)
#         Urls.pop(index)
    
#     return topUrls,iters

# def hot_huxing_analsy():
#     data=pd.read_csv('./chongming.csv',sep=',',header=0,encoding='utf-8',index_col=None)
#     dataHuxing = data["户型"]
#     dataAttention = data["关注度"]
#     huxing_types = np.unique(dataHuxing)
#     hxCountAll = []
#     dataAttentionAvgAll = []

#     for huxing_type in huxing_types:
#         hxCount = 0
#         dataAttentionAvg = 0
#         for huxing,attention in zip(dataHuxing,dataAttention):
#             if huxing == huxing_type:
#                 hxCount += 1
#                 dataAttentionAvg += attention
#         if hxCount == 0:
#             dataAttentionAvg = -1
#         else : 
#             dataAttentionAvg = dataAttentionAvg * 1.0 / hxCount
#         dataAttentionAvgAll.append(dataAttentionAvg)
#         hxCountAll.append(hxCount)

#     attentionHotest = max(dataAttentionAvgAll)
#     hxCountHotest = hxCountAll[dataAttentionAvgAll.index(max(dataAttentionAvgAll))]
#     hxHotest = None

#     for attentionAvg,hx,hxCount in zip(dataAttentionAvgAll,huxing_types,hxCountAll):
#         if attentionAvg != -1:
#             print(f"该地区{hx}户型平均关注度为{attentionAvg:.2f},该地区共有{hxCount}个该户型")
#         else :
#             print(f"该地区{hx}户型暂时没有,您可以关注其他地区相应房型或者关注该地区其他房型")
#         if attentionAvg == attentionHotest:
#             hxHotest = hx

#     hotestHxPriceAvg = ershoufang_hx_danjia(hxHotest,data,hxCountHotest)
#     hotestTopAttentionUrls,nums = ershoufang_top10_url_print(hxHotest,data)

#     print(f"其中,{hxHotest}户型关注度最高,其在该地区的单价平均值为{hotestHxPriceAvg:.2f}元,为您列举了该户型{nums}个关注度最高的二手房链接:")
#     for url in hotestTopAttentionUrls:
#         print(url)

# huxing_percent()