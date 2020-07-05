#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:01:19 2020

@author: alica
"""


from bs4 import BeautifulSoup
import requests

#爬取剧照

#春天的故事

header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'}

#获取网页链接
spring_img_url_list = []
for page in range(0,150,30):
    spring_img_url = 'https://movie.douban.com/subject/1293632/photos?type=S&start='+str(page)+'&sortby=like&size=a&subtype=a'
    spring_img_url_list.append(spring_img_url)

#print(spring_img_url_list)

#获取图片链接
spring_img_list = []
for u in spring_img_url_list:
    #获取源代码
    spring_img_html = requests.get(u, headers = header) 
    #将已下载的html内容解析为soup文档
    spring_img_soup = BeautifulSoup(spring_img_html.text, 'lxml')
    #找到图片所属容器(div)
    spring_img_ul = spring_img_soup.find('ul', class_='poster-col3 clearfix')
    #找到img标签
    spring_img = spring_img_ul.find_all('img')
    spring_img_list.extend(spring_img)

#print(spring_img_list)

#储存图片
x = 0        
for img in spring_img_list:
    img_src = img.get('src')
    x += 1
    i = requests.get(img_src)
    with open('/Users/alica/Desktop/rohmer/'+'%s.jpg'%x,'wb') as f:
        f.write(i.content)
