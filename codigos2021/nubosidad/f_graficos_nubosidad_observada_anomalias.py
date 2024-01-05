import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import f_paletas_colores
from f_procesamiento_nubosidad_observada_anomalias import tendencia_theil_sen
from c_clases_smn import frecuencias_oktas

def stacked_plot_barras_climatologia(frecuencias, 
                                     estaciones, id_estacion = 87148,
                                     colores = f_paletas_colores.paleta_9_colores, agrupo = None,
                                     anio_inicio = 1983, anio_final = 2016,
                                     idioma = "ingles"):
    
    nombre_estacion = estaciones[id_estacion]
    
    width = 0.98      #ancho de las barras
    if idioma == "ingles":
        meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    elif idioma == "español":
        meses = ['E', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    
    
    plt.figure(num=1, figsize=(8, 5), dpi=600) #genero figura
    ax = plt.gca()
    ax.set_facecolor('#E7E7DE') #seteo color de fondo
    
    if agrupo == None: #si frecuencias no esta agrupado
        ax.bar(frecuencias.index, np.array(frecuencias).transpose()[0], width,
               label='0', color = colores[0])
        for okta in range(1,9):
            ax.bar(frecuencias.index, np.array(frecuencias).transpose()[okta], width, 
                       bottom=sum(np.array(frecuencias).transpose()[0:okta]),
                       label=str(okta), color = colores[okta])
    elif agrupo == 3: #si frecuencias esta agrupado con el grupo 3: 0, 1-2-3, 4, 5-6-7, 8
        ax.bar(frecuencias.index, np.array(frecuencias).transpose()[0], width,
               label='0', color = colores[0])
        labels=["0","1-2-3","4","5-6-7","8"]
        for okta in range(1,5):
            ax.bar(frecuencias.index, np.array(frecuencias).transpose()[okta], width, 
                       bottom=sum(np.array(frecuencias).transpose()[0:okta]),
                       label=labels[okta], color = colores[okta])

    handles, labels = ax.get_legend_handles_labels() #para poder invertir el orden de las oktas en la leyenda

    if idioma == "ingles":
        ax.set_ylabel('Frequency %')
    elif idioma == "español":
        ax.set_ylabel('Frequencia %')
    
    if idioma == "ingles":
        ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.1, 1), prop={'size': 8})
    elif idioma == "español":
        ax.legend(handles[::-1], labels[::-1], title='Octa', bbox_to_anchor=(1.1, 1), prop={'size': 8})

    plt.ylim(0, 100)
    plt.xlim(frecuencias.index[0]-0.5, frecuencias.index[-1]+0.5)
    ax.set_xticks(frecuencias.index)
    ax.set_xticklabels(meses)
    
    if idioma == "ingles":
        plt.xlabel("Month")
        plt.title(f"Climatology of monthly frequency of daily total cloud cover ({anio_inicio}-{anio_final}) SMN \n {nombre_estacion} ({id_estacion})")
    elif idioma == "español":
        plt.xlabel("Mes")
        plt.title(f"Climatología de frecuencia mensual de cobertura nubosa media diaria ({anio_inicio}-{anio_final}) SMN \n {nombre_estacion} ({id_estacion})")
    
    
    if agrupo:
        plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_{id_estacion}_grupo{agrupo}_{idioma}.png")
    else:
        plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_{id_estacion}_{idioma}.png")
    plt.show()

    
