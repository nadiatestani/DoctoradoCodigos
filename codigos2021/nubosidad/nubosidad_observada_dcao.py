#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:07:29 2021

@author: nadia

Nubosidad observada
"""
#%% cargo modulos

import numpy as np
from datetime import datetime
import csv
import pandas as pd
import matplotlib.pyplot as plt

#%% Defino funciones:
#%% Abro los datos de nubosidad de estaciones del SMN brindados por el DCAO. Defino funcion.

def abrir_datos_nubosidad_dcao(nombre_archivo, formato_fechas): 
    """
    Abre datos de archivos nubosidad DCAO

    Parameters
    ----------
    nombre_archivo : str
        incluye ruta. Ex. "../../../datos/smn/nubosidad_dcao/nubosidad_1959_1990.dat"
    formato_fechas : str
        formato fechas. Ex.formato_fechas="%Y/%m/%d"

    Returns
    -------
    df_data : pd.DataFrame
        columns=['estacion', 'fecha',"hora", 'TCC']

    """
    with open(nombre_archivo, "rt") as f: #abro archivo en modo escritura
            rows=csv.reader(f) #abro las filas como listas usando csv
            lista_data=[]
            indices_filas_sin_datos=[]
            for i, row in enumerate(rows):
                
                try:
                    fila=row[0].split()
                    #print(fila, i)
                    
                    #estacion
                    estacion=int(fila[0])
                    
                    #fecha
                    if formato_fechas=="%d%m%Y" and len(fila[1])==7: #si el formato es ddmmyyyy y el largo es 7, es que le falta un 0 adelante
                        fila[1]="0"+fila[1]
                        fecha=datetime.strptime(fila[1], formato_fechas)
                    elif formato_fechas=="%d %m%Y": #si esta separada la fila del dia de la fila del mesyanio
                        if len(fila)==5:#si estan efectivamente separados el dia y el mesanio
                            if len(fila[1])==1: #si le falta el cero adelante del dia
                                dia="0"+fila[1]
                            else:
                                dia=fila[1]
                            if len(fila[2])==5: #si le falta el cero adelante del mes
                                mesanio="0"+fila[2]
                            else:
                                mesanio=fila[2]
                            fecha=datetime.strptime(dia+mesanio, "%d%m%Y")
                        else: #si las columnas de dia y mesanio se juntan en alguna fila
                            if len(fila[1])==7: #si le falta el cero adelante del dia
                                diamesanio="0"+fila[1]
                            else:
                                diamesanio=fila[1]
                            fecha=datetime.strptime(diamesanio, "%d%m%Y")        
                    else:
                        fecha=datetime.strptime(fila[1], formato_fechas)
                    
                    #hora UTC y TCC
                    if formato_fechas=="%d %m%Y" and len(fila)==5: #si esta separada la fila del dia de la fila del mesyanio
                        if len(fila[3])>2: #si el largo de la hora es mayor que dos (hay casos en que la hora es=18nan)
                            try:
                                hora=int(fila[3][:2])
                            except ValueError:
                                hora=int(fila[3][:1])
                        else:
                            hora=int(fila[3])
                        if fila[4]=="/":
                            TCC=np.nan
                        else:
                            TCC=int(fila[4])
                    
                    else:
                        if len(fila[2])>2: #si el largo de la hora es mayor que dos (hay casos en que la hora es=18nan)
                            try:
                                hora=int(fila[2][:2])
                            except ValueError:
                                hora=int(fila[2][:1])
                        else:
                            hora=int(fila[2])
                        if fila[3]=="/":
                            TCC=np.nan
                        else:
                            TCC=int(fila[3])
                    lista=[estacion,fecha,hora,TCC]
                    lista_data.append(lista)
                except IndexError as e:
                    print("No se pudo abrir la fila:", row," con indice",i," se detecto este error:",e)
                    indices_filas_sin_datos.append(i)
            df_data=pd.DataFrame(lista_data,columns=['estacion', 'fecha',"hora", 'TCC'])
            df_data.index=df_data["fecha"]
            df_data=df_data[["estacion","hora", "TCC"]]
            return df_data 

#%% Metadata. Defino funciones.

#tabla cantidad de datos por hora por estacion
def metadata(df_data_x_estacion,estacion,fecha_inicio,fecha_final):
    """
    Devuelve tabla con cantidad de data de df_data_por_estacion por hora, para estacion

    Parameters
    ----------
    df_data_x_estacion : dict of dataframe
        clave: numero estacion. dataframe: salida de abrir_datos_nubosidad_dcao
        
    estacion : int
    
    fecha_inicio: str
    
    fecha_final: str
    
    Returns
    -------
    pandas dataframe de estacion
    columns=["TTC Total datos no faltantes","TCC Total datos faltantes","TTC Total no visibles","TTC Total visibles","TCC Porcentaje datos faltantes", "TTC Porcentaje no visibles","TTC Porcentaje visibles"]
    """
    lista_final=[]
    for i in range(0,24): #para cada hora
        data=df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==i]["TCC"].value_counts()    
        data=data.sort_index()
        total=data.sum()
        total_dias=len(pd.date_range(start=fecha_inicio,end=fecha_final))
        if total!=0:
            try:
                total_no_visibles=data[9]
            except KeyError:
                total_no_visibles=0
            if total_no_visibles==0:
                porcentaje_no_visibles=0
            else:
                porcentaje_no_visibles=total_no_visibles/total*100
            if total_no_visibles==0:
                total_visibles=total
            else:
                total_visibles=total-total_no_visibles
            porcentaje_visibles=total_visibles/total*100
            total_datos_faltantes=total_dias-total
            porcentaje_datos_faltantes=total_datos_faltantes/total_dias*100
        else:
            total_no_visibles=0
            total_visibles=0
            porcentaje_no_visibles=0
            porcentaje_visibles=0
            porcentaje_datos_faltantes=100
        lista=[total,total_datos_faltantes,total_no_visibles,total_visibles,round(porcentaje_datos_faltantes,2),round(porcentaje_no_visibles,2),round(porcentaje_visibles,2)]
        lista_final.append(lista)
    df_final=pd.DataFrame(lista_final,index=np.arange(0,24),columns=["TTC Total datos no faltantes","TCC Total datos faltantes","TTC Total no visibles","TTC Total visibles","TCC Porcentaje datos faltantes", "TTC Porcentaje no visibles","TTC Porcentaje visibles"])
    return df_final

#histogramas con detalle de datos
def metadata_histograma(df_data_x_estacion,estacion_nombre,estacion,fecha_inicio,fecha_final):
    """
    Hace tres histogramas (frecuencia por hora) con metadata: "TTC Datos totales no faltantes", "TTC Porcentaje datos faltantes", "TTC Porcentaje datos visibles"

    Parameters
    ----------
    df_data_x_estacion : dict of dataframe
        clave: numero estacion. dataframe: salida de abrir_datos_nubosidad_dcao
    
    estacion_nombre: str
    
    estacion : int
    
    fecha_inicio: str
    
    fecha_final: str

    Returns
    -------
    plot: histograma: "TTC Datos totales no faltantes", "TTC Porcentaje datos faltantes", "TTC Porcentaje datos visibles"
    se guarda en carpeta: "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/metadata/"

    """
    df_metadata=metadata(df_data_x_estacion,estacion,fecha_inicio,fecha_final)
    
    fig = plt.figure(num=1, figsize=(9, 6), dpi=80)
    
    plt.subplot(3, 1, 1) # define la figura de arriba
    plt.bar(df_metadata["TTC Total datos no faltantes"].index,df_metadata["TTC Total datos no faltantes"].transpose(),color="seagreen")# dibuja la curva
    plt.xticks([])# saca las marcas
    plt.yticks(np.arange(0,13000,2000))
    plt.yticks(np.arange(0,13000,2000),
               np.arange(0,13000,2000)/1000)
    plt.ylabel(r"Datos x$10^3$")
    plt.ylim((0,13000))
    plt.title("TTC Datos totales no faltantes")
    
    plt.subplot(3, 1, 2) # define la figura del medio
    plt.bar(df_metadata["TCC Porcentaje datos faltantes"].index,df_metadata["TCC Porcentaje datos faltantes"].transpose(),color="seagreen") # dibuja la curva
    plt.plot(df_metadata["TCC Porcentaje datos faltantes"].index,[50]*len(df_metadata["TCC Porcentaje datos faltantes"].index),color="orange")
    plt.xticks([])# saca las marcas
    plt.yticks(np.arange(0,110,20))
    plt.ylim((0,110))
    plt.ylabel(r"Porcentaje $\%$")
    plt.title("TTC Porcentaje datos faltantes")
    
    plt.subplot(3, 1, 3) # define la figura de abajo
    plt.bar(df_metadata["TTC Porcentaje visibles"].index,df_metadata["TTC Porcentaje visibles"].transpose(),color="seagreen") # dibuja la curva
    plt.xticks(np.arange(0,24,2))
    plt.yticks(np.arange(0,110,20))
    plt.ylim((0,110))
    plt.ylabel(r"Porcentaje $\%$")
    plt.xlabel("Hora UTC")
    plt.title("TTC Porcentaje datos visibles")
    
    fig.suptitle("Estacion: "+ estacion_nombre +" ("+str(estacion)+")"+"   "+"Periodo: "+fecha_inicio+"_"+fecha_final,fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/metadata/"+str(estacion)+".png")

#series de datos: scatter plots
def data_series(df_data_x_estacion,estacion_nombre,estacion,fecha_inicio,fecha_final):
    """
    Hace series con data: "TTC" para horas 02, 08, 14, 20 UTC

    Parameters
    ----------
    df_data_x_estacion : dict of dataframe
        clave: numero estacion. dataframe: salida de abrir_datos_nubosidad_dcao
    
    estacion_nombre: str
    
    estacion : int
    
    fecha_inicio: str
    
    fecha_final: str

    Returns
    -------
    plot: scatter
    se guarda en carpeta: "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data/series/"

    """
    
    fig = plt.figure(num=2, figsize=(10, 6), dpi=80)
    
    plt.subplot(2, 2, 1) # define la figura de arriba
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1],marker = '.',color="seagreen")
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1]==9].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1]==9],marker = '.',color="orange")
    plt.ylabel("TCC (oktas)")
    plt.yticks(np.arange(0,10))
    plt.xticks([])# saca las marcas
    plt.title("02 UTC")

    plt.subplot(2, 2, 2)
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1],marker = '.',color="seagreen")
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1]==9].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1]==9],marker = '.',color="orange")
    plt.xticks([])# saca las marcas
    plt.yticks([])# saca las marcas
    plt.title("08 UTC")
    
    plt.subplot(2, 2, 3)
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1],marker = '.',color="seagreen")
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1]==9].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1]==9],marker = '.',color="orange")
    plt.ylabel("TCC (oktas)")
    plt.yticks(np.arange(0,10))
    plt.xticks(pd.date_range(fecha_inicio,fecha_final,freq="4Y"),[pd.date_range(fecha_inicio,fecha_final,freq="4Y")[i].year for i in range(len(pd.date_range(fecha_inicio,fecha_final,freq="4Y")))])
    plt.xlabel("Fecha")
    plt.title("14 UTC")
    
    plt.subplot(2, 2, 4)
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1],marker = '.',color="seagreen")
    plt.scatter(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1]==9].index,df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1]==9],marker = '.',color="orange")
    plt.xlabel("Fecha")
    plt.xticks(pd.date_range(fecha_inicio,fecha_final,freq="4Y"),[pd.date_range(fecha_inicio,fecha_final,freq="4Y")[i].year for i in range(len(pd.date_range(fecha_inicio,fecha_final,freq="4Y")))])
    plt.yticks([])# saca las marcas
    plt.title("20 UTC")
    
    fig.suptitle("Estacion: "+ estacion_nombre +" ("+str(estacion)+")"+"   "+"Periodo: "+fecha_inicio+"_"+fecha_final,fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data/series/"+str(estacion)+".png")


#%% Data. Defino funciones.

#histogramas de datos
def data_histogramas(df_data_x_estacion,estacion_nombre,estacion,fecha_inicio,fecha_final):
    """
    Hago histograma de TCC para las 02 08 14 20 UTC

    Parameters
    ----------
    df_data_x_estacion : dict of dataframe
        clave: numero estacion. dataframe: salida de abrir_datos_nubosidad_dcao
    
    estacion_nombre: str
    
    estacion : int
    
    fecha_inicio: str
    
    fecha_final: str

    Returns
    -------
    plot: histograma
        Guarda histograma en ruta: "../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data/histogramas/"

    """
    fig = plt.figure(num=2, figsize=(10, 6), dpi=80)
    
    bins = np.arange(10) - 0.5
    plt.subplot(2, 2, 1) # define la figura de arriba
    plt.hist(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==2]["TCC"][0:-1]!=9],density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,0.6,0.1))
    plt.ylim((0,0.5))
    plt.xticks([])
    plt.xlim([-1, 9])
    plt.title("02 UTC")

    plt.subplot(2, 2, 2)
    plt.hist(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==8]["TCC"][0:-1]!=9],density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.yticks(np.arange(0,0.6,0.1),[])
    plt.ylim((0,0.5))
    plt.xticks([])
    plt.xlim([-1, 9])
    plt.title("08 UTC")
    
    plt.subplot(2, 2, 3)
    plt.hist(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==14]["TCC"][0:-1]!=9],density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,0.6,0.1))
    plt.ylim((0,0.5))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title("14 UTC")
    
    plt.subplot(2, 2, 4)
    plt.hist(df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1][df_data_x_estacion[estacion][df_data_x_estacion[estacion]["hora"]==20]["TCC"][0:-1]!=9],density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.xlabel("TCC (Oktas)")
    plt.yticks(np.arange(0,0.6,0.1),[])
    plt.grid(axis="y")
    plt.ylim((0,0.5))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.title("20 UTC")
    
    fig.suptitle("Estacion: "+ estacion_nombre +" ("+str(estacion)+")"+"   "+"Periodo: "+fecha_inicio+"_"+fecha_final,fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data/histogramas/"+str(estacion)+".png")

#%% Proceso Data: medias mensuales. Defino funciones.
#calculo media de cada mes para cada hora 2,8,14,20
#si hay mas del 50% de datos faltantes se pone na
#si anguna de las horas tiene na, la media de todas la computo como na

#
def media_mensual_horaria(df_data_x_estacion, estacion, hora):
    data=df_data_x_estacion[estacion]["TCC"][df_data_x_estacion[estacion]["hora"]==hora][0:-1][df_data_x_estacion[estacion]["TCC"][df_data_x_estacion[estacion]["hora"]==hora][0:-1]!=9]
    data=data.sort_index()
    data_group=data.groupby(pd.Grouper(freq="M"))
    data_group_size=data_group.size()
    data_group_media=data_group.mean()
    media=[]
    for i in range(len(data_group_size)):
        serie_completa_len=data_group_media.index[i].day #cantidad de datos que deberia haber por mes (uno por dia)
        if data_group_size[i]>=serie_completa_len/2: #si hay menos del 50% de los datos faltantes
            media.append(data_group_media[i])
        else: 
            media.append(np.nan)
    return media

def media_mensual_diaria(df_data_x_estacion, estacion):
    media02=media_mensual_horaria(df_data_x_estacion, estacion, 2)
    media08=media_mensual_horaria(df_data_x_estacion, estacion, 8)
    media14=media_mensual_horaria(df_data_x_estacion, estacion, 14)
    media20=media_mensual_horaria(df_data_x_estacion, estacion, 20)
    medias=pd.concat([pd.Series(media02),pd.Series(media08),pd.Series(media14),pd.Series(media20)], axis=1)
    media_mensual_dia=[]
    for i in range(len(medias)):
        if pd.isna(medias.loc[i][0]) and pd.isna(medias.loc[i][1]) and pd.isna(medias.loc[i][2]) and pd.isna(medias.loc[i][3]): #si alguna de las horas su media es na
            media_mensual_dia.append(np.nan)
        else:
            media_mensual_dia.append(round((medias.loc[i]).mean())) #redondeo a entero mas cercano
    media_mensual_dia_df=pd.DataFrame(media_mensual_dia, columns=[estacion])
    indices=df_data_x_estacion[estacion].groupby(pd.Grouper(freq="M")).mean().index
    media_mensual_dia_df.index=indices
    return media_mensual_dia_df

def data_procesada_series():
    fig=plt.figure(num=3, figsize=(14.5, 6), dpi=80)
    plt.subplot(3, 3, 1)
    plt.plot(media_mensual_diaria_estaciones[87395],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.ylabel("TCC (Oktas)")
    plt.yticks(np.arange(2,7,1))
    plt.xticks([])
    plt.title(str(87395),fontweight=800)
        
    plt.subplot(3, 3, 2)
    plt.plot(media_mensual_diaria_estaciones[87166],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.yticks([])
    plt.xticks([])
    plt.title(str(87166),fontweight=800)
    
    plt.subplot(3, 3, 3)
    plt.plot(media_mensual_diaria_estaciones[87393],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.yticks([])
    plt.xticks([])
    plt.title(str(87393),fontweight=800)
    
    plt.subplot(3, 3, 4)
    plt.plot(media_mensual_diaria_estaciones[87289],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.ylabel("TCC (Oktas)")
    plt.yticks(np.arange(2,7,1))
    plt.xticks([])
    plt.title(str(87289),fontweight=800)
       
    plt.subplot(3, 3, 5)
    plt.plot(media_mensual_diaria_estaciones[87178],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.yticks([])
    plt.title(str(87178),fontweight=800)
    
    plt.subplot(3, 3, 6)
    plt.plot(media_mensual_diaria_estaciones[87270],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.yticks([])
    plt.title(str(87270),fontweight=800)
    
    plt.subplot(3, 3, 7)
    plt.plot(media_mensual_diaria_estaciones[87155],lw=0.2,marker="o",markersize=3, color="seagreen")
    plt.title(str(87155),fontweight=800)
    plt.ylabel("TCC (Oktas)")
    plt.yticks(np.arange(2,7,1))
    
    fig.suptitle("TCC media mensual (Oktas)",fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data_procesada/series.png")

def data_procesada_histogramas():
    fig=plt.figure(num=3, figsize=(12, 8), dpi=80)
    bins = np.arange(10) - 0.5
    plt.subplot(3, 3, 1)
    plt.hist(media_mensual_diaria_estaciones[87395], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87395),fontweight=800)
        

    
    plt.subplot(3, 3, 2)
    plt.hist(media_mensual_diaria_estaciones[87166], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87166),fontweight=800)
    
    plt.subplot(3, 3, 3)
    plt.hist(media_mensual_diaria_estaciones[87393], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87393),fontweight=800)
    
    plt.subplot(3, 3, 4)
    plt.hist(media_mensual_diaria_estaciones[87289], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87289),fontweight=800)
       
    plt.subplot(3, 3, 5)
    plt.hist(media_mensual_diaria_estaciones[87178], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87178),fontweight=800)
    
    plt.subplot(3, 3, 6)
    plt.hist(media_mensual_diaria_estaciones[87270], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87270),fontweight=800)
    
    plt.subplot(3, 3, 7)
    plt.hist(media_mensual_diaria_estaciones[87155], density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87155),fontweight=800)
    fig.suptitle("TCC media mensual (Oktas) Dic1983-Dic2016",fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data_procesada/histogramas.png")

def data_procesada_histogramas_estacion(mes1,mes2,mes3,estacion):
    fig=plt.figure(num=3, figsize=(12, 8), dpi=80)
    bins = np.arange(10) - 0.5
    plt.subplot(3, 3, 1)
    data=pd.concat([media_mensual_diaria_estaciones[87395][media_mensual_diaria_estaciones[87395].index.month==mes1],
                    media_mensual_diaria_estaciones[87395][media_mensual_diaria_estaciones[87395].index.month==mes2],
                    media_mensual_diaria_estaciones[87395][media_mensual_diaria_estaciones[87395].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87395),fontweight=800)
        

    
    plt.subplot(3, 3, 2)
    data=pd.concat([media_mensual_diaria_estaciones[87166][media_mensual_diaria_estaciones[87166].index.month==mes1],
                media_mensual_diaria_estaciones[87166][media_mensual_diaria_estaciones[87166].index.month==mes2],
                media_mensual_diaria_estaciones[87166][media_mensual_diaria_estaciones[87166].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87166),fontweight=800)
    
    plt.subplot(3, 3, 3)
    data=pd.concat([media_mensual_diaria_estaciones[87393][media_mensual_diaria_estaciones[87393].index.month==mes1],
                media_mensual_diaria_estaciones[87393][media_mensual_diaria_estaciones[87393].index.month==mes2],
                media_mensual_diaria_estaciones[87393][media_mensual_diaria_estaciones[87393].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87393),fontweight=800)
    
    plt.subplot(3, 3, 4)
    data=pd.concat([media_mensual_diaria_estaciones[87289][media_mensual_diaria_estaciones[87289].index.month==mes1],
                media_mensual_diaria_estaciones[87289][media_mensual_diaria_estaciones[87289].index.month==mes2],
                media_mensual_diaria_estaciones[87289][media_mensual_diaria_estaciones[87289].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9),[])
    plt.xlim([-1, 9])
    plt.title(str(87289),fontweight=800)
       
    plt.subplot(3, 3, 5)
    data=pd.concat([media_mensual_diaria_estaciones[87178][media_mensual_diaria_estaciones[87178].index.month==mes1],
                media_mensual_diaria_estaciones[87178][media_mensual_diaria_estaciones[87178].index.month==mes2],
                media_mensual_diaria_estaciones[87178][media_mensual_diaria_estaciones[87178].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87178),fontweight=800)
    
    plt.subplot(3, 3, 6)
    data=pd.concat([media_mensual_diaria_estaciones[87270][media_mensual_diaria_estaciones[87270].index.month==mes1],
                media_mensual_diaria_estaciones[87270][media_mensual_diaria_estaciones[87270].index.month==mes2],
                media_mensual_diaria_estaciones[87270][media_mensual_diaria_estaciones[87270].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2),[])
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87270),fontweight=800)
    
    plt.subplot(3, 3, 7)
    data=pd.concat([media_mensual_diaria_estaciones[87155][media_mensual_diaria_estaciones[87155].index.month==mes1],
                media_mensual_diaria_estaciones[87155][media_mensual_diaria_estaciones[87155].index.month==mes2],
                media_mensual_diaria_estaciones[87155][media_mensual_diaria_estaciones[87155].index.month==mes3]])
    plt.hist(data, density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
    plt.grid(axis="y")
    plt.ylabel("Frecuencia")
    plt.yticks(np.arange(0,1,0.2))
    plt.ylim((0,0.9))
    plt.xticks(range(9))
    plt.xlim([-1, 9])
    plt.xlabel("TCC (Oktas)")
    plt.title(str(87155),fontweight=800)
    fig.suptitle("TCC media mensual (Oktas) Dic1983-Dic2016 "+estacion,fontweight=800)
    plt.show()
    return fig.savefig("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data_procesada/histogramas"+estacion+".png")

#%% Corro funciones:
#%% Abro los datos de nubosidad de estaciones del SMN brindados por el DCAO. Corro funciones.

df_data_1959_1990=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/nubosidad_1959_1990.dat", formato_fechas="%Y/%m/%d")     
df_data_1991_2014=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/pedidoNubes19912014.dat", formato_fechas="%d%m%Y")  
df_data_2015=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/pedidoNubes2015.dat", formato_fechas="%d %m%Y") 
df_data_201617=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/pedidoNubes201617.dat", formato_fechas="%d%m%Y")  
df_data_2019=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/pedidoNubes2019.dat", formato_fechas="%d%m%Y") 
df_data_2020=abrir_datos_nubosidad_dcao("../../../datos/smn/nubosidad_dcao/pedidoNubes2020.dat", formato_fechas="%d%m%Y")

#los uno
df_data=pd.concat([df_data_1959_1990,df_data_1991_2014,df_data_2015,df_data_201617,df_data_2019,df_data_2020], axis=0) 

#tomo el periodo que usamos para el analisis satelital: Diciembre 1983-Diciembre2016
df_data=df_data.sort_index() #ordeno por fechas para indexar
df_data_dic1983_dic2016=df_data.loc[pd.date_range(start="1983-12-01",end="2016-12-31")]

#separo por estaciones 
numero_estaciones=list(set(df_data_dic1983_dic2016["estacion"]))
df_data_por_estacion={numero_estacion: df_data_dic1983_dic2016[df_data_dic1983_dic2016["estacion"]==numero_estacion] for numero_estacion in numero_estaciones}

#%% Metadata. Corro funciones. 

estaciones={"Concordia Aero": 87395, "Corrientes Aero": 87166,"Ituzaingo": 87173, "Mercedes Aero (Ctes)": 87281, "Monte Caseros Aero": 87393, "Obera Aero": 87281, "Paso de los Libres Aero": 87289, "Pcia. Roque Saenz Peña": 87148, "Posadas Aero": 87178, "Reconquista Aero": 87270, "Resistencia Aero":87155}

for estacion in estaciones:
    metadata_histograma(df_data_por_estacion,estacion,estaciones[estacion],fecha_inicio="01/12/1983", fecha_final="31/12/2016")
    data_series(df_data_por_estacion,estacion,estaciones[estacion],fecha_inicio="01/12/1983", fecha_final="31/12/2016")

"""
elijo horas para trabajar: 02 08 14 20 (son las horas en las que hay datos de 1983 a 1990), hago la climatologia promediando en estas horas

