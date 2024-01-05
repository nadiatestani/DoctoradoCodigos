#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:19:27 2021

@author: nadia

f_puntos_cercanos.py
"""

#f_puntos_cercanos.py

import numpy as np

def puntos_cercanos(ID_estacion, dict_puntos_smn, lista_puntos_satelital, cantidad_puntos):
    """
    Genera lista con cantidad_puntos tuplas de (lon, lat) mas cercanos a estacion ID_estacion
    
    ID_estacion: ID OMM
    dict_puntos_smn: {estacion: (lon_smn, lat_smn)}
    lista_puntos_satelital: make_grid(lons_satelital, lats_satelital)
    cantidad_puntos: numero de puntos cercanos a estacion que se quieren obtener
    
    Salida: [(lon_sat, lat_sat),...] #donde lon_sat lat_sat son los mas cercanos a punto de estacion ID_estacion
    """

    lon_estacion = dict_puntos_smn[ID_estacion][0]
    lat_estacion = dict_puntos_smn[ID_estacion][1]

    distancia_a_estacion = {punto_sat : np.sqrt ((punto_sat[0]-lon_estacion)**2 + (punto_sat[1]-lat_estacion)**2) for punto_sat in lista_puntos_satelital}
    #lo ordeno
    distancia_a_estacion = {k: v for k, v in sorted(distancia_a_estacion.items(), key=lambda item: item[1])}
    puntos_distancia = list(distancia_a_estacion)[:cantidad_puntos] #tomo los mas cercanos
    return puntos_distancia
