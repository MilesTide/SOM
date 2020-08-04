# -*- coding: utf-8 -*-
# coding: utf-8
import os
import pandas as pd
import csv
import talib
import numpy as np
import  datetime
import dateutil.parser

path1 = "F:\DayCandles2017-201807\SA03.csv"
data = pd.DataFrame(pd.read_csv(path1, header=None))
data2 = np.array(data)
num = 0
coordinate = set(data2[:,-1])#共有多少坐标
temp = []
up = 0
down = 0
csvFile="F:/DayCandles2017-201807/SA03UpDown.csv"
for pos in coordinate:   #遍历坐标
    for z in range(len(data)):  #筛选和坐标相同的数据
        if  data2[z][-1] == pos: #这一类数目大于20 data2[z][-2]>=20 and
            temp.extend([[data2[z][0],data2[z][1], data2[z][-1]]])#名称，日期，坐标
            #num = num+1
            if data2[z][-5]==1:
                up=up+1
            elif data2[z][-5]==0:
                down=down+1
    dataAlone = np.array(temp)
    print("坐标", pos)
    print("总数量", len(dataAlone))
    print("上涨数量", up)
    print("下降数量", down)
    print("成功率",format(up/len(dataAlone),'.2%'))
    print("数目",num)
    with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
        text = [pos,len(dataAlone),up,down,format(up/len(dataAlone),'.2%')]
        csv.writer(f).writerow(text)
    f.close()
    temp=[]
    up = 0
    down = 0
    up_rate = 0