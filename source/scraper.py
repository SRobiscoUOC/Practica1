#!/usr/bin/env python
# coding: utf-8

# Este es el programa principal de nuestro sistema
# recibibe como parámetros la fecha inicial y final del intervalo de tiempo
# del que deseamos recoger los datos de las detecciones

# Lo primero que hacemos es importar nuestras funciones auxiliares
import csv
from scraper_functions import execute_form



# Importamos el resto de cosas que vamos a necesitar
import argparse

# Lo segundo que hacemos es tomar los dos parámetros de entrada y parsearlos
parser = argparse.ArgumentParser()
# Preparamos los dos argumentos con su ayuda
parser.add_argument('--Fecha_inicio', help='Introduce la fecha de inicio del intervalo (Formato: "AAAAMMDD")', required=True)
parser.add_argument('--Fecha_fin', help='Introduce la fecha de fin del intervalo (Formato: "AAAAMMDD")', required=True)
# Parseamos
args = parser.parse_args()

# Tomamos los valores
fechaInicio = args.Fecha_inicio
fechaFin = args.Fecha_fin

# Llamamos a la función y guardamos el dataset.
# Ejemplos de fechas con el número de filas esperado:
#   writer.writerows(execute_form('20150101','20221105'))     # 119 filas
#   writer.writerows(execute_form('20200301','20221105'))     #   7 filas

with open('../dataset/detecciones_ondas_gravitacionales.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(execute_form(fechaInicio, fechaFin))
