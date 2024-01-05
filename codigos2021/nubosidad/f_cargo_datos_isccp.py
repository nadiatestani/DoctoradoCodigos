#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:29:45 2021

@author: nadia

f_cargo_datos_isccp.py
"""

#f_cargo_datos_isccp.py

import pandas as pd
import xarray as xr

def cargo_datos_ISCCP():
    """
     Carga datos ISCCP y los acomoda en una lista: cada elemento de la lista es el campo de una fecha

    """
    #armo lista de nombres
    datelist = pd.date_range(start="1983-07-15",end="2017-07-15",freq="M")
    nc_name_list=[]
    for date in datelist:
        nc_name_list.append("ISCCP-Basic.HGM.v01r00.GLOBAL."+str(date)[0:4]+"."+str(date)[5:7]+".99.9999.GPC.10KM.CS00.EA1.00.nc")
    
    #cargo ruta
    nc_ruta="../../../datos/nubosidad/ISCCP-H_HGM"
    
    #cargo datos en lista. Cada elemento es un array con los datos, recorto la region que voy a trabjaar y las variables que voy a usar.
    data_list=[]
    for name in nc_name_list:
        data=xr.open_dataset(nc_ruta+"/"+name)[["cldamt","cldamt_types"]]
        data=data.loc[dict(lon=slice(270, 331),lat=slice(-61,16))]
        data_list.append(data)
    
    return data_list 