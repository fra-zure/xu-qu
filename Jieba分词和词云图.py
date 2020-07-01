#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:55:35 2020

@author: apple
"""


import jieba  # 中文分词包
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from os import path
 

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('Chinesestop.txt',encoding='UTF-8').readlines()]#打开停用词表
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 给出文档路径
filename = "printemps.csv"
outfilename = "out.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')

# 将输出结果写入out.txt中
for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')
    print("-------------------正在分词和去停用词-----------")
outputs.close()
inputs.close()
print("删除停用词和分词成功！！！")
 # 调用包PIL中的open方法，读取图片文件，通过numpy中的array方法生成数组


spring = np.array(Image.open("/Users/apple/Desktop/spring.jpg"))#词云的色彩提取图片
genclr = ImageColorGenerator(spring)

text = open('/Users/apple/Desktop/out.txt', 'r', encoding='utf-8').read() #读入分好词的文档


# 2. 生成词云
def create_word_cloud(filename):
    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，一般路径
        font_path='/System/Library/Fonts/STHeiti Medium.ttc',
        height=1080,
        width=1545,
        # 设置字体最大值
        max_font_size = 300,
        # 设置字体最小值
        min_font_size = 31,
        # 设置颜色
        color_func = genclr)
      
        
    myword = wc.generate(text)  # 生成词云
    
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('/Users/apple/Desktop/b.png')  # 把词云保存下


if __name__ == '__main__':
    create_word_cloud('word_py')



