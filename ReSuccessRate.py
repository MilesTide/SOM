# -*- coding: utf-8 -*-
# coding: utf-8
import os
import pandas as pd
import csv
import talib
import numpy as np
import  datetime
import dateutil.parser

FilesPath = 'F:\DayCandles2017-201807'
FilesList = os.listdir(FilesPath)
path1 = "F:\DayCandles2017-201807\zuobiao.csv"
data = pd.DataFrame(pd.read_csv(path1, header=None))
data2 = np.array(data)
num = 0
coordinate = set(data2[:,-1])#共有多少坐标
temp = []
up = 0
down = 0
up_rate = 0
csvFile="F:/DayCandles2017-201807/UpDown.csv"
for pos in coordinate:   #遍历坐标
    for z in range(len(data)):  #筛选和坐标相同的数据
        if  data2[z][-1] == pos: #这一类数目大于20 data2[z][-2]>=20 and
            temp.extend([[data2[z][0],data2[z][1], data2[z][-1]]])#名称，日期，坐标
            num = num+1
    dataAlone = np.array(temp)
    for j in range(len(dataAlone)):
        for i in range(len(FilesList)):  # len(FilesList)
            fileName = FilesList[i]
            if fileName == dataAlone[j][0]:
                #print(dataAlone[j][0])#股票名称
                path2 = os.path.join(FilesPath, fileName)
                data3 = np.array(pd.DataFrame(pd.read_csv(path2, header=0)))
                for k in range(len(data3)):
                    if dateutil.parser.parse(dataAlone[j][1]) == dateutil.parser.parse(data3[k][0]):
                        #print(data3[k][0])#日期
                        if len(data3) - k > 3:
                            if data3[k + 3][4] - data3[k][4] >= 0:
                                up = up + 1
                                if (data3[k + 3][4] - data3[k][4]) / data3[k + 3][4] >= 0.005:
                                    up_rate = up_rate + 1
                                    #print((data3[k + 3][4] - data3[k][4]) / data3[k + 3][4])
                            if data3[k + 3][4] - data3[k][4] < 0:
                                down = down + 1
    print("坐标", pos)
    print("总数量", len(dataAlone))
    print("上涨数量", up)
    print("下降数量", down)
    print("上涨超过0.5%", up_rate)
    print("成功率",format(up/len(dataAlone),'.2%'))
    print("数目",num)
    with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
        text = [pos,len(dataAlone),up,down,up_rate,format(up/len(dataAlone),'.2%')]
        csv.writer(f).writerow(text)
    f.close()
    temp=[]
    up = 0
    down = 0
    up_rate = 0