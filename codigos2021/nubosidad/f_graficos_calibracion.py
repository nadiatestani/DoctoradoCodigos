#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:27:11 2021

@author: nadia

f_graficos_calibracion.py
"""

#f_graficos_calibracion.py

import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import os
import datetime as dt

from f_porc_to_oktas import data_frame_oktas
import f_paletas_colores
from c_clases_satelite import dataframe_satelite, frecuencias_oktas
from c_clases_smn import dataframe_smn

def grafico_puntos(lista_puntos_satelital, dict_puntos_smn, lista_puntos_smn_importantes, shape_paises, shape_provincias):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el smn 
    en un entorno a corrientes
    """
    #defino puntos a marcar
    geometry_1 = [Point(xy) for xy in lista_puntos_satelital] #lista con puntos 1
    geometry_2 = [Point(xy) for xy in list(dict_puntos_smn.values())] #lista con puntos 2
    geometry_3 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    geodata1 = gpd.GeoDataFrame(lista_puntos_satelital, geometry=geometry_1)
    geodata2 = gpd.GeoDataFrame(list(dict_puntos_smn.values()), geometry = geometry_2)
    geodata3 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_3)
    
    #inicio figura
    fig1 = plt.figure(figsize = [10, 6], dpi = 200)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 0.7, alpha = 0.8)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.4', alpha = 0.8)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 20, c = "seagreen") 
    geodata2.plot(ax = ax, markersize = 20, c = "cornflowerblue") 
    geodata3.plot(ax = ax, markersize = 20, c = "firebrick") 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-61, -53)[::1])
    plt.xticks(np.arange(-61, -53)[::1])
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-32, -25)[::1])
    plt.yticks(np.arange(-32, -25)[::1])
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    #ax.legend(["ISCCP","SMN", "SMN calibration"], loc = "lower left")
    ax.legend(["ISCCP", "SMN", "SMN calibration"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con numeros de estacion
    list_smn_etiquetas = [(lon-360, lat) for lon, lat in list(dict_puntos_smn.values())]
    for i, clave in enumerate(dict_puntos_smn):
        ax.annotate(str(clave), list_smn_etiquetas[i], size = 8, weight='bold')
    
    #agrego titulo
    plt.title("Satellital (ISCCP) and observed (SMN) cloud data points")
    
    #guardo figura
    #si trabajo desde PC:
    #plt.savefig("../../../resultados/resultados2021/nubosidad/calibracion/puntos.png")
    plt.savefig("puntos.png")

def grafico_puntos_paper(lista_puntos_satelital, dict_puntos_smn, lista_puntos_smn_importantes, shape_paises, shape_provincias):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el smn 
    en un entorno a corrientes
    """
    #defino puntos a marcar
    geometry_1 = [Point(xy) for xy in lista_puntos_satelital] #lista con puntos 1
    #geometry_2 = [Point(xy) for xy in list(dict_puntos_smn.values())] #lista con puntos 2
    geometry_3 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    geodata1 = gpd.GeoDataFrame(lista_puntos_satelital, geometry=geometry_1)
    #geodata2 = gpd.GeoDataFrame(list(dict_puntos_smn.values()), geometry = geometry_2)
    geodata3 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_3)
    
    #inicio figura
    fig1 = plt.figure(figsize = [10, 6], dpi = 600)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 0.7, alpha = 0.6)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.4', alpha = 0.6)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 20, c = "seagreen") 
    #geodata2.plot(ax = ax, markersize = 20, c = "cornflowerblue") 
    geodata3.plot(ax = ax, markersize = 20, c = "firebrick") 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-61, -53)[::1])
    plt.xticks(np.arange(-61, -53)[::1])
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-32, -25)[::1])
    plt.yticks(np.arange(-32, -25)[::1])
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    #ax.legend(["ISCCP","SMN", "SMN calibration"], loc = "lower left")
    ax.legend(["ISCCP", "SMN"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con numeros de estacion
    dict_puntos_smn_calibracion = dict(zip(lista_puntos_smn_importantes, [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]))
    list_smn_etiquetas = [(lon-360, lat) for lon, lat in list(dict_puntos_smn_calibracion.values())]
    for i, clave in enumerate(dict_puntos_smn_calibracion):
        ax.annotate(str(clave), list_smn_etiquetas[i], size = 7, weight='bold')
    
    #agrego titulo
    #plt.title("Satellital (ISCCP) and observed (SMN) cloud data points")
    
    #guardo figura
    #si trabajo desde PC:
    #plt.savefig("../../../resultados/resultados2021/nubosidad/calibracion/puntos.png")
    plt.savefig("puntos_paper.png") 
    

def grafico_puntos_paper(lista_puntos_satelital, dict_puntos_smn, lista_puntos_smn_importantes, shape_paises, shape_provincias):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el smn 
    en un entorno a corrientes
    """
    #defino puntos a marcar
    geometry_1 = [Point(xy) for xy in lista_puntos_satelital] #lista con puntos 1
    #geometry_2 = [Point(xy) for xy in list(dict_puntos_smn.values())] #lista con puntos 2
    geometry_3 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    geodata1 = gpd.GeoDataFrame(lista_puntos_satelital, geometry=geometry_1)
    #geodata2 = gpd.GeoDataFrame(list(dict_puntos_smn.values()), geometry = geometry_2)
    geodata3 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_3)
    
    #inicio figura
    fig1 = plt.figure(figsize = [10, 6], dpi = 600)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 0.7, alpha = 0.6)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.4', alpha = 0.6)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 20, c = "seagreen") 
    #geodata2.plot(ax = ax, markersize = 20, c = "cornflowerblue") 
    geodata3.plot(ax = ax, markersize = 20, c = "firebrick") 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-61, -53)[::1])
    plt.xticks(np.arange(-61, -53)[::1])
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-32, -25)[::1])
    plt.yticks(np.arange(-32, -25)[::1])
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    #ax.legend(["ISCCP","SMN", "SMN calibration"], loc = "lower left")
    ax.legend(["ISCCP", "SMN"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con numeros de estacion
    dict_puntos_smn_calibracion = dict(zip(lista_puntos_smn_importantes, [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]))
    list_smn_etiquetas = [(lon-360, lat) for lon, lat in list(dict_puntos_smn_calibracion.values())]
    for i, clave in enumerate(dict_puntos_smn_calibracion):
        ax.annotate(str(clave), list_smn_etiquetas[i], size = 7, weight='bold')
    
    #agrego titulo
    #plt.title("Satellital (ISCCP) and observed (SMN) cloud data points")
    
    #guardo figura
    #si trabajo desde PC:
    #plt.savefig("../../../resultados/resultados2021/nubosidad/calibracion/puntos.png")
    plt.savefig("puntos_paper.png")    
    


def histograma_oktas_sat(data_frame_cldamt_punto, fecha_inicio_str, fecha_final_str, lon, lat, estaciones = False, meses = False):
    """
    Grafico histograma de nubosidad en oktas para un punto de lon y lat 
    
    estaciones: hace 4 graficos, uno por estacion
    meses: hace 12 graficos, uno por mes
    
    Tengo que estar en directorio donde se van a guardar los graficos para ese punto
    """    
    plt.close()
    if estaciones == False and meses == False:
        fig = plt.figure(num=1, figsize=(8, 5), dpi=80)
        bins = np.arange(10) - 0.5
        plt.plot() # define la figura
        plt.hist(data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str],density=True,color="seagreen",bins=bins,align='mid',edgecolor='black')
        plt.grid(axis="y")
        plt.ylabel("frequency")
        plt.yticks(np.arange(0,0.6,0.1))
        plt.ylim((0,0.5))
        plt.xticks(range(9))
        plt.xlim([-1, 9])
        plt.xlabel("okta")
        plt.title(f"ISCCP-H cldamt {fecha_inicio_str} - {fecha_final_str}\n lon: {lon-360} - lat: {lat}")
        plt.savefig("histograma_"+str(lon-360)+"_"+str(lat)+".png")
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        fig.suptitle(f"ISCCP-H cldamt {fecha_inicio_str} - {fecha_final_str}\n lon: {lon-360} - lat: {lat}", size=18)
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                data = pd.concat([data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str][data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str].index.month == mes1],
                                  data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str][data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str].index.month == mes2],
                                  data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str][data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str].index.month == mes3]])
                ax[j, i].hist(data, density=True, color="seagreen", bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                ax[j, i].set_ylim((0,0.9))
                ax[j, i].set_yticks(np.arange(0,1, 0.2))
                ax[j, i].set_xlim([-1, 9])
                ax[j, i].set_xticks(range(9))
                ax[j, i].set_title(estacion[j][i])
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        fig.tight_layout()
        #plt.savefig("histograma_estacional"+str(lon-360)+"_"+str(lat)+".png")
        plt.show
        
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        fig.suptitle(f"ISCCP-H cldamt {fecha_inicio_str} - {fecha_final_str}\n lon: {lon-360} - lat: {lat}", size=18)
        meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
        meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        for j in range(0, 4):
            for i in range(0, 3):
                bins = np.arange(10) - 0.5
                data = data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str][data_frame_cldamt_punto[2].loc[fecha_inicio_str:fecha_final_str].index.month == meses_num[j][i]]
                ax[j, i].hist(data, density=True, color="seagreen", bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                ax[j, i].set_ylim((0,0.9))
                ax[j, i].set_yticks(np.arange(0,1, 0.2))
                ax[j, i].set_xlim([-1, 9])
                ax[j, i].set_xticks(range(9))
                ax[j, i].set_title(meses[j][i]) 
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 3: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        fig.tight_layout()
        plt.savefig("histograma_mensual"+str(lon-360)+"_"+str(lat)+".png")
        plt.show
    
    elif estaciones == True and meses == True:
        raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")


def histograma_oktas_sat_smn(id_omm, df_data_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon, lat, estaciones = False, meses = False, agrupo = None):
    """
    Grafico histograma de nubosidad en oktas para un punto de lon y lat 
    
    estaciones: hace 4 graficos, uno por estacion
    meses: hace 12 graficos, uno por mes
    
    Tengo que estar en directorio donde se van a guardar los graficos para ese punto
    """    
    plt.close()
    
    instancia_serie_satelital = dataframe_satelite(data_frame_cldamt_punto).genero_serie("cldamt_oktas", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_satelite
    instancia_serie_smn = dataframe_smn(df_data_smn).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    
    if estaciones == False and meses == False:
        fig = plt.figure(num=1, figsize=(8, 5), dpi=80)
        bins = np.arange(10) - 0.5
        width = (bins[1]-bins[0])/3
        plt.plot() # define la figura
        plt.hist(instancia_serie_satelital.serie,density=True,color="seagreen",bins=bins+width/2,align='mid',edgecolor='black', width = width)
        plt.hist(instancia_serie_smn.serie,density=True,color="firebrick",bins=bins,align='right',edgecolor='black', width = width)
        plt.grid(axis="y")
        plt.ylabel("frequency")
        if instancia_serie_smn.es_diario():
            if agrupo:
                plt.yticks(np.arange(0,0.55,0.10))
                plt.ylim((0,0.50))
            else:
                plt.yticks(np.arange(0,0.35,0.05))
                plt.ylim((0,0.3))
        else:
            plt.yticks(np.arange(0,0.6,0.1))
            plt.ylim((0,0.5))
        if agrupo == 1:
            plt.xticks([0,1,2,3,4],["0","1-2","3-4","5-6","7-8"])
            plt.xlim([-1,5])
        elif agrupo == 2:
            plt.xticks([0,1,2],["0-1-2","3-4-5","6-7-8"])
            plt.xlim([-1,3])    
        #
        else:
            plt.xticks(range(9))
            plt.xlim([-1, 9])
        plt.xlabel("TCC (oktas)")
        plt.legend(["ISCCP-H","SMN"], loc = "upper right")
        if instancia_serie_smn.es_diario(): #si el paso es diario
            plt.title(f"Daily mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}")
            if agrupo:
                plt.savefig(f"isccp_smn_histograma_diario_{lon}_{lat}_{id_omm}_grupo{agrupo}.png")
            else:
                plt.savefig(f"isccp_smn_histograma_diario_{lon}_{lat}_{id_omm}.png")
        else:
            plt.title(f"Monthly mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}")
            plt.savefig(f"isccp_smn_histograma_mensual_{lon}_{lat}_{id_omm}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if instancia_serie_smn.es_diario(): #si el paso es diario
            fig.suptitle(f"Daily mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}", size=18)
        else:
            fig.suptitle(f"Monthly mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}", size=18)
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5
                width = (bins[1]-bins[0])/3
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                data_ISCCP = pd.concat([instancia_serie_satelital.serie[instancia_serie_satelital.serie.index.month == mes1],
                                        instancia_serie_satelital.serie[instancia_serie_satelital.serie.index.month == mes2],
                                        instancia_serie_satelital.serie[instancia_serie_satelital.serie.index.month == mes3]])
                data_SMN = pd.concat([instancia_serie_smn.serie[instancia_serie_smn.serie.index.month == mes1],
                                      instancia_serie_smn.serie[instancia_serie_smn.serie.index.month == mes2],
                                      instancia_serie_smn.serie[instancia_serie_smn.serie.index.month == mes3]])
                
                ax[j, i].hist(data_ISCCP, density=True, color="seagreen", bins=bins+width/2, align='mid', edgecolor='black', width = width)
                ax[j, i].hist(data_SMN, density=True, color="firebrick", bins=bins, align='right', edgecolor='black', width = width)
                ax[j, i].grid(axis="y")
                
                if instancia_serie_smn.es_diario():
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:
                        ax[j, i].set_yticks(np.arange(0,0.35,0.05))
                        ax[j, i].set_ylim((0,0.3))
                else:
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0,1, 0.2))
                
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(estacion[j][i])
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie_smn.es_diario():
                        if agrupo:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5])       
                        else:
                            ax[j, i].set_yticklabels([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
                    else:
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])   
                if i == 1 and j == 0:
                    ax[j, i].legend(["ISCCP-H","SMN"], loc = "upper right")
        fig.tight_layout()
        if instancia_serie_smn.es_diario(): #si el paso es diario
            if agrupo:
                plt.savefig(f"isccp_smn_histograma_estacional_diario_{lon}_{lat}_{id_omm}_grupo{agrupo}.png")
            else:
                plt.savefig(f"isccp_smn_histograma_estacional_diario_{lon}_{lat}_{id_omm}.png")
        else:
            plt.savefig(f"isccp_smn_histograma_estacional_mensual_{lon}_{lat}_{id_omm}.png")
        plt.show()
        
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        if instancia_serie_smn.es_diario(): #si el paso es diario
            fig.suptitle(f"Daily mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}", size=18)
        else:
            fig.suptitle(f"Monthly mean total cloud cover (oktas) {fecha_inicio_str} - {fecha_final_str}\n SMN: {id_omm} ; ISCCP-H: {lon}, {lat}", size=18)
        meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
        meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        for j in range(0, 4):
            for i in range(0, 3):
                bins = np.arange(10) - 0.5
                width = (bins[1]-bins[0])/3
                data_ISCCP = instancia_serie_satelital.serie[instancia_serie_satelital.serie.index.month == meses_num[j][i]]
                data_SMN = instancia_serie_smn.serie[instancia_serie_smn.serie.index.month == meses_num[j][i]]
                ax[j, i].hist(data_ISCCP, density=True, color="seagreen", bins=bins+width/2, align='mid', edgecolor='black', width = width)
                ax[j, i].hist(data_SMN, density=True, color="firebrick", bins=bins, align='right', edgecolor='black', width = width)
                ax[j, i].grid(axis="y")
                if instancia_serie_smn.es_diario():
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:
                        ax[j, i].set_yticks(np.arange(0,0.35,0.05))
                        ax[j, i].set_ylim((0,0.3))
                else:
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0,1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(meses[j][i]) 
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie_smn.es_diario():
                        if agrupo:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4,0.5])  
                        else:
                            ax[j, i].set_yticklabels([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
                    else:
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 3: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
                #agrego leyenda solo a grafico superior derecho
                if i == 2 and j == 0:
                    ax[j, i].legend(["ISCCP-H","SMN"], loc = "upper right")
        fig.tight_layout()
        if instancia_serie_smn.es_diario(): #si el paso es diario
            if agrupo:
                plt.savefig(f"isccp_smn_histograma_mensual_diario_{lon}_{lat}_{id_omm}_grupo{agrupo}.png")
            else:
                plt.savefig(f"isccp_smn_histograma_mensual_diario_{lon}_{lat}_{id_omm}.png")
        else:
            if agrupo:
                plt.savefig(f"isccp_smn_histograma_mensual_mensual_{lon}_{lat}_{id_omm}_grupo{agrupo}.png")
            else:
                plt.savefig(f"isccp_smn_histograma_mensual_mensual_{lon}_{lat}_{id_omm}.png")
        plt.show()
    
    elif estaciones == True and meses == True:
        raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")

        
###################### series diarias de distintas formas como en se definieron para smn en f_graficos_smn #################### 

def scatter(lon, lat, df_data, fecha_inicio_str, fecha_final_str, variable = "cldamt_oktas", etiqueta_datos_faltantes = False):
    """
    Hace scatter plots con data: variable (str) del df_data entre fecha_inicio_str yyyy-mm-dd y fecha_final_str yyyy-mm-dd
    """    
    instancia_serie = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_satelite
    fig = plt.figure(num=2, figsize=(8, 5), dpi=80)    
    plt.plot() 
    plt.scatter(instancia_serie.serie.index, instancia_serie.serie, marker = '.', color="cornflowerblue")
    if instancia_serie.es_diario(): #si el paso es diario
        plt.title(f"Daily total cloud cover (oktas) ISCCP-H \n {lon} {lat}")
    else:
        plt.title(f"Monthly mean total cloud cover (oktas) ISCCP-H \n {lon} {lat}")
    plt.yticks(np.arange(0, 9, 1))
    plt.ylim((0,9))
    plt.ylabel("TCC (oktas)")
    plt.xlabel("Date")
    plt.grid(axis="y")
    if etiqueta_datos_faltantes == True:
        porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
        plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (400,320), xycoords='figure pixels', size = 10, weight='bold')
    fig.savefig(f"scatter_{str(lon)}_{str(lat)}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show()

def histograma(lon, lat, df_data, fecha_inicio_str, fecha_final_str, variable = "cldamt_oktas", estaciones = False, meses = False, agrupo = None):
    """
    Hace histogramas con data: variable(str) del df_data entre fecha_inicio_str yyyy-mm-dd y fecha_final_str yyyy-mm-dd
    """
    instancia_serie = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    if estaciones == False and meses == False:
        plt.close()   
        fig = plt.figure(num=1, figsize=(8, 5), dpi=80)
        bins = np.arange(10) - 0.5
        plt.plot()
        plt.hist(instancia_serie.serie, density = True, color = "cornflowerblue", bins = bins, align = 'mid', edgecolor = 'black')
        plt.grid(axis="y")
        plt.ylabel("frequency")
        if instancia_serie.es_diario(): #si es diario
            if agrupo:
                plt.yticks(np.arange(0,0.55,0.10))
                plt.ylim((0,0.50))
            else:
                plt.yticks(np.arange(0,0.25,0.05))
                plt.ylim((0,0.20))
        else: #si es mensual
            plt.yticks(np.arange(0,1,0.2))
            plt.ylim((0,0.9))
        #
        if agrupo == 1:
            plt.xticks([0,1,2,3,4],["0","1-2","3-4","5-6","7-8"])
            plt.xlim([-1,5])
        elif agrupo == 2:
            plt.xticks([0,1,2],["0-1-2","3-4-5","6-7-8"])
            plt.xlim([-1,3])    
        #
        else:
            plt.xticks(range(9))
            plt.xlim([-1, 9])
        plt.xlabel("TCC (oktas)")
        if instancia_serie.es_diario(): #si es diario
            plt.title(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}")
        else:
            plt.title(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}")
        
        if agrupo == 1:
            fig.savefig(f"histograma_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
        elif agrupo == 2:
            fig.savefig(f"histograma_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
        else:
            fig.savefig(f"histograma_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if instancia_serie.es_diario(): #si es diario
            fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}", size=18)
        else:
            fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}", size=18)
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                data = pd.concat([instancia_serie.serie[instancia_serie.serie.index.month == mes1],
                                  instancia_serie.serie[instancia_serie.serie.index.month == mes2],
                                  instancia_serie.serie[instancia_serie.serie.index.month == mes3]])
                ax[j, i].hist(data, density=True, color="cornflowerblue", bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                if instancia_serie.es_diario(): #si es diario
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0, 1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(estacion[j][i])
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie.es_diario(): #si es diario
                        if agrupo:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5])       
                        else:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                                       
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        fig.tight_layout()
        if instancia_serie.es_diario(): #si es diario
            if agrupo == 1:
                plt.savefig(f"histograma_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
                plt.show()
            elif agrupo == 2:
                plt.savefig(f"histograma_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
                plt.show()
            else:
                plt.savefig(f"histograma_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
                plt.show()
        else:
            if agrupo:
                plt.savefig(f"histograma_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"histograma_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
            plt.show()
        
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        if instancia_serie.es_diario(): #si es diario
            fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}", size=18)
        else: 
            fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {lon} {lat}", size=18)
        meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
        meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        for j in range(0, 4):
            for i in range(0, 3):
                bins = np.arange(10) - 0.5
                data = instancia_serie.serie[instancia_serie.serie.index.month == meses_num[j][i]]
                ax[j, i].hist(data, density=True, color="cornflowerblue", bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                if instancia_serie.es_diario(): #si es diario
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0, 1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(meses[j][i]) 
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie.es_diario(): #si es diario
                        if agrupo:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4,0.5])   
                        else:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 3: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        fig.tight_layout()
        if instancia_serie.es_diario(): #si es diario
            if agrupo == 1:
                plt.savefig(f"histograma_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
                plt.show()
            elif agrupo == 2:
                plt.savefig(f"histograma_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
                plt.show()
            else:
                plt.savefig(f"histograma_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
                plt.show()
        else:
            if agrupo:
                plt.savefig(f"histograma_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"histograma_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
            plt.show()
    
    elif estaciones == True and meses == True:
        raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")


def stackplot(frecuencias, lon, lat, df_data, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores, etiqueta_datos_faltantes = False, frecuencias_DJF = None, frecuencias_MAM = None, frecuencias_JJA = None, frecuencias_SON = None, estaciones = False, meses = False, agrupo = None, freq_relativa = False):
    """ frecuencias: df con frecuencia de oktas por anio """
    instancia_serie = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)
    
    if estaciones == False and meses == False:
        plt.figure(num=1, figsize=(8, 5), dpi=200)
        ax = plt.gca()
        ax.set_facecolor('#E7E7DE')
        if agrupo == 1:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0","1-2","3-4","5-6","7-8"], colors =  colores) 
        elif agrupo == 2:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0-1-2","3-4-5","6-7-8"], colors =  colores) 
        else:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0","1","2","3","4","5","6","7","8"], colors =  colores)       
        handles, labels = ax.get_legend_handles_labels() #para poder invertir el orden de las oktas en la leyenda
        ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.1, 1), prop={'size': 8})
        if freq_relativa:
            plt.ylabel("Frequency %")
        else:
            plt.ylabel("Frequency")
        
        if freq_relativa:
            ylim = 100
        
        else:
            if frecuencias_oktas(frecuencias).es_diario():
                ylim = 365
            else: 
                ylim = 12
        plt.ylim(0, ylim)
        plt.xlim(frecuencias.index[0], frecuencias.index[-1])
        plt.xlabel("Year")
        if frecuencias_oktas(frecuencias).es_diario():
            plt.title(f"Frecuency of daily mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat}")
        else:
            plt.title(f"Frecuency of monthly mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat}")
        if etiqueta_datos_faltantes == True:
            porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
            plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (1000,830), xycoords='figure pixels', size = 10, bbox=dict(boxstyle="round4", fc="#E7E7DE", alpha = 0.6))
        else: #ver esto
            None
        
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        
        else:
            if agrupo:
                plt.savefig(f"stackedarea_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()
        
    elif estaciones == False and meses == True:    
        plt.figure(num=1, figsize=(8, 5), dpi=200)
        ax = plt.gca()
        ax.set_facecolor('#E7E7DE')
        if agrupo == 1:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0","1-2","3-4","5-6","7-8"], colors =  colores) 
        elif agrupo == 2:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0-1-2","3-4-5","6-7-8"], colors =  colores) 
        else:
            plt.stackplot(frecuencias.index,np.array(frecuencias).transpose(), labels=["0","1","2","3","4","5","6","7","8"], colors =  colores)       
        handles, labels = ax.get_legend_handles_labels() #para poder invertir el orden de las oktas en la leyenda
        ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.1, 1), prop={'size': 8})
        if freq_relativa:
            plt.ylabel("Frequency %")
        else:
            plt.ylabel("Frequency")
        
        if freq_relativa:
            ylim = 100
        
        else:
            ylim = 31
            
        plt.ylim(0, ylim)
        
        plt.xlim(frecuencias.index[0], frecuencias.index[-1])
        plt.xticks(frecuencias.index[::48],  pd. to_datetime(frecuencias.index[::48]).year) 
        plt.xlabel("Year")
        plt.title(f"Monthly frecuency of daily mean total cloud cover (oktas) ISCCP-H \n {lon} {lat}")
        
        if etiqueta_datos_faltantes == True:
            porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
            plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (1000,830), xycoords='figure pixels', size = 10, bbox=dict(boxstyle="round4", fc="#E7E7DE", alpha = 0.6))
        else: #ver esto
            None
        
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        
        else:
            if agrupo:
                plt.savefig(f"stackedarea_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_mensual_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
    
        instancia_frecuencia_DJF = frecuencias_oktas(frecuencias_DJF)
        frecuencias_DJF = instancia_frecuencia_DJF.selecciono_fechas(fecha_inicio_str, fecha_final_str)
        
        instancia_frecuencia_MAM = frecuencias_oktas(frecuencias_MAM)
        frecuencias_MAM = instancia_frecuencia_MAM.selecciono_fechas(fecha_inicio_str, fecha_final_str)
                    
        instancia_frecuencia_JJA = frecuencias_oktas(frecuencias_JJA)
        frecuencias_JJA = instancia_frecuencia_JJA.selecciono_fechas(fecha_inicio_str, fecha_final_str)
        
        instancia_frecuencia_SON = frecuencias_oktas(frecuencias_SON)
        frecuencias_SON = instancia_frecuencia_SON.selecciono_fechas(fecha_inicio_str, fecha_final_str)
        
        frecuencias_estaciones = [[frecuencias_DJF, frecuencias_MAM], [frecuencias_JJA, frecuencias_SON]]
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if frecuencias_oktas(frecuencias).es_diario():
            fig.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat}", size=18)
        else:
            fig.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat}", size=18)

        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
           
                ax[j, i].set_facecolor('#E7E7DE')
                if agrupo == 1:
                    ax[j, i].stackplot(frecuencias_estaciones[j][i].index,np.array(frecuencias_estaciones[j][i]).transpose(), labels=["0","1-2","3-4","5-6","7-8"], colors =  colores) 
                elif agrupo == 2:
                    ax[j, i].stackplot(frecuencias_estaciones[j][i].index,np.array(frecuencias_estaciones[j][i]).transpose(), labels=["0-1-2","3-4-5","6-7-8"], colors =  colores) 
                else:
                    ax[j, i].stackplot(frecuencias_estaciones[j][i].index,np.array(frecuencias_estaciones[j][i]).transpose(), labels=["0","1","2","3","4","5","6","7","8"], colors =  colores) 
                if freq_relativa:
                    ax[j, i].set_ylim((0, 100))
                else:
                    if frecuencias_oktas(frecuencias).es_diario():
                        ax[j, i].set_ylim((0, 91))
                    else: 
                        ax[j, i].set_ylim((0, 3))
                
                ax[j,i].set_xlim(frecuencias.index[0], frecuencias.index[-1])
                ax[j, i].set_title(estacion[j][i])

                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    if freq_relativa:
                        ax[j, i].set_ylabel("Frequency %")
                    else:
                        ax[j, i].set_ylabel("Frequency")
                    #if frecuencias_oktas(frecuencias).es_diario(): #si es diario
                     #   ax[j, i].set_yticklabels([0, 120, 240, 360])
                    #else: #si es mensual
                     #   ax[j, i].set_yticklabels([0, 3, 6, 9, 12])
                else:
                    ax[j, i].set_yticklabels([])
                    if j == 1: #solo para los de abajo pongo el xlabel
                        ax[j, i].set_xlabel("Year")  
                    else:
                        ax[j, i].set_xticklabels([])
                        
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("Year")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        ax = plt.gca()
        handles, labels = ax.get_legend_handles_labels() #para poder invertir el orden de las oktas en la leyenda
        if agrupo == 1:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.19, 1.0), prop={'size': 8})
        elif agrupo == 2:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.20, 1.0), prop={'size': 8})
        else:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.17, 1.0), prop={'size': 8})
            
        fig.tight_layout()
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_estaciones_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_estaciones_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        else:
            if agrupo:
                plt.savefig(f"stackedarea_estaciones_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_estaciones_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()   
        
def barplot_oktas_separadas(frecuencias, lon, lat, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores):
    
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)

    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=200)
    if frecuencias_oktas(frecuencias).es_diario():
        plt.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat} ", size=14)
    else: 
        plt.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year ISCCP-H \n {lon} {lat} ", size=14)
    
    if frecuencias_oktas(frecuencias).es_diario():
        ylim = 160
    else: 
        ylim = 12
    
    for i in range(0, 3):
                for j in range(0, 3):
                    ax[i, j].set_facecolor('#E7E7DE')
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], color = colores[3*i+j])
                    ax[i, j].set_ylim((0,ylim))
                    ax[i, j].set_yticks(np.arange(0,ylim+1, ylim//6))
                    ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        ax[i, j].set_ylabel("Frequency")
                    else:
                        ax[i, j].set_yticklabels([])
                    if i == 2: #solo para los de abajo pongo el xlabel
                        ax[i, j].set_xlabel("Year")  
                    else:
                        ax[i, j].set_xticklabels([])
    fig.tight_layout()
    plt.savefig(f"barplot_oktas_separadas_{lon}_{lat}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show()
    
    
    
    
def histogramas_partidos(lon, lat, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, fecha_inicio_str_0 = None, fecha_final_str_0 = None, variable = "cldamt_oktas", estaciones = False, meses = False, agrupo = None):
    """
    Hace dos o 3 histogramas con data: variable(str) del df_data entre fecha_inicio_str_1 yyyy-mm-dd y fecha_final_str_1 yyyy-mm-dd
                                   y variable(str) del df_data entre fecha_inicio_str_2 yyyy-mm-dd y fecha_final_str_2 yyyy-mm-dd
    """
    instancia_serie_1 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_1, fecha_final_str_1) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_2, fecha_final_str_2) #uso clases de c_clases_smn
    if fecha_inicio_str_0:
        instancia_serie_0 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_0, fecha_final_str_0) #uso clases de c_clases_smn
    
    if estaciones == False and meses == False:
        plt.close()   
        fig = plt.figure(num=1, figsize=(8, 5), dpi=80)
        bins = np.arange(10) - 0.5
        plt.plot()
        if fecha_inicio_str_0:
            plt.hist([instancia_serie_0.serie, instancia_serie_1.serie, instancia_serie_2.serie], density = True, color = ["firebrick","darkorange", "darkcyan"], bins = bins, align = 'mid', edgecolor = 'black')
        else:
            plt.hist([instancia_serie_1.serie, instancia_serie_2.serie], density = True, color = ["darkorange", "darkcyan"], bins = bins, align = 'mid', edgecolor = 'black')
        plt.grid(axis="y")
        plt.ylabel("frequency")
        if instancia_serie_1.es_diario(): #si es diario
            if agrupo:
                plt.yticks(np.arange(0,0.55,0.10))
                plt.ylim((0,0.50))
            else:
                plt.yticks(np.arange(0,0.30,0.05))
                plt.ylim((0,0.25))
        else: #si es mensual
            plt.yticks(np.arange(0,1,0.2))
            plt.ylim((0,0.9))
        if agrupo == 1:
            plt.xticks([0,1,2,3,4],["0","1-2","3-4","5-6","7-8"])
            plt.xlim([-1,5])
        elif agrupo == 2:
            plt.xticks([0,1,2],["0-1-2","3-4-5","6-7-8"])
            plt.xlim([-1,3])  
        else:
            plt.xticks(range(9))
            plt.xlim([-1, 9])
        plt.xlabel("TCC (oktas)")
        
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                plt.title(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]} {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}")
                    
            else:
                plt.title(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}")
                
        else:
            if fecha_inicio_str_0:
                plt.title(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]} {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}")
            else:
                plt.title(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}")
        if fecha_inicio_str_0:
            plt.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        else:
            plt.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        if fecha_inicio_str_0:
            if agrupo == 1:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo1.png")
            elif agrupo == 2:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo2.png")
            else:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
        else:
            if agrupo:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
            else:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
            else:
                fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
            else:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                if fecha_inicio_str_0:
                    data_0 = pd.concat([instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes1],
                                      instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes2],
                                      instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes3]])
                data_1 = pd.concat([instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes1],
                                  instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes2],
                                  instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes3]])
                data_2 = pd.concat([instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes1],
                                  instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes2],
                                  instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes3]])
                if fecha_inicio_str_0:
                    ax[j, i].hist([data_0, data_1, data_2], density=True, color= ["firebrick","darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                else:
                    ax[j, i].hist([data_1, data_2], density=True, color= ["darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                if instancia_serie_1.es_diario(): #si es diario
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:   
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0, 1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(estacion[j][i])
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie_1.es_diario(): #si es diario
                        if agrupo:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5])       
                        else:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        if fecha_inicio_str_0:
            fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8])  
        else:
            fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8])       
        fig.tight_layout()
        
        if instancia_serie_1.es_diario(): 
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                    
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()
  
            else:
                if agrupo:
                        plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
        
                            
            plt.show()
    
    
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
            else:
                fig.suptitle(f"Daily total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
            else:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) ISCCP-H {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {lon} {lat}", size=18)
        meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
        meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        for j in range(0, 4):
            for i in range(0, 3):
                bins = np.arange(10) - 0.5
                if fecha_inicio_str_0:
                    data_0 = instancia_serie_0.serie[instancia_serie_0.serie.index.month == meses_num[j][i]]
                data_1 = instancia_serie_1.serie[instancia_serie_1.serie.index.month == meses_num[j][i]]
                data_2 = instancia_serie_2.serie[instancia_serie_2.serie.index.month == meses_num[j][i]]
                if fecha_inicio_str_0:
                    ax[j, i].hist([data_0,data_1, data_2], density=True, color= ["firebrick","darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                else:
                    ax[j, i].hist([data_1, data_2], density=True, color= ["darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                if instancia_serie_1.es_diario(): #si es diario
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0, 1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(meses[j][i]) 
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie_1.es_diario(): #si es diario
                        if agrupo:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4,0.5])   
                        else:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 3: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        if fecha_inicio_str_0:
            fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}",f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8]) 
        else:
            fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8]) 
        fig.tight_layout()
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                    
                
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                    
                
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()
                
                
#########################################################
def histogramas_partidos_poster(lon, lat, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, fecha_inicio_str_0 = None, fecha_final_str_0 = None, variable = "cldamt_oktas", estaciones = False, meses = False, agrupo = None):
    """
    Hace dos o 3 histogramas con data: variable(str) del df_data entre fecha_inicio_str_1 yyyy-mm-dd y fecha_final_str_1 yyyy-mm-dd
                                   y variable(str) del df_data entre fecha_inicio_str_2 yyyy-mm-dd y fecha_final_str_2 yyyy-mm-dd
    """
    instancia_serie_1 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_1, fecha_final_str_1) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_2, fecha_final_str_2) #uso clases de c_clases_smn
    if fecha_inicio_str_0:
        instancia_serie_0 = dataframe_satelite(df_data).genero_serie("cldamt_oktas", fecha_inicio_str_0, fecha_final_str_0) #uso clases de c_clases_smn
    
    if estaciones == False and meses == False:
        plt.close()   
        fig = plt.figure(num=1, figsize=(3.5, 2.5), dpi=200) #cambiar tamaño segun corresponda
        bins = np.arange(10) - 0.5 #ver si hay que cambiarlo
        plt.plot()
        if fecha_inicio_str_0:
            plt.hist([instancia_serie_0.serie, instancia_serie_1.serie, instancia_serie_2.serie], density = True, color = ["firebrick","darkorange", "darkcyan"], bins = bins, align = 'mid', edgecolor = 'black')
        else:
            plt.hist([instancia_serie_1.serie, instancia_serie_2.serie], density = True, color = ["darkorange", "darkcyan"], bins = bins, align = 'mid', edgecolor = 'black')
        plt.grid(axis="y")
        plt.ylabel("Frequency")
        if instancia_serie_1.es_diario(): #si es diario
            if agrupo:
                plt.yticks(np.arange(0,0.55,0.10))
                plt.ylim((0,0.50))
            else:
                plt.yticks(np.arange(0,0.30,0.05))
                plt.ylim((0,0.25))
        else: #si es mensual
            plt.yticks(np.arange(0,1,0.2))
            plt.ylim((0,0.9))
        if agrupo == 1:
            plt.xticks([0,1,2,3,4],["0","1-2","3-4","5-6","7-8"])
            plt.xlim([-1,5])
        elif agrupo == 2:
            plt.xticks([0,1,2],["0-1-2","3-4-5","6-7-8"])
            plt.xlim([-1,3])  
        else:
            plt.xticks(range(9))
            plt.xlim([-1, 9])
        plt.xlabel("TCC (oktas)")
        
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                plt.title(f"Daily CA \n ISCCP-H {lon} {lat}")
                    
            else:
                plt.title(f"Daily CA \n ISCCP-H {lon} {lat}")
                
        else:
            if fecha_inicio_str_0:
                plt.title(f"Monthly CA \n ISCCP-H {lon} {lat}")
            else:
                plt.title(f"Monthly CA \n ISCCP-H {lon} {lat}")
        if fecha_inicio_str_0:
            plt.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        else:
            plt.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        if fecha_inicio_str_0:
            if agrupo == 1:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo1_poster.png")
            elif agrupo == 2:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo2_poster.png")
            else:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
        else:
            if agrupo:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
            else:
                fig.savefig(f"histograma_partido_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[4.5, 4.5], dpi=200) #ver si lo tengo que cambiar
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily CA \n ISCCP-H {lon} {lat}")
            else:
                fig.suptitle(f"Daily CA \n ISCCP-H {lon} {lat}")
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly CA \n ISCCP-H {lon} {lat}")
            else:
                fig.suptitle(f"Monthly CA \n ISCCP-H {lon} {lat}")
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        for j in range(0, 2):
            for i in range(0, 2):
                bins = np.arange(10) - 0.5 #VER SI LO TENGO QUE CAMBIAR
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                if fecha_inicio_str_0:
                    data_0 = pd.concat([instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes1],
                                      instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes2],
                                      instancia_serie_0.serie[instancia_serie_0.serie.index.month == mes3]])
                data_1 = pd.concat([instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes1],
                                  instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes2],
                                  instancia_serie_1.serie[instancia_serie_1.serie.index.month == mes3]])
                data_2 = pd.concat([instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes1],
                                  instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes2],
                                  instancia_serie_2.serie[instancia_serie_2.serie.index.month == mes3]])
                if fecha_inicio_str_0:
                    ax[j, i].hist([data_0, data_1, data_2], density=True, color= ["firebrick","darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                else:
                    ax[j, i].hist([data_1, data_2], density=True, color= ["darkorange", "darkcyan"], bins=bins, align='mid', edgecolor='black')
                ax[j, i].grid(axis="y")
                if instancia_serie_1.es_diario(): #si es diario
                    if agrupo:
                        ax[j, i].set_ylim((0,0.50))
                        ax[j, i].set_yticks(np.arange(0,0.55, 0.1))
                    else:   
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,0.9))
                    ax[j, i].set_yticks(np.arange(0, 1, 0.2))
                if agrupo == 1:
                    ax[j,i].set_xlim([-1,5])
                    ax[j,i].set_xticks([0,1,2,3,4])
                    ax[j,i].set_xticklabels(["0","1-2","3-4","5-6","7-8"])
                elif agrupo == 2:
                    ax[j,i].set_xlim([-1,3])
                    ax[j,i].set_xticks([0,1,2])
                    ax[j,i].set_xticklabels(["0-1-2","3-4-5","6-7-8"])
                else:
                    ax[j, i].set_xlim([-1, 9])
                    ax[j, i].set_xticks(range(9))
                    ax[j,i].set_xticklabels(["0","1","2","3","4","5","6","7","8"])
                    
                ax[j, i].set_title(estacion[j][i])
                if i == 0: #solo para los del lateral izquierdo pongo el ylabel
                    ax[j, i].set_ylabel("frequency")
                    if instancia_serie_1.es_diario(): #si es diario
                        if agrupo:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5])       
                        else:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        #if fecha_inicio_str_0:
         #   fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.6,0.75])# loc = [0.85,0.8])  
        #else:
         #   fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.68,0.69])# loc = [0.85,0.8])    
        fig.tight_layout()
        
        if instancia_serie_1.es_diario(): 
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                    
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                plt.show()
  
            else:
                if agrupo:
                        plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{lon}_{lat}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
        
                            
            plt.show()
    