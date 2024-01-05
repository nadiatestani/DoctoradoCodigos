#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 07:04:43 2021

@author: nadia

f_serie_en_puntos_xarrays.py
"""

#f_serie_en_puntos_xarray.py

import numpy as np

def serie_cldamt_un_punto(data_list, lon, lat):
    lon_index = np.where(data_list[0].cldamt.lon.values == lon)[0][0] 
    lat_index = np.where(data_list[0].cldamt.lat.values == lat)[0][0] 
    cldamt_lista=[float(data.cldamt[dict(lon=lon_index, lat=lat_index)][0].values) for data in data_list]
    return(cldamt_lista)