def stacked_plot_barras_climatologia_media_espacial(frecuencias, 
                                     colores = f_paletas_colores.paleta_9_colores, agrupo = None,
                                     anio_inicio = 1983, anio_final = 2016,
                                     idioma = "ingles", titulo = False):
    
    width = 0.98      #ancho de las barras
    if idioma == "ingles":
        meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    elif idioma == "español":
        meses = ['E', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    
    
    plt.figure(num=1, figsize=(8, 5), dpi=600) #genero figura
    ax = plt.gca()
    ax.set_facecolor('#E7E7DE') #seteo color de fondo
    
    if agrupo == None: #si frecuencias no esta agrupado
        ax.bar(frecuencias.index, np.array(frecuencias).transpose()[0], width,
               label='0', color = colores[0])
        for okta in range(1,9):
            ax.bar(frecuencias.index, np.array(frecuencias).transpose()[okta], width, 
                       bottom=sum(np.array(frecuencias).transpose()[0:okta]),
                       label=str(okta), color = colores[okta])
    elif agrupo == 3: #si frecuencias esta agrupado con el grupo 3: 0, 1-2-3, 4, 5-6-7, 8
        ax.bar(frecuencias.index, np.array(frecuencias).transpose()[0], width,
               label='0', color = colores[0])
        labels=["0","1-2-3","4","5-6-7","8"]
        for okta in range(1,5):
            ax.bar(frecuencias.index, np.array(frecuencias).transpose()[okta], width, 
                       bottom=sum(np.array(frecuencias).transpose()[0:okta]),
                       label=labels[okta], color = colores[okta])

    handles, labels = ax.get_legend_handles_labels() #para poder invertir el orden de las oktas en la leyenda

    if idioma == "ingles":
        ax.set_ylabel('Frequency %')
    elif idioma == "español":
        ax.set_ylabel('Frequencia %')
    
    if idioma == "ingles":
        ax.legend(handles[::-1], labels[::-1], title='Okta', bbox_to_anchor=(1.1, 1), prop={'size': 8})
    elif idioma == "español":
        ax.legend(handles[::-1], labels[::-1], title='Octa', bbox_to_anchor=(1.1, 1), prop={'size': 8})

    plt.ylim(0, 100)
    plt.xlim(frecuencias.index[0]-0.5, frecuencias.index[-1]+0.5)
    ax.set_xticks(frecuencias.index)
    ax.set_xticklabels(meses)
    
    if titulo == True:
        if idioma == "ingles":
            plt.xlabel("Month")
            plt.title(f"Climatology of monthly frequency of daily total cloud cover ({anio_inicio}-{anio_final}) SMN \n NEA")
        elif idioma == "español":
            plt.xlabel("Mes")
            plt.title(f"Climatología de frecuencia mensual de cobertura nubosa media diaria ({anio_inicio}-{anio_final}) SMN \n NEA")
    
    elif titulo == False:
        if idioma == "ingles":
            plt.xlabel("Month")
        elif idioma == "español":
            plt.xlabel("Mes")
    
    if titulo == True:       
        if agrupo:
            plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_NEA_grupo{agrupo}_{idioma}.png")
        else:
            plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_NEA_{idioma}.png")
    elif titulo == False:       
        if agrupo:
            plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_NEA_grupo{agrupo}_{idioma}_sin_titulo.png")
        else:
            plt.savefig(f"climatologia_frecuencia_relativa_stackedarea_NEA_{idioma}_sin_titulo.png")
    plt.show()
        
    
def barplot_oktas_separadas_climatologia(frecuencias,
                                         estaciones, id_estacion = 87148,
                                         colores = f_paletas_colores.paleta_9_colores,
                                         anio_inicio=1983, anio_final=2016,
                                         idioma = "ingles"):
    
    nombre_estacion = estaciones[id_estacion]
    
    if idioma == "ingles":
        meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    elif idioma == "español":
        meses = ['E', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    
    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=600)
    
    if idioma == "ingles":
        plt.suptitle(f"Climatology of monthly frequency of daily total cloud cover ({anio_inicio}-{anio_final}) SMN \n {nombre_estacion} ({id_estacion})", size=14)
    elif idioma == "español":
        plt.suptitle(f"Climatología de frecuencia mensual de cobertura nubosa media diaria ({anio_inicio}-{anio_final}) SMN \n {nombre_estacion} ({id_estacion})", size=14)
        
    ylim = 30

    for i in range(0, 3):
                for j in range(0, 3):
                    
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], 
                                 color = colores[3*i+j], width = 0.9)
                    ax[i, j].set_ylim((0,ylim))
                    ax[i, j].set_yticks(np.arange(0,ylim+1, ylim//5))
                    if idioma == "ingles":
                        ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                    elif idioma == "español":
                        ax[i, j].set_title(f"Octa = {oktas[3*i+j]}", size = 11)
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        if idioma == "ingles":
                            ax[i, j].set_ylabel("Frequency %")
                        elif idioma == "español":
                            ax[i, j].set_ylabel("Frecuencia %")
                    else:
                        ax[i, j].set_yticklabels([])
                    if i == 2: #solo para los de abajo pongo el xlabel
                        if idioma == "ingles":
                            ax[i, j].set_xlabel("Month")
                        elif idioma == "español":
                            ax[i, j].set_xlabel("Mes")
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i,j].set_xticklabels(meses)
                        #ax[i,j].set_xticklabels(frecuencias.index)
                    else:
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i, j].set_xticklabels([])
    
    fig.tight_layout()
    
    plt.savefig(f"climatologia_frecuencia_relativa_barplot_oktas_separadas_{id_estacion}_{idioma}.png")    

    plt.show()

