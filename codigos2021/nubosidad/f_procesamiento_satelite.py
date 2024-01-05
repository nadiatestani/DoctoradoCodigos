#f_procesamiento_satelite.py

import pandas as pd
import numpy as np
import os
import datetime as dt
from scipy.interpolate import make_interp_spline
import xarray as xr
import pymannkendall as mk
import scipy

#armo lista de listas con las frecuencias de cada okta (mensual) para cada anio 
def frecuencia_oktas_por_anio(lon, lat, df_data, ruta_salida):
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
        data = df_data.loc[str(anio)]["cldamt_oktas"]
        cantidad_datos = len(data)
        data_values = data.value_counts()
        
        for i in range(0,9):
            if i in data_values.index:
                freqs[i].append(data_values[i])
                freqs_relativas[i].append(data_values[i]/cantidad_datos*100)
            else:
                freqs[i].append(0)
                freqs_relativas[i].append(0)
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    freqs_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    freqs_relativas_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_dias_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_dias_{lon}_{lat}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_meses_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_meses_{lon}_{lat}.csv"))
    return freqs_guardo, freqs_relativas_guardo

#armo lista de listas con las frecuencias de cada okta (mensual) para cada estacion
def frecuencia_oktas_por_anio_estaciones(lon, lat, df_data, ruta_salida, estacion):
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
    
    for anio in df_data.index.year.unique():
        data = df_data.loc[str(anio)]["cldamt_oktas"]
        
        if estacion == "DJF":
            if anio == df_data.index.year[0]:
                data_estacion = np.nan
            else:
                data_anio_previo = df_data.loc[str(anio-1)]["cldamt_oktas"] 
                data_estacion = pd.concat([data_anio_previo[data_anio_previo.index.month == 12],data[data.index.month == 1],
                                           data[data.index.month == 2]])
            
        elif estacion == "MAM":
            data_estacion = pd.concat([data[data.index.month == 3],data[data.index.month == 4],data[data.index.month == 5]])
           
        elif estacion == "JJA":
            data_estacion = pd.concat([data[data.index.month == 6],data[data.index.month == 7],data[data.index.month == 8]])
            
        elif estacion == "SON":
            data_estacion = pd.concat([data[data.index.month == 9],data[data.index.month == 10],data[data.index.month == 11]])
        
        if estacion == "DJF" and anio == df_data.index.year[0]:
            for i in range(0,9):
                freqs[i].append(np.nan)
                freqs_relativas[i].append(np.nan)
        
        else:
            data_values = data_estacion.value_counts()
            cantidad_datos =  len(data_estacion)
            for i in range(0,9):
                if i in data_values.index:
                    freqs[i].append(data_values[i])
                    freqs_relativas[i].append(data_values[i]/cantidad_datos*100)
                else:
                    freqs[i].append(0)
                    freqs_relativas[i].append(0)
        
                
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    freqs_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    freqs_relativas_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_{estacion}_dias_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_{estacion}_dias_{lon}_{lat}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_{estacion}_meses_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_{estacion}_meses_{lon}_{lat}.csv"))
    return freqs_guardo, freqs_relativas_guardo

#armo lista de listas con las frecuencias de cada okta (mensual) para cada estacion
def frecuencia_oktas_por_anio_meses(lon, lat, df_data, ruta_salida, mes):
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
        data = df_data.loc[str(anio)]["cldamt_oktas"]
        data_mes = data[data.index.month == mes]
        cantidad_datos =  len(data_mes)
        data_values = data_mes.value_counts()
        for i in range(0,9):
            if i in data_values.index:
                freqs[i].append(data_values[i])
                freqs_relativas[i].append(data_values[i]/cantidad_datos*100)
            else:
                freqs[i].append(0)
                freqs_relativas[i].append(0)
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = df_data.index.year.unique()
    freqs_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = df_data.index.year.unique()
    freqs_relativas_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    #si los datos son diarios:
    if df_data.index[1]-df_data.index[0] == dt.timedelta(1) :
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_mes_{mes}_dias_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_mes_{mes}_dias_{lon}_{lat}.csv"))
    #si los datos son mensuales:
    else: 
        freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_anual_mes_{mes}_meses_{lon}_{lat}.csv"))
        freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_anual_mes_{mes}_meses_{lon}_{lat}.csv"))
    return freqs_guardo, freqs_relativas_guardo

