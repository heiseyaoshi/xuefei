#!usr/env/bin python3
# -*- coding:utf-8 -*-
import pandas as pd

def co2():
    df = pd.read_excel("ClimateChange.xlsx",sheetname='Data')
    df = df[df['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    df = df.drop(['Country name','Series code','Series name','SCALE','Decimals'],axis=1)
    df.replace({'..':pd.np.nan},inplace=True)
    df = df.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df.dropna(how='all',inplace=True)
    df['Sum emissions']=df.sum(axis=1)
    df = df['Sum emissions']

    df1 = pd.read_excel("ClimateChange.xlsx",sheetname='Country')
    df1.set_index('Country code',inplace=True)
    df1.drop(['Capital city','Region','Lending category'],axis=1,inplace=True)
    df2 = pd.concat([df,df1],axis=1)

    
    data_sum = df2.groupby('Income group').sum()
    data_max = df2.sort_values(by='Sum emissions',ascending=False).groupby('Income group').head(1).set_index('Income group')
    data_max.columns=['Highest emissions','Highest emission country']
    data_max = data_max.reindex(
            columns=['Highest emission country','Highest emissions'])
    data_min = df2.sort_values(by='Sum emissions').groupby('Income group').head(1).set_index('Income group')
    data_min.columns=['Lowest emissions','Lowest emission country']
    
    data_min = data_min.reindex(
            columns=['Lowest emission country','Lowest emissions'])



    result= pd.concat([data_sum,data_max,data_min],axis=1)
    print(result)
    return result

if __name__=="__main__":
    co2()
