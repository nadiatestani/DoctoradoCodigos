import numpy as np
import pandas as pd
import pymannkendall as mk
import scipy

def f_serie_anomalias_mensuales(frecuencia_relativa_mensual, frecuencia_relativa_mensual_climatologia):
    frecuencia_relativa_anomalia = frecuencia_relativa_mensual.copy()
    for fecha in frecuencia_relativa_anomalia.index:
        for mes in frecuencia_relativa_anomalia.index.month.unique():
            if fecha.month == mes:
                frecuencia_relativa_anomalia.loc[fecha] = frecuencia_relativa_mensual.loc[fecha]-frecuencia_relativa_mensual_climatologia.loc[mes]
    return frecuencia_relativa_anomalia

def promedio_movil(serie, ventana):
    lista_salida = [None] * len(serie)
    for i in range(0, len(serie) - ventana):
        lista_salida [i + int(ventana / 2)] = np.nanmean(serie[i:i + ventana])      
    return(lista_salida)

#agrego tendencias

#tendencia lineal por cuadrados minimos
def tendencia(serie):
    valores = serie.values[np.isfinite(serie.values)]
    fechas = np.arange(0, len(serie), 1)[np.isfinite(serie.values)]
    
    # si el vector es todo de nan entonces que no calcule la tendencia, y que devuelva nan
    if valores.size <= 1:
        tendencia = np.nan
        significativo = np.nan
        
    # si el vector tiene valores distintos de nan calcula tendencia y significancia
    elif valores.size > 1:
        coef = np.polyfit(fechas, valores, 1)
        tendencia = coef[0]  # dada entre un intervalo de tiempo. A esta salida si quiero tendencia decadal e ingrese datos de toda la serie mensual lo multiplico por 10*12 y si quiero por decada y vienen dados por un dato anual se multiplica por 10
        coord_origen = coef[1]
        z_test = mk.original_test(valores, alpha = 0.05)[3]
        if abs(z_test) >= 1.96:
            significativo = True
        elif abs(z_test) < 1.96:
            significativo = False
    return(coord_origen, tendencia, significativo)

#agrego tendencias
#tendencia lineal por metodo theil-sen
def tendencia_theil_sen(serie):
    
    valores = serie.values[np.isfinite(serie.values)]
    fechas = np.arange(0, len(serie), 1)[np.isfinite(serie.values)]
    
    # si el vector es todo de nan entonces que no calcule la tendencia, y que devuelva nan
    if valores.size <= 1:
        tendencia = np.nan
        significativo = np.nan
        
    # si el vector tiene valores distintos de nan calcula tendencia y significancia
    elif valores.size > 1:
        coef = scipy.stats.mstats.theilslopes(y=valores, x=fechas, alpha=0.95)
        tendencia = coef[0]  # dada entre un intervalo de tiempo. A esta salida si quiero tendencia decadal e ingrese datos de toda la serie mensual lo multiplico por 10*12 y si quiero por decada y vienen dados por un dato anual se multiplica por 10
        coord_origen = coef[1]
        z_test = mk.original_test(valores, alpha = 0.05)[3]
        if abs(z_test) >= 1.96:
            significativo = True
        elif abs(z_test) < 1.96:
            significativo = False
    return(coord_origen, tendencia, significativo)

def f_tabla_tendencias_agrupo(frecuencias_relativas_anomalias,fecha_inicio_str, fecha_final_str, estaciones_ordenadas, ides_omm_ordenado):
    numRows = len(ides_omm_ordenado)
    numCols = 5

    tabla_tendencias = pd.DataFrame(index=range(numRows),columns=range(numCols))
    tabla_tendencias_significativas = pd.DataFrame(index=range(numRows),columns=range(numCols))
    for j, id_omm in enumerate(ides_omm_ordenado):

        frecuencia_relativa_anomalia = frecuencias_relativas_anomalias[id_omm]
        frecuencias = frecuencia_relativa_anomalia.loc[fecha_inicio_str:fecha_final_str]

        #okta 0 
        tendencia_okta_0 = tendencia_theil_sen(frecuencias["0"])
        pendiente_0 = tendencia_okta_0[1]*10*12 #decadal
        significativo_0 = tendencia_okta_0[2]
        tabla_tendencias.iloc[j,0] = round(pendiente_0, 2) #filas, columnas
        tabla_tendencias_significativas.iloc[j,0] = significativo_0

        #oktas 123
        media_123 = (frecuencias["1"]+
                    frecuencias["2"]+
                    frecuencias["3"])
        tendencia_okta_123 = tendencia_theil_sen(media_123)
        pendiente_123 = tendencia_okta_123[1]*10*12 #decadal
        significativo_123 = tendencia_okta_123[2]
        tabla_tendencias.iloc[j,1] = round(pendiente_123, 2) #filas, columnas
        tabla_tendencias_significativas.iloc[j,1] = significativo_123

        #okta 4
        tendencia_okta_4 = tendencia_theil_sen(frecuencias["4"])
        pendiente_4 = tendencia_okta_4[1]*10*12 #decadal
        significativo_4 = tendencia_okta_4[2]
        tabla_tendencias.iloc[j,2] = round(pendiente_4, 2) #filas, columnas
        tabla_tendencias_significativas.iloc[j,2] = significativo_4

        #oktas 567
        media_567 = (frecuencias["5"]+
                    frecuencias["6"]+
                    frecuencias["7"])
        tendencia_okta_567 = tendencia_theil_sen(media_567)
        pendiente_567 = tendencia_okta_567[1]*10*12 #decadal
        significativo_567 = tendencia_okta_567[2]
        tabla_tendencias.iloc[j,3] = round(pendiente_567, 2) #filas, columnas
        tabla_tendencias_significativas.iloc[j,3] = significativo_567

        #okta 8
        tendencia_okta_8 = tendencia_theil_sen(frecuencias["8"])
        pendiente_8 = tendencia_okta_8[1]*10*12 #decadal
        significativo_8 = tendencia_okta_8[2]
        tabla_tendencias.iloc[j,4] = round(pendiente_8, 2) #filas, columnas
        tabla_tendencias_significativas.iloc[j,4] = significativo_8


    tabla_tendencias.index =  list(estaciones_ordenadas.values())
    tabla_tendencias.columns = ["0", "1-2-3", "4", "5-6-7", "8"]
    tabla_tendencias_significativas.index = list(estaciones_ordenadas.values())
    tabla_tendencias_significativas.columns = ["0", "1-2-3", "4", "5-6-7", "8"]
    #guardo
    tabla_tendencias.to_excel(f"tabla_tendencias_agrupo_{fecha_inicio_str}_{fecha_final_str}.xlsx")
    tabla_tendencias_significativas.to_excel(f"tabla_tendencias_significativas_agrupo_{fecha_inicio_str}_{fecha_final_str}.xlsx")
    
    return(print(f"Se generaron tablas de tendencias de oktas agrupadas para el periodo {fecha_inicio_str}_{fecha_final_str}"))