def frecuencia_oktas_por_mes(lon, lat, df_data, ruta_salida):
    """ df_data: df con media DIARIA de nubosidad en cada estacion
    """
    freqs = [[], [], [], [], [], [], [], [], []]
    freqs_relativas = [[], [], [], [], [], [], [], [], []]
    indices = []
    
    #df_data.index = pd.to_datetime(df_data.index)

    for anio in df_data.index.year.unique():
        data_anio = df_data.loc[str(anio)]

        for month in data_anio.index.month.unique():
            data_mes = data_anio[data_anio.index.month == month]["cldamt_oktas"]
            data_mes_values = data_mes.value_counts()
            cantidad_datos_mes = data_mes.count()
            for i in range(0,9):
                    if sum(data_mes_values.index == i) != 0:
                        freqs[i].append(data_mes_values[i])
                        freqs_relativas[i].append(data_mes_values[i]/cantidad_datos_mes*100)
                    else:
                        freqs[i].append(0)
                        freqs_relativas[i].append(0)
            indices.append(dt.date(anio,month,1))
        
    freqs_guardo = pd.DataFrame(freqs).T
    freqs_guardo.index = indices
    freqs_guardo.index.name = "fecha"
    freqs_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    freqs_relativas_guardo = pd.DataFrame(freqs_relativas).T
    freqs_relativas_guardo.index = indices
    freqs_relativas_guardo.index.name = "fecha"
    freqs_relativas_guardo.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    freqs_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_mensual_en_dias_{lon}_{lat}.csv"))
    freqs_relativas_guardo.to_csv(os.path.join(ruta_salida, f"frecuencia_relativa_mensual_en_dias_{lon}_{lat}.csv"))
    return freqs_guardo, freqs_relativas_guardo

def agrupo_frecuencias(frecuencias, grupo = 1):
    if grupo == 1:
        frecuencia_agrupo = pd.concat([frecuencias.iloc[:,0], frecuencias.iloc[:,1]+frecuencias.iloc[:,2],
                                       frecuencias.iloc[:,3] + frecuencias.iloc[:,4], 
                                       frecuencias.iloc[:,5] + frecuencias.iloc[:,6],
                                       frecuencias.iloc[:,7] + frecuencias.iloc[:,8]], axis = 1)
        frecuencia_agrupo.columns = ["0", "1-2", "3-4", "5-6", "7-8"]
    else:
        frecuencia_agrupo = pd.concat([frecuencias.iloc[:,0]+frecuencias.iloc[:,1]+frecuencias.iloc[:,2],
                                       frecuencias.iloc[:,3]+frecuencias.iloc[:,4]+frecuencias.iloc[:,5],
                                       frecuencias.iloc[:,6]+frecuencias.iloc[:,7]+frecuencias.iloc[:,8]], axis = 1)
        frecuencia_agrupo.columns = ["0-1-2", "3-4-5", "6-7-8"]
    return frecuencia_agrupo

