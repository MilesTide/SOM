#!/usr/bin/env python 
# -*- coding:utf-8 -*-
'''
处理2017-2018.07的数据
'''
import os
import pandas as pd
import csv
import talib
import numpy as np

def Ma_Down(array):
    if(array[-6]>array[-5]>array[-4]>array[-3]>array[-2]>array[-1]):
        return 1
    else:
        return 0

def Ma_Up(array):
    if(array[-6]>array[-5]<array[-4]<array[-3]<array[-2]<array[-1]):
        return 1
    else:
        return 0

def Creat_csv(name):
    csvFile = os.path.join(FilesPath,name)
    with open(csvFile,'w',newline='') as f:
        csv_write = csv.writer(f)
        header = ['StockNumber','Date']
        csv_write.writerow(header)
        f.close()

def ProcessData(name):
    csvFile = os.path.join(FilesPath,name)
    flag = 0
    for i in range(len(FilesList)):  # len(FilesList)
        fileName = FilesList[i]
        print(fileName)
        if (fileName[0:2].upper() != 'SH' and fileName[0:2].upper() != 'SZ'):
            continue
        path = os.path.join(FilesPath, fileName)
        data = pd.DataFrame(pd.read_csv(path, header=None))
        temp = 10000000# temp用来记录满足达到涨幅条件那一天，初始值给一个超大值防止影响数据运行
        for j in range(len(data.loc[:, 0])):  #控制文件内部循环
            if (temp <= j <= temp + 7 or j<=10):  # 看涨七天内的数据不再记录
                continue
            fileDate = data[0][j]
            openPrice = data[1][j]
            highPrice = data[2][j]
            lowPrice = data[3][j]
            lastPrice = data[4][j]
            if(openPrice> lastPrice):#绿线，下跌
                upperShadow = highPrice - openPrice
                lowerShadow = lastPrice - lowPrice
                realBody = openPrice - lastPrice
            else:#红线，上涨
                upperShadow = highPrice - lastPrice
                lowerShadow = openPrice - lowPrice
                realBody = lastPrice - openPrice

            #锤子线
            if ((lowerShadow >= 2 * (upperShadow + realBody)) and (realBody > 2 * upperShadow) and (realBody > 0.1 * (highPrice - lowPrice))):
                data5 = data[4][j-11:j-1]
                print(fileName)
                print(j)
                ma = talib.MA(data5,timeperiod=5)
                ma = np.array(ma)

                if(Ma_Down(ma) or Ma_Up(ma)):#连续下降或者上升
                    with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
                        text = [fileName,fileDate]
                        csv.writer(f).writerow(text)
                    f.close()
                    temp = j #开始监控涨幅数据，此标记七天之后的数据不再检测
                    flag = flag + 1
                else:
                    continue
    print(flag)


if __name__ == '__main__':
    #FilesPath = 'E:\DayCandles2017-201807\DayCandles2017-201807'
    FilesPath ='E:\元数据DayCandles2017-201807'
    FilesList = os.listdir(FilesPath)
    Creat_csv('HammerList.csv')#不要忘了后缀名
    ProcessData('HammerList.csv')#传你要写入的文件名