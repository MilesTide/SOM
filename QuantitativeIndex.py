#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao

import numpy as np
import talib as tb
import pandas as pd
import os

FilesPath = 'F:\DayCandles2017-201807'
FilesList = os.listdir(FilesPath)
for i in range(len(FilesList)):  # len(FilesList)
    fileName = FilesList[i]
    print(fileName)
    if (fileName[0:2].upper() != 'SH' and fileName[0:2].upper() != 'SZ'):
        continue
    path = os.path.join(FilesPath, fileName)
    # date、openPrice	、highPrice、lowPrice、closePrice、turnover、volume
    data = pd.DataFrame(pd.read_csv(path, header=None,
                                    names=['date', 'open', 'high', 'low', 'close', 'turnover','volume']))
    if(len(data)<30):
        print("长度不够",fileName)
        continue
    #计算收盘价的一个简单移动平均数SMA
    #data['SMA'] = tb.SMA(data['close'], timeperiod=6)

    #EMA指标
    #data['EMA'] = tb.EMA(data['close'], timeperiod=30)
    # 重叠指标,计算布林线，三指数移动平均
    #data['BollUpper'], data['BollUpper'], data['BollLower'] = tb.BBANDS(data['close'], matype=tb.MA_Type.T3, timeperiod=6)
    # KDJ 值对应的函数是 STOCH
    #data['KDJ_K'], data['KDJ_D'] = tb.STOCH(data['high'],data['low'], data['close'],fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
    #成交量指标
    #data['AD'] = tb.AD(data['high'], data['low'], data['close'], data['volume'])
    #data['ADOSC'] = tb.ADOSC(data['high'], data['low'], data['close'], data['volume'], fastperiod=3, slowperiod=10)
    #data['OBV'] = tb.OBV(data['close'], data['volume'])
    #data['ADX'] = tb.ADX(data['high'], data['low'], data['close'], timeperiod=14)
    #data['APO'] = tb.APO(data['close'], fastperiod=12, slowperiod=26, matype=0)
    #data['MFI'] = tb.MFI(data['high'], data['low'], data['close'], data['volume'], timeperiod=14)
    #data['MOM'] = tb.MOM(data['close'], timeperiod=10)
    #阿隆指标
    #data['aroondown'],data['aroonup']  = tb.AROON(data['high'], data['low'],timeperiod=25)

    #波动率指标
    #data['ATR'] = tb.ATR(data['high'], data['low'], data['close'], timeperiod=14)
    '''KDJ+RSI+MACD+W&R
    #KDJ与国内显示结果相同
    low_list = data['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=data['low'].expanding().min(), inplace=True)
    high_list = data['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=data['high'].expanding().max(), inplace=True)
    rsv = (data['close'] - low_list) / (high_list - low_list) * 100
    data['K'] = pd.DataFrame(rsv).ewm(com=2).mean()#等同于 k=1/3*K(t)+2/3*K(t-1)
    data['D'] = data['K'].ewm(com=2).mean()
    data['J'] = 3 * data['K'] - 2 * data['D']
    # RSI指标
    data['RSI6'] = tb.RSI(data['close'], timeperiod=6)
    data['RSI12'] = tb.RSI(data['close'], timeperiod=12)
    # 移动平均线指标，MACD指标
    data['MACD'], macdsignal,macdhist = tb.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    # 威廉指标
    data['WILLR'] = tb.WILLR(data['high'], data['low'], data['close'], timeperiod=14)
    # 成交量指标
    #data['ADOSC'] = tb.ADOSC(data['high'], data['low'], data['close'], data['volume'], fastperiod=3, slowperiod=10)
    data.to_csv(path, mode='w', index=False)
    #均线指标
    real = MA(close, timeperiod=30, matype=0)
    
    #KDJ+DMI
    # KDJ与国内显示结果相同
    low_list = data['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=data['low'].expanding().min(), inplace=True)
    high_list = data['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=data['high'].expanding().max(), inplace=True)
    rsv = (data['close'] - low_list) / (high_list - low_list) * 100
    data['K'] = pd.DataFrame(rsv).ewm(com=2).mean()  # 等同于 k=1/3*K(t)+2/3*K(t-1)
    data['D'] = data['K'].ewm(com=2).mean()
    data['J'] = 3 * data['K'] - 2 * data['D']
    #DMI中的ADX和ADXR
    data['ADX'] = tb.ADX(data['high'], data['low'], data['close'], timeperiod=14)
    data['ADXR'] = tb.ADXR(data['high'], data['low'], data['close'], timeperiod=14)
    data.to_csv(path, mode='w', index=False)
    '''
    # KDJ与国内显示结果相同
    low_list = data['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=data['low'].expanding().min(), inplace=True)
    high_list = data['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=data['high'].expanding().max(), inplace=True)
    rsv = (data['close'] - low_list) / (high_list - low_list) * 100
    K = pd.DataFrame(rsv).ewm(com=2).mean()  # 等同于 k=1/3*K(t)+2/3*K(t-1)
    D = K.ewm(com=2).mean()
    data['J'] = 3 * K - 2 * D
    data['J']=round(data['J'],2)
    #成交量上涨
    vol_1 = data['volume'].shift(1)
    data['volChange'] = round((data['volume'] - vol_1) / vol_1, 2)
    data['volChange'].fillna(0, inplace=True)
    # 均线指标
    data['MA10'] = round(tb.MA(data['close'], timeperiod=10, matype=0),2)
    data['MA30'] = round(tb.MA(data['close'], timeperiod=30, matype=0),2)
    data['MA60'] = round(tb.MA(data['close'], timeperiod=60, matype=0),2)

    data['MA10'].fillna(0, inplace=True)
    data['MA30'].fillna(0, inplace=True)
    data['MA60'].fillna(0, inplace=True)
    data.to_csv(path, mode='w', index=False)
print('success')
