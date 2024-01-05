import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes #para sumar mapa grande
import cartopy #para sumar mapa grande
import cartopy.mpl.geoaxes #para sumar mapa grande
from matplotlib.patches import Rectangle #para graficar rectangulo en mapa grande
    
# mapa con estaciones del smn
def f_mapa(dict_puntos_smn, lista_puntos_smn_importantes, nombres_ides_omm_ordenado, shape_paises, shape_provincias):
    """
    Grafica puntos con estaciones del smn en un entorno a corrientes
    
    dict_puntos_smn: diccionario con codigo de estacion de key y tuplas con las coordenadas como values
    lista_puntos_smn_importantes: lista de codigos de estacion a usar
    nombres_ides_omm_ordenado: nombres de estaciones
    shape_paises
    shape_provincias
    """
    #defino puntos a marcar
    geometry_1 = [Point(xy) for xy in [dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes]] #lista con puntos 2
    geodata1 = gpd.GeoDataFrame([dict_puntos_smn[punto] for punto in lista_puntos_smn_importantes], geometry = geometry_1)
    
    #inicio figura
    fig1 = plt.figure(figsize = [8, 5], dpi = 1000)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_provincias, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.6', linewidth = 0.6, alpha = 0.5, zorder = 1)
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.5', linewidth = 2, alpha = 0.7, zorder = 2)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 50, c = "#D23232", zorder = 4) 
    
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
    
    return(fig1)
    