#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 18:15:18 2021

@author: nadia
"""

"""
Visualizo la informacion:
    Abro uno de los archivos .nc de nubosidad mensual
    Veo las variables
"""

import xarray as xr
nc_ruta="Documentos/Doctorado/datos/precipitacion/cmap_enh_precip_mon_mean"
nc_name="precip.mon.mean.nc"
dset=xr.open_dataset(nc_ruta+"/"+nc_name)
#print(dset)
#dset["precip"].values


#len(dset["precip"].values[:,:,:]) #time,lat,lon

#calculo la media de precip mensual en el periodo usado para nubosidad En1984-Dic2016

#%%
#PERIODO COMPLETO 1984-2016
media=dset["precip"][60:456,:,:].mean("time", keep_attrs=True) #.values
desvio=dset["precip"][60:456,:,:].std("time", keep_attrs=True) #.values

#%%
#POR MES 1984-2016
import numpy as np
import xarray as xr

def media_desvio_mensual(dset,mes):
    dset=dset["precip"][60:456,:,:] #indexo en el tiempo que quiero
    n=1
    arr_3D=np.empty((1,72,144))
    for i in range(0,len(dset["time"])):
        if (str(dset[i,:,:]["time"].values)[5:7]==mes):
            variable_data=[dset[i,:,:].values]
            arr_3D=np.concatenate([arr_3D,variable_data])
            n=n+1
            arr_3D=np.reshape(arr_3D,(n,72,144))
    arr_3D=arr_3D[1:np.shape(arr_3D)[0],:,:]
    media_mensual=np.nanmean(arr_3D,axis=0)
    desvio_mensual=np.nanstd(arr_3D,axis=0)
    
    #cargo lats y lons para armar xarray
    lats=dset[0,:,:]["lat"][:].values
    lons=dset[0,:,:]["lon"][:].values
    coords=[("lat", lats),("lon", lons)]
    
    #salida media
    xarray_media=xr.DataArray(media_mensual, coords=coords)
    xarray_media.name="precip media mensual "+ mes
    xarray_media.attrs['units']=dset.attrs["units"]
    xarray_media.attrs['mes']=mes
    
    #salida desvio
    xarray_desvio=xr.DataArray(desvio_mensual, coords=coords)
    xarray_desvio.name="precip desvio mensual "+ mes
    xarray_desvio.attrs['units']=dset.attrs["units"]
    xarray_desvio.attrs['mes']=mes
        
    return([xarray_media,xarray_desvio])

meses=["01","02","03","04","05","06","07","08","09","10","11","12"]
media_mensual_list=[None]*12
desvio_mensual_list=[None]*12
for i in range(0,12):
    media_mensual_list[i]=media_desvio_mensual(dset,meses[i])[0]
    desvio_mensual_list[i]=media_desvio_mensual(dset,meses[i])[1]

#%%
#POR ESTACION Dic1983-Nov2016
import numpy as np
import xarray as xr

def media_desvio_trimestral(dset,mes1,mes2,mes3):
    """
    dset
    mes1
    mes2
    mes3
    """
    dset=dset["precip"][59:455,:,:]
    n1=1
    arr_3D1=np.empty((1,72,144))
    for i in range(0,len(dset["time"])):
        if (str(dset[i,:,:]["time"].values)[5:7]==mes1):
            variable_data1=[dset[i,:,:].values]
            arr_3D1=np.concatenate([arr_3D1,variable_data1])
            n1=n1+1
            arr_3D1=np.reshape(arr_3D1,(n1,72,144))
    arr_3D1=arr_3D1[1:np.shape(arr_3D1)[0],:,:]
    
    n2=1
    arr_3D2=np.empty((1,72,144))
    for i in range(0,len(dset["time"])):
        if (str(dset[i,:,:]["time"].values)[5:7]==mes2):
            variable_data2=[dset[i,:,:].values]
            arr_3D2=np.concatenate([arr_3D2,variable_data2])
            n2=n2+1
            arr_3D2=np.reshape(arr_3D2,(n2,72,144))
    arr_3D2=arr_3D2[1:np.shape(arr_3D2)[0],:,:]
    
    n3=1
    arr_3D3=np.empty((1,72,144))
    for i in range(0,len(dset["time"])):
        if (str(dset[i,:,:]["time"].values)[5:7]==mes3):
            variable_data3=[dset[i,:,:].values]
            arr_3D3=np.concatenate([arr_3D3,variable_data3])
            n3=n3+1
            arr_3D3=np.reshape(arr_3D3,(n3,72,144))
    arr_3D3=arr_3D3[1:np.shape(arr_3D3)[0],:,:]
    
    arr_3D_3meses=np.concatenate([arr_3D1,arr_3D2,arr_3D3])
    media_trimestral=np.nanmean(arr_3D_3meses,axis=0)
    desvio_trimestral=np.nanstd(arr_3D_3meses,axis=0)
    
    #cargo lats y lons para armar xarrays
    lats=dset.mean("time", keep_attrs=True)["lat"][:].values
    lons=dset.mean("time", keep_attrs=True)["lon"][:].values
    coords=[("lat", lats),("lon", lons)]
    
    #xarray media
    xarray_media=xr.DataArray(media_trimestral, coords=coords)
    xarray_media.name="precip media trimestral "+ mes1+"-"+mes2+"-"+mes3
    xarray_media.attrs['units']=dset.attrs["units"]
    xarray_media.attrs['meses']=[mes1,mes2,mes3]
    
    #xarray media
    xarray_desvio=xr.DataArray(desvio_trimestral, coords=coords)
    xarray_desvio.name="precip desvio trimestral "+ mes1+"-"+mes2+"-"+mes3
    xarray_desvio.attrs['units']=dset.attrs["units"]
    xarray_desvio.attrs['meses']=[mes1,mes2,mes3]
    
    return([xarray_media,xarray_desvio])

#armo lista con medias trimestrales
media_trimestral_list=[None]*4
media_trimestral_list[0]=media_desvio_trimestral(dset,"03","04","05")[0]
media_trimestral_list[1]=media_desvio_trimestral(dset,"06","07","08")[0]
media_trimestral_list[2]=media_desvio_trimestral(dset,"09","10","11")[0]
media_trimestral_list[3]=media_desvio_trimestral(dset,"12","01","02")[0]

#armo lista con desvios trimestrales
desvio_trimestral_list=[None]*4
desvio_trimestral_list[0]=media_desvio_trimestral(dset,"03","04","05")[1]
desvio_trimestral_list[1]=media_desvio_trimestral(dset,"06","07","08")[1]
desvio_trimestral_list[2]=media_desvio_trimestral(dset,"09","10","11")[1]
desvio_trimestral_list[3]=media_desvio_trimestral(dset,"12","01","02")[1]


#%%
"""
Defino funcion que grafica climatologia mensual de alguna variable definida previamente en una determinada region (region cuadrada)
"""
#carga librerias necesarias
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean

def grafico_campos_climatologia(paises,provincias,data_list_climatologia,indice_list,variable,climatologia_tipo,lat_min,lat_max,lon_min,lon_max,unidades_nombre,valor_minimo, valor_maximo, delta_valor,xticks_min,xticks_max, yticks_min, yticks_max,grid,region, ruta_salida, paleta_color,espacio_entre_lat_lon,orientacion):
    """
    Parameters
    ----------
    paises : shapely.geometry.multipolygon.MultiPolygon
        shape con paises a graficar en mapa
    provincias : shapely.geometry.multipolygon.MultiPolygon
        shape con provincias a graficar en mapa
    data_list_climatologia : list
        lista con data climatologica, en cada elemento de la lista hay un NetCDF i.e un xarray.core.dataset.Dataset
    indice_list : float
        indice del elemento de la lista a abrir
    variable : string
        nombre de la variable de los NetCDF a graficar
    climatologia_tipo: string
        "mensual" o "trimestral" 
    lat_min : float
        latitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lat_max : float
        latitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lon_min : float
        longitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    lon_max : float
        longitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    unidades_nombre : string
        nombre que se desea para las unidades de la variable, aparece en el grafico
    valor_minimo : float
        valor minimo que toma la escala de la variable
    valor_maximo : float
        valor maximo que toma la escala de la variable
    delta_valor : float
        intervalo entre valores de la escala de la variable
    xticks_min : float
        minimo de longitud que se marca en el grafico en grados oeste con el signo -
    xticks_max : float
        maximo de longitud que se marca en el grafico en grados oeste con el signo -
    yticks_min : float
        minimo de latitud que se marca en el grafico en grados sur con el signo -.
    yticks_max : float
        maximo de latitud que se marca en el grafico en grados sur con el signo -.
    grid : optional
        The default is True.
    region: string
        Nombre de la region
    ruta_salida : str
        Ruta donde se guardan los graficos
    paleta_color: rain (de cero a positivos) / curl (para negativos y positivos) /matter (de cero a positivos en rosas)
    espacio_entre_lat_lon: float
        4 para region chica (menos separacion), 8 para region grande (mas separacion)
    orientacion: str
        "H": horizontal "V": vertical
    Returns
    -------
    Guarda graficos y los muestra.

    """
    #carga librerias necesarias
    #import matplotlib.pyplot as plt
    #import cartopy.crs as ccrs
    #import cmocean
    
    #limpio graficos
    plt.close()
    
    #selecciona variable
    variable_data=data_list_climatologia[indice_list]
    #variable_data=data[variable].mean("time", keep_attrs=True) #selecciona variable y toma el unico valor para cada punto de grilla
    variable_data.attrs["units"]=unidades_nombre #cambio el nombre de la unidad

    #selecciono region
    lats=variable_data["lat"][:]
    lons=variable_data["lon"][:]
    lat_lims=[lat_min,lat_max]
    lon_lims=[360+lon_min,360+lon_max] #lean 360-64 (64 O) 360-31 (31 O) 
    lat_inds=np.where((lats>lat_lims[0]) & (lats<lat_lims[1]))[0]
    lon_inds=np.where((lons>lon_lims[0]) & (lons<lon_lims[1]))[0]
    variable_data_subset=variable_data[lat_inds,lon_inds]

    #extraigo mes (climatologia mensual) o meses (climatologia trimestral)
    if (climatologia_tipo=="mensual"):
        meses=str(data_list_climatologia[indice_list].name)[-2]+str(data_list_climatologia[indice_list].name)[-1]
        if (meses=="01"):
            mes="Enero"
        if (meses=="02"):
            mes="Febrero"
        if (meses=="03"):
            mes="Marzo"
        if (meses=="04"):
            mes="Abril"
        if (meses=="05"):
            mes="Mayo"
        if (meses=="06"):
            mes="Junio"
        if (meses=="07"):
            mes="Julio"
        if (meses=="08"):
            mes="Agosto"
        if (meses=="09"):
            mes="Septiembre"
        if (meses=="10"):
            mes="Octubre"
        if (meses=="11"):
            mes="Noviembre"
        if (meses=="12"):
            mes="Diciembre"
            
    if (climatologia_tipo=="trimestral"):
        meses=str(data_list_climatologia[indice_list].name)[-8:-1]+str(data_list_climatologia[indice_list].name)[-1]
        if (meses=="03-04-05"):
            mes="MAM"
        if (meses=="06-07-08"):
            mes="JJA"
        if (meses=="09-10-11"):
            mes="SON"
        if (meses=="12-01-02"):
            mes="DEF"
            
    #ploteo
    if (orientacion=="H"):
        fig1 = plt.figure(figsize=[9,5],dpi=200) #horizontal region 1
    if (orientacion=="V"):
        fig1 = plt.figure(figsize=[7.5,7.5],dpi=200) #vertical sudamerica
    ax = fig1.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=0))

    if (paleta_color=="rain"):
        variable_data_subset.plot.contourf(ax=ax,
                   levels=np.arange(valor_minimo, valor_maximo, delta_valor),
                   extend='neither',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': variable_data_subset.units},
                   cmap=cmocean.cm.rain)
    
    if (paleta_color=="curl"):
        variable_data_subset.plot.contourf(ax=ax,
                   levels=np.arange(valor_minimo, valor_maximo, delta_valor),
                   extend='neither',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': variable_data_subset.units},
                   cmap=cmocean.cm.curl_r)

    if (paleta_color=="matter"):
        variable_data_subset.plot.contourf(ax=ax,
                   levels=np.arange(valor_minimo, valor_maximo, delta_valor),
                   extend='neither',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': variable_data_subset.units},
                   cmap=cmocean.cm.matter)
    
    if (paleta_color=="ice"):
        variable_data_subset.plot.contourf(ax=ax,
                   levels=np.arange(valor_minimo, valor_maximo, delta_valor),
                   extend='neither',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': variable_data_subset.units},
                   cmap=cmocean.cm.ice_r)
    
        #######ver estas lineas###############
    #facecolors = np.ma.array(variable_data_subset, mask=np.isnan(variable_data_subset))
    #ax.set_array(facecolors)
        #######ver estas lineas###############
    ax.add_geometries(provincias, crs=ccrs.PlateCarree(), facecolor='none', 
                  edgecolor='0.5',linewidth=0.7,alpha=0.8)

    ax.add_geometries(paises, crs=ccrs.PlateCarree(), facecolor='none', 
                  edgecolor='0.4',alpha=0.8)

    ax.coastlines(color='0.3')

    ax.set_xticklabels(np.arange(xticks_min,xticks_max)[::espacio_entre_lat_lon])
    plt.xticks(np.arange(xticks_min,xticks_max)[::espacio_entre_lat_lon])
    ax.set_xlabel("Longitud")

    ax.set_yticklabels(np.arange(yticks_min,yticks_max)[::espacio_entre_lat_lon])
    plt.yticks(np.arange(yticks_min,yticks_max)[::espacio_entre_lat_lon])
    ax.set_ylabel("Latitud")

    if (grid==True):
        plt.grid(linestyle="--", alpha=0.3)

    plt.title(variable+" "+region+" "+mes)
    #plt.tight_layout()
    plt.savefig(ruta_salida+"/"+variable+" "+region+" "+mes)
    plt.show()
    
#%%
"""
Grafico climatologias
"""

import numpy as np

#cargo shape con paises
from shapely.geometry.multipolygon import MultiPolygon
from cartopy.io import shapereader
import geopandas

resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'
shpfilename = shapereader.natural_earth(resolution, category, name) #cargo paises de natural_earth
# cargo el shapefile usando geopandas
df = geopandas.read_file(shpfilename)
# leo los paises que voy a necesitar
paises=MultiPolygon([df.loc[df['ADMIN'] == 'Argentina']['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == 'Brazil']['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == 'Paraguay']['geometry'].values[0],
                     df.loc[df['ADMIN'] == 'Uruguay']['geometry'].values[0],
                     df.loc[df['ADMIN'] == 'Bolivia']['geometry'].values[0],
                     df.loc[df['ADMIN'] == 'Chile']['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Colombia"]['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Ecuador"]['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Venezuela"]['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Guyana"]['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Suriname"]['geometry'].values[0],
                     df.loc[df['ADMIN'] == "Panama"]['geometry'].values[0][0],
                     df.loc[df['ADMIN'] == "Costa Rica"]['geometry'].values[0][0]]) #los paso a multipolygon para poder graficarlos

#cargo shape con provincias de argentina con datos del IGN 
#descargo los datos de aca: https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG "Provincia"
IGN=geopandas.read_file("/home/nadia/Documentos/Doctorado/datos/mapas/provincia/provincia.shp")
provincias=[None]*24
for i in range(0,24):
    provincias[i]=IGN["geometry"][i]
provincias=MultiPolygon(provincias) #paso a multipolygon para poder ponerlo en mapa

#%%
#ploteo para sudamerica 
for i in range(0,12):
    grafico_campos_climatologia(paises,provincias,media_mensual_list,i,"precipitacion media mensual (1984-2016)","mensual",-60,15,-90,-30,"mm/día",0,20,2,-85,-30,-55,15,True,"Sudamérica","/home/nadia/Documentos/Doctorado/resultados/resultados2021/precipitacion/cmap_climatologia","ice",8,"V")


for i in range(0,12):
    grafico_campos_climatologia(paises,provincias,desvio_mensual_list,i,"precipitacion desvío estándar mensual (1984-2016)","mensual",-60,15,-90,-30,"mm/día",0,10,1,-85,-30,-55,15,True,"Sudamérica","/home/nadia/Documentos/Doctorado/resultados/resultados2021/precipitacion/cmap_climatologia","matter",8,"V")


for i in range(0,4):
    grafico_campos_climatologia(paises,provincias,media_trimestral_list,i,"precipitacion media trimestral (1984-2016)","trimestral",-60,15,-90,-30,"mm/día",0,20,2,-85,-30,-55,15,True,"Sudamérica","/home/nadia/Documentos/Doctorado/resultados/resultados2021/precipitacion/cmap_climatologia","ice",8,"V")

for i in range(0,4):
    grafico_campos_climatologia(paises,provincias,desvio_trimestral_list,i,"precipitacion desvío estándar trimestral (1984-2016)","trimestral",-60,15,-90,-30,"mm/día",0,10,1,-85,-30,-55,15,True,"Sudamérica","/home/nadia/Documentos/Doctorado/resultados/resultados2021/precipitacion/cmap_climatologia","matter",8,"V")

#%% 
"""
calculo la media de precipitacion en determinada region 
grafico una serie temporal de todo el periodo, y por mes
"""
#defino funcion que calcula media mensual de una determinada variable en determinada region

import numpy as np
import pandas as pd

def media_espacial(dset,lat_min,lat_max,lon_min,lon_max,clipped):
    """
    Calcula media mensual de una determinada variable en determinada region

    Parameters
    ----------
    dset:
        netcdf 
    lat_min : float
        latitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lat_max : float
        latitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lon_min : float
        longitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    lon_max : float
        longitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    clipped: True or False
        True: la entrada es la lista de la variable clipeada
        False: la entrada es la lista sin clipear
    Returns float
    -------
    media espacial de la variable seleccionada en la region seleccionada
    """
    
    
    
    if (clipped==False):
        variable_data=dset["precip"][:,:,:].values #selecciona variable y toma el unico valor para cada punto de grilla
        #selecciono region
        lats=dset["lat"][:]
        lons=dset["lon"][:]
        lat_lims=[lat_min,lat_max]
        lon_lims=[360+lon_min,360+lon_max] #lean 360-64 (64 O) 360-31 (31 O) 
        lat_inds=np.where((lats>lat_lims[0]) & (lats<lat_lims[1]))[0]
        lon_inds=np.where((lons>lon_lims[0]) & (lons<lon_lims[1]))[0]
        variable_data_subset=variable_data[:,lat_inds,:][:,:,lon_inds]
        
    if (clipped==True):
        variable_data=dset["precip"][:,:,:].values
        #selecciono region
        lats=variable_data["y"][:]
        lons=variable_data["x"][:]
        lat_lims=[lat_min,lat_max]
        lon_lims=[360+lon_min,360+lon_max] #lean 360-64 (64 O) 360-31 (31 O) 
        lat_inds=np.where((lats>lat_lims[0]) & (lats<lat_lims[1]))[0]
        lon_inds=np.where((lons>lon_lims[0]) & (lons<lon_lims[1]))[0]
        variable_data_subset=variable_data[:,lat_inds,:][:,:,lon_inds]
    
    #calculo media espacial del subset de la variable data
    media_espacial=np.nanmean(variable_data_subset,axis=(1,2))
    return(media_espacial)


#armo funcion que devuelve data frame donde primera columna sea la fecha y la segunda columna sea la media espacial
def media_espacial_df(dset,lat_min,lat_max,lon_min,lon_max,clipped):
    """
    

    Parameters
    ----------
    dset:
        netcdf
    lat_min : float
        latitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lat_max : float
        latitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado
    lon_min : float
        longitud minima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    lon_max : float
        longitud maxima a seleccionar de las variables, obs: van con decimales 0.5 y cada 1 grado, usar grados oeste con su signo -
    clipped: True or False
        True: la entrada es la lista de la variable clipeada
        False: la entrada es la lista sin clipear

    Returns
    -------
    Data frame con primer columna fecha segunda columna la media espacial de la variable elegida para esa fecha

    """
    media_espacial_df=pd.DataFrame(columns=["fecha","Media_espacial_precip"])
    if (clipped==False):
        for i in range(0,len(dset["time"])):
            #extraigo mes
            mes=str(dset["time"].values[i])[5:7]
            #extraigo anio
            anio=str(dset["time"].values[i])[0:4]
            #¢alculo media
            media_espacial_i=media_espacial(dset,lat_min,lat_max,lon_min,lon_max,False)[i]
            media_espacial_df=media_espacial_df.append({"fecha": mes+"-"+anio, "Media_espacial_precip": media_espacial_i},ignore_index=True)
    
    if (clipped==True):
        for i in range(0,len(dset["time"])):
            #extraigo mes
            mes=str(dset["time"].values[i])[-5:-3] #hay que ver como cambia el dset, en la funcion de arriba tambien 
            #extraigo anio
            anio=str(dset["time"].values[i])[-10:-6]
            #¢alculo media
            media_espacial_i=media_espacial(dset,lat_min,lat_max,lon_min,lon_max,True)[i]
            media_espacial_df=media_espacial_df.append({"fecha": mes+"-"+anio, "Media_espacial_precip": media_espacial_i},ignore_index=True)
            
    media_espacial_df["fecha"]=pd.to_datetime(media_espacial_df["fecha"])
    return(media_espacial_df)

precip_media_espacial_df_sudamerica=media_espacial_df(dset,-60,15,-90,-30,False)
precip_media_espacial_df_region1=media_espacial_df(dset,-39,-16,-64,-31,False)
precip_media_espacial_df_region2=media_espacial_df(dset,-32,-22,-64,-53,False)
#precip_media_espacial_df_corrientes=media_espacial_df(dset,-32,-22,-64,-53,True)

precip_media_espacial_df_sudamerica.to_csv("/home/nadia/Documentos/Doctorado/datos/precipitacion/cmap_enh_precip_mon_mean/precip_media_espacial_df_sudamerica.csv")
precip_media_espacial_df_region1.to_csv("/home/nadia/Documentos/Doctorado/datos/precipitacion/cmap_enh_precip_mon_mean/precip_media_espacial_df_region1.csv")
precip_media_espacial_df_region2.to_csv("/home/nadia/Documentos/Doctorado/datos/precipitacion/cmap_enh_precip_mon_mean/precip_media_espacial_df_region2.csv")

#%%
"""
grafico la serie temporal para precip
"""
#anual
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk

def serie_periodo_completo(data_frame_entrada,region,ruta_salida):
    fig1, ax = plt.subplots(figsize=[10,6],dpi=200)
    plt.plot(data_frame_entrada["fecha"],data_frame_entrada["Media_espacial_precip"],color="k",alpha=0.7)
    
    #agrego lineas de tendencia, si es significativa con un 95% (test mann kendall) lo hago con linea llena y si no con linea intermitente
    coef1 = np.polyfit(np.arange(0,len(data_frame_entrada["fecha"]),1),np.array(data_frame_entrada["Media_espacial_precip"]),1)
    linear_fit_1=np.poly1d(coef1) 
    if (abs(mk.original_test(data_frame_entrada["Media_espacial_precip"], alpha=0.05)[3])>1.96):
        plt.plot(data_frame_entrada["fecha"],linear_fit_1(np.arange(0,len(data_frame_entrada["fecha"]),1)),color="k",ls="-")
    else:
        plt.plot(data_frame_entrada["fecha"],linear_fit_1(np.arange(0,len(data_frame_entrada["fecha"]),1)),color="k",ls=":")

    media1=np.round(np.nanmean(data_frame_entrada["Media_espacial_precip"]),1)
    desvio1=np.round(np.nanstd(data_frame_entrada["Media_espacial_precip"]),2)
    tendencia1=np.round(coef1[0]*12*10,2) #decadal

    plt.text(8000,8,"Media (mm/día) \nDesvío (mm/día) \nTendencia decadal (mm/día/dec)",color="k",ha="left",backgroundcolor="white")
    plt.text(12500,8,str(media1)+" \n"+str(desvio1)+" \n"+ str(tendencia1),color="k",ha="left",backgroundcolor="white")
    
    ax.tick_params(axis='x',direction='out',bottom=True,labelrotation=25, labelsize=10,pad=1.5)
    ax.set_ylim(0,10)
    #plt.xticks(data_frame_entrada_cldamt["fecha"][::24])
    ax.set_xlabel("Fecha", size=10)
    ax.set_ylabel("Precipitación mm/día", size=10)
    ax.grid()
    plt.title("Precipitación media mensual media "+region+ " (serie completa)")
    nombre="precipitacion_media_espacial_mensual_"+region+"_"+"(serie completa)"
    plt.savefig(ruta_salida+nombre, dpi=140)
    plt.show


#%%
#lo corro
ruta_salida="/home/nadia/Documentos/Doctorado/resultados/resultados2021/precipitacion/cmap_series"
serie_periodo_completo(precip_media_espacial_df_sudamerica,"Sudamérica",ruta_salida)
serie_periodo_completo(precip_media_espacial_df_region1,"Región 1",ruta_salida)
serie_periodo_completo(precip_media_espacial_df_region2,"Región 2",ruta_salida)

#%% 
#veo con cldamt

cldamt_media_espacial_df_sudamerica=pd.read_csv("Documentos/Doctorado/datos/nubosidad/cldamt_media_espacial_df_sudamerica.csv", index_col=0)
cldamt_media_espacial_df_sudamerica["fecha"]=pd.to_datetime(cldamt_media_espacial_df_sudamerica["fecha"])
cldamt_media_espacial_df_region1=pd.read_csv("Documentos/Doctorado/datos/nubosidad/cldamt_media_espacial_df_region1.csv", index_col=0)
cldamt_media_espacial_df_region1["fecha"]=pd.to_datetime(cldamt_media_espacial_df_region1["fecha"])
cldamt_media_espacial_df_region2=pd.read_csv("Documentos/Doctorado/datos/nubosidad/cldamt_media_espacial_df_region2.csv", index_col=0)
cldamt_media_espacial_df_region2["fecha"]=pd.to_datetime(cldamt_media_espacial_df_region2["fecha"])

