import geopandas
from cartopy.io import shapereader
from shapely.geometry.multipolygon import MultiPolygon
import cmocean
import pandas as pd
import xarray as xr
import numpy as np
from shapely.geometry import mapping, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pymannkendall as mk
from f_mis_shapes import df_paises, df_provincias



def grafico_campos_climatologia_nubosidad(xrdata, nombre_variable,unidades_nombre, valor_minimo, valor_maximo, delta_valor, estacional = False, mensual = False, region = "SA", paleta_color = "rain", grid = False, poster = True, estadistico = "annual mean", tres_tipos_de_nubes = False):
    plt.close()
    if region == "SA":
        lat_min = -60
        lat_max = 15
        lon_min = -90
        lon_max = -30
        xticks_min = -85
        xticks_max = -30
        yticks_min = -55
        yticks_max = 15

    elif region == "NEA":
        lat_min = -32
        lat_max = -22
        lon_min = -64
        lon_max = -53
        xticks_min = -63
        xticks_max = -53
        yticks_min = -31
        yticks_max = -22

    elif region == "SESA":
        lat_min = -39
        lat_max = -16
        lon_min = -64
        lon_max = -31
        xticks_min = -60
        xticks_max = -31
        yticks_min = -35
        yticks_max = -18

    elif region == "Corrientes": 
        lat_min = -31
        lat_max = -26
        lon_min = -60
        lon_max = -55
        xticks_min = -59
        xticks_max = -55
        yticks_min = -30
        yticks_max = -26
        
    if tres_tipos_de_nubes == False:
        if estacional == False and mensual == False:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 12
                else:
                    espacio_entre_lat_lon = 8
            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 2
                else:
                    espacio_entre_lat_lon = 2
            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 4 
                else:
                    espacio_entre_lat_lon = 4
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 1
                else:
                    espacio_entre_lat_lon = 1
                    
            # selecciono region
            data_region = xrdata.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
            #data = xrdata.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
            
            # ploteo 
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[5, 3.5], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[7.5, 7.5], dpi=200) 

            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 3.5], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[8.5, 5.5], dpi=200)  
            
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6.5, 4], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[9, 5.5], dpi=200) 
                    
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[5.5, 4], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[8.5, 5.5], dpi=200) 

            ax = fig1.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=0))

            if (paleta_color == "rain"):
                data_region.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='neither',
                                     transform=ccrs.PlateCarree(),cbar_kwargs={'label': "%"},cmap=cmocean.cm.rain)

            elif (paleta_color == "matter"):
                data_region.plot.contourf(ax=ax, levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='neither',
                                     transform=ccrs.PlateCarree(),cbar_kwargs={'label': "%"},cmap=cmocean.cm.matter)

            # seteo el fondo gris para que los nans aparezcan en este color
            if region != "Corrientes": 
                ax.set_facecolor('tab:gray')
                
            ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

            ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

            ax.coastlines(color='0.3')

            #ax.set_xlim(np.min(data_region.lon.values) - 360, np.max(data_region.lon.values)-360)
            ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
            plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
            ax.set_xlabel("Lon")
            ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])

            #ax.set_ylim(np.min(data_region.lat.values), np.max(data_region.lat.values))
            plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
            ax.set_ylabel("Lat")

            if (grid == True):
                plt.grid(linestyle="--", alpha=0.3)

            plt.title(f"CA: {estadistico} \nDec1983-Nov2016")
            # plt.tight_layout()
            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}.png")
            plt.show()


        elif estacional == True and mensual == False:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 16
                else:
                    espacio_entre_lat_lon = 12

            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 2
                else:
                    espacio_entre_lat_lon = 2

            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 8 
                else:
                    espacio_entre_lat_lon = 6 
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 2 
                else:
                    espacio_entre_lat_lon = 2 
                    
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[4, 4], dpi=1000)  # vertical sudamerica POSTER
                else:
                    fig1 = plt.figure(figsize=[7.5, 7], dpi=200)  # vertical sudamerica VER

            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[5.5, 4], dpi=1000)  # nea POSTER
                else:
                    fig1 = plt.figure(figsize=[7.5, 5.5], dpi=200)  # nea
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6.5, 3.8], dpi=1000)  # ver
                else:
                    fig1 = plt.figure(figsize=[7.5, 4.3], dpi=200)  # ver
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[4.8, 4], dpi=1000)  # ver
                else:
                    fig1 = plt.figure(figsize=[6.5, 5.5], dpi=200)  # ver

            posiciones = [221, 222, 223, 224]
            estaciones = ["DJF", "MAM", "JJA", "SON"]
            estaciones_nombre = ["DEF", "MAM", "JJA", "SON"]

            for i in range(0,4):
                xrdata_estacion = xrdata[estaciones[i]] #selecciono estacion del diccionario xrdata
                data_estacion = xrdata_estacion.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]

                ax = fig1.add_subplot(posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))

                if (paleta_color == "rain"):
                    im = data_estacion.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo+1, delta_valor), transform=ccrs.PlateCarree(),cmap=cmocean.cm.rain, extend='neither', cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []})

                elif (paleta_color == "matter"):
                    im = data_estacion.plot.contourf(ax=ax, levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='neither',transform=ccrs.PlateCarree(),cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []},cmap=cmocean.cm.matter)

                # seteo el fondo gris para que los nans aparezcan en este color
                if region != "Corrientes": 
                    ax.set_facecolor('tab:gray')
                
                ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

                ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

                ax.coastlines(color='0.3')

                #ax.set_xlim(np.min(data_estacion.lon.values) - 360, np.max(data_estacion.lon.values)-360)
                plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                if i == 2 or i ==3 : #solo para los de abajo
                    ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                    ax.set_xlabel("Lon")
                else:
                    ax.set_xticklabels([])
                    ax.set_xlabel("")

                #ax.set_ylim(np.min(data_estacion.lat.values) - 360, np.max(data_estacion.lat.values)-360)
                plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                if i == 0 or i == 2 : #solo para los de la izquierda
                    ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                    ax.set_ylabel("Lat")
                else:
                    ax.set_yticklabels([])
                    ax.set_ylabel("")

                if (grid == True):
                    plt.grid(linestyle="--", alpha=0.3)
                ax.set_title(estaciones_nombre[i]) #CAMBIAR LUEGO DE POSTER POR estaciones

            plt.subplots_adjust(wspace=-0.3)
            cbar_ax = fig1.add_axes([0.85, 0.13, 0.05, 0.75])
            fig1.colorbar(im, cax=cbar_ax, label = unidades_nombre )

            plt.suptitle(f"CA: {estadistico} Dec1983-Nov2016")


            #plt.colorbar()
            #plt.tight_layout()
            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_estaciones_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}_estaciones.png")
            plt.show()
            
        elif estacional == False and mensual == True:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 20
                else:
                    espacio_entre_lat_lon = 16

            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 4
                else:
                    espacio_entre_lat_lon = 3

            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 8 
                else:
                    espacio_entre_lat_lon = 7 
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 2 
                else:
                    espacio_entre_lat_lon = 2 
                    
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[4.2, 6.2], dpi=200)  # vertical sudamerica POSTER [4,6]
                else:
                    fig1 = plt.figure(figsize=[4.9, 7.2], dpi=200)  # vertical sudamerica VER

            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[4.4, 5.3], dpi=200)  # nea POSTER
                else:
                    fig1 = plt.figure(figsize=[6.3, 7], dpi=200)  # nea
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[5.1, 5.2], dpi=200)  # ver [4.9, 4.4]
                else:
                    fig1 = plt.figure(figsize=[7.1, 7], dpi=200)  # ver [8.1, 7]
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[4.4, 5.3], dpi=200)  # ver
                else:
                    fig1 = plt.figure(figsize=[6.3, 7], dpi=200)  # ver

            posiciones = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1), (3,2)]
            meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            meses_nombre = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ag", "Sep", "Oct", "Nov", "Dec"]

            for i in range(0,12):
                xrdata_mes = xrdata[meses[i]] #selecciono mes del diccionario xrdata
                data_mes = xrdata_mes.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
                ax = plt.subplot2grid((4,3), posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))
                
                #ax = fig1.add_subplot(posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))

                if (paleta_color == "rain"):
                    im = data_mes.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo+1, delta_valor), transform=ccrs.PlateCarree(),cmap=cmocean.cm.rain, extend='neither', cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []})

                elif (paleta_color == "matter"):
                    im = data_mes.plot.contourf(ax=ax, levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='neither',transform=ccrs.PlateCarree(),cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []},cmap=cmocean.cm.matter)

                # seteo el fondo gris para que los nans aparezcan en este color
                if region != "Corrientes": 
                    ax.set_facecolor('tab:gray')
                
                ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

                ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

                ax.coastlines(color='0.3')

                #ax.set_xlim(np.min(data_estacion.lon.values) - 360, np.max(data_estacion.lon.values)-360)
                plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                if i == 9 or i == 10 or i == 11 : #solo para los de abajo
                    ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                    ax.set_xlabel("Lon")
                else:
                    ax.set_xticklabels([])
                    ax.set_xlabel("")

                #ax.set_ylim(np.min(data_estacion.lat.values) - 360, np.max(data_estacion.lat.values)-360)
                plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                if i == 0 or i == 3 or i == 6 or i == 9 : #solo para los de la izquierda
                    ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                    ax.set_ylabel("Lat")
                else:
                    ax.set_yticklabels([])
                    ax.set_ylabel("")

                if (grid == True):
                    plt.grid(linestyle="--", alpha=0.3)
                ax.set_title(meses_nombre[i])

            plt.subplots_adjust(wspace=-0.3, hspace=0.4)
            cbar_ax = fig1.add_axes([0.85, 0.13, 0.05, 0.75])
            fig1.colorbar(im, cax=cbar_ax, label = unidades_nombre )

            plt.suptitle(f"CA: {estadistico} Dec1983-Nov2016", y=0.95)


            #plt.colorbar()
            #plt.tight_layout()
            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_meses_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}_meses.png")
            plt.show()      
                
    elif tres_tipos_de_nubes == True:
        if estacional == False and mensual == False:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 12
                else:
                    espacio_entre_lat_lon = 12
            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 3
                else:
                    espacio_entre_lat_lon = 3
            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 8 
                else:
                    espacio_entre_lat_lon = 8
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 2
                else:
                    espacio_entre_lat_lon = 2
            
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.7], dpi=200)  # vertical sudamerica POSTER
                else:
                    fig1 = plt.figure(figsize=[8, 3.5], dpi=200)  # vertical sudamerica
            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.2], dpi=200)  # 
                else:
                    fig1 = plt.figure(figsize=[8.5, 2.8], dpi=200)  # 
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 1.9], dpi=200)  # 
                else:
                    fig1 = plt.figure(figsize=[8.5, 2.4], dpi=200)  # 
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.5], dpi=200)  # 
                else:
                    fig1 = plt.figure(figsize=[8, 3], dpi=200)  # 

            posiciones = [131, 132, 133]
            alturas = ["Low clouds", "Middle clouds", "High clouds"]

            for i in range(0,3):
                xrdata_altura = xrdata[alturas[i]] #selecciono altura de la nube del diccionario xrdata
                data_altura = xrdata_altura.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]

                ax = fig1.add_subplot(posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))

                if (paleta_color == "rain"):
                    im = data_altura.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo+1, delta_valor), transform=ccrs.PlateCarree(),cmap=cmocean.cm.rain, extend='neither', cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []})

                elif (paleta_color == "matter"):
                    im = data_altura.plot.contourf(ax=ax, levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='neither',transform=ccrs.PlateCarree(),cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []},cmap=cmocean.cm.matter)

                # seteo el fondo gris para que los nans aparezcan en este color
                if region != "Corrientes": 
                    ax.set_facecolor('tab:gray')
                
                ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

                ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

                ax.coastlines(color='0.3')

                ax.set_xlim(np.min(data_altura.lon.values) - 360, np.max(data_altura.lon.values)-360)
                plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])

                ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                ax.set_xlabel("Lon")


                ax.set_ylim(np.min(data_altura.lat.values), np.max(data_altura.lat.values))
                plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                if i == 0 : #solo para los de la izquierda
                    ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                    ax.set_ylabel("Lat")
                else:
                    ax.set_yticklabels([])
                    ax.set_ylabel("")

                if (grid == True):
                    plt.grid(linestyle="--", alpha=0.3)
                ax.set_title(alturas[i])

            plt.subplots_adjust(wspace=-0.1)
            cbar_ax = fig1.add_axes([0.88, 0.2, 0.05, 0.6])
            fig1.colorbar(im, cax=cbar_ax, label = unidades_nombre )

            plt.suptitle(f"CA: {estadistico} Dec1983-Nov2016")


            #plt.colorbar()
            #plt.tight_layout()
            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_alturas_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}_alturas.png")
            plt.show()
                        


