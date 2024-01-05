# to run the code without using jupyter

import warnings
warnings.filterwarnings("ignore") #para que muestre los warnings una sola vez

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import xarray as xr
import datetime as dt

from f_paper_nubosidad_NEA import f_mapa, f_media_mensual_smn, f_serie_anomalias_mensuales, f_calculo_CI, f_calculo_PC, f_cor_CI_media_anomalias_paper, f_frecuencia_oktas_por_mes, f_barplot_oktas_separadas_climatologia_media_espacial, f_barplot_media_mensual_ISCCP_y_SMN_climatologia_media_espacial

import f_paletas_colores

from f_abrir_datos_smn import abrir_datos_smn
from f_make_grid import make_grid
from f_mis_shapes import df_paises, df_provincias
from f_graficos_calibracion import grafico_puntos, grafico_puntos_paper, histograma_oktas_sat, histograma_oktas_sat_smn
from f_cargo_datos_isccp import cargo_datos_ISCCP
from f_porc_to_oktas import data_frame_oktas
from f_puntos_cercanos import puntos_cercanos
from f_tablas_de_contingencia_nubosidad import generar_tabla_contingencia

from f_graficos_calibracion import scatter, histograma, stackplot, barplot_oktas_separadas, histogramas_partidos, histograma_oktas_sat_smn, histogramas_partidos_poster
from f_procesamiento_satelite import frecuencia_oktas_por_anio, frecuencia_oktas_por_anio_estaciones, frecuencia_oktas_por_anio_meses, frecuencia_oktas_por_mes, agrupo_frecuencias, agrupo_data
import f_procesamiento_smn
from c_clases_satelite import dataframe_satelite, frecuencias_oktas
from c_clases_smn import dataframe_smn



################### load directories

cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))

#si estoy trabajando desde el servidor vegeta
ruta_a_archivos_isccp_mensual = "/pikachu/datos2/isccp-h/HGM" #ruta donde estan los archivos con datos de isccp-h
ruta_a_archivos_smn = "/pikachu/datos/nadia.testani/Doctorado/datos/smn/smn_variables_1961-2021/" #ruta donde estan los archivos con datos del smn
ruta_a_archivo_estaciones_smn = "/pikachu/datos/nadia.testani/Doctorado/datos/smn/" 
ruta_a_resultados = "/pikachu/datos/nadia.testani/Doctorado/resultados/resultados2021/nubosidad/paper" #ruta donde se guardan los resultados del analisis de nubosidad

##################  import dates

##periodo comun con satelite (Diciembre 1983 a Noviembre 2016)
fecha_inicio_str = "1983-12-15"
fecha_final_str = "2016-11-15"

##periodo completo años enteros y estaciones enteras March 1961 a February 2021
fecha_inicio_str_2 = "1961-03-01" 
fecha_final_str_2 = "2021-02-28" 

#climatologia: periodo comun con satelite (Diciembre 1983 a Noviembre 2016)
fecha_inicio_climatologia_str = "1983-12-15"
fecha_final_climatologia_str = "2016-11-15"


################## cargo datos

# Cargo datos de SMN
nombres_archivos = os.listdir(ruta_a_archivos_smn)
datos_smn = {}
for nombre_archivo in nombres_archivos:
    id_data = abrir_datos_smn(ruta_a_archivos = ruta_a_archivos_smn, nombre_archivo = nombre_archivo, 
                              variable = "nub")
    datos_smn[id_data[0]] = id_data[1]
    

# Cargo datos de ISCCPH mensual, recorto en region de interes y en las fechas que elijo para climatologia
isccp_mensual = xr.open_dataset(f"{ruta_a_archivos_isccp_mensual}/media_mensual_cldamt_cldamttypes.nc")[["cldamt","cldamt_types"]]
isccp_mensual_grande = isccp_mensual.loc[dict(lon=slice(298, 307),lat=slice(-33,-24))] #recorto region de interes (NEA) + 1 lon y lat para cada lado
isccp_mensual = isccp_mensual.loc[dict(lon=slice(299, 306),lat=slice(-32,-25))] #recorto region de interes (NEA)
isccp_mensual = isccp_mensual.sel(time=slice(fecha_inicio_climatologia_str, fecha_final_climatologia_str))
isccp_mensual_grande = isccp_mensual_grande.sel(time=slice(fecha_inicio_climatologia_str, fecha_final_climatologia_str))


###################### cargo informacion estaciones smn

# Cargo informacion sobre estaciones SMN
estaciones_smn = pd.read_excel(f"{ruta_a_archivo_estaciones_smn}Exp185151.xlsx", sheet_name = "Estaciones", 
                               names = ["EST", "NOMBRE", "LAT", "LON", "ALT"]) #smn

# Corrijo puntos manualmente 

#monte caseros
estaciones_smn.loc[estaciones_smn.EST == 87393, 'LAT'] = 30.27078
estaciones_smn.loc[estaciones_smn.EST == 87393, 'LON'] = 57.64046
#reconquista aero
estaciones_smn.loc[estaciones_smn.EST == 87270, 'LAT'] = 29.20159
estaciones_smn.loc[estaciones_smn.EST == 87270, 'LON'] = 59.69280

#paso de los libres aero
estaciones_smn.loc[estaciones_smn.EST == 87289, 'LAT'] = 29.68796
estaciones_smn.loc[estaciones_smn.EST == 87289, 'LON'] = 57.15317

#posadas aero
estaciones_smn.loc[estaciones_smn.EST == 87178, 'LAT'] = 27.39170
estaciones_smn.loc[estaciones_smn.EST == 87178, 'LON'] = 55.96673

#corrientes aero
estaciones_smn.loc[estaciones_smn.EST == 87166, 'LAT'] = 27.44915
estaciones_smn.loc[estaciones_smn.EST == 87166, 'LON'] = 58.75830

#concordia aero
estaciones_smn.loc[estaciones_smn.EST == 87395, 'LAT'] = 31.30297
estaciones_smn.loc[estaciones_smn.EST == 87395, 'LON'] = 58.00242

#resistencia aero
estaciones_smn.loc[estaciones_smn.EST == 87155, 'LAT'] = 27.44478
estaciones_smn.loc[estaciones_smn.EST == 87155, 'LON'] = 59.04856

#obera
estaciones_smn.loc[estaciones_smn.EST == 87187, 'LAT'] = 27.48733
estaciones_smn.loc[estaciones_smn.EST == 87187, 'LON'] = 55.12099

#roque saenz peña
estaciones_smn.loc[estaciones_smn.EST == 87148, 'LAT'] = 26.74565
estaciones_smn.loc[estaciones_smn.EST == 87148, 'LON'] = 60.48277

#mercedes
estaciones_smn.loc[estaciones_smn.EST == 87281, 'LAT'] = -29.22248
estaciones_smn.loc[estaciones_smn.EST == 87281, 'LON'] = -58.08762

#ituzaingo 
estaciones_smn.loc[estaciones_smn.EST == 87173, 'LAT'] = -27.58890
estaciones_smn.loc[estaciones_smn.EST == 87173, 'LON'] = -56.68925

############################


#extraigo la fecha de la primer y ultima medicion y calculo porcentaje de datos faltantes y lo acomodo en una tabla
print(f"CREATE TABLE 1")
print("\n")

codigos = list(estaciones_smn.EST)
nombres = ["Mercedes Aero", "Monte Caseros Aero", "Reconquista Aero", "Paso de los Libres Aero",
           "Posadas Aero", "Corrientes Aero", "Concordia Aero", "Resistencia Aero", "Ituzaingó", 
           "Oberá", "Presidencia Roque Saenz Peña Aero"]
