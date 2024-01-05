import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import os
import datetime as dt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes #para sumar mapa grande
import cartopy #para sumar mapa grande
import cartopy.mpl.geoaxes #para sumar mapa grande
from matplotlib.patches import Rectangle #para graficar rectangulo en mapa grande
from calendar import monthrange
import f_paletas_colores

#funcion que grafica puntos para paper
def f_mapa(lista_puntos_satelital, dict_puntos_smn, lista_puntos_smn_importantes, nombres_ides_omm_ordenado, shape_paises,
                         shape_provincias):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el smn 
    en un entorno a corrientes
    """
    #defino puntos a marcar
    geometry_1 = [Point(xy) for xy in lista_puntos_satelital] #lista con puntos 1
    geometry_2 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    geodata1 = gpd.GeoDataFrame(lista_puntos_satelital, geometry=geometry_1)
    geodata2 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_2)
    
    #inicio figura
    fig1 = plt.figure(figsize = [8, 5], dpi = 1000)  
    fig1.patch.set_facecolor('white')
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.6', linewidth = 0.6, alpha = 0.5, zorder = 1)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 2, alpha = 0.7, zorder = 2)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 10, c = "#306292", zorder = 3) 
    geodata2.plot(ax = ax, markersize = 20, c = "#D23232", zorder = 4) 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-60.5, -53.5))
    plt.xticks(np.arange(-60.5, -53.5))
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-31.5, -24.5))
    plt.yticks(np.arange(-31.5, -24.5))
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    ax.legend(["ISCCP", "SMN"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con nombres de estacion
    dict_puntos_smn_calibracion = dict(zip(lista_puntos_smn_importantes, [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]))
    list_smn_etiquetas = [(lon-0.6-360, lat+0.12) for lon, lat in list(dict_puntos_smn_calibracion.values())]
    for i, clave in enumerate(nombres_ides_omm_ordenado):
        if str(clave) != "Oberá" and str(clave) != "Roque Saenz Peña" and str(clave) != "Corrientes" and str(clave) != "Paso de los Libres":
            t = ax.annotate(str(clave), list_smn_etiquetas[i], size = 8,weight='bold', zorder = 5)
        elif str(clave) == "Oberá":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.40), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Corrientes":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.40), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Resistencia":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]-0.9, list_smn_etiquetas[i][1]-0.06), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Roque Saenz Peña":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.04), size = 8, weight='bold', zorder = 5)
        else:
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]-0.7, list_smn_etiquetas[i][1]-0.06), size = 8,weight='bold', zorder = 5)
    
    #Agrego nombres de provincias
    ax.annotate("Corrientes", (-58.5, -29), size = 9, color = '0.7')
    
    #Agrego nombres de paises
    ax.annotate("Argentina", (-58.5, -28.3), size = 13, style='italic', color = '0.6')
    ax.annotate("Brazil", (-55.5, -28.8), size = 13, style='italic', color = '0.6')
    #ax.annotate("Uruguay", (-58, -31.5), size = 13, style='italic', color = '0.6')
    ax.annotate("Paraguay", (-57, -26), size = 13, style='italic', color = '0.6')
    
    #Agrego mapa de referencia
    axins = inset_axes(ax, width="34%", height="34%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
    axins.add_feature(cartopy.feature.BORDERS, edgecolor = '0.5')
    axins.add_feature(cartopy.feature.COASTLINE, edgecolor = '0.5')
    axins.set_xlim([-90, -27])
    axins.set_ylim([-60, 13])
    #box = [-60.5, -54.5, -31.5, -25.5]
    RE=Rectangle((-60.5,-31.5),-54.5--60.5,-25.5--31.5,linewidth=1,linestyle='-' ,zorder=2,\
    edgecolor='none',facecolor='#33C131', alpha = 0.5, transform=ccrs.PlateCarree()) 
    axins.add_patch(RE)
    
    plt.savefig("figura1_mapa_puntos.png") 
    
#adaptacion de mapa para poster solo con puntos de smn
#funcion que grafica puntos para paper
def f_mapa_poster(dict_puntos_smn, lista_puntos_smn_importantes, nombres_ides_omm_ordenado, shape_paises,
                         shape_provincias):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el smn 
    en un entorno a corrientes
    """
    #defino puntos a marcar
    #geometry_1 = [Point(xy) for xy in lista_puntos_satelital] #lista con puntos 1
    geometry_2 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    #geodata1 = gpd.GeoDataFrame(lista_puntos_satelital, geometry=geometry_1)
    geodata2 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_2)
    
    #inicio figura
    #cm = 1/2.54  # centimeters in inches
    fig1 = plt.figure(figsize = [8, 5], dpi = 1000)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.6', linewidth = 0.6, alpha = 0.5, zorder = 1)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 2, alpha = 0.7, zorder = 2)
    
    #grafico puntos
    #geodata1.plot(ax = ax, markersize = 10, c = "#306292", zorder = 3) 
    geodata2.plot(ax = ax, markersize = 50, c = "#D23232", zorder = 4) 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-60.5, -53.5))
    plt.xticks(np.arange(-60.5, -53.5))
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-31.5, -24.5))
    plt.yticks(np.arange(-31.5, -24.5))
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    #ax.legend(["SMN"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con nombres de estacion
    dict_puntos_smn_calibracion = dict(zip(lista_puntos_smn_importantes, [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]))
    list_smn_etiquetas = [(lon-0.6-360, lat+0.12) for lon, lat in list(dict_puntos_smn_calibracion.values())]
    for i, clave in enumerate(nombres_ides_omm_ordenado):
        if str(clave) != "Oberá" and str(clave) != "Roque Saenz Peña" and str(clave) != "Corrientes" and str(clave) != "Paso de los Libres":
            t = ax.annotate(str(clave), list_smn_etiquetas[i], size = 8,weight='bold', zorder = 5)
        elif str(clave) == "Oberá":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.40), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Corrientes":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.40), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Resistencia":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]-0.9, list_smn_etiquetas[i][1]-0.06), size = 8, weight='bold', zorder = 5)
        elif str(clave) == "Roque Saenz Peña":
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]+0.4, list_smn_etiquetas[i][1]-0.04), size = 8, weight='bold', zorder = 5)
        else:
            t = ax.annotate(str(clave), (list_smn_etiquetas[i][0]-0.7, list_smn_etiquetas[i][1]-0.06), size = 8,weight='bold', zorder = 5)
    
    #Agrego nombres de paises
    ax.annotate("Argentina", (-58.5, -28.3), size = 13, style='italic', color = '0.6')
    ax.annotate("Brazil", (-55.5, -28.8), size = 13, style='italic', color = '0.6')
    #ax.annotate("Uruguay", (-58, -31.5), size = 13, style='italic', color = '0.6')
    ax.annotate("Paraguay", (-57, -26), size = 13, style='italic', color = '0.6')
    
    #Agrego mapa de referencia
    axins = inset_axes(ax, width="34%", height="34%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
    axins.add_feature(cartopy.feature.BORDERS, edgecolor = '0.5')
    axins.add_feature(cartopy.feature.COASTLINE, edgecolor = '0.5')
    axins.set_xlim([-90, -27])
    axins.set_ylim([-60, 13])
    #box = [-60.5, -54.5, -31.5, -25.5]
    RE=Rectangle((-60.5,-31.5),-54.5--60.5,-25.5--31.5,linewidth=1,linestyle='-' ,zorder=2,\
    edgecolor='none',facecolor='#33C131', alpha = 0.5, transform=ccrs.PlateCarree()) 
    axins.add_patch(RE)
    
    plt.savefig("figura1_mapa_puntos_poster.png") 
    
def f_media_mensual_smn(id_omm, df_data, na = 20):
    """ construye serie de media mensual y lo guarda en ruta_salida como .csv
    admite el na% de datos faltantes"""

    data_group=df_data["nub"].groupby(pd.Grouper(freq="M"))
    data_group_media=data_group.mean() #hace la media aunque halla nans, a menos que todo el mes tenga nans
    data_group_faltantes = df_data.isnull().groupby(pd.Grouper(freq="M")).sum()
    data_group_size = data_group.size()
    posiciones_medias_a_conservar = data_group_faltantes.values <= data_group_size.values * na/100
    # elif na == 
    #me quedo con los meses donde la cantidad de datos faltantes haya sido menor al na% de los datos para el mes
    media = []
    for i, elemento in enumerate(data_group_media):
        if posiciones_medias_a_conservar[i][0] == True: # and pd.isna(elemento)!=True:
            media.append(elemento) #media.append(round(elemento)) 
        else:
            media.append(np.nan)
    indices=data_group_media.index
    media_mensual_df=pd.DataFrame(media, index = indices)
    media_mensual_df.index.name = "fecha"
    return media_mensual_df

def f_serie_anomalias_mensuales(frecuencia_relativa_mensual, frecuencia_relativa_mensual_climatologia):
    frecuencia_relativa_anomalia = frecuencia_relativa_mensual.copy()
    for fecha in frecuencia_relativa_anomalia.index:
        for mes in frecuencia_relativa_anomalia.index.month.unique():
            if fecha.month == mes:
                frecuencia_relativa_anomalia.loc[fecha] = frecuencia_relativa_mensual.loc[fecha]-frecuencia_relativa_mensual_climatologia.loc[mes]
    return frecuencia_relativa_anomalia

def f_calculo_CI(datos_dict, id_omm, na = 20):
    df_data = datos_dict[id_omm]
    CI = []
    indices = []
    for anio in df_data.index.year.unique():#iterar sobre los anios
        data_anio = df_data.loc[str(anio)]
        for month in data_anio.index.month.unique():
            data_mes = data_anio[data_anio.index.month == month]
            data_mes_values = data_mes.value_counts()
            cantidad_datos_mes = data_mes.size
            cantidad_datos_faltantes_mes = data_mes.isnull().sum().values[0]
            if (cantidad_datos_faltantes_mes > cantidad_datos_mes * na/100): #si hay mas del 20% de datos faltantes computa CI como na
                CI_anio_mes = np.nan
            else:
                #N8
                if (8.0,) in data_mes_values.index:
                    N8 = data_mes_values.loc[8].values[0]
                else:
                    N8 = 0
                    
                #N7
                if (7.0,) in data_mes_values.index:
                    N7 = data_mes_values.loc[7].values[0]
                else:
                    N7 = 0
                
                #N6
                if (6.0,) in data_mes_values.index:
                    N6 = data_mes_values.loc[6].values[0]
                else:
                    N6 = 0
                
                #N2
                if (2.0,) in data_mes_values.index:
                    N2 = data_mes_values.loc[2].values[0]
                else:
                    N2 = 0
                
                #N1
                if (1.0,) in data_mes_values.index:
                    N1 = data_mes_values.loc[1].values[0]
                else:
                    N1 = 0
            
                #N0
                if (0.0,) in data_mes_values.index:
                    N0 = data_mes_values.loc[0].values[0]
                else:
                    N0 = 0
                Ntot = cantidad_datos_mes
                CI_anio_mes = 50 + 50 * (N8 + N7 + N6 - N2 -N1 - N0) / Ntot
            CI.append(CI_anio_mes) 
            indices.append(dt.date(anio,month,1))     
    CI_guardo = pd.DataFrame(CI)
    CI_guardo.index = indices
    return(CI_guardo)

def f_calculo_PC(datos_dict, id_omm, na = 20):
    df_data = datos_dict[id_omm]
    PC = []
    indices = []
    for anio in df_data.index.year.unique():#iterar sobre los anios
        data_anio = df_data.loc[str(anio)]
        for month in data_anio.index.month.unique():
            data_mes = data_anio[data_anio.index.month == month]
            data_mes_values = data_mes.value_counts()
            cantidad_datos_mes = data_mes.size
            cantidad_datos_faltantes_mes = data_mes.isnull().sum().values[0]
            if (cantidad_datos_faltantes_mes > cantidad_datos_mes * na/100): #si hay mas del 20% de datos faltantes computa CI como na
                PC_anio_mes = np.nan
            else:
                #N8
                if (8.0,) in data_mes_values.index:
                    N8 = data_mes_values.loc[8].values[0]
                else:
                    N8 = 0
            
                #N0
                if (0.0,) in data_mes_values.index:
                    N0 = data_mes_values.loc[0].values[0]
                else:
                    N0 = 0
                Ntot = cantidad_datos_mes
                PC_anio_mes = 50 + 50 * (N8 - N0) / Ntot
            PC.append(PC_anio_mes) 
            indices.append(dt.date(anio,month,1))     
    PC_guardo = pd.DataFrame(PC)
    PC_guardo.index = indices
    return(PC_guardo)

def f_cor_CI_media_anomalias_paper(medias_dict, CI_dict, estaciones):
    
    nombre_estacion = estaciones[id_estacion]
    ides_estaciones = list(estaciones.keys())
    
    #datos
    x = medias_dict[ides_estacion[0]][0].values
    y = CI_dict[ides_estacion[0]][0].values
    
    #datos 2
    x_2 = medias_dict[ides_estacion[1]][0].values
    y_2 = CI_dict[ides_estacion[1]][0].values
    
    #calculo recta de regresion
    idx = np.isfinite(x) & np.isfinite(y)
    m, b = np.polyfit(x[idx], y[idx], 1) #m = slope, b=intercept
    
    #calculo R2
    correlation = np.corrcoef(x[idx], y[idx])[0,1]
    r_squared = correlation**2

    plt.figure(num=1, figsize=(5, 5), dpi=600) #genero figura
    ax = plt.gca()
    
    ax.scatter(x, y, c ="k", alpha = 0.7, zorder = 4)
    ax.scatter(x_2, y_2, c ="k", alpha = 0.7, zorder = 4)
    
    ax.plot(x, m*x + b, c = "#D01B25", zorder = 5)
    ax.text(-1.5, 5, '$R^2$ = %0.2f' % r_squared, c= "#D01B25", fontweight = 800, zorder = 6)
    ax.hlines(0, xmin = -3, xmax = 3, color = "grey", zorder = 3)
    ax.vlines(0, ymin = -50, ymax = 50, color = "grey", zorder = 2)
    
    ax.set_xlabel('Monthly cloud cover anomaly (oktas)')
    ax.set_ylabel(f'Monthly cloud index anomaly (%)')
     
    plt.ylim(-50, 50)
    plt.xlim(-3, 3)
    ax.grid(alpha = 0.5, zorder = 1)
    ax.annotate(nombre_estacion, (-2.7, 38), size = 17, style='italic', zorder = 7)
    ax.annotate("1961-2021", (-2.7, 34), size = 10, style='italic', zorder = 7)
    plt.savefig(f"figura1_cor_CI_media_mensual_{nombre_estacion}.png")
    plt.show()
    
def f_frecuencia_oktas_por_mes(id_omm, df_data):
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
    
    return freqs_guardo, freqs_relativas_guardo

def f_barplot_oktas_separadas_climatologia_media_espacial(frecuencias,
                                         colores = f_paletas_colores.paleta_3_colores_divergentes,
                                         anio_inicio=1983, anio_final=2016):
    
    meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses
    oktas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fig, ax = plt.subplots(3, 3, figsize=[7, 6], dpi=600)
    fig.patch.set_facecolor('white')
    ylim = 22
    colores = ["#3c3c3c", "#3c3c3c", "#3c3c3c"] #unify the colours

    for i in range(0, 3):
                for j in range(0, 3):
                    
                    ax[i, j].bar(frecuencias.index,np.array(frecuencias).transpose()[3*i+j], 
                                 color = colores[i], width = 0.9, zorder = 2)
                    ax[i, j].set_ylim((0,ylim))
                    ax[i, j].set_yticks(np.arange(0,ylim+1, ylim//5))
                    ax[i, j].set_title(f"Okta = {oktas[3*i+j]}", size = 11)
                
                    if j == 0: #solo para los del lateral izquierdo pongo el ylabel
                        ax[i, j].set_ylabel("Frequency %")
                    else:
                        ax[i, j].set_yticklabels([])
                    if i == 2: #solo para los de abajo pongo el xlabel
                        ax[i, j].set_xlabel("Month")
                        
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i,j].set_xticklabels(meses)
                        #ax[i,j].set_xticklabels(frecuencias.index)
                    else:
                        ax[i,j].set_xticks(frecuencias.index)
                        ax[i, j].set_xticklabels([])
                    ax[i,j].grid(axis = "y", alpha=0.5, zorder = 1)
    
    fig.tight_layout()
    plt.savefig(f"paper_climatologia_frecuencia_relativa_barplot_oktas_separadas_NEA.png") 
    plt.show()    
    
def f_barplot_media_mensual_ISCCP_y_SMN_climatologia_media_espacial(df_climatologia_isccp, df_climatologia_smn):
    fig = plt.figure(num=1, figsize=(8, 5), dpi=600) #genero figura

    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    ax3 = ax.twinx() # Create another axes that shares the same x-axis as ax.

    meses = ['J', 'F', 'M', 'A', 'M', "J", "J", "A", "S", "O","N", "D"] #inicial meses

    width = 0.4 #ancho de las barras

    b1 = df_climatologia_isccp[0].plot(kind='bar', color="#306292", ax=ax, width=width, position=1, zorder = 2)
    b2 = df_climatologia_smn[0].plot(kind='bar', color="#D23232", ax=ax2, width=width, position=0, zorder = 1)
    ax3.hlines(4, xmin= -0.5, xmax = 11.5, color = "grey", zorder = 1, alpha = 0.8)

    ax.set_ylabel('ISCCP-H Cloud amount (%)')
    ax.set_ylim(31.25, 68.75)
    ax.set_yticks((31.25,31.25+4.6875,31.25+2* 4.6875, 31.25+3*4.6875, 50, 50+4.6875, 50+2*4.6875, 50+3*4.6875,68.75))
    ax.set_xlim(-0.5, 11.5)
    ax.set_xticklabels(meses,rotation = 0)
    ax.grid(alpha = 0.5, zorder = 1)

    ax2.set_ylabel('SMN Cloud cover (okta)')
    ax2.set_ylim(3, 5)
    ax2.set_xlim(-0.5, 11.5)

    ax3.set_yticks([])
    ax3.set_xlim(-0.5, 11.5)

    plt.xlabel("Month")
    fig.legend(["ISCCP-H", "SMN"], bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)
    plt.savefig("paper_figura3b_climatologia_isccp_smn.png")
    plt.show()