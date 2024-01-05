import numpy as np

def f_promedio_movil(serie, ventana):
    lista_salida = [None] * len(serie)
    for i in range(0, len(serie) - ventana):
        lista_salida [i + int(ventana / 2)] = np.nanmean(serie[i:i + ventana])      
    return(lista_salida)