#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:02:38 2020

@author: apple
"""

import requests
from lxml import etree

#翻页
#https://movie.douban.com/celebrity/1054406/movies?start=0&format=pic&sortby=vote& #第一页
#https://movie.douban.com/celebrity/1054406/movies?start=10&format=pic&sortby=vote& #第二页
#https://movie.douban.com/celebrity/1054406/movies?start=20&format=pic&sortby=vote& #第三页
#https://movie.douban.com/celebrity/1054406/movies?start=30&format=pic&sortby=vote& #第四页
#以每页10为单位，递增10，只是 start=()的数字不一样，所以写一个循环

for page in range(0,70,10):
    url = 'https://movie.douban.com/celebrity/1054406/movies?start='+str(page)+'&format=pic&sortby=vote&'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    #给定 url 并用 requests.get() 方法来获取页面的text，用 etree.HTML() 来解析下载的页面数据“data”。
    data = requests.get(url,headers=headers).text
    s=etree.HTML(data)
    #获取元素的Xpath信息并获得文本
    file=s.xpath('//*[@id="content"]/div/div[1]/div[2]/ul/li/dl/dd/h6/a/text()')
   
    print(file)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 生成词云
def create_word_cloud(filename):
    wl = " ".join(file)
    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，一般路径
        font_path='Library/Fonts/方正楷体简体.ttf',
        height=2000,
        width=2000,
        # 设置字体最大值
        max_font_size=200,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=50)
      
    myword = wc.generate(wl)  # 生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('a.png')  # 把词云保存下


if __name__ == '__main__':
    create_word_cloud('word_py')
