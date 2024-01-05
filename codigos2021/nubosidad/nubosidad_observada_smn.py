#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:50:13 2021

@author: nadia
"""
#nubosidad_observada_smn.py
#pararse en directorio ./Doctorado/codigos/codigos2021/nubosidad
#los datos tienen que estar acomodados en una carpeta general: ./Doctorado 
#dentro de esa carpeta existe: ./codigos/codigos2021/nubosidad
#                              ./datos/smn/smn_variables_1961-2021 
#                              ./resultados/resultados2021/nubosidad


import os
import pandas as pd
import matplotlib.pyplot as plt

from f_abrir_datos_smn import abrir_datos_smn
from f_graficos_smn import scatter, histograma, stackplot, barplot_oktas_separadas, barplot_oktas_juntas, lineplot_oktas_separadas, lineplot_oktas_juntas, histogramas_partidos
from f_procesamiento_smn import media_mensual, frecuencia_oktas_por_anio


#%% Abro datos y los acomodo en diccionario
ruta_a_archivos = "../../../datos/smn/smn_variables_1961-2021/"
nombres_archivos = os.listdir(ruta_a_archivos)
data = {}
for nombre_archivo in nombres_archivos:
    id_data = abrir_datos_smn(ruta_a_archivos = ruta_a_archivos, nombre_archivo = nombre_archivo, variable = "nub")
    data[id_data[0]] = id_data[1]

ides_omm = list(data.keys())
#fecha_inicio_str = "1983-12"
#fecha_final_str = "2016-12"
#fecha_inicio_str_1 = "1983-12"
#fecha_final_str_1 = "1999-12"
#fecha_inicio_str_2 = "2000-01"
#fecha_final_str_2 = "2016-12"

fecha_inicio_str = "1961-01-01"
fecha_final_str = "2020-12-31"
fecha_inicio_str_1 = "1961-01-01"
fecha_final_str_1 = "1989-12-31"
fecha_inicio_str_2 = "1990-01-01"
fecha_final_str_2 = "2020-12-31"
#%% Procesamiento: media mensual
"""calculo media mensual de nubosidad diaria: 
   si hay mas del 10%, 30% o 50% de datos faltantes se pone na
   redondeo al entero mas cercano"""
   
porcentaje_na_admitido = 20
data_mensual = {}
ruta_salida = f"../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/admite_{porcentaje_na_admitido}porc_na/"

for id_omm in ides_omm:    
    data_mensual[id_omm] = media_mensual(id_omm, data[id_omm], f"{ruta_salida}datos/", porcentaje_na_admitido)
    data_mensual[id_omm].columns = ["nub"]

#%% Graficos: series diarias

def ejecutar_graficos_diarios(id_omm, frecuencias, df_data, fecha_inicio_str, fecha_final_str, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2):
    ruta_salida = f"../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/admite_{porcentaje_na_admitido}porc_na/"
    os.chdir(ruta_salida)
    if "series_diario" not in os.listdir():
        print(f"genera directorio llamado: series_diario en {ruta_salida}")
        os.mkdir("series_diario")
    else:
        print(f"se para en el directorio llamado: series_diario en {ruta_salida}")
    os.chdir("./series_diario") #se para en series_diario, aca se van a guardar los resultados 
    if str(id_omm) not in os.listdir():
        print(f"genera directorio llamado: {id_omm} en {ruta_salida}series_diario")
        os.mkdir(str(id_omm))
    else:
        print(f"se para en el directorio llamado: {id_omm} en {ruta_salida}series_diario")
    os.chdir(f"./{id_omm}")  #se para en series_diario, aca se van a guardar los resultados de la estacion id_omm
    
    scatter(id_omm, df_data, fecha_inicio_str, fecha_final_str)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = False, meses = False)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = True, meses = False)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = False, meses = True)
    plt.close()
    stackplot(frecuencias, id_omm, df_data, fecha_inicio_str, fecha_final_str)
    plt.close()
    barplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    plt.close()
    #barplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    #lineplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    #lineplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = False, meses = False)
    plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = True, meses = False)
    plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = False, meses = True)
    plt.close()
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

for id_omm in ides_omm:
    df_data = data[id_omm]
    ruta_salida = f"../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/admite_{porcentaje_na_admitido}porc_na/datos/"
    os.chdir(ruta_salida)
    if f"frecuencia_anual_dias_{id_omm}.csv" not in os.listdir():
        print(f"genera un archivo: frecuencia_anual_dias_{id_omm}.csv en {ruta_salida}")
        frecuencia = frecuencia_oktas_por_anio(id_omm, df_data, ".")
    else:
        frecuencia = pd.read_csv(f"frecuencia_anual_dias_{id_omm}.csv", index_col="fecha")
    directorio_raiz = "../../../../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)
    ejecutar_graficos_diarios(id_omm, frecuencia, df_data, fecha_inicio_str, fecha_final_str, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2)
    

#%% Graficos: series mensuales

def ejecutar_graficos_mensuales(id_omm, frecuencias, df_data, fecha_inicio_str, fecha_final_str, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2):
    ruta_salida = f"../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/admite_{porcentaje_na_admitido}porc_na/"
    os.chdir(ruta_salida)
    if "series" not in os.listdir():
        print(f"genera directorio llamado: series en {ruta_salida}")
        os.mkdir("series")
    else:
        print(f"se para en el directorio llamado: series en {ruta_salida}")
    os.chdir("./series") #se para en series, aca se van a guardar los resultados 
    if str(id_omm) not in os.listdir():
        print(f"genera directorio llamado: {id_omm} en {ruta_salida}series")
        os.mkdir(str(id_omm))
    else:
        print(f"se para en el directorio llamado: {id_omm} en {ruta_salida}series")
    os.chdir(f"./{id_omm}")  #se para en series_diario, aca se van a guardar los resultados de la estacion id_omm
    
    scatter(id_omm, df_data, fecha_inicio_str, fecha_final_str)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = False, meses = False)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = True, meses = False)
    plt.close()
    histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = False, meses = True)
    plt.close()
    stackplot(frecuencias, id_omm, df_data, fecha_inicio_str, fecha_final_str)
    plt.close()
    barplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    #barplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    #lineplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    #plt.close()
    #lineplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str)
    plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = False, meses = False)
    plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = True, meses = False)
    plt.close()
    histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, variable = "nub", estaciones = False, meses = True)
    plt.close()
    #vuelvo a directorio de trabajo
    directorio_raiz = "../../../../../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)

for id_omm in ides_omm:
    df_data = data_mensual[id_omm]
    ruta_salida = f"../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn/data_mensual/admite_{porcentaje_na_admitido}porc_na/datos/"
    os.chdir(ruta_salida)
    if f"frecuencia_anual_meses_{id_omm}.csv" not in os.listdir():
        print(f"genera un archivo: frecuencia_anual_meses_{id_omm}.csv en {ruta_salida}")
        frecuencia = frecuencia_oktas_por_anio(id_omm, df_data, ".")
    else:
        frecuencia = pd.read_csv(f"frecuencia_anual_meses_{id_omm}.csv", index_col="fecha")
    directorio_raiz = "../../../../../../../../codigos/codigos2021/nubosidad"
    os.chdir(directorio_raiz)
    ejecutar_graficos_mensuales(id_omm, frecuencia, df_data, fecha_inicio_str, fecha_final_str, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2)