def barplot_oktas_separadas_climatologia_media_espacial(frecuencias,
                                         colores = f_paletas_colores.paleta_9_colores,
                                         anio_inicio=1983, anio_final=2016,
                                         idioma = "ingles", titulo = False):
    
    if idioma == "ingles":
        meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    elif idioma == "español":
        meses = ['E', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    
    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=600)
    
    if titulo == True:
        if idioma == "ingles":
            plt.suptitle(f"Climatology of monthly frequency of daily total cloud cover ({anio_inicio}-{anio_final}) SMN \n NEA", size=14)
        elif idioma == "español":
            plt.suptitle(f"Climatología de frecuencia mensual de cobertura nubosa media diaria ({anio_inicio}-{anio_final}) SMN \n NEA", size=14)
        
    ylim = 30

    for i in range(0, 3):
                for j in range(0, 3):
                    
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], 
                                 color = colores[3*i+j], width = 0.9)
                    ax[i, j].set_ylim((0,ylim))
                    ax[i, j].set_yticks(np.arange(0,ylim+1, ylim//5))
                    if idioma == "ingles":
                        ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                    elif idioma == "español":
                        ax[i, j].set_title(f"Octa = {oktas[3*i+j]}", size = 11)
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        if idioma == "ingles":
                            ax[i, j].set_ylabel("Frequency %")
                        elif idioma == "español":
                            ax[i, j].set_ylabel("Frecuencia %")
                    else:
                        ax[i, j].set_yticklabels([])
                    if i == 2: #solo para los de abajo pongo el xlabel
                        if idioma == "ingles":
                            ax[i, j].set_xlabel("Month")
                        elif idioma == "español":
                            ax[i, j].set_xlabel("Mes")
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i,j].set_xticklabels(meses)
                        #ax[i,j].set_xticklabels(frecuencias.index)
                    else:
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i, j].set_xticklabels([])
    
    fig.tight_layout()
    
    if titulo == True:
        plt.savefig(f"climatologia_frecuencia_relativa_barplot_oktas_separadas_NEA_{idioma}.png")    
    elif titulo == False:
        plt.savefig(f"climatologia_frecuencia_relativa_barplot_oktas_separadas_NEA_{idioma}_sin_titulo.png") 
    plt.show()    
    
