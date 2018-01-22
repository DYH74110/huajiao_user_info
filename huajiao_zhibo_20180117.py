
# -*- coding:utf-8 -*-
import urllib
import requests
from bs4 import BeautifulSoup
import re
import os
import time

global time_fl   #用于保存文件的命名，区别获取时间
time_fl=time.strftime("%Y-%m-%d-%H-%M", time.localtime())
print(time_fl)

global live_url  #全局变量 保存主播的主页到文件
live_url=''

global number    #全局变量，为每个文件保存当number=1 的时候，保存keys
number=1

num_id=1   #记录直播数
def get_info(url):
    response=requests.get(url)
    content=response.content
    data=BeautifulSoup(content,'html.parser')
    # print(data)
    span=data.find_all('span')
    name=span[0].string    #网名
    id  =span[1].string    #花椒号
    addr=span[2].string    #地址
    live=span[3].string    #live-level
    self=span[4].string    #self-level

    print('姓名：',name)
    print('花椒号：',id)
    print('地址：',addr)
    print('主播等级：',live)
    print('用户等级：',self)

    h4info=data.find_all('h4')
    # print(h4info)
    follow=h4info[0].string.replace(' ','').replace('\n','')  #粉丝数
    like  =h4info[1].string.replace(' ','').replace('\n','')  #收到的赞
    gift_r=h4info[2].string.replace(' ','').replace('\n','')  # 收礼数
    gift_o=h4info[3].string.replace(' ','').replace('\n','')  # 送礼数
    print('粉丝数：',follow)
    print('收到的赞：',like)
    print('收礼数：',gift_r)
    print('送礼数：',gift_o)

    #保存文件
    data={'name':name,'id':id,'addr':addr,'live':live,'self':self,'follow':follow,
          'like':like,'gift_r':gift_r,'gift_o':gift_o,'user_url':url,'live_url':live_url}
    print(data.values())

    global time_fl
    file='data\花椒信息保存%s.txt'%time_fl  #文件名增加处理时间 分开文件保存

    global number
    if number==1:
        with open(file, 'w', encoding='utf-8') as f:  # 需要重新定义编码 写入 新的文件 a/w 都可以
            key=data.keys()
            f.write(str(key) + '\n')
            print('\n')  # 换行
    number+=1    #number自加1


    with open(file,'a',encoding='utf-8') as f:  #需要重新定义编码，a :在原有文件上加入数据
        values=data.values()
        f.write(str(values)+'\n')
        print('保存完成！！！')   #换行


# URL=['http://www.huajiao.com/user/103243781?seelive=yes','http://www.huajiao.com/user/88881008']
# for i in range(10):
#     get_info(URL[i])

# 获取直播主页上主播的主编号
def get_zid(url):
    response=requests.get(url)
    html=response.text
    zid=re.findall('<span class="js-author-id">(.*?)</span>',html,re.S)
    print("主播编号：%s"%zid[0])

    user_url='http://www.huajiao.com/user/%s'%zid[0]
    print('主播信息网址：%s'%user_url)
    get_info(user_url)     #获取主播的信息



# 获取直播主页上主播的副编号
url='http://www.huajiao.com/category/1000'
# global debug
debug=True
def get_mid(url):
    html=requests.get(url)
    content=html.text
    id=re.findall('<a href="/(.*?)" class="figure" target="_blank">',content,re.S)  #获取主播编号
    # print('编号：',id)
    global num_id
    num_id=1      #计数编号
    for int in range(len(id)):
        id_num=id[int]
        print('直播编号：',id_num)
        num_id+=1
        global live_url
        live_url='http://www.huajiao.com/%s'%id_num
        print('主播现场直播网址：%s'%live_url)
        global debug
        get_zid(live_url)    #获取主播编号


get_mid(url)
print('合计:%s直播'%num_id)