#######################################
def grafico_campos_climatologia_nubosidad_tendencias(xrdata, unidades_nombre, valor_minimo, valor_maximo, delta_valor, estacional = False, mensual = False, region = "SA", grid = False, poster = True, estadistico = "Annual tendency", tres_tipos_de_nubes = False):
    
    plt.close()
    if region == "SA":
        lat_min = -60
        lat_max = 15
        lon_min = -90
        lon_max = -30
        xticks_min = -85
        xticks_max = -30
        yticks_min = -55
        yticks_max = 15

    elif region == "NEA":
        lat_min = -32
        lat_max = -22
        lon_min = -64
        lon_max = -53
        xticks_min = -63
        xticks_max = -53
        yticks_min = -31
        yticks_max = -22

    elif region == "SESA":
        lat_min = -39
        lat_max = -16
        lon_min = -64
        lon_max = -31
        xticks_min = -60
        xticks_max = -31
        yticks_min = -35
        yticks_max = -18

    elif region == "Corrientes": 
        lat_min = -31
        lat_max = -26
        lon_min = -60
        lon_max = -55
        xticks_min = -59
        xticks_max = -55
        yticks_min = -30
        yticks_max = -26
        
    if tres_tipos_de_nubes == False:
        if estacional == False and mensual == False:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 12
                else:
                    espacio_entre_lat_lon = 8
            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 2
                else:
                    espacio_entre_lat_lon = 2
            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 4 
                else:
                    espacio_entre_lat_lon = 4
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 1 
                else:
                    espacio_entre_lat_lon = 1 

            # recorto region
            variable_data = xrdata[0].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
            variable_significancia = xrdata[1].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
            # me quedo solo con los que son significativos para marcar esas regiones con puntitos
            variable_significancia = variable_significancia.where(variable_significancia.values == 1)

            # ploteo 
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[5, 3.5], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[7.5, 7.5], dpi=200) 

            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 3.5], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[8.5, 5.5], dpi=200)  
            
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6.5, 4], dpi=1000)  #ver
                else:
                    fig1 = plt.figure(figsize=[9, 5.5], dpi=200) #ver
            
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[5.5, 4], dpi=1000)  # [4,4]
                else:
                    fig1 = plt.figure(figsize=[8.5, 5.5], dpi=200) #ver
            

            ax = fig1.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=0))
            
            
            variable_data.plot.contourf(ax=ax, levels=np.arange(valor_minimo, valor_maximo, delta_valor),
                                            extend='both',transform=ccrs.PlateCarree(),
                                            cbar_kwargs={'label': unidades_nombre},cmap=cmocean.cm.balance)
        
                
            # grafico puntos en los lugares donde es significativo
            variable_significancia.plot.contourf(ax=ax, levels=[0, 1], hatches=['.'], alpha=0, add_colorbar=False)

            # seteo el fondo gris para que los nans aparezcan en este color
            if region != "Corrientes": 
                ax.set_facecolor('tab:gray')

            ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',
                              edgecolor='0.5', linewidth=0.7, alpha=0.9)

            ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',
                              edgecolor='0.4', alpha=0.9)

            ax.coastlines(color='0.3')

            ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
            plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
            ax.set_xlabel("Lon")

            ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
            plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
            ax.set_ylabel("Lat")

            if (grid == True):
                plt.grid(linestyle="--", alpha=0.3)

            plt.title(f"CA: {estadistico} \nDec1983-Nov2016")

            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_poster.png")
                plt.show()
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}.png")
                plt.show()

        elif estacional == True and mensual == False: #xrdata es un diccionario donde cada elemento es un xarray 
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 16
                else:
                    espacio_entre_lat_lon = 12

            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 2
                else:
                    espacio_entre_lat_lon = 2

            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 8 
                else:
                    espacio_entre_lat_lon = 6 
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 2 
                else:
                    espacio_entre_lat_lon = 2 
            
            
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[4, 4], dpi=1000) 
                else:
                    fig1 = plt.figure(figsize=[7.5, 7.5], dpi=200)  

            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[5.5, 4], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[7.5, 5.5], dpi=200)  
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6.5, 3.8], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[7.5, 4.3], dpi=200)  
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[4.8, 4], dpi=1000)  
                else:
                    fig1 = plt.figure(figsize=[6.5, 5.5], dpi=200)  


            posiciones = [221, 222, 223, 224]
            estaciones = ["DJF", "MAM", "JJA", "SON"]
            estaciones_nombres = ["DEF", "MAM", "JJA", "SON"]

            for i in range(0,4):
                xrdata_estacion = xrdata[estaciones[i]] #selecciono estacion del diccionario xrdata
                variable_data_estacion = xrdata_estacion[0].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
                variable_significancia_estacion = xrdata_estacion[1].loc[dict(lon=slice(360+lon_min,360+lon_max), lat=slice(lat_min, lat_max))]
                # me quedo solo con los que son significativos para marcar esas regiones con puntitos
                variable_significancia_estacion = variable_significancia_estacion.where(variable_significancia_estacion.values == 1)

                ax = fig1.add_subplot(posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))

                im = variable_data_estacion.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='both',transform=ccrs.PlateCarree(),cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []},cmap=cmocean.cm.balance)

                # grafico puntos en los lugares donde es significativo
                variable_significancia_estacion.plot.contourf(ax=ax, levels=[0, 1], hatches=["."], alpha=0, add_colorbar=False) 

                # seteo el fondo gris para que los nans aparezcan en este color
                if region != "Corrientes": 
                    ax.set_facecolor('tab:gray')
                

                ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

                ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

                ax.coastlines(color='0.3')
                
                ax.set_xlim(np.min(variable_data_estacion.lon.values) - 360, np.max(variable_data_estacion.lon.values)-360)
                plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                if i == 2 or i ==3 : #solo para los de abajo
                    ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                    ax.set_xlabel("Lon")
                else:
                    ax.set_xticklabels([])
                    ax.set_xlabel("")
                
                ax.set_ylim(np.min(variable_data_estacion.lat.values), np.max(variable_data_estacion.lat.values))
                plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                if i == 0 or i == 2 : #solo para los de la izquierda
                    ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                    ax.set_ylabel("Lat")
                else:
                    ax.set_yticklabels([])
                    ax.set_ylabel("")

                if (grid == True):
                    plt.grid(linestyle="--", alpha=0.3)
                
                ax.set_title(estaciones_nombres[i])

            plt.subplots_adjust(wspace=-0.3)
            cbar_ax = fig1.add_axes([0.85, 0.13, 0.05, 0.75])
            fig1.colorbar(im, cax=cbar_ax, label = unidades_nombre )

            plt.suptitle(f"CA: {estadistico} Dec1983-Nov2016")

            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_estaciones_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}_estaciones.png")
            plt.show()
            
    elif tres_tipos_de_nubes == True:     
        
        if estacional == False and mensual == False:
            if region == "SA":
                if poster:
                    espacio_entre_lat_lon = 12
                else:
                    espacio_entre_lat_lon = 12
            elif region == "NEA":
                if poster:
                    espacio_entre_lat_lon = 3
                else:
                    espacio_entre_lat_lon = 3
            elif region == "SESA":
                if poster:
                    espacio_entre_lat_lon = 8 #ver
                else:
                    espacio_entre_lat_lon = 8
            elif region == "Corrientes":
                if poster:
                    espacio_entre_lat_lon = 2 #ver
                else:
                    espacio_entre_lat_lon = 2
            
            if region == "SA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.7], dpi=200)  
                else:
                    fig1 = plt.figure(figsize=[8, 3.5], dpi=200)  
            elif region == "NEA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.2], dpi=200)   
                else:
                    fig1 = plt.figure(figsize=[8.5, 2.8], dpi=200)  
            elif region == "SESA":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 1.9], dpi=200)  
                else:
                    fig1 = plt.figure(figsize=[8.5, 2.4], dpi=200)  
            elif region == "Corrientes":
                if poster == True:
                    fig1 = plt.figure(figsize=[6, 2.5], dpi=200)  
                else:
                    fig1 = plt.figure(figsize=[8, 3], dpi=200)  

            posiciones = [131, 132, 133]
            alturas = ["Low clouds", "Middle clouds", "High clouds"]
            
            for i in range(0,3):
                xrdata_altura = xrdata[alturas[i]] #selecciono altura de la nube del diccionario xrdata
                variable_data = xrdata_altura[0].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
                variable_significancia = xrdata_altura[1].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
                # me quedo solo con los que son significativos para marcar esas regiones con puntitos
                variable_significancia = variable_significancia.where(variable_significancia.values == 1)

                ax = fig1.add_subplot(posiciones[i], projection=ccrs.PlateCarree(central_longitude=0))
                
                im = variable_data.plot.contourf(ax=ax,levels=np.arange(valor_minimo, valor_maximo, delta_valor),extend='both',transform=ccrs.PlateCarree(),cbar_kwargs = {'shrink':0.0001, "label":" ", "ticks": []},cmap=cmocean.cm.balance)

                # grafico puntos en los lugares donde es significativo
                variable_significancia.plot.contourf(ax=ax, levels=[0, 1], hatches=["."], alpha=0, add_colorbar=False) 

                # seteo el fondo gris para que los nans aparezcan en este color
                if region != "Corrientes": 
                    ax.set_facecolor('tab:gray')

                ax.add_geometries(df_provincias(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.5', linewidth=0.7, alpha=0.9)

                ax.add_geometries(df_paises(), crs=ccrs.PlateCarree(), facecolor='none',edgecolor='0.4', alpha=0.9)

                ax.coastlines(color='0.3')
                
                ax.set_xlim(np.min(variable_data.lon.values) - 360, np.max(variable_data.lon.values)-360)
                plt.xticks(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                ax.set_xticklabels(np.arange(xticks_min, xticks_max)[::espacio_entre_lat_lon])
                ax.set_xlabel("Lon")


                ax.set_ylim(np.min(variable_data.lat.values), np.max(variable_data.lat.values))
                plt.yticks(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                if i == 0 : #solo para los de la izquierda
                    ax.set_yticklabels(np.arange(yticks_min, yticks_max)[::espacio_entre_lat_lon])
                    ax.set_ylabel("Lat")
                else:
                    ax.set_yticklabels([])
                    ax.set_ylabel("")

                if (grid == True):
                    plt.grid(linestyle="--", alpha=0.3)
                ax.set_title(alturas[i])
                
            plt.subplots_adjust(wspace=-0.1)
            cbar_ax = fig1.add_axes([0.88, 0.2, 0.05, 0.6])
            fig1.colorbar(im, cax=cbar_ax, label = unidades_nombre )
            
            plt.suptitle(f"CA: {estadistico} Dec1983-Nov2016")

            if poster:
                plt.savefig(f"cldamt_{estadistico}_{region}_alturas_poster.png")
            else:
                plt.savefig(f"cldamt_{estadistico}_{region}_alturas.png")
            plt.show()


                

#grafica cldamt media espacial como serie temporal, de cldamt total y de cldamt bajas, medias y altas
#agregar opcion para corrientes
#hacer estacional

def serie_media_espacial(xrdata_total, xrdata_alturas, estacional = False, region = "SA", poster = True):

    if region == "SA":
        lat_min = -60
        lat_max = 15
        lon_min = -90
        lon_max = -30
        
    elif region == "NEA":
        lat_min = -32
        lat_max = -22
        lon_min = -64
        lon_max = -53
        
    elif region == "SESA":
        lat_min = -39
        lat_max = -16
        lon_min = -64
        lon_max = -31  
        
    elif region == "Corrientes":
        lat_min = -31
        lat_max = -26
        lon_min = -60
        lon_max = -55
    
    #recorto region
    serie_cldamt_total = xrdata_total.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
    serie_cldamt_bajas = xrdata_alturas["Low clouds"].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
    serie_cldamt_medias = xrdata_alturas["Middle clouds"].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
    serie_cldamt_altas = xrdata_alturas["High clouds"].loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))]
    
    if estacional:
        print("Todavia no esta corregida esta parte del codigo, de ser necesario se puede empezar con lo comentado en la funcion de graficado")
        #calculo media estacional
        #xrdata_total_estaciones = {"DJF": calculo_medias_estaciones(serie_cldamt_total, "DJF"),
        #                           "MAM": calculo_medias_estaciones(serie_cldamt_total, "MAM"),
        #                           "JJA": calculo_medias_estaciones(serie_cldamt_total, "JJA"),
        #                           "SON": calculo_medias_estaciones(serie_cldamt_total, "SON")}
        #xrdata_bajas_estaciones = {"DJF": calculo_medias_estaciones(serie_cldamt_bajas, "DJF"),
        #                           "MAM": calculo_medias_estaciones(serie_cldamt_bajas, "MAM"),
        #                           "JJA": calculo_medias_estaciones(serie_cldamt_bajas, "JJA"),
        #                           "SON": calculo_medias_estaciones(serie_cldamt_bajas, "SON")}
        #xrdata_medias_estaciones = {"DJF": calculo_medias_estaciones(serie_cldamt_medias, "DJF"),
        #                           "MAM": calculo_medias_estaciones(serie_cldamt_medias, "MAM"),
        #                           "JJA": calculo_medias_estaciones(serie_cldamt_medias, "JJA"),
        #                           "SON": calculo_medias_estaciones(serie_cldamt_medias, "SON")}
        #xrdata_altas_estaciones = {"DJF": calculo_medias_estaciones(serie_cldamt_altas, "DJF"),
        #                           "MAM": calculo_medias_estaciones(serie_cldamt_altas, "MAM"),
        #                           "JJA": calculo_medias_estaciones(serie_cldamt_altas, "JJA"),
        #                           "SON": calculo_medias_estaciones(serie_cldamt_altas, "SON")}
        
        #armo series medias para esa region
        #serie_media_cldamt_total_estaciones = {"DJF": xrdata_total_estaciones["DJF"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "MAM": xrdata_total_estaciones["MAM"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "JJA": xrdata_total_estaciones["JJA"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "SON": xrdata_total_estaciones["SON"].mean(dim = ["lat","lon"], skipna=True)}
        
        #serie_media_cldamt_bajas_estaciones = {"DJF": xrdata_bajas_estaciones["DJF"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "MAM": xrdata_bajas_estaciones["MAM"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "JJA": xrdata_bajas_estaciones["JJA"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "SON": xrdata_bajas_estaciones["SON"].mean(dim = ["lat","lon"], skipna=True)}
        
        #serie_media_cldamt_medias_estaciones = {"DJF": xrdata_medias_estaciones["DJF"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "MAM": xrdata_medias_estaciones["MAM"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "JJA": xrdata_medias_estaciones["JJA"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "SON": xrdata_medias_estaciones["SON"].mean(dim = ["lat","lon"], skipna=True)}
        
        #serie_media_cldamt_altas_estaciones = {"DJF": xrdata_altas_estaciones["DJF"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "MAM": xrdata_altas_estaciones["MAM"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "JJA": xrdata_altas_estaciones["JJA"].mean(dim = ["lat","lon"], skipna=True),
        #                                       "SON": xrdata_altas_estaciones["SON"].mean(dim = ["lat","lon"], skipna=True)}
        
        #serie_fechas = xrdata_total.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))].time #ver
        
        #ploteo
        #if poster == True:
        #    fig1, ax = plt.subplots(figsize=[6, 4], dpi=200)
        #else:
        #    fig1, ax = plt.subplots(figsize=[10, 6], dpi=200)
        
        #posiciones = [221, 222, 223, 224]
        #estaciones = ["DJF", "MAM", "JJA", "SON"]
        
        #for i in range(0,4):
        #    serie_fechas = xrdata_total_estaciones[estaciones[i]].time 
        #    serie_media_cldamt_total = serie_media_cldamt_total_estaciones[estaciones[i]]
        #    serie_media_cldamt_bajas = serie_media_cldamt_bajas_estaciones[estaciones[i]]
        #    serie_media_cldamt_medias = serie_media_cldamt_medias_estaciones[estaciones[i]]
        #    serie_media_cldamt_altas = serie_media_cldamt_altas_estaciones[estaciones[i]]
            
        #    ax = fig1.add_subplot(posiciones[i])
        #    plt.plot(serie_fechas, serie_media_cldamt_total, color = "k", alpha=0.7)
        #    plt.plot(serie_fechas, serie_media_cldamt_bajas, color = "teal", alpha=0.7)
        #    plt.plot(serie_fechas, serie_media_cldamt_medias, color = "purple", alpha=0.7)
        #    plt.plot(serie_fechas, serie_media_cldamt_altas, color = "crimson", alpha=0.7)
            
            #serie fechas
            #print(np.arange(0, len(serie_fechas), 1))
            #print(np.array(serie_media_cldamt_total.fillna(0) ))
            # agrego lineas de tendencia, si es significativa con un 95% (test mann kendall) lo hago con linea llena y si no con linea intermitente
            #coef1 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_total.fillna(0)), 1)
            #linear_fit_1 = np.poly1d(coef1)
            #if (abs(mk.original_test(serie_media_cldamt_total, alpha=0.05)[3]) > 1.96):
             #   plt.plot(serie_fechas, linear_fit_1(np.arange(0, len(serie_fechas), 1)), color="k", ls="-")
            #else:
             #   plt.plot(serie_fechas, linear_fit_1(np.arange(0, len(serie_fechas), 1)), color="k", ls=":")

            #coef2 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_bajas), 1)
            #linear_fit_2 = np.poly1d(coef2)
            #if (abs(mk.original_test(serie_media_cldamt_bajas, alpha=0.05)[3]) > 1.96):
            #    plt.plot(serie_fechas, linear_fit_2(np.arange(0, len(serie_fechas), 1)), color="teal", ls="-")
            #else:
            #    plt.plot(serie_fechas, linear_fit_2(np.arange(0, len(serie_fechas), 1)), color="teal", ls=":")

            #coef3 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_medias), 1)
            #linear_fit_3 = np.poly1d(coef3)
            #if (abs(mk.original_test(serie_fechas, alpha=0.05)[3]) > 1.96):
             #   plt.plot(serie_fechas, linear_fit_3(np.arange(0, len(serie_fechas), 1)), color="purple", ls="-")
            #else:
            #    plt.plot(serie_fechas, linear_fit_3(np.arange(0, len(serie_fechas), 1)), color="purple", ls=":")

            #coef4 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_altas), 1)
            #linear_fit_4 = np.poly1d(coef4)
            #if (abs(mk.original_test(serie_media_cldamt_altas, alpha=0.05)[3]) > 1.96):
            #    plt.plot(serie_fechas, linear_fit_4(np.arange(0, len(serie_fechas), 1)), color="crimson", ls="-")
            #else:
             #   plt.plot(serie_fechas, linear_fit_4(np.arange(0, len(serie_fechas), 1)), color="crimson", ls="--")

        #    media1 = np.round(np.nanmean(serie_media_cldamt_total), 1)
        #    desvio1 = np.round(np.nanstd(serie_media_cldamt_total), 2)
            #tendencia1 = np.round(coef1[0]*12*10, 2)  # decadal

        #    media2 = np.round(np.nanmean(serie_media_cldamt_bajas), 1)
        #    desvio2 = np.round(np.nanstd(serie_media_cldamt_bajas), 2)
            #tendencia2 = np.round(coef2[0]*12*10, 2)  # decadal

        #    media3 = np.round(np.nanmean(serie_media_cldamt_medias), 1)
        #    desvio3 = np.round(np.nanstd(serie_media_cldamt_medias), 2)
            #tendencia3 = np.round(coef3[0]*12*10, 2)  # decadal

        #    media4 = np.round(np.nanmean(serie_media_cldamt_altas), 1)
        #    desvio4 = np.round(np.nanstd(serie_media_cldamt_altas), 2)
            #tendencia4 = np.round(coef4[0]*12*10, 2)  # decadal
            
            #plt.text(5200, 85, "Mean (%) \nSD (%) \nTendency (%/dec)",color="k", ha="left", backgroundcolor="white")
            #plt.text(9500, 85, f"{media1:.3}\n{desvio1:.3}\n{tendencia1:.3}", color="k", ha="left", backgroundcolor="white")
            #plt.text(10500, 85, f"{media2:.3}\n{desvio2:.3}\n{tendencia2:.2}", color="teal", ha="left", backgroundcolor="white")
            #plt.text(11500, 85, f"{media3:.3}\n{desvio3:.3}\n{tendencia3:.2}", color="purple", ha="left", backgroundcolor="white")
            #plt.text(12500, 85, f"{media4:.3}\n{desvio4:.3}\n{tendencia4:.3}", color="crimson", ha="left", backgroundcolor="white")
            
         #   ax.set_ylim(0, 100)
            
        #plt.show()   
    
    elif estacional == False:
        
        #armo series medias para esa region 
        serie_media_cldamt_total = serie_cldamt_total.mean(dim = ["lat","lon"], skipna=True)
        serie_media_cldamt_bajas = serie_cldamt_bajas.mean(dim = ["lat","lon"], skipna=True)
        serie_media_cldamt_medias = serie_cldamt_medias.mean(dim = ["lat","lon"], skipna=True)
        serie_media_cldamt_altas = serie_cldamt_altas.mean(dim = ["lat","lon"], skipna=True)

        #serie de fechas 
        serie_fechas = xrdata_total.loc[dict(lon=slice(360+lon_min, 360+lon_max),lat=slice(lat_min, lat_max))].time

        #ploteo
        if poster == True:
            fig1, ax = plt.subplots(figsize=[5, 4], dpi=200)
        else:
            fig1, ax = plt.subplots(figsize=[10, 6], dpi=200)
        plt.plot(serie_fechas, serie_media_cldamt_total, color = "k", alpha=0.7)
        plt.plot(serie_fechas, serie_media_cldamt_bajas, color = "teal", alpha=0.7)
        plt.plot(serie_fechas, serie_media_cldamt_medias, color = "purple", alpha=0.7)
        plt.plot(serie_fechas, serie_media_cldamt_altas, color = "crimson", alpha=0.7)

        # agrego lineas de tendencia, si es significativa con un 95% (test mann kendall) lo hago con linea llena y si no con linea intermitente
        coef1 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_total), 1)
        linear_fit_1 = np.poly1d(coef1)
        if (abs(mk.original_test(serie_media_cldamt_total, alpha=0.05)[3]) > 1.96):
            plt.plot(serie_fechas, linear_fit_1(np.arange(0, len(serie_fechas), 1)), color="k", ls="-")
        else:
            plt.plot(serie_fechas, linear_fit_1(np.arange(0, len(serie_fechas), 1)), color="k", ls=":")

        coef2 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_bajas), 1)
        linear_fit_2 = np.poly1d(coef2)
        if (abs(mk.original_test(serie_media_cldamt_bajas, alpha=0.05)[3]) > 1.96):
            plt.plot(serie_fechas, linear_fit_2(np.arange(0, len(serie_fechas), 1)), color="teal", ls="-")
        else:
            plt.plot(serie_fechas, linear_fit_2(np.arange(0, len(serie_fechas), 1)), color="teal", ls=":")

        coef3 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_medias), 1)
        linear_fit_3 = np.poly1d(coef3)
        if (abs(mk.original_test(serie_fechas, alpha=0.05)[3]) > 1.96):
            plt.plot(serie_fechas, linear_fit_3(np.arange(0, len(serie_fechas), 1)), color="purple", ls="-")
        else:
            plt.plot(serie_fechas, linear_fit_3(np.arange(0, len(serie_fechas), 1)), color="purple", ls=":")

        coef4 = np.polyfit(np.arange(0, len(serie_fechas), 1), np.array(serie_media_cldamt_altas), 1)
        linear_fit_4 = np.poly1d(coef4)
        if (abs(mk.original_test(serie_media_cldamt_altas, alpha=0.05)[3]) > 1.96):
            plt.plot(serie_fechas, linear_fit_4(np.arange(0, len(serie_fechas), 1)), color="crimson", ls="-")
        else:
            plt.plot(serie_fechas, linear_fit_4(np.arange(0, len(serie_fechas), 1)), color="crimson", ls="--")

        media1 = np.round(np.nanmean(serie_media_cldamt_total), 1)
        desvio1 = np.round(np.nanstd(serie_media_cldamt_total), 2)
        tendencia1 = np.round(coef1[0]*12*10, 2)  # decadal

        media2 = np.round(np.nanmean(serie_media_cldamt_bajas), 1)
        desvio2 = np.round(np.nanstd(serie_media_cldamt_bajas), 2)
        tendencia2 = np.round(coef2[0]*12*10, 2)  # decadal

        media3 = np.round(np.nanmean(serie_media_cldamt_medias), 1)
        desvio3 = np.round(np.nanstd(serie_media_cldamt_medias), 2)
        tendencia3 = np.round(coef3[0]*12*10, 2)  # decadal

        media4 = np.round(np.nanmean(serie_media_cldamt_altas), 1)
        desvio4 = np.round(np.nanstd(serie_media_cldamt_altas), 2)
        tendencia4 = np.round(coef4[0]*12*10, 2)  # decadal

        if poster == True:
            plt.text(5000, 83, "Mean (%) \nSD (%) \nTendency (%/dec)",color="k", ha="left", backgroundcolor="white", fontsize =  'small')
            plt.text(8850, 83, f"{media1:.3}\n{desvio1:.3}\n{tendencia1:.3}", color="k", ha="left", backgroundcolor="white", fontsize =  'small')
            plt.text(10100, 83, f"{media2:.3}\n{desvio2:.3}\n{tendencia2:.2}", color="teal", ha="left", backgroundcolor="white", fontsize =  'small')
            plt.text(11350, 83, f"{media3:.3}\n{desvio3:.3}\n{tendencia3:.2}", color="purple", ha="left", backgroundcolor="white", fontsize =  'small')
            plt.text(12550, 83, f"{media4:.3}\n{desvio4:.3}\n{tendencia4:.3}", color="crimson", ha="left", backgroundcolor="white", fontsize =  'small')

        else:
            plt.text(5200, 85, "Mean (%) \nSD (%) \nTendency (%/dec)",color="k", ha="left", backgroundcolor="white")
            plt.text(9500, 85, f"{media1:.3}\n{desvio1:.3}\n{tendencia1:.3}", color="k", ha="left", backgroundcolor="white")
            plt.text(10500, 85, f"{media2:.3}\n{desvio2:.3}\n{tendencia2:.2}", color="teal", ha="left", backgroundcolor="white")
            plt.text(11500, 85, f"{media3:.3}\n{desvio3:.3}\n{tendencia3:.2}", color="purple", ha="left", backgroundcolor="white")
            plt.text(12500, 85, f"{media4:.3}\n{desvio4:.3}\n{tendencia4:.3}", color="crimson", ha="left", backgroundcolor="white")

        ax.tick_params(axis='x', direction='out', bottom=True, labelrotation=90, labelsize=10, pad=1.5)

        ax.minorticks_on()
        ax.yaxis.set_tick_params(which='minor', bottom=False)

        ax.set_ylim(0, 100)
        if poster:
            ax.set_xlabel("Date")
            ax.set_ylabel("CA %")
        else:
            ax.set_xlabel("Date", size=14)
            ax.set_ylabel("CA %", size=14)

        ax.grid()
        if poster:
            plt.title(f"{region} CA mean")
        else:
            plt.title(f"{region} CA mean", size=16)
        if poster:
            plt.legend(["CA", "Low-Level CA", "Mid-Level CA", "High-Level CA"], prop={'size':7})
        else:
            plt.legend(["CA", "Low-Level CA", "Mid-Level CA", "High-Level CA"])
        if poster == True:
            plt.savefig(f"CA_{region}_mean_serie_poster.png", dpi=140)
        else:
            plt.savefig(f"CA_{region}_mean_serie.png", dpi=140)
        plt.show()
        
