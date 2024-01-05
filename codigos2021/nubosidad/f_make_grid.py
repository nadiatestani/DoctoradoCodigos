#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 09:12:43 2021

@author: nadia

f_make_grid.py 
"""

#f_make_grid.py
def make_grid(lons_list, lats_list):
    """ Recibe lista de longitudes y latitudes 
    Devuelve lista de tuplas con las coordenadas de los puntos de la grilla que se forma con ellas"""
    lons_reshape = lons_list * len(lats_list)
    lons_reshape.sort()
    lats_reshape = lats_list * len(lons_list)
    lista_puntos = [(lon, lat) for lon, lat in zip(lons_reshape,lats_reshape)]
    return lista_puntos