def agrupo_data(df_data, grupo = 1):
    if grupo == 1:
        agrupo = []
        for i in range(0,len(df_data["cldamt_oktas"])):
            if df_data["cldamt_oktas"][i] == 0:
                agrupo.append(0)
            elif df_data["cldamt_oktas"][i] == 1 or df_data["cldamt_oktas"][i] == 2:
                agrupo.append(1)
            elif df_data["cldamt_oktas"][i] == 3 or df_data["cldamt_oktas"][i] == 4:
                agrupo.append(2)
            elif df_data["cldamt_oktas"][i] == 5 or df_data["cldamt_oktas"][i] == 6:
                agrupo.append(3)
            elif df_data["cldamt_oktas"][i] == 7 or df_data["cldamt_oktas"][i] == 8:
                agrupo.append(4)
            else:
                agrupo.append(np.nan)
                    
        agrupo = pd.DataFrame(agrupo).set_index(df_data.index)
        agrupo.columns = ["cldamt_oktas"]
        
    elif grupo == 2:
        agrupo = []
        for i in range(0,len(df_data["cldamt_oktas"])):
            if df_data["cldamt_oktas"][i] == 0 or df_data["cldamt_oktas"][i] == 1 or df_data["cldamt_oktas"][i] == 2:
                agrupo.append(0)
            elif df_data["cldamt_oktas"][i] == 3 or df_data["cldamt_oktas"][i] == 4 or df_data["cldamt_oktas"][i] == 5:
                agrupo.append(1)
            elif df_data["cldamt_oktas"][i] == 6 or df_data["cldamt_oktas"][i] == 7 or df_data["cldamt_oktas"][i] == 8:
                agrupo.append(2)
            else:
                agrupo.append(np.nan)
                    
        agrupo = pd.DataFrame(agrupo).set_index(df_data.index)
        agrupo.columns = ["cldamt_oktas"]
    return agrupo

def cldamt_tipo(xrdata, tipo = "BAJAS"):
    if tipo == "BAJAS":
        #cldamt_tipo = xrdata["cldamt_types"].loc[dict(lev_3=slice(0, 6))]
        cldamt_tipo = xrdata["cldamt_types"].loc[dict(lev_3 = 1)] + xrdata["cldamt_types"].loc[dict(lev_3 = 2)] + xrdata["cldamt_types"].loc[dict(lev_3 = 3)] + xrdata["cldamt_types"].loc[dict(lev_3 = 4)] + xrdata["cldamt_types"].loc[dict(lev_3 = 5)] + xrdata["cldamt_types"].loc[dict(lev_3 = 6)]
        
    elif tipo == "MEDIAS":
        cldamt_tipo = xrdata["cldamt_types"].loc[dict(lev_3 = 7)] + xrdata["cldamt_types"].loc[dict(lev_3 = 8)] + xrdata["cldamt_types"].loc[dict(lev_3 = 9)] + xrdata["cldamt_types"].loc[dict(lev_3 = 10)] + xrdata["cldamt_types"].loc[dict(lev_3 = 11)] + xrdata["cldamt_types"].loc[dict(lev_3 = 12)]
        
    elif tipo == "ALTAS":
        cldamt_tipo = xrdata["cldamt_types"].loc[dict(lev_3 = 13)] + xrdata["cldamt_types"].loc[dict(lev_3 = 14)] + xrdata["cldamt_types"].loc[dict(lev_3 = 15)] + xrdata["cldamt_types"].loc[dict(lev_3 = 16)] + xrdata["cldamt_types"].loc[dict(lev_3 = 17)] + xrdata["cldamt_types"].loc[dict(lev_3 = 18)]
        
    else:
        raise ValueError ("Solo puede ser tipo BAJAS MEDIAS o ALTAS")
    return cldamt_tipo



