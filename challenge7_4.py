#!/usr/env/bin python3
# -*- coding:utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
def Temperature():

    df_Global = pd.read_csv('GlobalSurfaceTemperature.csv')
    df_Green = pd.read_csv('GreenhouseGas.csv')
    df_Co2ppm = pd.read_csv('CO2ppm.csv')

    
    df_Green = pd.DataFrame(df_Green[['N2O','CH4','CO2']].values,
            index = pd.to_datetime(df_Green['Year'].astype(str)),
            columns = ['N2O','CH4','CO2']
            )
    df_Global = pd.DataFrame(df_Global[['Median','Upper','Lower']].values,
            index = pd.to_datetime(df_Global['Year'].astype(str)),
            columns = ['Median','Upper','Lower']
            )
    
    df_Co2ppm = pd.DataFrame(df_Co2ppm.iloc[:, 1].values,
            index  = pd.to_datetime(df_Co2ppm['Year'].astype(str)),
            columns = ['CO2_PPM']
            )
    
    df_merge = pd.concat([
        df_Green,df_Co2ppm,df_Global],axis=1)

    print(df_merge)
    #shujutianchong

    feature = df_merge.iloc[:,0:4].fillna(method='ffill').fillna(method='bfill')
    print(feature)

    feature_train = feature['1970-01-01':'2010-01-10']
    feature_test = feature['2011-01-01':'2017-01-01']



    target_Median = df_merge.iloc[:,4]
    target_Median_train = target_Median['1970-01-01':'2010-01-01']
    model_Median = LinearRegression()
    model_Median.fit(feature_train,target_Median_train)
    Media_prediction = model_Median.predict(feature_test)


    target_Upper = df_merge.iloc[:,5]
    target_Upper_train = target_Upper['1970-01-01':'2010-01-01']
    model_Upper = LinearRegression()
    model_Upper.fit(feature_train,target_Upper_train)
    Upper_prediction = model_Upper.predict(feature_test)


    target_Lower = df_merge.iloc[:,6]
    target_Lower_train = target_Lower['1970-01-01':'2010-01-01']
    model_Lower=LinearRegression()
    model_Lower.fit(feature_train,target_Lower_train)
    Lower_prediction = model_Lower.predict(feature_test)
    return  list(Media_prediction),list(Upper_prediction),list(Lower_prediction)



if __name__=="__main__":
    Temperature()





