descarto estaciones con mas del 50% de los datos faltantes en estas horas
estacion:
    87148: descarto 
    87155: mas datos a las 02 08 14 20 
    87166: mas datos a las 02 08 14 20
    87173: descarto
    87178: mas datos en 02 08 14 20
    87187: descarto
    87270: mas datos en 02 08 14 20
    87281: descarto
    87289: mas datos en 02 08 14 20
    87393: mas datos en 02 08 14 20
    87395: mas datos en 02 08 14 20 
  
"""
#%% Data. Corro funciones.
#hago histogramas de datos
estaciones_definitivas={"Concordia Aero": 87395, "Corrientes Aero": 87166,  "Monte Caseros Aero": 87393, "Paso de los Libres Aero": 87289, "Posadas Aero": 87178, "Reconquista Aero": 87270, "Resistencia Aero":87155}

for estacion in estaciones_definitivas:
    try:
        data_histogramas(df_data_por_estacion,estacion,estaciones[estacion],fecha_inicio="01/12/1983", fecha_final="31/12/2016")
    except ValueError:
        print("Error en la estacion:"+ estacion)
#%% Proceso Data: medias mensuales. opcion 1. Corro funciones. 

media_mensual_diaria_estaciones=pd.concat([media_mensual_diaria(df_data_por_estacion,87395),
                                           media_mensual_diaria(df_data_por_estacion,87166),
                                           media_mensual_diaria(df_data_por_estacion,87393),
                                           media_mensual_diaria(df_data_por_estacion,87289),
                                           media_mensual_diaria(df_data_por_estacion,87178),
                                           media_mensual_diaria(df_data_por_estacion,87270),
                                           media_mensual_diaria(df_data_por_estacion,87155)],axis=1)

#guardo df as csv
media_mensual_diaria_estaciones.to_csv("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data_procesada/media_mensual_diaria_estaciones.csv")

#grafico
data_procesada_series()
data_procesada_histogramas()
data_procesada_histogramas_estacion(12, 1, 2, "DEF")
data_procesada_histogramas_estacion(3, 4, 5, "MAM")
data_procesada_histogramas_estacion(6, 7, 8, "JJA")
data_procesada_histogramas_estacion(9, 10, 11, "SON")

#veo datos faltantes por estacion ANUAL
def procentaje_datos_faltantes(estacion):
    total=len(media_mensual_diaria_estaciones[estacion])
    faltantes=sum(pd.isna(media_mensual_diaria_estaciones[estacion]))
    return round(faltantes/total*100, 2)

def procentaje_datos_faltantes_estacion(mes1, mes2, mes3, estacion):
    data=pd.concat([media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes1],
                media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes2],
                media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes3]])
    total=len(data)
    faltantes=sum(pd.isna(data))
    return round(faltantes/total*100, 2)

procentaje_datos_faltantes(87395)
procentaje_datos_faltantes(87166)
procentaje_datos_faltantes(87393)
procentaje_datos_faltantes(87289)
procentaje_datos_faltantes(87178)
procentaje_datos_faltantes(87270)
procentaje_datos_faltantes(87155)
procentaje_datos_faltantes(87166)

procentaje_datos_faltantes_estacion(12,1,2,87395)
procentaje_datos_faltantes_estacion(3,4,5,87395)
procentaje_datos_faltantes_estacion(6,7,8,87395)
procentaje_datos_faltantes_estacion(9,10,11,87395)


procentaje_datos_faltantes_estacion(12,1,2,87166)
procentaje_datos_faltantes_estacion(3,4,5,87166)
procentaje_datos_faltantes_estacion(6,7,8,87166)
procentaje_datos_faltantes_estacion(9,10,11,87166)

procentaje_datos_faltantes_estacion(12,1,2,87393)
procentaje_datos_faltantes_estacion(3,4,5,87393)
procentaje_datos_faltantes_estacion(6,7,8,87393)
procentaje_datos_faltantes_estacion(9,10,11,87393)

#seguir de aca 
procentaje_datos_faltantes(87166)
procentaje_datos_faltantes(87393)
procentaje_datos_faltantes(87289)
procentaje_datos_faltantes(87178)
procentaje_datos_faltantes(87270)
procentaje_datos_faltantes(87155)
procentaje_datos_faltantes(87166)
#%% Proceso Data: medias mensuales. opcion 2. Corro funciones. 

media_mensual_diaria_estaciones=pd.concat([media_mensual_diaria(df_data_por_estacion,87395),
                                           media_mensual_diaria(df_data_por_estacion,87166),
                                           media_mensual_diaria(df_data_por_estacion,87393),
                                           media_mensual_diaria(df_data_por_estacion,87289),
                                           media_mensual_diaria(df_data_por_estacion,87178),
                                           media_mensual_diaria(df_data_por_estacion,87270),
                                           media_mensual_diaria(df_data_por_estacion,87155)],axis=1)

#guardo df as csv
media_mensual_diaria_estaciones.to_csv("../../../resultados/resultados2021/nubosidad/nubosidad_observada/smn_dcao/data_procesada/media_mensual_diaria_estaciones_opc2.csv")

#grafico
data_procesada_series()
data_procesada_histogramas()
data_procesada_histogramas_estacion(12, 1, 2, "DEF")
data_procesada_histogramas_estacion(3, 4, 5, "MAM")
data_procesada_histogramas_estacion(6, 7, 8, "JJA")
data_procesada_histogramas_estacion(9, 10, 11, "SON")

#veo datos faltantes por estacion ANUAL
def procentaje_datos_faltantes(estacion):
    total=len(media_mensual_diaria_estaciones[estacion])
    faltantes=sum(pd.isna(media_mensual_diaria_estaciones[estacion]))
    return round(faltantes/total*100, 2)

def procentaje_datos_faltantes_estacion(mes1, mes2, mes3, estacion):
    data=pd.concat([media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes1],
                media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes2],
                media_mensual_diaria_estaciones[estacion][media_mensual_diaria_estaciones[estacion].index.month==mes3]])
    total=len(data)
    faltantes=sum(pd.isna(data))
    return round(faltantes/total*100, 2)

procentaje_datos_faltantes(87395)
procentaje_datos_faltantes(87166)
procentaje_datos_faltantes(87393)
procentaje_datos_faltantes(87289)
procentaje_datos_faltantes(87178)
procentaje_datos_faltantes(87270)
procentaje_datos_faltantes(87155)
procentaje_datos_faltantes(87166)

procentaje_datos_faltantes_estacion(12,1,2,87395)
procentaje_datos_faltantes_estacion(3,4,5,87395)
procentaje_datos_faltantes_estacion(6,7,8,87395)
procentaje_datos_faltantes_estacion(9,10,11,87395)

#seguir de aca 
procentaje_datos_faltantes(87166)
procentaje_datos_faltantes(87393)
procentaje_datos_faltantes(87289)
procentaje_datos_faltantes(87178)
procentaje_datos_faltantes(87270)
procentaje_datos_faltantes(87155)
procentaje_datos_faltantes(87166)