# %% Calculos estadisticos: funcion. Media y desvio climatologico anual, por mes y por estacion.
def calculo_media_isccp(xrdata, mensual = False, estacional = False):
    
    if mensual == False and estacional == False:
        media = xrdata.mean(dim = "time", skipna = True, keep_attrs = True)
    
    elif mensual == True and estacional == False:
        meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        media = dict()
        for mes in meses:
            fechas_mes = xrdata.time[pd.to_datetime(xrdata.time).month == mes]
            xrdata_mes = xrdata.loc[dict(time = fechas_mes)]
            media[mes] = xrdata_mes.mean(dim = "time", skipna = True, keep_attrs = True)
        
    elif estacional == True and mensual == False: 
        fechas_DJF = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 12], xrdata.time[pd.to_datetime(xrdata.time).month == 1], xrdata.time[pd.to_datetime(xrdata.time).month == 2]))  
        fechas_MAM = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 3] , xrdata.time[pd.to_datetime(xrdata.time).month == 4], xrdata.time[pd.to_datetime(xrdata.time).month == 5]))
        fechas_JJA = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 6], xrdata.time[pd.to_datetime(xrdata.time).month == 7], xrdata.time[pd.to_datetime(xrdata.time).month == 8]))
        fechas_SON = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 9], xrdata.time[pd.to_datetime(xrdata.time).month == 10], xrdata.time[pd.to_datetime(xrdata.time).month == 11]))
        
        xrdata_DJF = xrdata.loc[dict(time = fechas_DJF)]
        xrdata_MAM = xrdata.loc[dict(time = fechas_MAM)]
        xrdata_JJA = xrdata.loc[dict(time = fechas_JJA)]
        xrdata_SON = xrdata.loc[dict(time = fechas_SON)]
        
        media = {"DJF": xrdata_DJF.mean(dim = "time", skipna = True, keep_attrs = True), 
                 "MAM": xrdata_MAM.mean(dim = "time", skipna = True, keep_attrs = True), 
                 "JJA": xrdata_JJA.mean(dim = "time", skipna = True, keep_attrs = True), 
                 "SON": xrdata_SON.mean(dim = "time", skipna = True, keep_attrs = True)}
    return media 

def calculo_medias_estaciones(xrdata, estacion = "DJF"):
    #VER ESTO como sacar la condicion de que descarte el primer anio!!! 
    serie_fechas = pd.to_datetime(xrdata.time)
    xr_medias_estacion_list =  [] #donde se van acomodando los datos
    for anio in serie_fechas.year.unique():#iterar sobre los anios
        data_anio = xrdata.loc[dict(time = xrdata.time[serie_fechas.year == anio])]
        #data_anio = xrdata.sel[dict(time = xrdata.time[serie_fechas.year == anio])]
        
        if estacion == "DJF":
            try:
                data_anio_previo = xrdata.loc[dict(time = xrdata.time[serie_fechas.year == anio-1])]
                Dec = data_anio_previo[pd.to_datetime(data_anio_previo.time).month == 12]
                Jan = data_anio[pd.to_datetime(data_anio.time).month == 1]
                Feb = data_anio[pd.to_datetime(data_anio.time).month == 2]
                data_estacion = xr.concat((Dec,Jan,Feb), dim = "time")               
                data_media_estacion = data_estacion.mean(dim = "time", skipna = True, keep_attrs = True)
                data_media_estacion.attrs['time'] = anio
                xr_medias_estacion_list.append(data_media_estacion)
            except IndexError as e:
                print(f"No estan los datos para {anio} para {estacion}, devuelve este error:{e}")
                data_media_estacion = np.nan

        elif estacion == "MAM":
            try:
                Mar = data_anio[pd.to_datetime(data_anio.time).month == 3]
                Abr = data_anio[pd.to_datetime(data_anio.time).month == 4]
                May = data_anio[pd.to_datetime(data_anio.time).month == 5]
                data_estacion = xr.concat((Mar,Abr,May), dim = "time")                 
                data_media_estacion = data_estacion.mean(dim = "time", skipna = True, keep_attrs = True)
                data_media_estacion.attrs['time'] = anio
                xr_medias_estacion_list.append(data_media_estacion)
            except IndexError as e:
                print(f"No estan los datos para {anio} para {estacion}, devuelve este error:{e}")
                data_media_estacion = np.nan
                
        elif estacion == "JJA":
            try:
                Jun = data_anio[pd.to_datetime(data_anio.time).month == 6]
                Jul = data_anio[pd.to_datetime(data_anio.time).month == 7]
                Ag = data_anio[pd.to_datetime(data_anio.time).month == 8]
                data_estacion = xr.concat((Jun, Jul, Ag), dim = "time")                     
                data_media_estacion = data_estacion.mean(dim = "time", skipna = True, keep_attrs = True)
                data_media_estacion.attrs['time'] = anio
                xr_medias_estacion_list.append(data_media_estacion)
                
            except IndexError as e:
                print(f"No estan los datos para {anio} para {estacion}, devuelve este error:{e}")
                data_media_estacion = np.nan
            
            
        elif estacion == "SON":
            try:
                Sep = data_anio[pd.to_datetime(data_anio.time).month == 9]
                Oct = data_anio[pd.to_datetime(data_anio.time).month == 10]
                Nov = data_anio[pd.to_datetime(data_anio.time).month == 11]
                data_estacion = xr.concat((Sep,Oct,Nov), dim = "time")                     
                data_media_estacion = data_estacion.mean(dim = "time", skipna = True, keep_attrs = True)
                data_media_estacion.attrs['time'] = anio
                xr_medias_estacion_list.append(data_media_estacion)
            except IndexError as e:
                print(f"No estan los datos para {anio} para {estacion}, devuelve este error:{e}")
                data_media_estacion = np.nan
            
    xr_medias_estacion = xr.concat(xr_medias_estacion_list, dim = "time")
    return xr_medias_estacion
    
