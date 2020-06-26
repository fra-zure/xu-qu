#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 00:13:19 2020

@author: apple
"""

import photomosaic
image = photomosaic.imread("/Users/apple/Desktop/test3.jpg") #我们要合成的图片模板，
pool = photomosaic.make_pool('/Users/apple/Desktop/rohmer/*.jpg') #图片池，这里用我们刚才爬取的图片
mosaic = photomosaic.basic_mosaic(image, pool, (100, 100))   
photomosaic.imsave('0.png',mosaic)
