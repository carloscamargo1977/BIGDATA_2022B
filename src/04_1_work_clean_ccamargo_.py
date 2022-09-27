# pseudo codigo
# main()
#    datos = get_data(filename)
#    unicos = duplicados(data)
#    limpios = cleaning (data) 
#    reporte = generate_report(data)
#    save_data(reporte)

import os
from pathlib import Path
import pandas as pd
import numpy as np
from dateutil.parser import parse

root_dir = Path(".").resolve()
file_name = "llamadas123_julio_2022.csv"

def get_data(filename):
    data_dir = 'raw'
    file_path = os.path.join(root_dir, "data", data_dir, filename) #Ruta del archivo que necesito
    datos = pd.read_csv(file_path, encoding='latin-1', sep=';')
    print('get_data')
    print('La tabla contiene', datos.shape[0], 'filas', datos.shape[1], 'columnas')
    return datos

def duplicados(datos):
    data = datos.drop_duplicates()
    data.reset_index(inplace=True, drop=True)
    return data
    
def cleaning(data):
    col = "UNIDAD"
    data[col].fillna("SIN_DATO", inplace=True)
    data[col].value_counts(dropna=False, normalize=True) 
    col = "FECHA_INICIO_DESPLAZAMIENTO_MOVIL"
    data[col] = pd.to_datetime(data[col], errors = "coerce", format = "%Y/%m/%d")
    col = "EDAD"
    data[col].fillna("SIN_DATO", inplace=True)
    data[col].value_counts(dropna=False, normalize=True)
    data[col].replace({"SIN_DATO": np.nan}, inplace=True)
    f = lambda x: x if pd.isna(x) else int(x)
    data[col] = data[col].apply(f)
    col = "RECEPCION"
    list_fechas = list()
    for fecha in data[col]:
        try:
            new_fecha = parse(fecha)
        except Exception as e:        
             new_fecha = pd.to_datetime(fecha, errors="coerce")
        list_fechas.append(data)
        data["RECEPCION_corr"]=list_fechas
        data.head(10)
    return data
  
def generate_report(data):
    # Crear un diccionario vacio
    dict_resumen = dict()

    # loop para llenar el diccionario de columnas con valores unicos
    for col in data.columns:
        valores_unicos = data[col].unique()
        n_valores = len(valores_unicos)
        dict_resumen[col] = n_valores

    reporte = pd.DataFrame.from_dict(dict_resumen, orient='index') 
    reporte.rename({0: 'Count'}, axis=1, inplace=True) # 1 buscar en la columna, 0 en las filas

    print('generate_report')
    print(reporte.head())
    return reporte

def save_data(reporte, filename):
    # Guardar la tabla:

    out_name = 'resumen2_' + filename # Renombrar ya el archivo de salida
    out_path = os.path.join(root_dir, 'data', 'processed', out_name)
    reporte.to_csv(out_path)

def main():

    filename = "llamadas123_julio_2022.csv"
    datos = get_data(filename)
    reporte = generate_report(datos)
    save_data(reporte, filename)

    print('DONE!!!')

if __name__ == "__main__":
    main()