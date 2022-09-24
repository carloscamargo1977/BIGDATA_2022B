import numpy as np
import argparse

def calcular_valores_centrales(lista_numeros, verbose=1):

    media = np.mean(lista_numeros)
    desv_std = np.std(lista_numeros)

    if verbose==1:
       print("calcular_valores_centrales")
       print("media", media)
       print("desv std", desv_std)
    else:
        pass
    return media, desv_std

def calcular_suma(lista_numeros, verbose=1):
    """
    Calcula la suma de una lista de numeros
    arg:
        lista_numeros: lista de numeros
    """
       
    resultado = np.sum(lista_numeros)
    if verbose==1:
       print("calcular_suma")
       print("suma", resultado)
    else:
        pass
    return resultado

def calular_extremos(lista_numeros, verbose=1):
    """
    Calcula el valor minimo y maximo de una lista de numeros
    Args:
      lista_numeros (lista): lista de numeros con valores enteros
    
    Returns:
      tuple: (minimo, maximo)
    """   
    min_val = np.min(lista_numeros)
    max_val = np.max(lista_numeros)
    
    if verbose == 1:
       print("calular_extremos")
       print("Valor minimo", min_val)
       print("Valor maximo", max_val)
    else:
        pass
    return min_val, max_val

def calcular_valores(lista_numeros, verbose=1):
    suma            = calcular_suma(lista_numeros, verbose)
    media, desv_std = calcular_valores_centrales(lista_numeros, verbose)
    min_val, max_val = calular_extremos(lista_numeros, verbose)
        
    return suma, media, desv_std, min_val, max_val

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", type=int, default=1, help="para decidir si imprime informacion")

    args = parser.parse_args()

    verbose = args.verbose

    
    lista_numeros = [1, 5, 8, 3, 45, 93]
    suma, media, desv_std, min_val, max_val = calcular_valores(lista_numeros, 1)
    
    print("DONE!!!")    

if __name__ == "__main__":
    main()