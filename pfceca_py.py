{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOWxDvxPm3D9eyloMRPGOh5",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/carloscamargo1977/BIGDATA_2022B/blob/master/pfceca_py.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "cVDrItAkNd55"
      },
      "outputs": [],
      "source": [
        "# PSEUCODIGO\n",
        "# main()\n",
        "#   datos = leer_datos(nombre del archivo : str) -> pd.dataframe\n",
        "#   datos_no_dup = remover_duplicados_y_nulos(datos: pd.dataframe) ->pd.dat\n",
        "#   datos = convertir_str_a_num(datos, col='EDAD') -> pd.dataframe\n",
        "#   datos = coggerir_fechas(datos, col='FECHA1') -> pd.dataframe\n",
        "#   datos = coggerir_fechas(datos, col='FECHA2') -> pd.dataframe\n",
        "#   save_data()\n",
        "\n",
        "import numpy as np\n",
        "import pandas as pd \n",
        "import os\n",
        "from pathlib import Path\n",
        "from dateutil.parser import parse\n",
        "\n",
        "#root_dir = Path(\".\").resolve()\n",
        "root_dir = \"gs://proyectofinalceca/data/\"\n",
        "filename = \"Consolidado_datos_abiertos_2021_2022.csv\"\n",
        "\n",
        "def leer_datos(filename):\n",
        "    data_dir = 'raw'\n",
        "    file_path = os.path.join(root_dir, data_dir, filename) #Ruta del archivo, encuentro la base que necesito\n",
        "    datos = pd.read_csv(file_path, encoding='latin-1', sep=';')\n",
        "    print('get_data')\n",
        "    print('La tabla contiene', datos.shape[0], 'filas', datos.shape[1], 'columnas')\n",
        "    return datos\n",
        "\n",
        "def renovar_duplicados_y_nulos(datos):\n",
        "    data = datos.drop_duplicates()\n",
        "    data.reset_index(inplace=True, drop=True)\n",
        "    col = \"UNIDAD\"\n",
        "    data[col].fillna(\"SIN_DATO\", inplace=True)\n",
        "    data[col].value_counts(dropna=False, normalize=True)\n",
        "    col = \"EDAD\"\n",
        "    data[col].fillna(\"SIN_DATO\", inplace=True)\n",
        "    data[col].value_counts(dropna=False, normalize=True)\n",
        "    data[col].replace({\"SIN_DATO\": np.nan}, inplace=True)\n",
        "    data[col]\n",
        "    \n",
        "    \n",
        "    \n",
        "    \n",
        "    return data\n",
        "\n",
        "def convetir_str_a_num(data, col=\"EDAD\"):\n",
        "    f = lambda x: x if pd.isna(x) else int(x) \n",
        "    data[col] = data[col].apply(f)\n",
        "    data.info()\n",
        "\n",
        "    return data\n",
        "\n",
        "def corregir_fecha(data, col = \"FECHA1\"):\n",
        "    col = \"FECHA_INICIO_DESPLAZAMIENTO_MOVIL\"\n",
        "    data[col] = pd.to_datetime(data[col], errors = \"coerce\")\n",
        "    data.info()\n",
        "    fecha = \"1985-02-30 00:00:00\"\n",
        "    pd.to_datetime(fecha, errors = \"coerce\", format = \"%Y/%m/%d\")\n",
        "    col = \"RECEPCION\"\n",
        "    data[col]\n",
        "    list_fechas = list()\n",
        "    for fecha in data[col]:\n",
        "        try:\n",
        "            new_fecha = parse(fecha)\n",
        "        except Exception as e:        \n",
        "            new_fecha = pd.to_datetime(fecha, errors=\"coerce\") # el error es este el print muestra pero se reemplaza con new_fecha\n",
        "            list_fechas.append(new_fecha)\n",
        "            list_fechas\n",
        "            data[\"RECEPCION_Carr\"] = list_fechas\n",
        "            data.head()\n",
        "\n",
        "def generate_report(data):\n",
        "    dict_resumen = dict()  # Crear un diccionario vacio\n",
        "    for col in data.columns:\n",
        "        valores_unicos = data[col].unique()\n",
        "        n_valores = len(valores_unicos)\n",
        "        dict_resumen[col] = n_valores\n",
        "\n",
        "    reporte = pd.DataFrame.from_dict(dict_resumen, orient='index') \n",
        "    reporte.rename({0: 'Count'}, axis=1, inplace=True) # axis 1 buscar en la columna, 0 en las filas\n",
        "\n",
        "    print('generate_report')\n",
        "    print(reporte.head())\n",
        "    return reporte\n",
        "\n",
        "def save_data(reporte, filename): # Guardar tabla\n",
        "    out_name = 'Limpieza2_' + filename # Indicar nombre al archivo de salida\n",
        "    #out_path = os.path.join(root_dir, 'data', 'processed', out_name)\n",
        "    #reporte.to_csv(out_path, sep=';')\n",
        "    reporte.to_csv(\"gs://proyectofinalceca/data/processed/\" + out_name,encoding =\"latin1\",sep=\";\")\n",
        "\n",
        "def main():\n",
        "\n",
        "    filename = \"Consolidado_datos_abiertos_2021_2022.csv\"\n",
        "    datos = leer_datos(filename)\n",
        "    #renovar_duplicados_y_nulos(datos)\n",
        "    \n",
        "    datos[\"LOCALIDAD\"] =  datos[\"LOCALIDAD\"].replace(\n",
        "        {\"Barrios Unidos\":\"BARRIOS UNIDOS\",\"Fontib¢n\":\"FONTIBON\",\"San Crist¢bal\":\"SAN CRISTOBAL\",\n",
        "         \"Engativ\\xa0\":\"ENGATIVA\",\"Suba\":\"SUBA\",\"Bosa\":\"BOSA\", \"Kennedy\":\"KENNEDY\", \"Usaqu‚n\":\"USAQUEN\", \n",
        "         \"Antonio Nari¤o\":\"ANTONIO NARIÑO\",\"Puente Aranda\":\"PUENTE ARANDA\",\"Rafael Uribe Uribe\":\"RAFAEL URIBE URIBE\" ,\n",
        "         \"Usme\":\"USME\" ,\"Usme\":\"USME\",\"Chapinero\":\"CHAPINERO\",\"Santa Fe\":\"SANTA FE\",\n",
        "         \"Teusaquillo\":\"TEUSAQUILLO\",\"Tunjuelito\":\"TUNJUELITO\",\"La Candelaria\":\"LA CANDELARIA\",\"Sumapaz\":\"SUMAPAZ\",\n",
        "         \"Ciudad Bol¡var\":\"CIUDAD BOLIVAR\",\"Los M\\xa0rtires\":\"LOS MARTIRES\"\n",
        "        }\n",
        "    )\n",
        "    \n",
        "    save_data(datos, filename)\n",
        "    print('LISTO')\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "JKweZ3RzQ5wi"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}