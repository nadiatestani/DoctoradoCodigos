import numpy as np
import pandas as pd
import datetime as dt
from calendar import monthrange

def f_serie_anomalias_mensuales(frecuencia_relativa_mensual, frecuencia_relativa_mensual_climatologia):
    frecuencia_relativa_anomalia = frecuencia_relativa_mensual.copy()
    for fecha in frecuencia_relativa_anomalia.index:
        for mes in frecuencia_relativa_anomalia.index.month.unique():
            if fecha.month == mes:
                frecuencia_relativa_anomalia.loc[fecha] = frecuencia_relativa_mensual.loc[fecha]-frecuencia_relativa_mensual_climatologia.loc[mes]
    return frecuencia_relativa_anomalia