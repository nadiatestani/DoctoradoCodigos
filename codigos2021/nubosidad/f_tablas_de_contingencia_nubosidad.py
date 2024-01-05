#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 14:43:58 2021

@author: nadia

f_tablas_de_contingencia_nubosidad.py
"""
#f_tablas_de_contingencia_nubosidad.py

#df_data_smn
#df_data_satelital
import pandas as pd
import numpy as np
import datetime as dt
import xlsxwriter

from c_clases_satelite import dataframe_satelite
from c_clases_smn import dataframe_smn

#defino test
def testeo_tabla_contingencia(tabla, tabla_teorica, alpha = 0.05):
    comparacion_casillero = []
    for i in range(0, 9):
        for j in range(0, 9):
            if tabla_teorica[i][j] == 0:
                comparacion_casillero.append(0.0)
            else: 
                comparacion_casillero.append((tabla[i][j]-tabla_teorica[i][j])**2/tabla_teorica[i][j])
    chi_cuadrado_observado = sum(comparacion_casillero)
    numero_filas = 9
    # numero_columnas = 9
    if alpha == 0.1:
        chi_cuadrado_teorico = 74.397 #lo saco de tabla para grados de libertad = (numero_filas - 1)  (numero_columnas - 1) = 8 * 8 = 64 (aproximo por 60 g.l que es lo que hay en la tabla)
    elif alpha == 0.05:
        chi_cuadrado_teorico = 79.082
    elif alpha == 0.01:
        chi_cuadrado_teorico = 88.3794 #lo saco de tabla para grados de libertad = (numero_filas - 1)  (numero_columnas - 1) = 8 * 8 = 64 (aproximo por 60 g.l que es lo que hay en la tabla)
    else:
        print("Solo se pueden ingresar alpha = 0.1 0.05 y 0.01. Se va a computar alpha = 0.05")
        alpha = 0.05
        chi_cuadrado_teorico = 79.082 #lo saco de tabla para grados de libertad = (numero_filas - 1)  (numero_columnas - 1) = 8 * 8 = 64 (aproximo por 60 g.l que es lo que hay en la tabla)    
    n = tabla["count"]["count"] #tamanio de la muestra
    k = numero_filas
    coef_de_contingencia = np.sqrt(chi_cuadrado_observado / (chi_cuadrado_observado + n))
    coef_de_contingencia_maximo = np.sqrt((k - 1) / k)
    coeficiente_de_contingencia_normalizado = coef_de_contingencia / coef_de_contingencia_maximo
    print("####################################")
    print("######## EXPLICO TEST #########")
    print(f"Si Chi_2_observado es mayor que Chi_2_teorico entonces rechazo la siguiente hipótesis nula: \n ---> la tabla observada es igual a la tabla teorica al azar \n a favor de la hipotesis alternativa: \n ---> la tabla observada es distinta a la tabla teorica al azar \n entonces las variables estan relacionadas con un {1-alpha*100} % de confianza")
    print("####################################")
    print("######## EN ESTE CASO: #########")
    print(f"En este caso: \n # Chi_2_observado = {chi_cuadrado_observado} \n # Chi_2_teorico = {chi_cuadrado_teorico} \n # alpha = {alpha}")
    if chi_cuadrado_observado > chi_cuadrado_teorico:
        print(f"Entonces, con un {(1-alpha)*100}% de confianza, se rechaza la hipotesis nula a favor de la alternativa --> LAS VARIABLES ESTAN RELACIONADAS")
    elif chi_cuadrado_observado <= chi_cuadrado_teorico:
        print(f"Entonces, con un {(1-alpha)*100}% de confianza, no se puede rechazar la hipotesis nula a favor de la alternativa --> NO SE PUEDE DECIR QUE LAS VARIABLES ESTEN RELACIONADAS")
    print("####################################")
    #resumo info en una tabla que pueda guardar
    tabla_testeo_contingencia = pd.DataFrame(index=["Chi_2_observado", "Chi_2_teorico", "Alpha", "Rechaza H0 i.e las variables estan relacionadas", "Mensaje", "Coeficiente de contingencia normalizado"], columns = ["Resultado"])
    tabla_testeo_contingencia["Resultado"]["Chi_2_observado"] = float(str(chi_cuadrado_observado))
    tabla_testeo_contingencia["Resultado"]["Chi_2_teorico"] = float(str(chi_cuadrado_teorico))
    tabla_testeo_contingencia["Resultado"]["Alpha"] = float(str(alpha))
    if chi_cuadrado_observado > chi_cuadrado_teorico:
        tabla_testeo_contingencia["Resultado"]["Rechaza H0 i.e las variables estan relacionadas"] = "SI"
        tabla_testeo_contingencia["Resultado"]["Mensaje"] = f"Con un nivel de significancia {alpha}, se rechaza la hipotesis nula (la tabla de contingencia observada es igual a la tabla teórica al azar) a favor de la hipotesis alternativa (la tabla de contingencia observada es distinta a la tabla teórica al azar). Entonces, las variables están relacionadas con un {(1-alpha)*100}% de confianza"
    elif chi_cuadrado_observado <= chi_cuadrado_teorico:
        tabla_testeo_contingencia["Resultado"]["Rechaza H0 i.e las variables estan relacionadas"] = "NO"
        tabla_testeo_contingencia["Resultado"]["Mensaje"] = f"Con un nivel de significancia {alpha}, no se puede rechazar la hipotesis nula (la tabla de contingencia observada es igual a la tabla teórica al azar) a favor de la hipotesis alternativa (la tabla de contingencia observada es distinta a la tabla teórica al azar). Entonces, no se puede decir que las variables estén relacionadas con un {(1-alpha)*100}% de confianza"
    tabla_testeo_contingencia["Resultado"]["Coeficiente de contingencia normalizado"] = round(coeficiente_de_contingencia_normalizado, 2)
    return tabla_testeo_contingencia


def generar_tabla_contingencia(ID_estacion, data_frame_smn, fecha_inicio_str, fecha_final_str, data_frame_cldamt_punto, lon, lat, alpha = 0.05, estaciones = False, meses = False):
    
    instancia_serie_satelital = dataframe_satelite(data_frame_cldamt_punto).genero_serie("cldamt_oktas", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_satelite
    instancia_serie_smn = dataframe_smn(data_frame_smn).genero_serie("nub", fecha_inicio_str, fecha_final_str) #uso clases de c_clases_smn
    if instancia_serie_smn.es_diario():
        unico_data_frame = pd.concat([instancia_serie_satelital.paso_hora_a_cero(), instancia_serie_smn.paso_hora_a_cero()], axis = 1)#, join = "inner")
    else:
        unico_data_frame = pd.concat([instancia_serie_satelital.paso_mes_a_uno(), instancia_serie_smn.paso_mes_a_uno()], axis = 1)#, join = "inner")
    unico_data_frame.columns=["ISCCP", "SMN"]
    #unico_data_frame.index = pd.to_datetime(unico_data_frame.index)
    
    print("####### instancia_serie_satelital.serie ###########")
    print(instancia_serie_satelital.serie)
    print("####### instancia_serie_smn.serie ###########")
    print(instancia_serie_smn.serie)
    print("####### unico_data_frame ###########")
    print(unico_data_frame)
    
    if estaciones == False and meses == False:
        tabla = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
        indices = unico_data_frame.index 
        for fecha in indices:
            if np.sum(pd.isna(unico_data_frame.loc[str(fecha)]).values) == 0 :
                for i in range(0,9):
                    if int(unico_data_frame.loc[str(fecha)]["SMN"]) == i:
                        tabla[i]["count"] += 1
                        for j in range(0,9):
                            if unico_data_frame.loc[str(fecha)]["ISCCP"] == j :
                                tabla["count"][j] += 1
                                tabla[i][j] += 1
        tabla["count"]["count"] = sum (tabla["count"])
        
        ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
        band_0 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3)
        band_1 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3)
        band_2 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3)
        over = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3)
        under = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3)
        tabla_porcentajes = pd.DataFrame({"band_0": [band_0], "band_1" : [band_1], "band_2" : [band_2], "over" : [over], "under": [under]}, index = [f"{lon-360}_{lat}_{ID_estacion}"])
        ###
        
        #creo tabla teorica al azar para testear la tabla de contingecia observada
        tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
        for i in range(0,9):
            for j in range(0,9):
                tabla_teorica[i][j] = tabla[i]["count"]*tabla[j]["count"]/tabla["count"]["count"]
        
        #cargo los resultados de testear la tabla con la tabla teorica
        tabla_testeo = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
        
        #guardo todo en un mismo xlsx
        writer = pd.ExcelWriter(f"tablas_contingencia_{lon}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
        tabla.to_excel(writer,sheet_name='Tabla')   
        tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
        tabla_teorica.to_excel(writer,sheet_name='Tabla teorica')  
        tabla_testeo.to_excel(writer,sheet_name='Tabla testeo')  
        writer.save()
    
    elif estaciones == True and meses == False:
        
        estacion = [["DJF", "MAM"], ["JJA", "SON"]]
        estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
        
        tablas = {}
        tablas_teoricas = {}
        tablas_testeo = {}
        
        band_0 = []
        band_1 = []
        band_2 = []
        over = []
        under = []
        
        for j in range(0, 2):
            for i in range(0, 2):
                tabla = pd.DataFrame(0, index = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
                
                mes1 = estacion_meses[j][i][0]
                mes2 = estacion_meses[j][i][1]
                mes3 = estacion_meses[j][i][2]
                data = pd.concat([unico_data_frame[unico_data_frame.index.month == mes1],
                                 unico_data_frame[unico_data_frame.index.month == mes2],
                                 unico_data_frame[unico_data_frame.index.month == mes3]])
                indices = data.index
                for fecha in indices:
                    if np.sum(pd.isna(data.loc[str(fecha)]).values) == 0 :
                        for m in range(0,9):
                            if int(data.loc[str(fecha)]["SMN"]) == m:
                                tabla[m]["count"] += 1
                                for n in range(0,9):
                                    if data.loc[str(fecha)]["ISCCP"] == n :
                                        tabla["count"][n] += 1
                                        tabla[m][n] += 1
                tabla["count"]["count"] = sum (tabla["count"])       
                
                ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
                band_0.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3))
                band_1.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3))
                band_2.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3))
                over.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3))
                under.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3))
                
                tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
                for k in range(0,9):
                    for l in range(0,9):
                        tabla_teorica[k][l] = tabla[k]["count"]*tabla[l]["count"]/tabla["count"]["count"]
                        
                tablas[estacion[j][i]] = tabla
                tablas_teoricas[estacion[j][i]] = tabla_teorica
                tablas_testeo[estacion[j][i]] = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
        
        tabla_porcentajes = pd.DataFrame({"band_0": band_0, "band_1" : band_1, "band_2" : band_2, "over" : over, "under": under}, index = ["DJF", "MAM", "JJA", "SON"])        
        
        #guardo todo en un mismo xlsx
        writer = pd.ExcelWriter(f"tablas_contingencia_estacional_{lon}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
        for j in range(0, 2):
            for i in range(0, 2):
                tablas[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla {estacion[j][i]}')   
                tablas_teoricas[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla teorica {estacion[j][i]}')  
                tablas_testeo[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla testeo {estacion[j][i]}')  
        tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
        writer.save()   
    
    elif estaciones == False and meses == True:
        meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
        meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]       
        
        tablas = {}
        tablas_teoricas = {}
        tablas_testeo = {}
        
        band_0 = []
        band_1 = []
        band_2 = []
        over = []
        under = []
        
        for j in range(0, 4):
            for i in range(0, 3):
                tabla = pd.DataFrame(0, index = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
                data = unico_data_frame[unico_data_frame.index.month == meses_num[j][i]]
                indices = data.index
                
                for fecha in indices:
                    if np.sum(pd.isna(data.loc[str(fecha)]).values) == 0 :
                        for m in range(0,9):
                            if int(data.loc[str(fecha)]["SMN"]) == m:
                                tabla[m]["count"] += 1
                                for n in range(0,9):
                                    if data.loc[str(fecha)]["ISCCP"] == n :
                                        tabla["count"][n] += 1
                                        tabla[m][n] += 1
                                        
                tabla["count"]["count"] = sum (tabla["count"])
                
                ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
                band_0.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3))
                band_1.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3))
                band_2.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3))
                over.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3))
                under.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3))
                
                tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
                for k in range(0,9):
                    for l in range(0,9):
                        tabla_teorica[k][l] = tabla[k]["count"]*tabla[l]["count"]/tabla["count"]["count"]
                
                tablas[meses[j][i]] = tabla
                tablas_teoricas[meses[j][i]] = tabla_teorica
                tablas_testeo[meses[j][i]] = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
        
        tabla_porcentajes = pd.DataFrame({"band_0": band_0, "band_1" : band_1, "band_2" : band_2, "over" : over, "under": under}, index = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])        
        
        #guardo todo en un mismo xlsx
        writer = pd.ExcelWriter(f"tablas_contingencia_mensual_{lon}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
        for j in range(0, 4):
            for i in range(0, 3):
                tablas[meses[j][i]].to_excel(writer,sheet_name=f'Tabla {meses[j][i]}')   
                tablas_teoricas[meses[j][i]].to_excel(writer,sheet_name=f'Tabla teorica {meses[j][i]}')  
                tablas_testeo[meses[j][i]].to_excel(writer,sheet_name=f'Tabla testeo {meses[j][i]}')  
        tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
        writer.save()     
        
    elif estaciones == True and meses == True:
        raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")
        
    ##concateno ambos dataframes (el de SMN y el de ISCCP)
    #indice_comun = pd.date_range(fecha_inicio_str,f"{fecha_final_str[0:5]}{int(fecha_final_str[5:8])+1}",freq="M")
    #data_frame_cldamt_punto_fechas = data_frame_cldamt_punto.loc[fecha_inicio_str:fecha_final_str].copy()
    #data_frame_cldamt_punto_fechas = data_frame_cldamt_punto_fechas.set_index(indice_comun)
    #mask = ((data_frame_smn.index >= fecha_inicio_str) & (data_frame_smn.index <= f"{fecha_final_str[0:5]}{int(fecha_final_str[5:8])+1}")).transpose()
    #data_frame_smn_fechas = data_frame_smn.loc[mask]
    ##data_frame_smn_fechas = data_frame_smn.loc[fecha_inicio_str:fecha_final_str].copy() #me tira error en esta linea
    #data_frame_smn_fechas = data_frame_smn_fechas.set_index(indice_comun)
    #unico_data_frame = pd.concat([data_frame_cldamt_punto_fechas[2], data_frame_smn], axis = 1, join = "inner")
    #unico_data_frame.rename(columns={2:"ISCCP", "0":"SMN"}, inplace = True)
    
    #if estaciones == False and meses == False:
    #    tabla = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
    #    indices = unico_data_frame.index.to_period("M") #solo anio y mes
    #    for fecha in indices:
    #        if np.sum(pd.isna(unico_data_frame.loc[str(fecha)]).values) == 0 :
    #            for i in range(0,9):
    #                if int(unico_data_frame.loc[str(fecha)]["SMN"].values[0]) == i:
    #                    tabla[i]["count"] += 1
    #                    for j in range(0,9):
    #                        if unico_data_frame.loc[str(fecha)]["ISCCP"].values[0] == j :
    #                            tabla["count"][j] += 1
    #                            tabla[i][j] += 1
    #    tabla["count"]["count"] = sum (tabla["count"])
    #    
    #    ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
    #    band_0 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3)
    #    band_1 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3)
    #    band_2 = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3)
    #    over = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3)
    #    under = round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3)
    #    tabla_porcentajes = pd.DataFrame({"band_0": [band_0], "band_1" : [band_1], "band_2" : [band_2], "over" : [over], "under": [under]}, index = [f"{lon-360}_{lat}_{ID_estacion}"])
    #    ###
        
    #    #creo tabla teorica al azar para testear la tabla de contingecia observada
    #    tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
    #    for i in range(0,9):
    #        for j in range(0,9):
    #            tabla_teorica[i][j] = tabla[i]["count"]*tabla[j]["count"]/tabla["count"]["count"]
    #    
    #    #cargo los resultados de testear la tabla con la tabla teorica
    #    tabla_testeo = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
    #    
    #    #guardo todo en un mismo xlsx
    #    writer = pd.ExcelWriter(f"tablas_contingencia_{lon-360}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
    #    tabla.to_excel(writer,sheet_name='Tabla')   
    #    tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
    #    tabla_teorica.to_excel(writer,sheet_name='Tabla teorica')  
    #    tabla_testeo.to_excel(writer,sheet_name='Tabla testeo')  
    #    writer.save()
        
    #elif estaciones == True and meses == False:
    #    
    #    estacion = [["DJF", "MAM"], ["JJA", "SON"]]
    #    estacion_meses = [[(12, 1, 2), (3, 4, 5)], [(6, 7, 8), (9, 10, 11)]]
    #    
    #    tablas = {}
    #    tablas_teoricas = {}
    #    tablas_testeo = {}
    #    
    #    band_0 = []
    #    band_1 = []
    #    band_2 = []
    #    over = []
    #    under = []
    #    
    #    for j in range(0, 2):
    #        for i in range(0, 2):
    #            tabla = pd.DataFrame(0, index = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
     #           
     #           mes1 = estacion_meses[j][i][0]
     #           mes2 = estacion_meses[j][i][1]
     #           mes3 = estacion_meses[j][i][2]
     #           data = pd.concat([unico_data_frame[unico_data_frame.index.month == mes1],
     #                            unico_data_frame[unico_data_frame.index.month == mes2],
     #                            unico_data_frame[unico_data_frame.index.month == mes3]])
     #           indices = data.index.to_period("M") #solo anio y mes
     #           for fecha in indices:
     #               if np.sum(pd.isna(data.loc[str(fecha)]).values) == 0 :
     #                   for m in range(0,9):
     #                       if int(data.loc[str(fecha)]["SMN"].values[0]) == m:
     #                           tabla[m]["count"] += 1
     #                           for n in range(0,9):
     #                               if data.loc[str(fecha)]["ISCCP"].values[0] == n :
     #                                   tabla["count"][n] += 1
     #                                   tabla[m][n] += 1
     #           tabla["count"]["count"] = sum (tabla["count"])       
     #           
     #           ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
     #           band_0.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3))
     #           band_1.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3))
     #           band_2.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3))
     #           over.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3))
     #           under.append( round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3))
     #           
     #           tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
     #           for k in range(0,9):
     #               for l in range(0,9):
     #                   tabla_teorica[k][l] = tabla[k]["count"]*tabla[l]["count"]/tabla["count"]["count"]
     #                   
     #           tablas[estacion[j][i]] = tabla
     #           tablas_teoricas[estacion[j][i]] = tabla_teorica
     #           tablas_testeo[estacion[j][i]] = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
     #   
     #   tabla_porcentajes = pd.DataFrame({"band_0": band_0, "band_1" : band_1, "band_2" : band_2, "over" : over, "under": under}, index = ["DJF", "MAM", "JJA", "SON"])        
        
        #guardo todo en un mismo xlsx
     #   writer = pd.ExcelWriter(f"tablas_contingencia_estacional_{lon-360}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
     #   for j in range(0, 2):
     #       for i in range(0, 2):
     #           tablas[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla {estacion[j][i]}')   
     #           tablas_teoricas[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla teorica {estacion[j][i]}')  
     #           tablas_testeo[estacion[j][i]].to_excel(writer,sheet_name=f'Tabla testeo {estacion[j][i]}')  
     #   tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
     #   writer.save()   
        
    #elif estaciones == False and meses == True:
    #    meses = [["January", "February", "March"], ["April", "May", "June"], ["July", "August", "September"], ["October", "November", "December"]]
    #    meses_num =[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]       
        
    #    tablas = {}
    #    tablas_teoricas = {}
    #    tablas_testeo = {}
        
    #    band_0 = []
    #    band_1 = []
    #    band_2 = []
    #    over = []
    #    under = []
        
    #    for j in range(0, 4):
    #        for i in range(0, 3):
    #            tabla = pd.DataFrame(0, index = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, "count"])
    #            data = unico_data_frame[unico_data_frame.index.month == meses_num[j][i]]
    #            indices = data.index.to_period("M") #solo anio y mes
                
    #            for fecha in indices:
    #                if np.sum(pd.isna(data.loc[str(fecha)]).values) == 0 :
    #                    for m in range(0,9):
    #                        if int(data.loc[str(fecha)]["SMN"].values[0]) == m:
    #                            tabla[m]["count"] += 1
    #                            for n in range(0,9):
    #                                if data.loc[str(fecha)]["ISCCP"].values[0] == n :
    #                                    tabla["count"][n] += 1
    #                                    tabla[m][n] += 1
    #                                    
    #            tabla["count"]["count"] = sum (tabla["count"])
    #            
    #            ### Armo el porcentaje de casos de exito, de exito con diferencia de 1 okta, con diferencia de 2 oktas, con mas de 3 oktas overestimated, y con mas de 3 oktas under
    #            band_0.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if i==j])/tabla["count"]["count"], 3))
    #            band_1.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+1 or j == i-1])/tabla["count"]["count"], 3))
    #            band_2.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j == i+2 or j == i-2])/tabla["count"]["count"], 3))
    #            over.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j >= i+3])/tabla["count"]["count"], 3))
    #            under.append(round(sum([tabla[i][j] for i in range(0,9) for j in range(0,9) if j <= i-3])/tabla["count"]["count"], 3))
    #            
    #            tabla_teorica = pd.DataFrame(0, index=[0, 1, 2, 3, 4, 5, 6, 7, 8], columns = [0, 1, 2, 3, 4, 5, 6, 7, 8])
    #            for k in range(0,9):
    #                for l in range(0,9):
    #                    tabla_teorica[k][l] = tabla[k]["count"]*tabla[l]["count"]/tabla["count"]["count"]
    #            
    #            tablas[meses[j][i]] = tabla
    #            tablas_teoricas[meses[j][i]] = tabla_teorica
    #            tablas_testeo[meses[j][i]] = testeo_tabla_contingencia(tabla, tabla_teorica, alpha )
    #    
    #    tabla_porcentajes = pd.DataFrame({"band_0": band_0, "band_1" : band_1, "band_2" : band_2, "over" : over, "under": under}, index = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])        
        
    #    #guardo todo en un mismo xlsx
    #    writer = pd.ExcelWriter(f"tablas_contingencia_mensual_{lon-360}_{lat}_{ID_estacion}.xlsx", engine='xlsxwriter')   
    #    for j in range(0, 4):
    #        for i in range(0, 3):
    #            tablas[meses[j][i]].to_excel(writer,sheet_name=f'Tabla {meses[j][i]}')   
    #            tablas_teoricas[meses[j][i]].to_excel(writer,sheet_name=f'Tabla teorica {meses[j][i]}')  
    #            tablas_testeo[meses[j][i]].to_excel(writer,sheet_name=f'Tabla testeo {meses[j][i]}')  
    #    tabla_porcentajes.to_excel(writer, sheet_name = "Tabla porcentajes")
    #    writer.save()     
        
    #elif estaciones == True and meses == True:
    #    raise ValueError ("Solo puede ser True estaciones o meses, no ambos en simultaneo")
                
    
