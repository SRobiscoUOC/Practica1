#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Este es el programa principal de nuestro sistema
# recibibe como parámetros la fecha inicial y final del intervalo de tiempo
# del que deseamos recoger los datos de las detecciones

# Lo primero que hacemos es importar nuestras funciones auxiliares
from scraper_functions import execute_form
# Importamos el resto de cosas que vamos a necesitar
import argparse

# Lo segundo que hacemos es tomar los dos parámetros de entrada
# y parsearlos
parser = argparse.ArgumentParser()
# Preparamos los dos argumentos con su ayuda
parser.add_argument("--Fecha_inicio", help="Introduce la fecha de inicio del intervalo")
parser.add_argument("--Fecha_fin", help="Introduce la fecha de fin del intervalo")
# Parseamos
args = parser.parse_args()

#Tomamos los valores
fechaInicio = args.Fecha_inicio
fechaFin = args.Fecha_fin

# Llamamos a la función
execute_form(fechaInicio,fechaFin)


# In[ ]:




