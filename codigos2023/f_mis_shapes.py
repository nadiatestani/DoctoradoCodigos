#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:09:24 2021

@author: nadia

f_mis_shapes.py
"""

#f_mis_shapes.py

from cartopy.io import shapereader
from shapely.geometry.multipolygon import MultiPolygon
import geopandas as gpd

def df_paises():
    """
    cargo shape con paises de sudamerica

    """
    df_paises = gpd.read_file(shapereader.natural_earth('10m', 'cultural', 'admin_0_countries')) # cargo paises de natural_earth con geopandas
    paises = MultiPolygon([df_paises.loc[df_paises['ADMIN'] == 'Argentina']['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == 'Brazil']['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == 'Paraguay']['geometry'].values[0],
                           df_paises.loc[df_paises['ADMIN'] == 'Uruguay']['geometry'].values[0],
                           df_paises.loc[df_paises['ADMIN'] == 'Bolivia']['geometry'].values[0],
                           df_paises.loc[df_paises['ADMIN'] == 'Chile']['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == "Colombia"]['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == "Ecuador"]['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] ==
                                  "Venezuela"]['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == "Guyana"]['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == "Suriname"]['geometry'].values[0],
                           df_paises.loc[df_paises['ADMIN'] == "Panama"]['geometry'].values[0][0],
                           df_paises.loc[df_paises['ADMIN'] == "Costa Rica"]['geometry'].values[0][0]])  # los paso a multipolygon para poder graficarlos
    return paises

def df_provincias():
    """cargo shape con provincias de argentina con datos del IGN
        descargo los datos de aca: https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG "Provincia"
        devuelvo los shapes de las provincias de argentina"""
    #si estoy trabajando desde servidor
    IGN = gpd.read_file("/pikachu/datos/nadia.testani/Doctorado/datos/mapas/provincia/provincia.shp")
    #si estoy desde la pc
    #IGN = gpd.read_file("../../../datos/mapas/provincia/provincia.shp")
    provincias = MultiPolygon([IGN["geometry"][i] for i in range(0, 24)]) # paso a multipolygon para poder ponerlo en mapa
    return provincias