lons = list(round(estaciones_smn.LON, 3))
lats = list(round(estaciones_smn.LAT,3))
alts = list(estaciones_smn.ALT)
fechas_0 = [str(datos_smn[cod].index[0].month) +"/" + str(datos_smn[cod].index[0].year) for cod in codigos]
fechas_menos1 = [str(datos_smn[cod].index[-1].month) +"/" + str(datos_smn[cod].index[-1].year) for cod in codigos]
porcentajes_faltantes = [round(datos_smn[cod].isnull()["nub"].sum()/len(datos_smn[cod]["nub"])*100, 3) for cod in codigos]

tabla_info_estaciones = pd.DataFrame({"Name": nombres,
                                      "Code": codigos,
                                      "Longitude [º]": lons,
                                      "Latitude [º]": lats,
                                      "Elevation [m]": alts,
                                      "Initial Date [mm/yyyy]":fechas_0,
                                      "Final Date [mm/yyyy]":fechas_menos1,
                                      "Missing values [%]": porcentajes_faltantes})

#la guardo
print(f"CHANGE THE WORKING DIRECTORY TO: {ruta_a_resultados}")
os.chdir(ruta_a_resultados) #se para en ruta general de resultados de nubosidad
print("\n")

# create excel writer
writer = pd.ExcelWriter("tabla_info_estaciones.xlsx")
# write dataframe to excel sheet named 'marks'
tabla_info_estaciones.to_excel(writer, 'info')
#save the excel file
#writer.save()
print(f"SAVE TABLE 1")

print("\n")
#vuelvo a ruta principal
os.chdir("../../../../../../../../home/nadia.testani/Doctorado/codigos/codigos2021/nubosidad") #codigos/codigos2021/nubosidad")  #VER
cwd = os.getcwd()
print("CHANGE THE WORKING DIRECTORY TO:{0}".format(cwd))




####################### figura 1

#%% Armo lista con los puntos satelitales
lons_satelital_mensual = list(isccp_mensual.lon.values)
lats_satelital_mensual = list(isccp_mensual.lat.values)
lista_puntos_satelital_mensual = make_grid(lons_satelital_mensual, lats_satelital_mensual)

#%% Cargo lista puntos smn
lista_puntos_smn = [(360 - lon, -1 * lat) for lon, lat in zip(estaciones_smn["LON"],estaciones_smn["LAT"])]
dict_puntos_smn = dict(zip(list(estaciones_smn["EST"]), lista_puntos_smn))
estaciones_ordenadas = {87148: "Roque Saenz Peña", 87155: "Resistencia", 87166: "Corrientes", 87178: "Posadas",
                        87187: "Oberá", 87270: "Reconquista", 87289: "Paso de los Libres",
                        87393: "Montecaseros", 87395: "Concordia"} #solo me quedo con las que uso
ides_omm_ordenado = list(estaciones_ordenadas.keys())
nombres_ides_omm_ordenado = list(estaciones_ordenadas.values())

#cargo shapes
shape_paises = df_paises()
shape_provincias = df_provincias()

#grafico
print(f"CHANGE THE WORKING DIRECTORY TO: {ruta_a_resultados}")
os.chdir(ruta_a_resultados) #se para en ruta general de resultados de nubosidad
print("\n")

print("PLOT AND SAVE IT (use f_mapa in f_paper_nubosidad_NEA)")
f_mapa(lista_puntos_satelital_mensual, dict_puntos_smn, ides_omm_ordenado, 
                     nombres_ides_omm_ordenado, shape_paises, shape_provincias)
plt.show()
print("\n")
#vuelvo a ruta principal
os.chdir("../../../../../../../../home/nadia.testani/Doctorado/codigos/codigos2021/nubosidad") #codigos/codigos2021/nubosidad")  #VER
cwd = os.getcwd()
print("CHANGE THE WORKING DIRECTORY: {0}".format(cwd))
