#!/usr/env/bin python3
# -*- coding:utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt


def clean_data():
    df_climate = pd.read_excel("ClimateChange.xlsx", sheetname="Data")
    df_temperature = pd.read_excel("GlobalTemperature.xlsx",headr=0)
    df_climate = pd.DataFrame(df_climate).loc[df_climate['Series code'].isin(['EN.ATM.CO2E.KT','EN.ATM.METH.KT.CE','EN.ATM.NOXE.KT.CE','EN.ATM.GHGO.KT.CE','EN.CLC.GHGR.MT.CE'])]

    df_climate.replace({"..":pd.np.nan},inplace=True)
    df_climate = df_climate.iloc[:,6:].fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df_climate.dropna(how='all',inplace=True)
    df_climate_clean = df_climate.sum()
    print(df_climate)
    print(df_climate_clean)

    return df_climate
    


            
if __name__ =="__main__":
    clean_data()
    





