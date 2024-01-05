import numpy as np
import pandas as pd
import datetime as dt
from calendar import monthrange

def f_desvio_mensual_smn(id_omm, df_data, na = 20, nombre_variable = "nub"):
    """ construye serie de media mensual y lo guarda en ruta_salida como .csv
    admite el na% de datos faltantes"""

    data_group=df_data[nombre_variable].groupby(pd.Grouper(freq="M"))
    data_group_desvio=data_group.std() #hace el desvio aunque halla nans, a menos que todo el mes tenga nans
    data_group_faltantes = df_data.isnull().groupby(pd.Grouper(freq="M")).sum()
    data_group_size = data_group.size()
    posiciones_desvios_a_conservar = data_group_faltantes.values <= data_group_size.values * na/100
    # elif na == 
    #me quedo con los meses donde la cantidad de datos faltantes haya sido menor al na% de los datos para el mes
    desvio = []
    for i, elemento in enumerate(data_group_desvio):
        if posiciones_desvios_a_conservar[i][0] == True: # and pd.isna(elemento)!=True:
            desvio.append(elemento) #media.append(round(elemento)) 
        else:
            desvio.append(np.nan)
    indices=data_group_desvio.index
    desvio_mensual_df=pd.DataFrame(desvio, index = indices)
    desvio_mensual_df.index.name = "fecha"
    return desvio_mensual_df