def barplot_oktas_separadas_RELATIVO(frecuencias, frecuencias_media_movil_12, frecuencias_media_movil_12_5, estaciones,
                                     id_estacion, fecha_inicio_str, fecha_final_str, 
                                     colores =f_paletas_colores.paleta_9_colores,
                                     incluir_tendencia_ts =  False, incluir_media_movil_12 = True, 
                                     incluir_media_movil_12_5 = False,
                                     idioma = "ingles"):
    
    nombre_estacion = estaciones[id_estacion]
    
    instancia_frecuencia = frecuencias_oktas(frecuencias)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)
    
    frecuencias_media_movil_12 = frecuencias_media_movil_12.loc[fecha_inicio_str:fecha_final_str]
    frecuencias_media_movil_12_5 = frecuencias_media_movil_12_5.loc[fecha_inicio_str:fecha_final_str]
    
    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=200)
    
    if idioma == "ingles":
        plt.suptitle(f"Anomaly of daily mean total cloud cover (oktas) monthly frequency SMN \n {nombre_estacion} ({id_estacion})", size=14)
    elif idioma == "español":
        plt.suptitle(f"Anomalía de la frecuencia mensual de cobertura nubosa media diaria (octas) SMN \n {nombre_estacion} ({id_estacion})", size=14)
    else:
        print("ingresa un idioma valido")
        
    
    ylim = 24

    for i in range(0, 3):
                for j in range(0, 3):
                    ax[i,j].axhline(0, color = "darkgrey")
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], 
                                 color = colores[3*i+j], width = 7)
                    if incluir_media_movil_12 == True:
                        ax[i, j].plot(frecuencias.index, 
                                       np.array(frecuencias_media_movil_12).transpose()[3*i+j],
                                       color = colores[3*i+j], alpha= 0.9)
                    if incluir_tendencia_ts == True:
                        #calculo tendencias lineal por theil sen
                        tendencia_okta_sen = tendencia_theil_sen(frecuencias.loc[fecha_inicio_str:fecha_final_str][str(3*i+j)])
                        pendiente_sen = tendencia_okta_sen[1]
                        origen_sen = tendencia_okta_sen[0]
                        significativo_sen = tendencia_okta_sen[2]
                        grafico_tendencia_sen = origen_sen + pendiente_sen * np.arange(0, len(frecuencias.index), 1)
                        ax[i,j].text(12000, 17, f"{round(pendiente_sen*10*12, 2)} %/dec",color="red", 
                                     ha="center", va = "center", fontsize =  'small',
                                     weight='bold') #horizontalalignment='center', verticalalignment='center'

                        #grafico tendencia lineal por thail-sen
                        if tendencia_okta_sen[2] == True:
                            ax[i, j].plot(frecuencias.index, 
                                           grafico_tendencia_sen,
                                           color = "red", alpha = 0.9)
                        else:
                            ax[i, j].plot(frecuencias.index, 
                                           grafico_tendencia_sen,
                                           color = "red", alpha = 0.9, ls = ":")
                    
                        
                    if incluir_media_movil_12_5 == True:
                        ax[i, j].plot(frecuencias.index, 
                                       np.array(frecuencias_media_movil_12_5).transpose()[3*i+j],
                                       color = "grey", alpha= 0.9)
                    
                    ax[i, j].set_ylim((-ylim,ylim))
                    ax[i, j].set_yticks(np.arange(-ylim,ylim+1, ylim//2))
                    if idioma == "ingles":
                        ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                    elif idioma == "español":
                        ax[i, j].set_title(f"Octa = {oktas[3*i+j]}", size = 11)
                    
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        if idioma == "ingles":
                            ax[i, j].set_ylabel("Frequency anomaly %")
                        elif idioma == "español":
                            ax[i, j].set_ylabel("Frecuencia anom %")
                    else:
                        ax[i, j].set_yticklabels([])
                    
                    if int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]) <= 3 :
                        intervalo_fechas = (int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]))*5 #6
                    else:
                        intervalo_fechas = (int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]))*3
                    
                    if i == 2: #solo para los de abajo pongo el xlabel
                        if idioma == "ingles":
                            ax[i, j].set_xlabel("Date")
                        if idioma == "español":
                            ax[i, j].set_xlabel("Fecha")
                        ax[i,j].set_xticks(frecuencias.index[::intervalo_fechas])
                        ax[i,j].set_xticklabels(frecuencias.index.year[::intervalo_fechas])
                    else:
                        ax[i,j].set_xticks(frecuencias.index[::intervalo_fechas])
                        ax[i, j].set_xticklabels([])
                        
    fig.tight_layout()
    if idioma == "ingles":
        plt.savefig(f"barplot_oktas_separadas_relativa_anomalia_{id_estacion}_{fecha_inicio_str}_{fecha_final_str}_ingles.png")
    elif idioma == "español":
        plt.savefig(f"barplot_oktas_separadas_relativa_anomalia_{id_estacion}_{fecha_inicio_str}_{fecha_final_str}_español.png")
    plt.show()
    
