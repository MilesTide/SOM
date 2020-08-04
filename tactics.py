# -*- coding: utf-8 -*-
# coding: utf-8
import numpy as np
import talib as tb
import pandas as pd
import os
path = 'F:\DayCandles2017-201807\ExtractDataT.csv'
# 'date',J,MA10,MA30,MA60，volChange,gap这里修改指标
data = pd.DataFrame(pd.read_csv(path, header=None,names=['name','date', 'success','higherShadows','lowerShadows','body','J','volChange', 'MA10', 'MA30', 'MA60']))
dataA=np.array(data)
path2 = 'F:\DayCandles2017-201807\ExtractData.csv'
# 'date',J,MAOrder，volChange
data2 = pd.DataFrame(pd.read_csv(path, header=None))
temp=[]
data2['name']=data['name']
data2['date']=data['date']
data2['success']=data['success']
data2['higherShadows']=data['higherShadows']
data2['lowerShadows']=data['lowerShadows']
data2['body']=data['body']
data2['J']=data['J']
data2['volChange']=data['volChange']
#data2['gap']=data['gap']
for i in range(len(data)):
    if dataA[i][-4] >=dataA[i][-3] >=dataA[i][-2]:#MA10>MA30>MA60
        temp.append(1)
    elif dataA[i][-4] >=dataA[i][-2] >=dataA[i][-3]:#MA10>MA60>MA30
        temp.append(2)
    elif dataA[i][-3] >= dataA[i][-4] >= dataA[i][-2]:#MA30>MA10>MA60
        temp.append(3)
    elif dataA[i][-3] >= dataA[i][-2] >= dataA[i][-4]:#MA30>MA60>MA10
        temp.append(4)
    elif dataA[i][-2] >= dataA[i][-4] >= dataA[i][-3]:#MA60>MA10>MA30
        temp.append(5)
    elif dataA[i][-2] >= dataA[i][-3] >= dataA[i][-4]:#MA60>MA30>MA10
        temp.append(6)
data2['MAOrder']=pd.DataFrame(temp)
data2.to_csv(path2, mode='w', index=False)
print(len(temp))
print('Success')