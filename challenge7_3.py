#!/usr/env/bin python3
# -*- coding:utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt


def clean_data():
    df_climate = pd.read_excel("ClimateChange.xlsx")
    df_temperature = pd.read_excel("GlobalTemperature.xlsx")
    df_climate = pd.DataFrame(df_climate).loc[df_climate['Series code'].isin(['EN.ATM.CO2E.KT','EN.ATM.METH.KT.CE','EN.ATM.NOXE.KT.CE','EN.ATM.GHGO.KT.CE','EN.CLC.GHGR.MT.CE'])]

    df_climate.replace({"..":pd.np.nan},inplace=True)
    df_climate = df_climate.iloc[:,6:].fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    del df_climate[df_climate.columns[-1]]
    df_climate_clean = df_climate.sum()
    df_climate_clean.index = pd.to_datetime(df_climate_clean.index,format='%Y')
    time_index =pd.to_datetime( df_temperature['Date'])
    data_temperature_clean = pd.DataFrame(df_temperature.iloc[:,[1,4]].values,
            index = time_index,
            columns = ['Land Max Temperature','Land And Ocean Average Temperature']
            )
    data_temperature_A = data_temperature_clean.resample('A').mean()
    data_temperature_Q = data_temperature_clean.resample('Q').mean()
    data_clean = data_temperature_A.loc['1990-12-31':'2010-12-31']
    df = pd.concat([data_clean.reset_index(), df_climate_clean.loc['1990':'2010'].reset_index()],axis=1)

    df_clean = pd.DataFrame(df.iloc[:,[1,2,4]].values,
            index = df['index'],
            columns =['Land Average Temperature','Land Max Temperature','Total GHG']
            )
    df_max_min = (df_clean-df_clean.min())/(df_clean.max()-df_clean.min())
    
    

    return  df_max_min,data_temperature_Q





def climate_plot():
    df_max_min, data_temperature_Q = clean_data()

    fig,axes = plt.subplots(nrows=2,ncols=2)
    ax1 = df_max_min.plot(
            kind='line',
            figsize=(16,9),
            ax= axes[0,0]
            )
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Values')

    df_max_min.index = [i.year for i in df_max_min.index]
    ax2 = df_max_min.plot(
            kind='bar',
            figsize=(16,9),
            ax = axes[0,1], 
            )
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Values')

    ax3 = data_temperature_Q.plot(
            kind ='area',
            figsize=(16,9),
            ax = axes[1,0]
            )
    ax3.set_xlabel('Ouarters')
    ax3.set_ylabel('Temperature')

    ax4 = data_temperature_Q.plot(
            kind = 'kde',
            figsize=(16,9),
            ax = axes[1,1]
            )
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')
    plt.show()
    return fig
            
if __name__ =="__main__":
   print(climate_plot())
