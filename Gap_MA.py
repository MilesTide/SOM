# -*- coding: utf-8 -*-
# coding: utf-8
import os
import pandas as pd
import csv
import talib
import numpy as np
import dateutil.parser

def ProcessData(name):
    #读取股票名称文件
    way= 'F:\DayCandles2017-201807\HammerList.csv'
    object = pd.DataFrame(pd.read_csv(way, header=0))
    object = np.array(object)
    for k in range(len(object)):
        objectName = object[k][0]
        objectDate = object[k][1]
        #和总文件比对，如果相同，提取出来记录到ExtractData.csv中
        csvFile = os.path.join(FilesPath,name)
        path = os.path.join(FilesPath, objectName)
        df = pd.DataFrame(pd.read_csv(path, header=0))
        data = np.array(df)
        for j in range(len(data)):  #控制文件内部循环
            fileDate = data[j][0]
            if(dateutil.parser.parse(fileDate)==dateutil.parser.parse(objectDate)):
                print(fileDate)
                if len(data) - j > 3:
                    a=min(data[j - 2][4],data[j - 2][1])-max(data[j - 3][4],data[j - 3][1])
                    b=min(data[j - 1][4],data[j - 1][1])-max(data[j - 2][4],data[j - 2][1])
                    c=min(data[j][4],data[j][1])-max(data[j - 1][4],data[j - 1][1])
                    d=max(a,b,c)
                    if data[j + 3][4] - data[j][4] >= 0 and d >0 :#连续三天看涨,并且有缺口
                        with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
                            text = [objectName, data[j][0],1,data[j][-5], data[j][-4], data[j][-3], data[j][-2], data[j][-1],1]
                            csv.writer(f).writerow(text)
                        f.close()
                        break
                    if data[j + 3][4] - data[j][4] >= 0 and d <=0 :#连续三天看涨,并且没有缺口
                        with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
                            text = [objectName, data[j][0],1,data[j][-5], data[j][-4], data[j][-3], data[j][-2], data[j][-1],0]
                            csv.writer(f).writerow(text)
                        f.close()
                        break
                    if data[j + 3][4] - data[j][4] < 0 and d>0:#连续三天看跌,并且有缺口
                        with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
                            text = [objectName, data[j][0], 0, data[j][-5], data[j][-4], data[j][-3], data[j][-2], data[j][-1],1]
                            csv.writer(f).writerow(text)
                        f.close()
                        break
                    if data[j + 3][4] - data[j][4] < 0 and d<=0:#连续三天看跌,并且没有缺口
                        with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
                            text = [objectName, data[j][0], 0, data[j][-5], data[j][-4], data[j][-3], data[j][-2], data[j][-1],0]
                            csv.writer(f).writerow(text)
                        f.close()
                        break
if __name__ == '__main__':
    FilesPath = 'F:\DayCandles2017-201807'
    FilesList = os.listdir(FilesPath)
    ProcessData('ExtractDataT.csv')#传你要写入的文件名

