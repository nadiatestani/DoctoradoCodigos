#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:51:25 2021

@author: nadia

f_abrir_datos_smn.py
"""

#f_abrir_datos_smn.py

import pandas as pd
import os


def abrir_datos_smn(ruta_a_archivos, nombre_archivo, variable): 
    """
    Abre datos de SMN de la variable seleccionada 

    Returns
    -------
    df_data : pd.DataFrame
        index =  fecha
        columns=["variable"]

    """
    data = pd.read_csv(os.path.join(ruta_a_archivos,nombre_archivo), sep="\t", index_col = ["fecha"], parse_dates = True, usecols = ["fecha", variable], na_values = r"\N")     
    id_estacion = pd.read_csv(os.path.join(ruta_a_archivos,nombre_archivo), sep="\t") ["omm_id"].unique()[0]
    return(id_estacion, data)