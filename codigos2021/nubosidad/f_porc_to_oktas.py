#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 07:07:16 2021

@author: nadia

f_porc_to_oktas.py
"""

#f_porc_to_oktas.py

import pandas as pd
import datetime
from f_serie_en_puntos_xarray import serie_cldamt_un_punto

def porc_to_oktas(list_porc):
    list_oktas=[]
    for elemento in list_porc:
        if elemento == 0:
            list_oktas.append(0)
        elif elemento > 0 and elemento < 18.75:
            list_oktas.append(1)
        elif elemento >= 18.75 and elemento < 31.25:
            list_oktas.append(2)
        elif elemento >= 31.25 and elemento < 43.75:
            list_oktas.append(3)
        elif elemento >= 43.75 and elemento < 56.25:
            list_oktas.append(4)
        elif elemento >= 56.25 and elemento < 68.75:
            list_oktas.append(5)
        elif elemento >= 68.75 and elemento < 81.25:
            list_oktas.append(6)
        elif elemento >= 81.25 and elemento < 100:
            list_oktas.append(7)
        else:
            list_oktas.append(8)
    return list_oktas

def data_frame_oktas(data, lon, lat):
    """
    Arma data_frame con series de cldamt % y oktas para un punto de lon y lat

    """
    if type(data)==list:
        cldamt_punto = serie_cldamt_un_punto(data, lon = lon, lat = lat) #10489 lon = 300.5, lat = -27.5
    else:
        cldamt_punto = data.loc[dict(lon=lon, lat=lat)]["cldamt"].values
    cldamt_punto_oktas = porc_to_oktas(cldamt_punto)
    if type(data)==list:
        fechas = [datetime.datetime.strptime(str(data.cldamt.time.values[0]), "%Y-%m-%dT00:00:00.000000000") for datos in data_list]
    else:
        fechas = [datetime.datetime.strptime(str(fecha), "%Y-%m-%dT%H:%M:00.000000000") for fecha in data.cldamt.time.values]
    data_frame_cldamt_punto=pd.DataFrame([fechas, cldamt_punto, cldamt_punto_oktas]).T
    data_frame_cldamt_punto.columns = ["fecha","cldamt","cldamt_oktas"]
    data_frame_cldamt_punto.set_index(keys = "fecha", drop = True, inplace = True)
    return data_frame_cldamt_punto