def clip_corrientes(xrdata):
    IGN = gpd.read_file("/pikachu/datos/nadia.testani/Doctorado/datos/mapas/provincia/provincia.shp")
    corrientes_coordenadas = np.array(IGN.geometry[19][0].exterior.coords)
    coords_1=np.copy(corrientes_coordenadas)
    coords_1[:, 0] = coords_1[:, 0] +  360  # sumo 360 a las longitudes para que tenga la misma referencia que los xarrays
    newpoly = Polygon(coords_1)  # armo poligono
    newconus = gpd.GeoDataFrame(index=[0], crs="epsg:4326", geometry=[newpoly]) # georeferencio el poligono

    xds = xrdata
    xds = xds.swap_dims({"lon": "x"})
    xds = xds.swap_dims({"lat": "y"})

    lats = xds["lat"][:].values
    lons = xds["lon"][:].values
    coords_2 = [("y", lats), ("x", lons)]

    #Lo regrillo para que pase de ser 1ºx1º a 0.05ºx0.05º asi se recorta bien. 
    #Lo hago con el metodo de interpolacion lineal. 
    #El regrillado lo hago solo en un entorno a corrientes para ahorrar memoria
    # ynuevo=np.linspace(-89.5, 89.5, 3600) #si se cubriera todo el globo
    # xnuevo=np.linspace(0.5, 359.5, 7200) #si se cubriera todo el globo
    ynuevo = np.linspace(-31.5, -25.5, 60)
    xnuevo = np.linspace(280.5, 315.5, 350)

    serie_fechas = pd.to_datetime(xds.time)
    data_procesada = []
    for i, fecha in enumerate(serie_fechas):
        xds_2 = xr.DataArray(xds.values[i], coords=coords_2)
        xds_3 = xds_2.rio.write_crs("epsg:4326", inplace=True)  # georeferencio
        xds_4 = xds_3.interp(y=ynuevo, x=xnuevo, method="linear")
        clipped = xds_4.rio.clip(newconus.geometry.apply(mapping), newconus.crs, drop=False, invert=False)  # lo recorto
        data_procesada.append(clipped)

    data_procesada_xr = xr.concat(data_procesada, dim = "time") 
    data_procesada_xr.coords["time"] = serie_fechas
    data_procesada_xr = data_procesada_xr.rename({"x": "lon"})
    data_procesada_xr = data_procesada_xr.rename({"y": "lat"})
    data_procesada_xr.name = xds.name
    #data_procesada_xr.attrs['units']=xds.attrs['units']
    return(data_procesada_xr)

