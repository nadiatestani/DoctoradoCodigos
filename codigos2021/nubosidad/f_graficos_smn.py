#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:38:49 2021

@author: nadia

f_graficos_smn
"""
#f_graficos_smn

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

import f_paletas_colores
from c_clases_smn import dataframe_smn, frecuencias_oktas

def scatter(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", etiqueta_datos_faltantes = True):
    """
    Hace scatter plots con data: variable (str) del df_data entre fecha_inicio_str yyyy-mm-dd y fecha_final_str yyyy-mm-dd
    """ 
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
        
    instancia_serie = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    fig = plt.figure(num=2, figsize=(8, 5), dpi=80)    
    plt.plot() 
    plt.scatter(instancia_serie.serie.index, instancia_serie.serie, marker = '.', color="cornflowerblue")
    if instancia_serie.es_diario(): #si el paso es diario
        plt.title(f"Daily total cloud cover (oktas) SMN\n {nombre_estacion} ({id_omm})")
    else:
        plt.title(f"Monthly mean total cloud cover (oktas) SMN\n {nombre_estacion} ({id_omm})")
    plt.yticks(np.arange(0, 9, 1))
    plt.ylim((0,9))
    plt.ylabel("TCC (oktas)")
    plt.xlabel("Date")
    plt.grid(axis="y")
    if etiqueta_datos_faltantes == True:
        porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
        plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (400,320), xycoords='figure pixels', size = 10, weight='bold')
    fig.savefig(f"scatter_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show()

def histograma(id_omm, df_data, fecha_inicio_str, fecha_final_str, variable = "nub", estaciones = False, meses = False, agrupo = None):
    """
    Hace histogramas con data: variable(str) del df_data entre fecha_inicio_str yyyy-mm-dd y fecha_final_str yyyy-mm-dd
    """
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_serie = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
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
            plt.yticks(np.arange(0,1.1,0.2))
            plt.ylim((0,1))
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
            plt.title(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})")
        else:
            plt.title(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})")
        
        if agrupo == 1:
            fig.savefig(f"histograma_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
        elif agrupo == 2:
            fig.savefig(f"histograma_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
        else:
            fig.savefig(f"histograma_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if instancia_serie.es_diario(): #si es diario
            fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
        else:
            fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
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
                    ax[j, i].set_ylim((0,1))
                    ax[j, i].set_yticks(np.arange(0, 1.1, 0.2))
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
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1])
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
                plt.savefig(f"histograma_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
                plt.show()
            elif agrupo == 2:
                plt.savefig(f"histograma_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
                plt.show()
            else:
                plt.savefig(f"histograma_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
                plt.show()
        else:
            if agrupo:
                plt.savefig(f"histograma_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"histograma_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
            plt.show()
        
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        if instancia_serie.es_diario(): #si es diario
            fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
        else: 
            fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str[0:4]}-{fecha_final_str[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
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
                    ax[j, i].set_ylim((0,1))
                    ax[j, i].set_yticks(np.arange(0, 1.1, 0.2))
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
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1])
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
                plt.savefig(f"histograma_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo1.png")
                plt.show()
            elif agrupo == 2:
                plt.savefig(f"histograma_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo2.png")
                plt.show()
            else:
                plt.savefig(f"histograma_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
                plt.show()
        else:
            if agrupo:
                plt.savefig(f"histograma_mensual_media_mensual{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"histograma_mensual_media_mensual{str(id_omm)}_{fecha_inicio_str}_{fecha_final_str}.png")
            plt.show()
    
    elif estaciones == True and meses == True:
        raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")

def stackplot(frecuencias, id_omm, df_data, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores, etiqueta_datos_faltantes = True, frecuencias_DJF = None, frecuencias_MAM = None, frecuencias_JJA = None, frecuencias_SON = None, estaciones = False, meses = False, agrupo = None, freq_relativa = False):
    """ frecuencias: df con frecuencia de oktas por anio """
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Ituzaingó"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_serie = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    
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
        
        if agrupo == 1:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.12, 1), prop={'size': 8})
        elif agrupo == 2:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.13, 1), prop={'size': 8})
        else:
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
            plt.title(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})")
        else:
            plt.title(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})")
        if etiqueta_datos_faltantes == True:
            porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
            plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (1000,830), xycoords='figure pixels', size = 10, bbox=dict(boxstyle="round4", fc="#E7E7DE", alpha = 0.6))
        else: #ver esto
            None
            
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
        
        else:
            if agrupo:
                plt.savefig(f"stackedarea_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
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
        
        if agrupo == 1:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.12, 1), prop={'size': 8})
        elif agrupo == 2:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.13, 1), prop={'size': 8})
        else:
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
        if dt.datetime.strptime(fecha_inicio_str,"%Y-%m-%d") > dt.datetime(2013,1,1):
            plt.xticks(frecuencias.index[::12],  pd. to_datetime(frecuencias.index[::12]).year) 
        else:
            plt.xticks(frecuencias.index[::48],  pd. to_datetime(frecuencias.index[::48]).year) 
        plt.xlabel("Year")
        plt.title(f"Monthly frecuency of daily mean total cloud cover (oktas) SMN \n {nombre_estacion} ({id_omm})")
        
        if etiqueta_datos_faltantes == True:
            porcentaje_datos_faltantes = instancia_serie.calculo_datos_faltantes()
            plt.annotate(f" Missing Values: %{porcentaje_datos_faltantes}", xy = (1000,830), xycoords='figure pixels', size = 10, bbox=dict(boxstyle="round4", fc="#E7E7DE", alpha = 0.6))
        else: #ver esto
            None
            
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_mensual_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_mensual_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
        
        else:
            if agrupo:
                plt.savefig(f"stackedarea_mensual_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_mensual_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
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
            fig.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=18)
        else:
            fig.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=18)

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
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.16, 1), prop={'size': 8})
        elif agrupo == 2:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.18, 1), prop={'size': 8})
        else:
            ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.13, 1), prop={'size': 8})
        fig.tight_layout()
        if freq_relativa:
            if agrupo:
                plt.savefig(f"stackedarea_relativa_estaciones_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_relativa_estaciones_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
        else:
            if agrupo:
                plt.savefig(f"stackedarea_estaciones_{id_omm}_{fecha_inicio_str}_{fecha_final_str}_grupo{agrupo}.png")
            else:
                plt.savefig(f"stackedarea_estaciones_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
        plt.show()   
        
def barplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores):
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)

    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=200)
    if frecuencias_oktas(frecuencias).es_diario():
        plt.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    else: 
        plt.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    
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
    plt.savefig(f"barplot_oktas_separadas_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show()

def barplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores):
 
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)

    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    lag = [-0.6, -0.45, -0.3, -0.15, 0, 0.15, 0.3, 0.45, 0.6] #seguir de aca 
    fig, ax = plt.subplots(figsize=[11, 6], dpi=200)
    if frecuencias_oktas(frecuencias).es_diario():
        plt.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    else: 
        plt.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    for i in range(0,9):
        plt.bar(frecuencias.index+lag[i], np.array(frecuencias).transpose()[i], color = colores[i], label = oktas[i],  width=0.13, align='center')
    ax.set_facecolor('#E7E7DE')
    if frecuencias_oktas(frecuencias).es_diario():
        ylim = 160
    else: 
        ylim = 12
    plt.ylim((0,ylim))
    plt.yticks(np.arange(0,ylim+1, ylim//6))
    plt.ylabel("Frequency")
    plt.xlabel("Year")  
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], oktas[::-1], title='Okta', bbox_to_anchor=(1, 1), prop={'size': 8})
    fig.tight_layout()
    plt.savefig(f"barplot_oktas_juntas_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show

def lineplot_oktas_separadas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores):
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)

    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=200)
    if frecuencias_oktas(frecuencias).es_diario():
        plt.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    else: 
        plt.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
        
    if frecuencias_oktas(frecuencias).es_diario():
        ylim = 160
    else: 
        ylim = 12
    
    for i in range(0, 3):
                for j in range(0, 3):
                    ax[i, j].set_facecolor('#E7E7DE')
                    ax[i, j].plot(frecuencias.index, frecuencias[str(3*i+j)], color = colores[3*i+j])
                    ax[i, j].fill_between(frecuencias.index,frecuencias[str(3*i+j)], color = colores[3*i+j], alpha=0.4)
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
    plt.savefig(f"lineplot_oktas_separadas_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show()

def lineplot_oktas_juntas(frecuencias, id_omm, fecha_inicio_str, fecha_final_str, colores = f_paletas_colores.paleta_9_colores):
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)

    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    plt.figure(num=1, figsize=(8, 5), dpi=200)
    
    if frecuencias_oktas(frecuencias).es_diario():
        plt.suptitle(f"Frecuency of daily mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    else: 
        plt.suptitle(f"Frecuency of monthly mean total cloud cover (oktas) per year SMN \n {nombre_estacion} ({id_omm})", size=14)
    
    ax = plt.gca()
    ax.set_facecolor('#E7E7DE')
    for i in range(0,9):
        plt.plot(frecuencias.index,frecuencias[str(i)], color = colores[i], label = i)
    if frecuencias_oktas(frecuencias).es_diario():
        ylim = 160
    else: 
        ylim = 12
    plt.ylim((0,ylim))
    plt.yticks(np.arange(0,ylim+1, ylim//6))
    plt.ylabel("Frequency")
    plt.xlabel("Year")  
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], oktas[::-1], title='Okta', bbox_to_anchor=(1.1, 1), prop={'size': 8})
    plt.tight_layout()
    plt.savefig(f"lineplot_oktas_juntas_{id_omm}_{fecha_inicio_str}_{fecha_final_str}.png")
    plt.show

def histogramas_partidos(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, fecha_inicio_str_0 = None, fecha_final_str_0 = None, variable = "nub", estaciones = False, meses = False, agrupo = None):
    """
    Hace dos o 3 histogramas con data: variable(str) del df_data entre fecha_inicio_str_1 yyyy-mm-dd y fecha_final_str_1 yyyy-mm-dd
                                   y variable(str) del df_data entre fecha_inicio_str_2 yyyy-mm-dd y fecha_final_str_2 yyyy-mm-dd
    """
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_serie_1 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_1, fecha_final_str_1) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_2, fecha_final_str_2) #uso clases de c_clases_smn
    if fecha_inicio_str_0:
        instancia_serie_0 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_0, fecha_final_str_0) #uso clases de c_clases_smn
        
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
                plt.yticks(np.arange(0,0.65,0.10))
                plt.ylim((0,0.60))
            else:
                plt.yticks(np.arange(0,0.30,0.05))
                plt.ylim((0,0.25))
        else: #si es mensual
            plt.yticks(np.arange(0,1.1,0.2))
            plt.ylim((0,1))
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
                plt.title(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]} {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})")
            else:
                plt.title(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})")
                
        else:
            if fecha_inicio_str_0:
                plt.title(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]} {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})")
            else:
                plt.title(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]} {fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})")
        if fecha_inicio_str_0:
            plt.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        else:
            plt.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"])
        if fecha_inicio_str_0:
            if agrupo == 1:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo1.png")
            elif agrupo == 2:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo2.png")
            else:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
        else:
            fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[10, 8], dpi=200)
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
            else:
                fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
            else:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
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
                        ax[j, i].set_ylim((0,0.60))
                        ax[j, i].set_yticks(np.arange(0,0.65, 0.1))
                    else:   
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,1))
                    ax[j, i].set_yticks(np.arange(0, 1.1, 0.2))
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
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])       
                        else:
                               ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 1: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        #if fecha_inicio_str_0:
         #   fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8])  
        #else:
         #   fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8])       
        fig.tight_layout()
        
        if instancia_serie_1.es_diario(): 
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                    
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()
  
            else:
                if agrupo:
                        plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
            plt.show()
    
    
    elif estaciones == False and meses == True:
        fig, ax = plt.subplots(4, 3, figsize = [10, 8], dpi = 200)
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
            else:
                fig.suptitle(f"Daily total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_0[0:4]}-{fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
            else:
                fig.suptitle(f"Monthly mean total cloud cover (oktas) SMN {fecha_inicio_str_1[0:4]}-{fecha_final_str_2[0:4]}\n {nombre_estacion} ({id_omm})", size=18)
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
                        ax[j, i].set_ylim((0,0.60))
                        ax[j, i].set_yticks(np.arange(0,0.65, 0.1))
                    else:
                        ax[j, i].set_ylim((0,0.35))
                        ax[j, i].set_yticks(np.arange(0,0.4, 0.1))
                else: #si es mensual
                    ax[j, i].set_ylim((0,1))
                    ax[j, i].set_yticks(np.arange(0, 1.1, 0.2))
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
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3, 0.4,0.5, 0.6])   
                        else:
                            ax[j, i].set_yticklabels([0, 0.1, 0.2, 0.3])
                    else: #si es mensual
                        ax[j, i].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1])
                else:
                    ax[j, i].set_yticklabels([])
                if j == 3: #solo para los de abajo pongo el xlabel
                    ax[j, i].set_xlabel("okta")  
                    #ax[j, i].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
                else:
                    ax[j, i].set_xticklabels([])
        #if fecha_inicio_str_0:
         #   fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}",f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8]) 
        #else:
         #   fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.85,0.8]) 
        fig.tight_layout()
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                    
                
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
    
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}.png")
                else:
                    plt.savefig(f"histograma_partido_mensual_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}.png")
                plt.show()

                
                
                
###########################
def histogramas_partidos_poster(id_omm, df_data, fecha_inicio_str_1, fecha_final_str_1, fecha_inicio_str_2, fecha_final_str_2, fecha_inicio_str_0 = None, fecha_final_str_0 = None, variable = "nub", estaciones = False, meses = False, agrupo = None):
    """
    Hace dos o 3 histogramas con data: variable(str) del df_data entre fecha_inicio_str_1 yyyy-mm-dd y fecha_final_str_1 yyyy-mm-dd
                                   y variable(str) del df_data entre fecha_inicio_str_2 yyyy-mm-dd y fecha_final_str_2 yyyy-mm-dd
    """
    if id_omm == 87148:
        nombre_estacion = "Roque Saenz Peña"
    elif id_omm == 87166:
        nombre_estacion = "Corrientes"
    elif id_omm == 87270:
        nombre_estacion = "Reconquista Aero"
    elif id_omm == 87395:
        nombre_estacion = "Concordia Aero"
    elif id_omm == 87393:
        nombre_estacion = "Montecaseros"
    elif id_omm == 87289:
        nombre_estacion = "Paso de los Libres Aero"
    elif id_omm == 87178:
        nombre_estacion = "Posadas Aero"
    elif id_omm == 87187:
        nombre_estacion = "Oberá"
    elif id_omm == 87155:
        nombre_estacion = "Resistencia Aero"
    elif id_omm == 87173:
        nombre_estacion = "Posadas"
    elif id_omm == 87281:
        nombre_estacion = "Mercedes Aero"
    else:
        nombre_estacion = " "
    instancia_serie_1 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_1, fecha_final_str_1) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_2, fecha_final_str_2) #uso clases de c_clases_smn
    if fecha_inicio_str_0:
        instancia_serie_0 = dataframe_smn(df_data).genero_serie("nub", fecha_inicio_str_0, fecha_final_str_0) #uso clases de c_clases_smn
        
    if estaciones == False and meses == False:
        plt.close()   
        fig = plt.figure(num=1, figsize=(3.5, 2.5), dpi=200)
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
                plt.title(f"Daily CA \n SMN {nombre_estacion} ({id_omm})")
            else:
                plt.title(f"Daily CA \n SMN {nombre_estacion} ({id_omm})")
                
        else:
            if fecha_inicio_str_0:
                plt.title(f"Monthly CA \n SMN {nombre_estacion} ({id_omm})")
            else:
                plt.title(f"Monthly CA \n SMN {nombre_estacion} ({id_omm})")
        if fecha_inicio_str_0:
            plt.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], fontsize=8)
        else:
            plt.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], fontsize=8)
        if fecha_inicio_str_0:
            if agrupo == 1:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo1_poster.png")
            elif agrupo == 2:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo2_poster.png")
            else:
                fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
        else:
            fig.savefig(f"histograma_partido_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
        plt.show()
        
    elif estaciones == True and meses == False:
        fig, ax = plt.subplots(2, 2, figsize=[4.5, 4.5], dpi=200)
        if instancia_serie_1.es_diario(): #si es diario
            if fecha_inicio_str_0:
                fig.suptitle(f"Daily CA \n SMN {nombre_estacion} ({id_omm})")
            else:
                fig.suptitle(f"Daily  CA \n SMN {nombre_estacion} ({id_omm})")
        else:
            if fecha_inicio_str_0:
                fig.suptitle(f"Monthly  CA \n SMN {nombre_estacion} ({id_omm})")
            else:
                fig.suptitle(f"Monthly  CA \n SMN {nombre_estacion} ({id_omm})")
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
                    ax[j, i].set_ylabel("Frequency")
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
         #   fig.legend([f"{fecha_inicio_str_0[0:4]}-{fecha_final_str_0[0:4]}", f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.80,0.71], fontsize=6)   #0.76,
        #else:
         #   fig.legend([f"{fecha_inicio_str_1[0:4]}-{fecha_final_str_1[0:4]}", f"{fecha_inicio_str_2[0:4]}-{fecha_final_str_2[0:4]}"], loc = [0.80,0.71], fontsize=6)       
        fig.tight_layout()
        
        if instancia_serie_1.es_diario(): 
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                plt.show()
            else:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_diaria_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                    
                plt.show()
        else:
            if fecha_inicio_str_0:
                if agrupo:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_0}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
                plt.show()
  
            else:
                if agrupo:
                        plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_grupo{agrupo}_poster.png")
                else:
                    plt.savefig(f"histograma_partido_estacional_media_mensual_{str(id_omm)}_{fecha_inicio_str_1}_{fecha_final_str_2}_poster.png")
            plt.show()
    
    
#%% ESTO TODAVIA NO SE BIEN COMO ENCARARLO:
"""    
def correlacion_entre_series(id_omm_1, df_data_1, id_omm_2, df_data_2, fecha_inicio_str, fecha_final_str, variable = "nub"):
    
    instancia_serie_1 = dataframe_smn(df_data_1).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_smn(df_data_2).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    
    fig = plt.figure(num=2, figsize=(8, 5), dpi=80)    
    plt.scatter(instancia_serie_1.serie, instancia_serie_2.serie, marker = '.', color="cornflowerblue", alpha = 0.1, s=300)
    if instancia_serie_1.es_diario(): #si el paso es diario
        plt.title(f"Daily total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    else:
        plt.title(f"Monthly mean total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    plt.yticks(np.arange(0, 9, 1))
    plt.ylim((0,9))
    plt.ylabel(f"{id_omm_2}")
    plt.xticks(np.arange(0, 9, 1))
    plt.xlim((0,9))
    plt.xlabel(f"{id_omm_1}")
    return fig.savefig(f"correlacion_{id_omm_1}_{id_omm_2}_{fecha_inicio_str}_{fecha_final_str}.png")

from scipy.stats import gaussian_kde
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap

def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=plt.get_cmap("Oranges"), dpi =8)
    fig.colorbar(density, label='Number of points', boundaries=[0,1,20,40,60, 80, 100, 120, 140])

def correlacion_entre_series(id_omm_1, df_data_1, id_omm_2, df_data_2, fecha_inicio_str, fecha_final_str, variable = "nub"):

    instancia_serie_1 = dataframe_smn(df_data_1).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    instancia_serie_2 = dataframe_smn(df_data_2).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    
    # Calculate the point density
    x=np.array(instancia_serie_1.serie)
    y=np.array(instancia_serie_2.serie)
    fig = plt.figure(figsize=(8, 5), dpi=200)
    using_mpl_scatter_density(fig, x, y)
    if instancia_serie_1.es_diario(): #si el paso es diario
        plt.title(f"Daily total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    else:
        plt.title(f"Monthly mean total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    plt.yticks(np.arange(0, 9, 1))
    plt.ylim((0,9))
    plt.ylabel(f"{id_omm_2}")
    plt.xticks(np.arange(0, 9, 1))
    plt.xlim((0,9))
    plt.xlabel(f"{id_omm_1}")
    plt.show()
    return fig.savefig(f"correlacion_{id_omm_1}_{id_omm_2}_{fecha_inicio_str}_{fecha_final_str}.png")

correlacion_entre_series(87395, data_mensual[87395], 87395, data_mensual[87395], fecha_inicio_str, fecha_final_str, variable = "nub")
#VER COMO UNIFICO BARRA DE COLORES 


def correlacion_entre_series(id_omm_1, frecuencias_1, id_omm_2, frecuencias_2, fecha_inicio_str, fecha_final_str, variable = "nub"):
    
    instancia_frecuencia_1 = frecuencias_oktas(frecuencias_1) #uso clases de c_clases_smn
    frecuencias_1 = instancia_frecuencia_1.selecciono_fechas(fecha_inicio_str, fecha_final_str)
    
    instancia_frecuencia_2 = frecuencias_oktas(frecuencias_2) #uso clases de c_clases_smn
    frecuencias_2 = instancia_frecuencia_2.selecciono_fechas(fecha_inicio_str, fecha_final_str)
    
    fig = plt.figure(num=2, figsize=(8, 5), dpi=80)    
    plt.scatter(np.array(frecuencias_1["3"]).transpose(), np.array(frecuencias_2["3"]).transpose(), marker = '.', color="cornflowerblue")
    if frecuencias_oktas(frecuencias_2).es_diario(): 
        plt.title(f"Daily total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    else:
        plt.title(f"Monthly mean total cloud cover frequency (oktas) SMN\n {id_omm_1} - {id_omm_2}")
    plt.yticks(np.arange(0, 12, 2))
    plt.ylim((0,12))
    plt.ylabel(f"{id_omm_2}")
    plt.xticks(np.arange(0, 12, 2))
    plt.xlim((0,12))
    plt.xlabel(f"{id_omm_1}")
    return fig.savefig(f"correlacion_{id_omm_1}_{id_omm_2}_{fecha_inicio_str}_{fecha_final_str}.png")
"""