#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:56:27 2020

@author: apple
"""
#马赛克实现原理：先将所要成像的图片转化成马赛克图片，然后从图库中用对应颜色的图片替换相应色块。
#图库中的图片处理：标记图库中每张图片的混合颜色，用于替换目标色块，并记录每张图片的特征用于成像，增加成像质量。

#我在代码中实现了灰度图像和RGB通道图像的筛选方法：
#灰度图像：
#直接计算所有像素灰度值的平均值，取最接近n个图像供后期再次筛选；
#RGB通道：
#分别计算R,G,B的平均值，对于一个图像我们得到的是一个类似与[20, 30,40]的数组，然后我们计算欧式距离，取最接近n个图像供后期再次筛选。

#1.导入需要用的库
from PIL import Image
import os
import numpy as np
from tqdm import tqdm


class Config:
    corp_size = 40
    filter_size = 20
    num = 100


class PicMerge:

    def __init__(self, pic_path, mode='RGB', pic_folder='/Users/apple/Desktop/rohmer/'):   #图片池，这里用我们刚才爬取的图片
        if mode.upper() not in ('RGB', 'L'):
            raise ValueError('Only accept "RGB" or "L" MODE, but we received "{}".'.format(self.mode))
        else:
            self.mode = mode.upper()
        print('Coding for every picture in folder "{}".'.format(pic_folder))
        self.mapping_table, self.pictures = self.mapping_table(pic_folder)
        self.picture = self.resize_pic(pic_path).convert(self.mode)
        
    @staticmethod
    def resize_pic(pic_path):
        picture = Image.open(pic_path)
        width, height = picture.size
        to_width = Config.corp_size * Config.num
        to_height = ((to_width / width) * height // Config.corp_size) * Config.corp_size
        picture = picture.resize((int(to_width), int(to_height)), Image.ANTIALIAS)
        return picture
    
#我们总共有64（即$8*8$）个像素点，分别去与平均值比较大小，高于平均值的记为1，小于平均值的记为0，
#这样我们每张图片都会得到一个长度为64类似[0,1,1,0,1,0....0,1,1]的‘编码’。

    def merge(self):
        width, height = self.picture.size
        w_times, h_times = int(width / Config.corp_size), int(height / Config.corp_size)
        picture = np.array(self.picture)
        print('Corp & Merge...')
        for i in tqdm(range(w_times), desc='CORP'):
            for j in range(h_times):
                if self.mode == 'L':
                    section = picture[j * Config.corp_size:(j + 1) * Config.corp_size,
                                      i * Config.corp_size:(i + 1) * Config.corp_size]
                    section_mean = section.mean()
                    candidate = sorted([(key_, abs(np.array(value_).mean() - section_mean))
                                        for key_, value_ in self.pictures.items()],
                                       key=lambda item: item[1])[:Config.filter_size]
                    most_similar = self.structure_similarity(section, candidate)
                    picture[j * Config.corp_size:(j + 1) * Config.corp_size,
                            i * Config.corp_size:(i + 1) * Config.corp_size] = most_similar
                elif self.mode == 'RGB':
                    section = picture[j * Config.corp_size:(j + 1) * Config.corp_size,
                                      i * Config.corp_size:(i + 1) * Config.corp_size, :]
                    candidate = self.color_similarity(section)
                    most_similar = self.structure_similarity(section, candidate)
                    picture[j * Config.corp_size:(j + 1) * Config.corp_size,
                            i * Config.corp_size:(i + 1) * Config.corp_size, :] = most_similar

        picture = Image.fromarray(picture)
        picture.show()
        picture.save('result.jpg')#将图片储存下来
        print('Work Done...')

    def structure_similarity(self, section, candidate):
        section = Image.fromarray(section).convert('L')
        one_hot = self.pic_code(np.array(section.resize((8, 8), Image.ANTIALIAS)))  
        candidate = [(key_, np.equal(one_hot, self.mapping_table[key_]).mean()) for key_, _ in candidate]
        most_similar = max(candidate, key=lambda item: item[1])
        return self.pictures[most_similar[0]]
    
#只需要提取图片结构，颜色意义不大，为计算简便，我们直接将所有图片转为灰度通道

    def color_similarity(self, pic_slice, top_n=Config.filter_size):
        slice_mean = self.rgb_mean(pic_slice)
        diff_list = [(key_, np.linalg.norm(slice_mean - self.rgb_mean(value_)))
                     for key_, value_ in self.pictures.items()]
        filter_ = sorted(diff_list, key=lambda item: item[1])[:top_n]
        return filter_

    @staticmethod
    def rgb_mean(rgb_pic):
    #若照片是RGB颜色模式，则计算其RGB平均值。   
        r_mean = np.mean(rgb_pic[:, :, 0])
        g_mean = np.mean(rgb_pic[:, :, 1])
        b_mean = np.mean(rgb_pic[:, :, 2])
        val = np.array([r_mean, g_mean, b_mean])
        return val

    def mapping_table(self, pic_folder):
        """
        1. 遍历pic_folder中的每张图片;
        2. 重置每张图片的大小至 (8,8) 并将其转化为灰色;
        3. 设置每张图片的进度条标题'CODE'
        4. 创建字典，将所有图片与它们的CODE放入其中.
        :pic_folder的参数: 图片文件夹的路径.
        :返回字典
        """
        suffix = ['jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG']
        if not os.path.isdir(pic_folder):
            raise OSError('Folder [{}] is not exist, please check.'.format(pic_folder))

        pic_list = os.listdir(pic_folder)
        results = {}
        pic_dic = {}
        for idx, pic in tqdm(enumerate(pic_list), desc='CODE'):
            if pic.split('.')[-1] in suffix:
                path = os.path.join(pic_folder, pic)
                try:
                    img = Image.open(path).resize((Config.corp_size, Config.corp_size), Image.ANTIALIAS)
                    results[idx] = self.pic_code(np.array(img.convert('L').resize((8, 8), Image.ANTIALIAS)))
                    if self.mode == 'RGB':
                        pic_dic[idx] = np.array(img.convert(self.mode))
                    else:
                        pic_dic[idx] = np.array(img.convert(self.mode))
                except OSError:
                    pass
        return results, pic_dic

    @staticmethod
    def pic_code(image: np.ndarray):
        """
        为image创建“独热编码” (one-hot code).
        avg是图像序列的均值.
        遍历image的每一个R通道像素，若像素值大于avg，则将其设为1，反之为0
        :image的参数：图片序列
        :返回：一个表示长度的稀疏列表 [图片宽 * 图片长]
        """
        width, height = image.shape
        avg = image.mean()
        one_hot = np.array([1 if image[i, j] > avg else 0 for i in range(width) for j in range(height)])
        return one_hot


if __name__ == "__main__":
    P = PicMerge(pic_path='test1.jpg', mode='RGB') #我们要合成的图片模板
    P.merge()