def calculo_desvio_isccp(xrdata, mensual = False, estacional = False):
    
    if mensual == False and estacional == False:
        desvio = xrdata.std(dim = "time", skipna = True, keep_attrs = True)
    
    elif mensual == True and estacional == False:
        meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        desvio = dict()
        for mes in meses:
            fechas_mes = xrdata.time[pd.to_datetime(xrdata.time).month == mes]
            xrdata_mes = xrdata.loc[dict(time = fechas_mes)]
            desvio[mes] = xrdata_mes.std(dim = "time", skipna = True, keep_attrs = True)
        
    elif estacional == True and mensual == False: 
        fechas_DJF = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 12], xrdata.time[pd.to_datetime(xrdata.time).month == 1], xrdata.time[pd.to_datetime(xrdata.time).month == 2]))  
        fechas_MAM = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 3] , xrdata.time[pd.to_datetime(xrdata.time).month == 4], xrdata.time[pd.to_datetime(xrdata.time).month == 5]))
        fechas_JJA = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 6], xrdata.time[pd.to_datetime(xrdata.time).month == 7], xrdata.time[pd.to_datetime(xrdata.time).month == 8]))
        fechas_SON = np.concatenate(( xrdata.time[pd.to_datetime(xrdata.time).month == 9], xrdata.time[pd.to_datetime(xrdata.time).month == 10], xrdata.time[pd.to_datetime(xrdata.time).month == 11]))
        
        xrdata_DJF = xrdata.loc[dict(time = fechas_DJF)]
        xrdata_MAM = xrdata.loc[dict(time = fechas_MAM)]
        xrdata_JJA = xrdata.loc[dict(time = fechas_JJA)]
        xrdata_SON = xrdata.loc[dict(time = fechas_SON)]
        
        desvio = {"DJF": xrdata_DJF.std(dim = "time", skipna = True, keep_attrs = True), 
                 "MAM": xrdata_MAM.std(dim = "time", skipna = True, keep_attrs = True), 
                 "JJA": xrdata_JJA.std(dim = "time", skipna = True, keep_attrs = True), 
                 "SON": xrdata_SON.std(dim = "time", skipna = True, keep_attrs = True)}
        
    return desvio


def tendencia_puntual(xrdata, lon, lat):
    
    valores = xrdata.loc[dict(lon = lon, lat = lat)][np.isfinite(xrdata.loc[dict(lon = lon, lat = lat)])]
    fechas = np.arange(0, len(xrdata.time), 1)[np.isfinite(xrdata.loc[dict(lon = lon, lat = lat)])]
    
    # si el vector es todo de nan entonces que no calcule la tendencia, y que devuelva nan
    if valores.size <= 1:
        tendencia = np.nan
        significativo = np.nan
        
    # si el vector tiene valores distintos de nan calcula tendencia y significancia
    elif valores.size > 1:
        coef = np.polyfit(fechas, valores, 1)
        tendencia = coef[0]  # dada entre un intervalo de tiempo. A esta salida si quiero tendencia decadal e ingrese datos de toda la serie mensual lo multiplico por 10*12 y si quiero por decada y vienen dados por un dato anual se multiplica por 10
        z_test = mk.original_test(valores, alpha = 0.05)[3]
        if abs(z_test) >= 1.96:
            significativo = True
        elif abs(z_test) < 1.96:
            significativo = False
    return(tendencia, significativo)

