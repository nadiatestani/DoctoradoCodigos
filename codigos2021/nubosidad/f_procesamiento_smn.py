#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 19:48:59 2021

@author: nadia

f_procesamiento_smn.py
"""
#f_procesamiento_smn.py

import pandas as pd
import numpy as np
import os
import datetime as dt
from scipy.interpolate import make_interp_spline
from calendar import monthrange

#calculo media mensual de nubosidad diaria: 
#si hay mas del 20% de datos faltantes se pone na
def media_mensual(id_omm, df_data, ruta_salida, na = 20):
    """ construye serie de media mensual y lo guarda en ruta_salida como .csv
    admite el na% de datos faltantes"""

    data_group=df_data["nub"].groupby(pd.Grouper(freq="M"))
    data_group_media=data_group.mean() #hace la media aunque halla nans, a menos que todo el mes tenga nans
    data_group_faltantes = df_data.isnull().groupby(pd.Grouper(freq="M")).sum()
    data_group_size = data_group.size()
    parametro_porcentaje_na_admitido = 100/na
    posiciones_medias_a_conservar = data_group_faltantes.values <= data_group_size.values // parametro_porcentaje_na_admitido
    # elif na == 
    #me quedo con los meses donde la cantidad de datos faltantes haya sido menor al na% de los datos para el mes
    media = []
    for i, elemento in enumerate(data_group_media):
        if posiciones_medias_a_conservar[i][0] == True and pd.isna(elemento)!=True:
            media.append(elemento) #media.append(round(elemento)) 
        else:
            media.append(np.nan)
    indices=data_group_media.index
    media_mensual_df=pd.DataFrame(media, index = indices)
    media_mensual_df.index.name = "fecha"
    #guardo
    media_mensual_df.to_csv(os.path.join(ruta_salida, f"media_mensual_{id_omm}.csv"))
    return media_mensual_df
    

#armo lista de listas con las frecuencias de cada okta (mensual) para cada anio 
def frecuencia_oktas_por_anio(id_omm, df_data, ruta_salida):
    """ df_data: df con media mensual de nubosidad en cada estacion. es el mensual: la salida de media_mensual() o el diario
    """
    freq_0 = []
    freq_1 = []
    freq_2 = []
    freq_3 = []
    freq_4 = []
    freq_5 = []
    freq_6 = []
    freq_7 = []
    freq_8 = []
    freqs = [freq_0, freq_1, freq_2, freq_3, freq_4, freq_5, freq_6, freq_7, freq_8]
    
    freq_r_0 = []
    freq_r_1 = []
    freq_r_2 = []
    freq_r_3 = []
    freq_r_4 = []
    freq_r_5 = []
    freq_r_6 = []
    freq_r_7 = []
    freq_r_8 = []
    freqs_relativas = [freq_r_0, freq_r_1, freq_r_2, freq_r_3, freq_r_4, freq_r_5, freq_r_6, freq_r_7, freq_r_8]
    
    for anio in df_data.index.year.unique():#iterar sobre los anios
        data = df_data.loc[str(anio)]
        data_values = data.value_counts()
        cantidad_datos = data.count()[0]
        for i in range(0,9):
            if sum(data_values.index == (i,)) != 0:
                freqs[i].append(data_values[(i,)])
                freqs_relativas[i].append(data_values[(i,)]/cantidad_datos*100)
            else:
                freqs[i].append(0)
                freqs_relativas[i].append(0)
                
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_dias_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_dias_{id_omm}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_meses_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_meses_{id_omm}.csv"))
    return freqs_guardo, freqs_relativas_guardo

#armo lista de listas con las frecuencias de cada okta (mensual) para cada estacion
def frecuencia_oktas_por_anio_estaciones(id_omm, df_data, ruta_salida, estacion):
    """ df_data: df con media mensual de nubosidad en cada estacion. es el mensual: la salida de media_mensual() o el diario
    """
    freq_0 = []
    freq_1 = []
    freq_2 = []
    freq_3 = []
    freq_4 = []
    freq_5 = []
    freq_6 = []
    freq_7 = []
    freq_8 = []
    freqs = [freq_0, freq_1, freq_2, freq_3, freq_4, freq_5, freq_6, freq_7, freq_8]
    
    freq_r_0 = []
    freq_r_1 = []
    freq_r_2 = []
    freq_r_3 = []
    freq_r_4 = []
    freq_r_5 = []
    freq_r_6 = []
    freq_r_7 = []
    freq_r_8 = []
    freqs_relativas = [freq_r_0, freq_r_1, freq_r_2, freq_r_3, freq_r_4, freq_r_5, freq_r_6, freq_r_7, freq_r_8]
    
    for anio in df_data.index.year.unique():#iterar sobre los anios
        
        data = df_data.loc[str(anio)]
        
        if estacion == "DJF":
            if anio == df_data.index.year[0]:
                data_estacion = np.nan
            else:
                data_anio_previo = df_data.loc[str(anio-1)]
                data_estacion = pd.concat([data_anio_previo[data_anio_previo.index.month == 12],
                                           data[data.index.month ==1],data[data.index.month == 2]])
                
        elif estacion == "MAM":
            data_estacion = pd.concat([data[data.index.month == 3],data[data.index.month == 4],data[data.index.month == 5]])
        
        elif estacion == "JJA":
            data_estacion = pd.concat([data[data.index.month == 6],data[data.index.month == 7],data[data.index.month == 8]])
           
        elif estacion == "SON":
            data_estacion = pd.concat([data[data.index.month == 9],data[data.index.month == 10],data[data.index.month == 11]])
             
        
        if type(data_estacion) == pd.DataFrame :
            data_estacion = pd.DataFrame(data_estacion)
            data_values = data_estacion.value_counts()
            cantidad_datos = data_estacion.count()[0]
            for i in range(0,9):
                if sum(data_values.index == (i,)) != 0:
                    freqs[i].append(data_values[(i,)])
                    freqs_relativas[i].append(data_values[(i,)]/cantidad_datos*100)
                else:
                    freqs[i].append(0)
                    freqs_relativas[i].append(0)
            
        else:
            for i in range(0,9):
                freqs[i].append(np.nan)
                freqs_relativas[i].append(np.nan)
           
             
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_{estacion}_dias_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_{estacion}_dias_{id_omm}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_{estacion}_meses_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_{estacion}_meses_{id_omm}.csv"))
    return freqs_guardo, freqs_relativas_guardo

#armo lista de listas con las frecuencias de cada okta (mensual) para cada estacion
def frecuencia_oktas_por_anio_meses(id_omm, df_data, ruta_salida, mes):
    """ df_data: df con media mensual de nubosidad en cada estacion. es el mensual: la salida de media_mensual() o el diario
    """
    freq_0 = []
    freq_1 = []
    freq_2 = []
    freq_3 = []
    freq_4 = []
    freq_5 = []
    freq_6 = []
    freq_7 = []
    freq_8 = []
    freqs = [freq_0, freq_1, freq_2, freq_3, freq_4, freq_5, freq_6, freq_7, freq_8]
    
    freq_r_0 = []
    freq_r_1 = []
    freq_r_2 = []
    freq_r_3 = []
    freq_r_4 = []
    freq_r_5 = []
    freq_r_6 = []
    freq_r_7 = []
    freq_r_8 = []
    freqs_relativas = [freq_r_0, freq_r_1, freq_r_2, freq_r_3, freq_r_4, freq_r_5, freq_r_6, freq_r_7, freq_r_8]
    
    for anio in df_data.index.year.unique():#iterar sobre los anios
        data = df_data.loc[str(anio)]
        data_mes = data[data.index.month == mes]
        data_values = data_mes.value_counts()
        cantidad_datos = data_mes.count()[0]
        for i in range(0,9):
            if sum(data_values.index == (i,)) != 0:
                freqs[i].append(data_values[(i,)])
                freqs_relativas[i].append(data_values[i]/cantidad_datos*100)
            else:
                freqs[i].append(0)
                freqs_relativas[i].append(0)
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_mes_{mes}_dias_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_mes_{mes}_dias_{id_omm}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_mes_{mes}_meses_{id_omm}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_mes_{mes}_meses_{id_omm}.csv"))
    return freqs_guardo, freqs_relativas_guardo

def frecuencia_oktas_por_mes(id_omm, df_data, ruta_salida):
    """ 
    df_data: df con media DIARIA de nubosidad en cada estacion. 
    """
    freqs = [[], [], [], [], [], [], [], [], []]
    freqs_relativas = [[], [], [], [], [], [], [], [], []]
    indices = []
    
    for anio in df_data.index.year.unique(): #iterar sobre los anios
        data_anio = df_data.loc[str(anio)]
        for month in data_anio.index.month.unique():
            data_mes = data_anio[data_anio.index.month == month]
            data_mes_values = data_mes.value_counts()
            cantidad_datos_mes = data_mes.count()[0] #ver 
            cantidad_dias_mes = monthrange(anio, month)[1] 
            if cantidad_datos_mes < cantidad_dias_mes * 0.8:
                #si la cantidad de datos del mes es menor al 80% de numero de dias del mes 
                #entonces computo la frecuencia relativa como na 
                for i in range(0,9):
                    freqs_relativas[i].append(np.nan)
               
                    if sum(data_mes_values.index == (i,)) != 0: #si esta el indice en la lista de valores 
                        freqs[i].append(data_mes_values[i])         
                    else:
                        freqs[i].append(0)

            else:
                for i in range(0,9):
                    if sum(data_mes_values.index == (i,)) != 0: #si esta el indice en la lista de valores 
                        freqs[i].append(data_mes_values[i])
                        freqs_relativas[i].append(data_mes_values[i]/cantidad_datos_mes*100)
                    else:
                        freqs[i].append(0)
                        freqs_relativas[i].append(0)
            indices.append(dt.date(anio,month,1))
            
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = indices
    freqs_guardo.index.name = "fecha"
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = indices
    freqs_relativas_guardo.index.name = "fecha"
    
    freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_mensual_en_dias_{id_omm}.csv"))
    freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_mensual_en_dias_{id_omm}.csv"))
    return freqs_guardo, freqs_relativas_guardo


def agrupo_frecuencias(frecuencias, grupo=1):
    if grupo == 1:
        frecuencia_agrupo = pd.concat([frecuencias.iloc[:,0], frecuencias.iloc[:,1]+frecuencias.iloc[:,2],
                                       frecuencias.iloc[:,3]+frecuencias.iloc[:,4],
                                       frecuencias.iloc[:,5]+frecuencias.iloc[:,6],
                                       frecuencias.iloc[:,7]+frecuencias.iloc[:,8]], axis = 1)
        frecuencia_agrupo.columns = ["0", "1-2", "3-4", "5-6","7-8"]
    elif grupo == 2:
        frecuencia_agrupo = pd.concat([frecuencias.iloc[:,0]+frecuencias.iloc[:,1]+frecuencias.iloc[:,2],
                                       frecuencias.iloc[:,3]+frecuencias.iloc[:,4]+frecuencias.iloc[:,5],
                                       frecuencias.iloc[:,6]+frecuencias.iloc[:,7]+frecuencias.iloc[:,8]], axis = 1)
        frecuencia_agrupo.columns = ["0-1-2","3-4-5","6-7-8"]
    
    elif grupo == 3:
        frecuencia_agrupo = pd.concat([frecuencias.iloc[:,0],
                                       frecuencias.iloc[:,1]+frecuencias.iloc[:,2]+frecuencias.iloc[:,3],
                                       frecuencias.iloc[:,4],
                                       frecuencias.iloc[:,5]+frecuencias.iloc[:,6]+frecuencias.iloc[:,7],
                                       frecuencias.iloc[:,8]], axis = 1)
        frecuencia_agrupo.columns = ["0", "1-2-3","4","5-6-7", "8"]
    return frecuencia_agrupo


def agrupo_data(df_data, grupo = 1):
    if grupo == 1:
        agrupo = []
        for i in range(0,len(df_data["nub"])):
            if df_data["nub"][i] == 0:
                agrupo.append(0)
            elif df_data["nub"][i] == 1 or df_data["nub"][i] == 2:
                agrupo.append(1)
            elif df_data["nub"][i] == 3 or df_data["nub"][i] == 4:
                agrupo.append(2)
            elif df_data["nub"][i] == 5 or df_data["nub"][i] == 6:
                agrupo.append(3)
            elif df_data["nub"][i] == 7 or df_data["nub"][i] == 8:
                agrupo.append(4)
            else:
                agrupo.append(np.nan)
                    
        agrupo = pd.DataFrame(agrupo).set_index(df_data.index)
        agrupo.columns = ["nub"]
        
    elif grupo == 2:
        agrupo = []
        for i in range(0,len(df_data["nub"])):
            if df_data["nub"][i] == 0 or df_data["nub"][i] == 1 or df_data["nub"][i] == 2:
                agrupo.append(0)
            elif df_data["nub"][i] == 3 or df_data["nub"][i] == 4 or df_data["nub"][i] == 5:
                agrupo.append(1)
            elif df_data["nub"][i] == 6 or df_data["nub"][i] == 7 or df_data["nub"][i] == 8:
                agrupo.append(2)
            else:
                agrupo.append(np.nan)
                    
        agrupo = pd.DataFrame(agrupo).set_index(df_data.index)
        agrupo.columns = ["nub"]
    
    return agrupo
