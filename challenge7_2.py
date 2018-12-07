#!usr/env/bin python3
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def co2_gdp_plot():
    df = pd.read_excel("ClimateChange.xlsx",sheetname ='Data')
    df1=df[df['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    df2=df[df['Series code']=='NY.GDP.MKTP.CD'].set_index('Country code')
    ''' 
    df1= df1.drop(['Country name','Series name','SCALE','Decimals'],axis=1)
    df2= df2.drop(['Country name','Series name','SCALE','Decimals'],axis=1)
    '''
    df1.replace({'..':pd.np.nan},inplace=True)
    df2.replace({'..':pd.np.nan},inplace=True)
    df1=df1.iloc[:,5:].fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df2=df2.iloc[:,5:].fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df1.dropna(how='all',inplace=True)
    df2.dropna(how='all',inplace=True)
    print(df1)
    
    
    df1['CO2.SUM']=df1.sum(axis=1)
    df2['GDP.SUM']=df2.sum(axis=1)
    df1 = df1['CO2.SUM']
    df2 = df2['GDP.SUM']
    
    print(df1)

    df3 = pd.concat([df1,df2],axis=1)
    df3 = df3.fillna(value=0)
    df_norm=(df3-df3.min())/(df3.max()-df3.min())
    china =[]
    for i in df_norm[df_norm.index == 'CHN'].values:
        china.extend(np.round(i,3).tolist())

    countries_labels= ['CHN','USA','GBR','FRA','RUS']

    sticks_labels =[]

    labels_position = []


    for i in range(len(df_norm)):
        if df_norm.index[i] in countries_labels:
            sticks_labels.append(df_norm.index[i])
            labels_position.append(i)

    fig = plt.subplot()

    df_norm.plot(kind='line',title='GDP-CO2',ax=fig)
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.xticks(labels_position,sticks_labels,rotation='vertical')
    plt.show()

    return fig,china





if __name__ == "__main__":
    co2_gdp_plot()



    


    