def tendencia_puntual_theil_sen(xrdata, lon, lat):
    
    valores = xrdata.loc[dict(lon = lon, lat = lat)][np.isfinite(xrdata.loc[dict(lon = lon, lat = lat)])]
    fechas = np.arange(0, len(xrdata.time), 1)[np.isfinite(xrdata.loc[dict(lon = lon, lat = lat)])]
    
    # si el vector es todo de nan entonces que no calcule la tendencia, y que devuelva nan
    if valores.size <= 1:
        tendencia = np.nan
        significativo = np.nan
        
    # si el vector tiene valores distintos de nan calcula tendencia y significancia
    elif valores.size > 1:
        coef = scipy.stats.mstats.theilslopes(y=valores, x=fechas, alpha=0.95)
        tendencia = coef[0]  # dada entre un intervalo de tiempo. A esta salida si quiero tendencia decadal e ingrese datos de toda la serie mensual lo multiplico por 10*12 y si quiero por decada y vienen dados por un dato anual se multiplica por 10
        coord_origen = coef[1]
        z_test = mk.original_test(valores, alpha = 0.05)[3]
        if abs(z_test) >= 1.96:
            significativo = True
        elif abs(z_test) < 1.96:
            significativo = False
        
    return(coord_origen, tendencia, significativo)


