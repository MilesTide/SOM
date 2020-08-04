# -*- coding: utf-8 -*-
# coding: utf-8
import pandas as pd
import numpy as np
import csv

way1= "F:\DayCandles2017-201807\zuobiao.csv"
way2= "F:/DayCandles2017-201807/UpDown.csv"
csvFile="F:\DayCandles2017-201807\五万.csv"
data1 = pd.DataFrame(pd.read_csv(way1,header=None))
data2 = pd.DataFrame(pd.read_csv(way2,header=None))
data3 = np.array(data1)
data4 = np.array(data2)

for pos1 in data4:
    for pos2 in data3:
        if(pos1[0]==pos2[-1]):
            with open(csvFile,'a',newline='') as f:
                text=[pos2[0],pos2[1],pos1[0],pos1[1],pos1[2],pos1[3],pos1[4]]
                csv.writer(f).writerow(text)
            f.close()


