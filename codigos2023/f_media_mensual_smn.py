import numpy as np
import pandas as pd
import datetime as dt
from calendar import monthrange

def f_media_mensual_smn(id_omm, df_data, na = 20, nombre_variable = "nub"):
    """ construye serie de media mensual y lo guarda en ruta_salida como .csv
    admite el na% de datos faltantes"""

    data_group=df_data[nombre_variable].groupby(pd.Grouper(freq="M"))
    data_group_media=data_group.mean() #hace la media aunque halla nans, a menos que todo el mes tenga nans
    data_group_faltantes = df_data.isnull().groupby(pd.Grouper(freq="M")).sum() #agregue [nombre_variable]
    data_group_size = data_group.size()
    posiciones_medias_a_conservar = data_group_faltantes.values <= data_group_size.values * na/100
    # elif na == 
    #me quedo con los meses donde la cantidad de datos faltantes haya sido menor al na% de los datos para el mes
    media = []
    for i, elemento in enumerate(data_group_media):
        if posiciones_medias_a_conservar[i][0] == True: # and pd.isna(elemento)!=True:
            media.append(elemento) #media.append(round(elemento)) 
        else:
            media.append(np.nan)
    indices=data_group_media.index
    media_mensual_df=pd.DataFrame(media, index = indices)
    media_mensual_df.index.name = "fecha"
    return media_mensual_df
