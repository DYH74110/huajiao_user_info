#!/user/bin/env python
# -*- coding:utf-8 -*-
#author:dyh time 20171020
# 50174821
# http://www.huajiao.com/user/38022738

import requests
import os
import re
import json

def strip(path):
    path=re.sub(r'[?\\*|"<>:/]','',str(path))
    return path

# re.sub('<[^>]+>','',re.sub(' ','',re.findall(r'.*<h4>(.*?)<p>收到的赞</p>.*', i, re.S)[0]))

class spider:
    def __init__(self):
        self.session=requests.session()

    def run(self,str_ulr):
        # 获取主播的变编号
        get_ids=self.get_ids(str_url)
        # print(get_ids)
        num_url=0  #记录抓取的主播客户数
        for ids in get_ids:
            get_info=self.get_info(ids)
            get_item=self.get_item(get_info)
            num_url=num_url+1
            # break   #调试使用，查看一条记录
        print("总主播数：",num_url)



    # 下载数据
    def dowload(self,str_url):
        try:
            return self.session.get(str_url)
            # print(response.text)
        except Exception as f:
            print(f)

    #获取主播的编号
    def get_ids(self,str_url):
        response=self.dowload(str_url)
        ids_list=response.text
        # print(ids_list)
        ids=re.findall(r'<ul class="vlist">(.*?)</ul>',ids_list,re.S)[0]
        # print(ids)
        # 获取个人信息网页链接地址
        data_video_id=re.findall(r'<li data-video-id.*?<a target="_blank" href="(.*?)".*?</li>',ids,re.S)
        # print(data_video_id)
        return set(data_video_id)
        # 获取照片地址
        # img_src=re.findall(r'<li data-video-id.*?<img src="(.*?)">.*?</li>',ids,re.S)
        # print(img_src)

    def get_info(self,ids):
        # print(ids)
        url='http://www.huajiao.com'+ids
        print("主播直播主页：",url)
        response=self.dowload(url)
        html=response.text
        # 获取花椒id 用id在花椒用户网址上查看信息
        id_num=re.findall(r'<div class="feed-info clearfix">.*?<span>花椒号：(.*?)</span>.*?</div>',html,re.S)
        print('花椒号：'+str(id_num))
        user_url='http://www.huajiao.com/user/' +str(id_num[0])
        print("花椒会员信息网址：",user_url+"\n")

        user_info=self.dowload(user_url)
        # html_z=re.sub(' ','',user_info.text)  #空值转化
        # print(json.load(user_info.text))
        html_zb=re.findall(r'.*?<div id="doc-bd">(.*?)<div class="feeds-fans clearfix">.*?',user_info.text,re.S)
        return  html_zb


    # 细化获取客户数信息
    # #根据花椒会员信息网址获取博主信息
    # #需要提取的信息：
    # 1：花椒名、2：花椒会员id、3：地址、4：个性签名、5：标签、6：送礼数、7：收礼数、8：收到的赞、9：粉丝数

    def get_item(self,html):
        # print(html)
        # info_gift=''
        for i in html:
            # print(i)
            # 涉及到空格的处理，音标
            hj_id=re.findall(r'.*<span class="number">花椒号：(.*?)</span>.*', i)[0]
            print('花椒号:', hj_id)

            hj_idlocation=re.findall(r'.*<span class="location">(.*?)</span>.*',i)[0]
            print('主播地址是:', hj_idlocation)

            hj_about=re.findall(r'.*<p class="about">(.*?)</p>.*',i,re.S)[0]
            print('主播说明:',hj_about)

            hj_tag=re.findall(r'.*<p class="tags">(.*?)</p>.*',i,re.S)[0]
            tag=[]
            for j in re.findall('<span>(.*?)</span>',hj_tag,re.S):
                tag.append(j)
            print('主播的标签是:',list(tag))

            info_follow=re.sub('<[^>]+>','',re.sub(' ','',re.findall(r'.*<h4>(.*?)<p>粉丝数</p>.*',i,re.S)[0]))
            print('粉丝数：',info_follow)

            info_prize=re.sub('<[^>]+>','',re.sub(' ','',re.findall(r'.*<h4>(.*?)<p>收到的赞</p>.*', i, re.S)[0]))
            print('收到的赞：', info_prize)

            info_gifti=re.sub('<[^>]+>','',re.sub(' ','',re.findall(r'.*<h4>(.*?)<p>收礼数</p>.*', i, re.S)[0]))
            print('收礼数：', info_gifti)

            info_gifto=re.sub('<[^>]+>','',re.sub('h4','',re.sub(' ','',re.findall(r'.*<h4>(.*?)<p>送礼数</p>.*', i, re.S)[0])))
            print('送礼数：', info_gifto)
            # print('\n')
            # print('\n')


            # 主播信息保存在列表中
            # info_hz=[]
            # info_hz.append(hj_id)
            # info_hz.append(hj_idlocation)
            # info_hz.append(hj_about)
            # info_hz.append(tag)
            # info_hz.append(info_follow)
            # info_hz.append(info_prize)
            # info_hz.append(info_gifti)
            # info_hz.append(info_gifto)


            # 主播信息保存在字典中
            info_hz={}
            info_hz={'hj_id': hj_id, 'hj_idlocation': hj_idlocation,
                     'hj_about': hj_about,'hj_tag': tag,
                     'info_follow': info_follow, 'info_prize': info_prize,
                     'info_gifti': info_gifti,'info_gifto': info_gifto}

            print('客户汇总数据：',info_hz)


            data='huajiao_zhibo_20171114.txt'
            # 首次抓取的时候获取标题
            # get_num=1
            # if get_num==1:
            #     with open(data,'a') as data_abel:
            #         data_abel.write(str(info_hz.keys()))
            # else:
            #     pass
            #     # get_num=get_num+1

            with open(data,'a') as data_con:
                data_con.write(str(info_hz.values()))
                print('\n')



        # print(html_tran)
        # hj_name=re.findall(r'<divclass="info-box"><h3>span>心灵歌者二萌</span>',html_zb,re.S)
        # print('花椒名:',hj_name)
        # hj_id=ids
        # print('花椒会员id:',str(id_num))
        # hj_idlocation=re.findall(r'<span class="location">.*?</span>',html_zb,re.S  -)
        # print('主播地址是：',hj_idlocation)
        # hj_about=re.findall(r'<p class="about">(.*?)</p>',html_zb,re.S)
        # print('主播说明:',hj_about)
        # hj_tag=re.findall(r'<p class="tags">(.*?)</p>',html_zb,re.S)
        # print('主播的标签是',hj_tag)
        # for i in hj_tag:
        #     print('主播的标签是：',i)
        #
        # info_full=re.findall(r'<ul class="clearfix">(.*?)</ul>',html_zb,re.S)
        # print('常规信息：',info_full)
        #
        # info_follow=re.findall(r'.*?<ul class="clearfix">.*?<h4>(.*?)</h4>.*?<p>粉丝数</p>.*?</ul>.*?',html_zb,re.S)
        # info_follow=re.findall(r'<h4>(\d+\S)</h4>\s+<p>粉丝数</p>.',html_zb,re.S)
        # print('粉丝数：',info_follow,"/n")
        #
        #
        # clearfix=re.findall(r'<ul class="clearfix">.*?</ul>',html_zb,re.S)
        # print('常规主播信息：',clearfix)

        # hj_follow=re.findall(r'<ul class="clearfix">\r\n                        <li>\r\n                            <h4>                    (.*?)\n    </h4>\r\n                            <p>粉丝数</p>.*?',html_zb,re.S)
        # print('粉丝数:',hj_follow)
        # hj_price=re.findall(r'<ul class="clearfix">\r\n                        <li>\r\n                            <h4>                    20869\n    </h4>\r\n                            <p>粉丝数</p>\r\n                        </li>\r\n                        <li>\r\n                            <h4>                    (.*?)\n    </h4>\r\n                            <p>收到的赞</p>.*?',clearfix)
        # print('收到的赞:',hj_price)



if __name__=='__main__':
    spider=spider()
    str_url='http://www.huajiao.com/catagory/1000'
    spider.run(str_url)



# 高价值
# http://www.huajiao.com/l/170641429