import pandas as pd
import numpy as np
import requests
from lxml import etree
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By#selenium4.0以上写法
page = 1
home_info_all = []#房子总信息
driver = webdriver.Chrome()
#数据爬取
for page in range(1,5,1):#1到5页的信息采集
    url = "https://cd.lianjia.com/ershoufang/pg{}/".format(page)
    driver.get(url)
    time.sleep(3)#等待加载
    js_bottom = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js_bottom)  # 跳转到底部，使其加载完毕
    home_list = driver.find_element(By.XPATH, '//ul[@class="sellListContent"]')
    home_infos = home_list.find_elements(By.XPATH, './li[@class="clear LOGCLICKDATA"]')
    for home_info in home_infos:#按照class属性值选取信息
        home_title = home_info.find_element(By.XPATH,'./div/div[@class="title"]')
        home_title_text = home_title.text
        home_flood = home_info.find_element(By.XPATH,'./div/div[@class="flood"]')
        home_flood_text = home_flood.text
        home_houseinfo = home_info.find_element(By.XPATH,'./div/div[@class="address"]')
        home_houseinfo_text = home_houseinfo.text
        home_priceinfo = home_info.find_element(By.XPATH,'./div/div[@class="priceInfo"]')
        home_priceinfo_text = home_priceinfo.text
        home_followinfo = home_info.find_element(By.XPATH,'./div/div[@class="followInfo"]')
        home_followinfo_text = home_followinfo.text
        home_info_all.append((home_title_text,home_flood_text,home_houseinfo_text,home_priceinfo_text,home_followinfo_text))
df = pd.DataFrame(home_info_all, columns=["名称", "地点", "简要信息", "售价", "关注度"])
#原始数据清洗
df.to_csv("cdhouse5page.csv")
df = pd.read_csv('cdhouse5page.csv')
pf = df["售价"]
num = []
pf_vs =np.ndarray.tolist(pf.values)#将对象转化为数组再转换为列表
for i in range(0,len(pf_vs),1):#分离每平米价格
    temp1 = pf_vs[i].split("\n")
    temp2 = temp1[2].split("元")
    temp3 = temp2[0].replace(",","")
    temp4 = int(temp3)
    num.append(temp4)
count1,count2,count3,count4,count5,count6 = 0,0,0,0,0,0
for i in range(0,len(num),1):
    if num[i] < 5000:
        count1 += 1
    elif 5000 <num[i] < 10000:
        count2 +=1
    elif 10000 <= num[i] <15000:
        count3 +=1
    elif 15000 <= num[i]< 20000:
        count4 +=1
    elif 20000 <= num[i] < 30000:
        count5 +=1
    else:
        count6 +=1
#构造所需格式的数据
price = [["小于5000元的商品房",count1],["5000元至10000元的商品房",count2],["10000元至15000元的商品房",count3],["15000元至20000元的商品房",count4],["20000元至30000元的商品房",count5],["30000元以上的商品房",count6]]
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
#可视化
c = (
    Pie()
    .add(
        "",
        price,#替换数据
        radius=["40%", "55%"],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="成都市房价：元/平"))
)
c.render_notebook()