def calculo_tendencia_isccp(xrdata, mensual = False, estacional = False):
    
    lats = xrdata.lat.values
    lons = xrdata.lon.values
    n_lats = len(lats)
    n_lons = len(lons)
    
    if mensual == False and estacional == False:
        tendencia_array = np.empty((2, n_lats, n_lons))

        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                tendencia_punto = tendencia_puntual(xrdata, lon, lat)

                if mensual == False and estacional == False:
                    tendencia_array[0, i, j] = tendencia_punto[0]*10*12 #porcentaje por decada
                elif mensual == True or estacional == True:
                    tendencia_array[0, i, j] = tendencia_punto[0]*10 #porcentaje por decada

                if tendencia_punto[1] == True:
                    tendencia_array[1, i, j] = 1
                elif tendencia_punto[1] == False:
                    tendencia_array[1, i, j] = 0


        coords = [("tendencia", np.array([1, 2])), ("lat", lats),("lon", lons)]  # add first coord

        # salida tendencia
        xarray_salida = xr.DataArray(tendencia_array, coords=coords)
        xarray_salida.name = "tendencia" 
        xarray_salida.attrs['units'] = "%/dec"

        return(xarray_salida)
    
    if mensual == False and estacional == True:
        #VER ESTO
        tendencia_array_DJF = np.empty((2, n_lats, n_lons))
        tendencia_array_MAM = np.empty((2, n_lats, n_lons))
        tendencia_array_JJA = np.empty((2, n_lats, n_lons))
        tendencia_array_SON = np.empty((2, n_lats, n_lons))

        xrdata_medias_DJF = calculo_medias_estaciones(xrdata, "DJF") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_MAM = calculo_medias_estaciones(xrdata, "MAM") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_JJA = calculo_medias_estaciones(xrdata, "JJA") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_SON = calculo_medias_estaciones(xrdata, "SON") #armar funcion que calcule la media estacional para cada anio
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                #DJF
                tendencia_punto_DJF = tendencia_puntual(xrdata_medias_DJF, lon, lat)
                tendencia_array_DJF[0, i, j] = tendencia_punto_DJF[0]*10 #porcentaje por decada
                if tendencia_punto_DJF[1] == True:
                    tendencia_array_DJF[1, i, j] = 1
                elif tendencia_punto_DJF[1] == False:
                    tendencia_array_DJF[1, i, j] = 0
                    
                #MAM
                tendencia_punto_MAM = tendencia_puntual(xrdata_medias_MAM, lon, lat)
                tendencia_array_MAM[0, i, j] = tendencia_punto_MAM[0]*10 #porcentaje por decada
                if tendencia_punto_MAM[1] == True:
                    tendencia_array_MAM[1, i, j] = 1
                elif tendencia_punto_MAM[1] == False:
                    tendencia_array_MAM[1, i, j] = 0

                #JJA
                tendencia_punto_JJA = tendencia_puntual(xrdata_medias_JJA, lon, lat)
                tendencia_array_JJA[0, i, j] = tendencia_punto_JJA[0]*10 #porcentaje por decada
                if tendencia_punto_JJA[1] == True:
                    tendencia_array_JJA[1, i, j] = 1
                elif tendencia_punto_JJA[1] == False:
                    tendencia_array_JJA[1, i, j] = 0
                    
                #SON
                tendencia_punto_SON = tendencia_puntual(xrdata_medias_SON, lon, lat)
                tendencia_array_SON[0, i, j] = tendencia_punto_SON[0]*10 #porcentaje por decada
                if tendencia_punto_SON[1] == True:
                    tendencia_array_SON[1, i, j] = 1
                elif tendencia_punto_SON[1] == False:
                    tendencia_array_SON[1, i, j] = 0

        coords = [("tendencia", np.array([1, 2])), ("lat", lats),("lon", lons)]  # add first coord

        # salida tendencia
        xarray_salida_DJF = xr.DataArray(tendencia_array_DJF, coords=coords)
        xarray_salida_DJF.name = "tendencia" 
        xarray_salida_DJF.attrs['units'] = "%/dec"
        
        xarray_salida_MAM = xr.DataArray(tendencia_array_MAM, coords=coords)
        xarray_salida_MAM.name = "tendencia" 
        xarray_salida_MAM.attrs['units'] = "%/dec"
        
        xarray_salida_JJA = xr.DataArray(tendencia_array_JJA, coords=coords)
        xarray_salida_JJA.name = "tendencia" 
        xarray_salida_JJA.attrs['units'] = "%/dec"
        
        xarray_salida_SON = xr.DataArray(tendencia_array_SON, coords=coords)
        xarray_salida_SON.name = "tendencia" 
        xarray_salida_SON.attrs['units'] = "%/dec"

        tendencias_dict = {"DJF": xarray_salida_DJF, 
                           "MAM": xarray_salida_MAM, 
                           "JJA": xarray_salida_JJA,
                           "SON": xarray_salida_SON}
        
        return(tendencias_dict)