def f_tabla_tendencias_agrupo_por_estacion(frecuencias_relativas_anomalias,fecha_inicio_str, fecha_final_str, estaciones_ordenadas, ides_omm_ordenado):
    
    for estacion in ["DJF", "MAM", "JJA", "SON"]:
        
        numRows = len(ides_omm_ordenado)
        numCols = 5

        tabla_tendencias = pd.DataFrame(index=range(numRows),columns=range(numCols))
        tabla_tendencias_significativas = pd.DataFrame(index=range(numRows),columns=range(numCols))
        
        for j, id_omm in enumerate(ides_omm_ordenado):

            frecuencia_relativa_anomalia = frecuencias_relativas_anomalias[id_omm][estacion]
            frecuencias = frecuencia_relativa_anomalia.loc[fecha_inicio_str:fecha_final_str]

            #okta 0 
            tendencia_okta_0 = tendencia_theil_sen(frecuencias[0])
            pendiente_0 = tendencia_okta_0[1]*10 #decadal
            significativo_0 = tendencia_okta_0[2]
            tabla_tendencias.iloc[j,0] = round(pendiente_0, 2) #filas, columnas
            tabla_tendencias_significativas.iloc[j,0] = significativo_0

            #oktas 123
            media_123 = (frecuencias[1]+
                        frecuencias[2]+
                        frecuencias[3])
            tendencia_okta_123 = tendencia_theil_sen(media_123)
            pendiente_123 = tendencia_okta_123[1]*10 #decadal
            significativo_123 = tendencia_okta_123[2]
            tabla_tendencias.iloc[j,1] = round(pendiente_123, 2) #filas, columnas
            tabla_tendencias_significativas.iloc[j,1] = significativo_123

            #okta 4
            tendencia_okta_4 = tendencia_theil_sen(frecuencias[4])
            pendiente_4 = tendencia_okta_4[1]*10 #decadal
            significativo_4 = tendencia_okta_4[2]
            tabla_tendencias.iloc[j,2] = round(pendiente_4, 2) #filas, columnas
            tabla_tendencias_significativas.iloc[j,2] = significativo_4

            #oktas 567
            media_567 = (frecuencias[5]+
                        frecuencias[6]+
                        frecuencias[7])
            tendencia_okta_567 = tendencia_theil_sen(media_567)
            pendiente_567 = tendencia_okta_567[1]*10 #decadal
            significativo_567 = tendencia_okta_567[2]
            tabla_tendencias.iloc[j,3] = round(pendiente_567, 2) #filas, columnas
            tabla_tendencias_significativas.iloc[j,3] = significativo_567

            #okta 8
            tendencia_okta_8 = tendencia_theil_sen(frecuencias[8])
            pendiente_8 = tendencia_okta_8[1]*10 #decadal
            significativo_8 = tendencia_okta_8[2]
            tabla_tendencias.iloc[j,4] = round(pendiente_8, 2) #filas, columnas
            tabla_tendencias_significativas.iloc[j,4] = significativo_8


        tabla_tendencias.index =  list(estaciones_ordenadas.values())
        tabla_tendencias.columns = ["0", "1-2-3", "4", "5-6-7", "8"]
        tabla_tendencias_significativas.index = list(estaciones_ordenadas.values())
        tabla_tendencias_significativas.columns = ["0", "1-2-3", "4", "5-6-7", "8"]
        #guardo
        tabla_tendencias.to_excel(f"tabla_tendencias_agrupo_{fecha_inicio_str}_{fecha_final_str}_{estacion}.xlsx")
        tabla_tendencias_significativas.to_excel(f"tabla_tendencias_significativas_agrupo_{fecha_inicio_str}_{fecha_final_str}_{estacion}.xlsx")

    return(print(f"Se generaron tablas de tendencias de oktas agrupadas para el periodo {fecha_inicio_str}_{fecha_final_str}"))