def barplot_oktas_separadas_RELATIVO_por_estacion(frecuencias_estacion, estacion_del_anio,
                                                  estaciones, id_estacion, fecha_inicio_str, fecha_final_str, 
                                                  colores =f_paletas_colores.paleta_9_colores,
                                                  incluir_tendencia_ts = True,
                                                  idioma = "ingles"):
    
    nombre_estacion = estaciones[id_estacion]
    
    instancia_frecuencia = frecuencias_oktas(frecuencias_estacion)
    frecuencias = instancia_frecuencia.selecciono_fechas(fecha_inicio_str, fecha_final_str)
    
    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[9, 7], dpi=600)
    
    if idioma == "ingles":
        plt.suptitle(f"Anomaly of daily mean total cloud cover (oktas) monthly frequency SMN \n {estacion_del_anio} {nombre_estacion} ({id_estacion})", size=14)
    elif idioma == "español":
        if estacion_del_anio == "DJF":
            plt.suptitle(f"Anomalía de la frecuencia mensual de cobertura nubosa media diaria (octas) SMN \n DEF {nombre_estacion} ({id_estacion})", size=14)
        else:    
            plt.suptitle(f"Anomalía de la frecuencia mensual de cobertura nubosa media diaria (octas) SMN \n {estacion_del_anio} {nombre_estacion} ({id_estacion})", size=14)
    else:
        print("ingresa un idioma valido")
        
    
    ylim = 24

    for i in range(0, 3):
                for j in range(0, 3):
                    ax[i,j].axhline(0, color = "darkgrey")
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], 
                                 color = colores[3*i+j], width = 0.9)
                    
                    if incluir_tendencia_ts == True:
                        #calculo tendencias lineal por theil sen
                        tendencia_okta_sen = tendencia_theil_sen(frecuencias[3*i+j])
                        pendiente_sen = tendencia_okta_sen[1]
                        origen_sen = tendencia_okta_sen[0]
                        significativo_sen = tendencia_okta_sen[2]
                        grafico_tendencia_sen = origen_sen + pendiente_sen * np.arange(0, len(frecuencias.index), 1)
                        ax[i,j].text(1995, 17, f"{round(pendiente_sen*10, 2)} %/dec",color="red", 
                                     ha="center", va = "center", fontsize =  'small',
                                     weight='bold') #horizontalalignment='center', verticalalignment='center'

                        #ax[i,j].text(12000, 17, f"{round(pendiente_sen*10*12, 2)} %/dec",color="red", 
                         #            ha="center", va = "center", fontsize =  'small',
                         #            weight='bold') #horizontalalignment='center', verticalalignment='center'

                        #grafico tendencia lineal por thail-sen
                        if tendencia_okta_sen[2] == True:
                            ax[i, j].plot(frecuencias.index, 
                                           grafico_tendencia_sen,
                                           color = "red", alpha = 0.9)
                        else:
                            ax[i, j].plot(frecuencias.index, 
                                           grafico_tendencia_sen,
                                           color = "red", alpha = 0.9, ls = ":")
                    
                    
                    ax[i, j].set_ylim((-ylim,ylim))
                    ax[i, j].set_yticks(np.arange(-ylim,ylim+1, ylim//2))
                    if idioma == "ingles":
                        ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                    elif idioma == "español":
                        ax[i, j].set_title(f"Octa = {oktas[3*i+j]}", size = 11)
                    
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        if idioma == "ingles":
                            ax[i, j].set_ylabel("Frequency anomaly %")
                        elif idioma == "español":
                            ax[i, j].set_ylabel("Frecuencia anom %")
                    else:
                        ax[i, j].set_yticklabels([])
                    
                    #if int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]) <= 3 :
                     #   intervalo_fechas = (int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]))*5 #6
                    #else:
                     #   intervalo_fechas = (int(fecha_final_str[0:4])-int(fecha_inicio_str[0:4]))*3
                    
                    if i == 2: #solo para los de abajo pongo el xlabel
                        if idioma == "ingles":
                            ax[i, j].set_xlabel("Date")
                        if idioma == "español":
                            ax[i, j].set_xlabel("Fecha")
                        #ax[i,j].set_xticks(frecuencias.index[::intervalo_fechas])
                        #ax[i,j].set_xticklabels(frecuencias.index.year[::intervalo_fechas])
                    else:
                        #ax[i,j].set_xticks(frecuencias.index[::intervalo_fechas])
                        ax[i, j].set_xticklabels([])
                        
    #fig.tight_layout()
    if idioma == "ingles":
            plt.savefig(f"barplot_oktas_separadas_relativa_anomalia_{id_estacion}_{fecha_inicio_str}_{fecha_final_str}_{estacion_del_anio}_ingles.png")
    elif idioma == "español":
        plt.savefig(f"barplot_oktas_separadas_relativa_anomalia_{id_estacion}_{fecha_inicio_str}_{fecha_final_str}_{estacion_del_anio}_español.png")
    plt.show()