def calculo_tendencia_isccp_theil_sen(xrdata, mensual = False, estacional = False):
    
    lats = xrdata.lat.values
    lons = xrdata.lon.values
    n_lats = len(lats)
    n_lons = len(lons)
    
    if mensual == False and estacional == False:
        tendencia_array = np.empty((2, n_lats, n_lons))

        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                tendencia_punto = tendencia_puntual_theil_sen(xrdata, lon, lat)

                if mensual == False and estacional == False:
                    tendencia_array[0, i, j] = tendencia_punto[1]*10*12 #porcentaje por decada
                elif mensual == True or estacional == True:
                    tendencia_array[0, i, j] = tendencia_punto[1]*10 #porcentaje por decada

                if tendencia_punto[2] == True:
                    tendencia_array[1, i, j] = 1
                elif tendencia_punto[2] == False:
                    tendencia_array[1, i, j] = 0


        coords = [("tendencia", np.array([1, 2])), ("lat", lats),("lon", lons)]  # add first coord

        # salida tendencia
        xarray_salida = xr.DataArray(tendencia_array, coords=coords)
        xarray_salida.name = "tendencia" 
        xarray_salida.attrs['units'] = "%/dec"

        return(xarray_salida)
    
    if mensual == False and estacional == True:
        #VER ESTO
        tendencia_array_DJF = np.empty((2, n_lats, n_lons))
        tendencia_array_MAM = np.empty((2, n_lats, n_lons))
        tendencia_array_JJA = np.empty((2, n_lats, n_lons))
        tendencia_array_SON = np.empty((2, n_lats, n_lons))

        xrdata_medias_DJF = calculo_medias_estaciones(xrdata, "DJF") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_MAM = calculo_medias_estaciones(xrdata, "MAM") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_JJA = calculo_medias_estaciones(xrdata, "JJA") #armar funcion que calcule la media estacional para cada anio
        xrdata_medias_SON = calculo_medias_estaciones(xrdata, "SON") #armar funcion que calcule la media estacional para cada anio
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                #DJF
                tendencia_punto_DJF = tendencia_puntual_theil_sen(xrdata_medias_DJF, lon, lat)
                tendencia_array_DJF[0, i, j] = tendencia_punto_DJF[1]*10 #porcentaje por decada
                if tendencia_punto_DJF[2] == True:
                    tendencia_array_DJF[1, i, j] = 1
                elif tendencia_punto_DJF[2] == False:
                    tendencia_array_DJF[1, i, j] = 0
                    
                #MAM
                tendencia_punto_MAM = tendencia_puntual_theil_sen(xrdata_medias_MAM, lon, lat)
                tendencia_array_MAM[0, i, j] = tendencia_punto_MAM[1]*10 #porcentaje por decada
                if tendencia_punto_MAM[2] == True:
                    tendencia_array_MAM[1, i, j] = 1
                elif tendencia_punto_MAM[2] == False:
                    tendencia_array_MAM[1, i, j] = 0

                #JJA
                tendencia_punto_JJA = tendencia_puntual_theil_sen(xrdata_medias_JJA, lon, lat)
                tendencia_array_JJA[0, i, j] = tendencia_punto_JJA[1]*10 #porcentaje por decada
                if tendencia_punto_JJA[2] == True:
                    tendencia_array_JJA[1, i, j] = 1
                elif tendencia_punto_JJA[2] == False:
                    tendencia_array_JJA[1, i, j] = 0
                    
                #SON
                tendencia_punto_SON = tendencia_puntual_theil_sen(xrdata_medias_SON, lon, lat)
                tendencia_array_SON[0, i, j] = tendencia_punto_SON[1]*10 #porcentaje por decada
                if tendencia_punto_SON[2] == True:
                    tendencia_array_SON[1, i, j] = 1
                elif tendencia_punto_SON[2] == False:
                    tendencia_array_SON[1, i, j] = 0

        coords = [("tendencia", np.array([1, 2])), ("lat", lats),("lon", lons)]  # add first coord

        # salida tendencia
        xarray_salida_DJF = xr.DataArray(tendencia_array_DJF, coords=coords)
        xarray_salida_DJF.name = "tendencia" 
        xarray_salida_DJF.attrs['units'] = "%/dec"
        
        xarray_salida_MAM = xr.DataArray(tendencia_array_MAM, coords=coords)
        xarray_salida_MAM.name = "tendencia" 
        xarray_salida_MAM.attrs['units'] = "%/dec"
        
        xarray_salida_JJA = xr.DataArray(tendencia_array_JJA, coords=coords)
        xarray_salida_JJA.name = "tendencia" 
        xarray_salida_JJA.attrs['units'] = "%/dec"
        
        xarray_salida_SON = xr.DataArray(tendencia_array_SON, coords=coords)
        xarray_salida_SON.name = "tendencia" 
        xarray_salida_SON.attrs['units'] = "%/dec"

        tendencias_dict = {"DJF": xarray_salida_DJF, 
                           "MAM": xarray_salida_MAM, 
                           "JJA": xarray_salida_JJA,
                           "SON": xarray_salida_SON}
        
        return(tendencias_dict)
