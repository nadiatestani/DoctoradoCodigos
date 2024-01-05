#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:01:49 2021

@author: nadia

#calibracion_nubosidad.py
"""

#calibracion_nubosidad.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

from f_make_grid import make_grid
from f_mis_shapes import df_paises, df_provincias
from f_graficos_calibracion import grafico_puntos, histograma_oktas_sat, histograma_oktas_sat_smn
from f_cargo_datos_isccp import cargo_datos_ISCCP
from f_porc_to_oktas import data_frame_oktas
from f_puntos_cercanos import puntos_cercanos
from f_tablas_de_contingencia_nubosidad import generar_tabla_contingencia
#%% Cargo datos
data_list = cargo_datos_ISCCP() #satelital
smn = pd.read_excel("../../../datos/smn/Exp185151.xlsx", sheet_name = "Estaciones", names = ["EST", "NOMBRE", "LAT", "LON", "ALT"]) #smn

#%% Cargo puntos de grilla satelital junto con puntos de las estaciones del smn
#satelital
lons_satelital = data_list[0].lon.values
lons_satelital = list(lons_satelital[lons_satelital > 360-61])
lons_satelital = list(np.array(lons_satelital)[np.array(lons_satelital) < 360-54])
lats_satelital = data_list[0].lat.values
lats_satelital = list(lats_satelital[lats_satelital > -32])
lats_satelital = list(np.array(lats_satelital)[np.array(lats_satelital) < -25])
lista_puntos_satelital = make_grid(lons_satelital, lats_satelital)

#puntos smn
lista_puntos_smn = [(360 - lon, -1 * lat) for lon, lat in zip(smn["LON"],smn["LAT"])]
dict_puntos_smn = dict(zip(list(smn["EST"]), lista_puntos_smn))
#lista_puntos_smn_calibracion = list(smn["EST"])
lista_puntos_smn_calibracion = [87393, 87270, 87289, 87178, 87166, 87395, 87155, 87173, 87187, 87148] 
#%% Grafico los puntos de grilla satelital junto con puntos de las estaciones del smn
#cargo shapes
shape_paises = df_paises()
shape_provincias = df_provincias()

#grafico
grafico_puntos(lista_puntos_satelital, dict_puntos_smn, lista_puntos_smn_calibracion, shape_paises, shape_provincias)

#%% Tomo los puntos mas cercanos a las estaciones de calibracion del SMN, paso de cldamt a oktas y grafico su histograma anual, por estacion y por mes

def ejecutar_salidas(ID_estacion, dict_puntos_smn, lista_puntos_satelital, data_list, fecha_inicio_str, fecha_final_str):
    directorio_resultados_calibracion = "../../../resultados/resultados2021/nubosidad/calibracion"
    os.chdir(directorio_resultados_calibracion)
    if str(ID_estacion) not in os.listdir():
        print(f"genera directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
        os.mkdir(str(ID_estacion))
    else:
        print(f"se para en el directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
    os.chdir(f"./{ID_estacion}")
    for punto_cercano in puntos_cercanos(ID_estacion, dict_puntos_smn, lista_puntos_satelital, 4): 
        plt.close()
        lon = punto_cercano[0]
        lat = punto_cercano[1]
        if f"{lon-360}_{lat}" not in os.listdir():
            print(f"genera directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}")
            os.mkdir(f"{lon-360}_{lat}") #genero directorio de salida si no esta
        else: 
            print(f"los resultados se guardan en el directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}/{ID_estacion}")
        os.chdir(f"./{lon-360}_{lat}") #me paro en el directorio de salida 
        data_frame_cldamt_punto = data_frame_oktas(data_list, lon = lon, lat = lat) #armo series en dataframe de pandas
        #y corro graficos
        histograma_oktas_sat(data_frame_cldamt_punto, fecha_inicio_str, fecha_final_str, lon = lon, lat = lat)
        histograma_oktas_sat(data_frame_cldamt_punto, fecha_inicio_str, fecha_final_str, lon = lon, lat = lat, estaciones = True, meses = False)
        histograma_oktas_sat(data_frame_cldamt_punto, fecha_inicio_str, fecha_final_str, lon = lon, lat = lat, estaciones = False, meses = True)
        os.chdir("..")    
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

#ejecuto la salida para las estaciones del smn 
for estacion in lista_puntos_smn_calibracion:
    ejecutar_salidas(estacion, dict_puntos_smn, lista_puntos_satelital, data_list, "1983-12", "2016-11")

#%% Incorporo a los histogramas la informacion de las estaciones del smn (dcao por ahora)

# abro datos de media_mensual_diaria_estaciones.csv 
# armo histogramas de smn + satelital juntos
ruta = "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/datos/"
data_mensual_smn = {}
for id_smn in lista_puntos_smn_calibracion:
    smn_media_mensual = pd.read_csv(ruta+"media_mensual_"+str(id_smn)+".csv", index_col="fecha",  parse_dates = True)
    data_mensual_smn[id_smn] = smn_media_mensual

def ejecutar_salidas(ID_estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, fecha_inicio_str, fecha_final_str):
    directorio_resultados_calibracion = "../../../resultados/resultados2021/nubosidad/calibracion"
    os.chdir(directorio_resultados_calibracion)
    if str(ID_estacion) not in os.listdir():
        print(f"genera directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
        os.mkdir(str(ID_estacion))
    else:
        print(f"se para en el directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
    os.chdir(f"./{ID_estacion}")
    for punto_cercano in puntos_cercanos(ID_estacion, dict_puntos_smn, lista_puntos_satelital, 4): 
        plt.close()
        lon = punto_cercano[0]
        lat = punto_cercano[1]
        if f"{lon-360}_{lat}" not in os.listdir():
            print(f"genera directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}")
            os.mkdir(f"{lon-360}_{lat}") #genero directorio de salida si no esta
        else: 
            print(f"los resultados se guardan en el directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}/{ID_estacion}")
        os.chdir(f"./{lon-360}_{lat}") #me paro en el directorio de salida 
        data_frame_cldamt_punto = data_frame_oktas(data_list, lon = lon, lat = lat) #armo series en dataframe de pandas
        #y corro graficos
        histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat)
        histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, estaciones = True, meses = False)
        histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, estaciones = False, meses = True)
        os.chdir("..")    
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

#ejecuto la salida para las estaciones del smn 
for estacion in lista_puntos_smn_calibracion:
    ejecutar_salidas(estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, "1983-12", "2016-11")

#%% Hago tablas de contingencia

ruta = "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/datos/"
data_mensual_smn = {}
for id_smn in lista_puntos_smn_calibracion:
    smn_media_mensual = pd.read_csv(ruta+"media_mensual_"+str(id_smn)+".csv", index_col="fecha",  parse_dates = True)
    data_mensual_smn[id_smn] = smn_media_mensual

def ejecutar_salidas(ID_estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, fecha_inicio_str, fecha_final_str):
    directorio_resultados_calibracion = "../../../resultados/resultados2021/nubosidad/calibracion"
    os.chdir(directorio_resultados_calibracion)
    if str(ID_estacion) not in os.listdir():
        print(f"genera directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
        os.mkdir(str(ID_estacion))
    else:
        print(f"se para en el directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
    os.chdir(f"./{ID_estacion}")
    for punto_cercano in puntos_cercanos(ID_estacion, dict_puntos_smn, lista_puntos_satelital, 4): 
        plt.close()
        lon = punto_cercano[0]
        lat = punto_cercano[1]
        if f"{lon-360}_{lat}" not in os.listdir():
            print(f"genera directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}")
            os.mkdir(f"{lon-360}_{lat}") #genero directorio de salida si no esta
        else: 
            print(f"los resultados se guardan en el directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}/{ID_estacion}")
        os.chdir(f"./{lon-360}_{lat}") #me paro en el directorio de salida 
        data_frame_cldamt_punto = data_frame_oktas(data_list, lon = lon, lat = lat) #armo series en dataframe de pandas
        #y corro tablas
        df_smn = data_mensual_smn[ID_estacion]
        generar_tabla_contingencia(ID_estacion, df_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, alpha = 0.05)
        os.chdir("..")    
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

#ejecuto la salida para las estaciones del smn 
for estacion in lista_puntos_smn_calibracion:
    ejecutar_salidas(estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, "1983-12", "2016-11")


#%% EJECUTO SALIDAS DE TODO JUNTO: histogramas de estaciones y satelital + tablas de contingencia.

ruta = "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/datos/"
data_mensual_smn = {}
for id_smn in lista_puntos_smn_calibracion:
    smn_media_mensual = pd.read_csv(ruta+"media_mensual_"+str(id_smn)+".csv", index_col="fecha",  parse_dates = True)
    data_mensual_smn[id_smn] = smn_media_mensual

def ejecutar_salidas(ID_estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, fecha_inicio_str, fecha_final_str):
    directorio_resultados_calibracion = "../../../resultados/resultados2021/nubosidad/calibracion"
    os.chdir(directorio_resultados_calibracion)
    if str(ID_estacion) not in os.listdir():
        print(f"genera directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
        os.mkdir(str(ID_estacion))
    else:
        print(f"se para en el directorio llamado: {ID_estacion} en {directorio_resultados_calibracion}")
    os.chdir(f"./{ID_estacion}")
    for punto_cercano in puntos_cercanos(ID_estacion, dict_puntos_smn, lista_puntos_satelital, 4): 
        plt.close()
        lon = punto_cercano[0]
        lat = punto_cercano[1]
        if f"{lon-360}_{lat}" not in os.listdir():
            print(f"genera directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}")
            os.mkdir(f"{lon-360}_{lat}") #genero directorio de salida si no esta
        else: 
            print(f"los resultados se guardan en el directorio llamado: {lon-360}_{lat} en {directorio_resultados_calibracion}/{ID_estacion}")
        os.chdir(f"./{lon-360}_{lat}") #me paro en el directorio de salida 
        data_frame_cldamt_punto = data_frame_oktas(data_list, lon = lon, lat = lat) #armo series en dataframe de pandas
        df_smn = data_mensual_smn[ID_estacion]
        
        #y corro graficos
        #histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat)
        #histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, estaciones = True, meses = False)
        #histograma_oktas_sat_smn(ID_estacion, data_mensual_smn[ID_estacion], fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, estaciones = False, meses = True)
        
        #y tablas de contingencia
        generar_tabla_contingencia(ID_estacion, df_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, alpha = 0.05)
        generar_tabla_contingencia(ID_estacion, df_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, alpha = 0.05, estaciones = True, meses = False)
        generar_tabla_contingencia(ID_estacion, df_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon = lon, lat = lat, alpha = 0.05, estaciones = False, meses = True)
        os.chdir("..")    
        
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

#ejecuto la salida para las estaciones del smn 
for estacion in lista_puntos_smn_calibracion:
    ejecutar_salidas(estacion, dict_puntos_smn, lista_puntos_satelital, data_list, data_mensual_smn, "1983-12", "2016-11")
    
#%%pendiente: VER QUE ESTACIONES USAR. HACER LAS SERIES TEMPORALES DE SMN_MENSUAL PARA ESO 
