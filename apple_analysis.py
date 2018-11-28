#1/usr/env/bin python3
# -*- coding:utf-8 -*-
import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv',header=0)
    index = pd.to_datetime(data.Date)
    df = pd.Series(data.Volume.values,index=index)
    data1= df.resample('Q').sum()
    second_volume=data1.sort_values()[-2]
    second_season=data1[data1==second_volume].index[0]
    return second_volume
if __name__=="__main__":
    print(quarter_volume())
