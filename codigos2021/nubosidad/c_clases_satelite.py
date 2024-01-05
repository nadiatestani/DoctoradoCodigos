#c_clases_satelite.py

import numpy as np
import pandas as pd
import datetime as dt

from f_procesamiento_satelite import frecuencia_oktas_por_anio

class dataframe_satelite():
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.serie = None
        
    def genero_serie(self, nombre_columna, fecha_inicio, fecha_final):
        """ fecha_inicio y fecha_final: str yyyy-mm-dd """
        self.serie = self.dataframe[fecha_inicio:fecha_final][nombre_columna]
        self.serie = serie_satelite(self.serie)
        return self.serie
    
    def calculo_frecuencia_anual(self, id_omm, ruta_salida):
        """ calculo la frecuencia anual de la serie de nubosidad """
        frecuencia = frecuencia_oktas_por_anio(lon, lat, self.dataframe, ruta_salida) #ver como hago con ese self.dataframe
        return frecuencia
    
class serie_satelite():
    
    def __init__(self, serie):
        self.serie = serie 
        self.datos_faltantes = None
        self.paso_temporal = None
        
    def calculo_datos_faltantes(self):
        """ calcula datos faltantes de serie """
        datos_faltantes = float(np.sum(pd.isna(self.serie)))
        datos_total = len(self.serie)
        self.datos_faltantes = round(datos_faltantes/datos_total * 100, 3)
        return self.datos_faltantes
    
    def es_diario(self):
        """ calcula paso temporal de la serie y veo si es diario """
        return self.serie.index[1]-self.serie.index[0] == dt.timedelta(1)

    def paso_hora_a_cero(self):
        """ si el index no esta centrado en hora 00:00 lo puedo pasar con esto """
        self.serie.index = self.serie.index.to_period("D")
        return self.serie
    
    def paso_mes_a_uno(self):
        """ si el index esta centrado en un dia lo puedo pasar a dia uno con esto """
        self.serie.index = self.serie.index.to_period("M")
        return self.serie
        
class frecuencias_oktas():
    
    def __init__(self, df_frecuencias):
        self.df_frecuencias = df_frecuencias
        self.df_indexado = None
        
    def selecciono_fechas(self, fecha_inicio, fecha_final):
        self.df_indexado =  self.df_frecuencias.loc[fecha_inicio:fecha_final]
        return self.df_indexado
    
    def es_diario(self):
        return sum(self.df_frecuencias.iloc[1]) > 12
    