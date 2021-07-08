#!/usr/bin/env python
# coding: utf-8

# # Tarea 3 (Pandas)
# 
# Hora de entrega: Viernes 28 de Mayo, 11:59 pm
# 
# Nombrar al archivo de la siguiente manera: Apellido_código.  
# Ejemplo:  Solis_20060983
# 
# Entregar la tarea en esta plantilla, no usar una adicional a esta. 
# 
# 
# 

# - Antes que nada, ¡necesitamos nuestros datos! 
# 1. Ve a la página de microdatos del [INEI](http://iinei.inei.gob.pe/microdatos/). 
# 2. Ve a "Consulta por encuestas" y ve a ENAHO metodología ACTUALIZADA. 
# 3. Elige aquella que dice "Condiciones de Vida y Pobreza - ENAHO" (la que no es panel). 
# 4. Elige el año 2020, y en período, elige la anual.   
# 5. Descarga los **archivos CSV** del Código módulo 1 (Características de la vivienda y el hogar) y el módulo 34 (Sumarias - Variables Calculadas). 
# 
# Esta tarea está pensada en ser desarrollada con los CSV (no los .dta o .sav, que son los archivos de stata ó spss respectivamente).
# 
# 
# La ENAHO es una encuesta muy amplia que está distribuida en varios módulos. En esta tarea veremos cómo podemos utilizar información de varios de estos módulos para sacar datos interesantes. 

# 1. Lee ambos archivos csv con pandas y asígnales un nombre para que puedas trabajar con ambos como base de datos. (Si es que sale un error, es debido a que nuestras encuestas están en español y tienen caracteres como ˜ de la ñ o el acento. Por ello, a las opciones de lectura del csv, agrega la siguiente opción ``` encoding = "latin-1" ```. 
# 
# (No olvides importar pandas 🐼)
# 
# 
# En caso tus columnas salgan con el nombre en mayúscula, puedes correr el siguiente comando para cambiarlas a minúsculas:
# 
# ``` python3 
# df.columns= df.columns.str.lower()
# ``` 
# Donde `df` es el nombre del dataframe.   
# (En esta clase no ahondamos en el manejo de strings, pero `lower()` es un método de este tipo de variables para convertir el string a minúscula.)

# In[1]:


import pandas as pd


# In[3]:


viviendas = pd.read_csv('Enaho01-2020-100.csv')


# In[4]:


sumaria = pd.read_csv('Sumaria-2020.csv')


# 2. - ¿Cuáles son las dimensiones de la sumaria? (o el número de filas y columnas).
#    - ¿Cuáles son las dimensiones del módulo de vivienda? (o el número de filas y columnas).

# In[5]:


sumaria.shape 


# In[6]:


viviendas.shape


# 3. En esta oportunidad no necesitaremos todas las variables de la ENAHO para hacer esta tarea. 
# - Quedémonos con las variables ``` CONGLOME VIVIENDA HOGAR MIEPERHO PERCEPHO POBREZA GASHOG2D INGHOG2D ``` de la sumaria. 
# - Quedémonos con las variables ``` CONGLOME VIVIENDA HOGAR RESULT NBI1 NBI2 NBI3 NBI4 NBI5 ``` del módulo de vivienda.
# 
#  
#  Nota: cada una de las variables es:
# - MIEPERHO: número de miembros del hogar. 
# - PERCEPHO: número de perceptores del hogar (que reciben un ingreso). 
# - POBREZA: Pobreza monetaria según la línea de pobreza. 
# - GASHOG2D: Gasto bruto anual del hogar. 
# - INGHOG2D: Ingreso anual neto total del hogar. 
# 
# Necesidades básicas:
# - NBI1: vivienda inadecuada.
# - NBI2: hacinamiento
# - NBI3: vivienda sin servicios higiénicos
# - NBI4: hogares con  niños que no asisten a la escuela.
# - NBI5: hogares con alta dependencia económica 
# 
# CONGLOME, VIVIENDA y HOGAR son los identificadores únicos a nivel de hogar (como un key id).

# In[7]:


needed = ['CONGLOME', 'VIVIENDA', 'HOGAR', 'RESULT', 'NBI1', 'NBI2', 'NBI3', 'NBI4', 'NBI5']
needed1 = ['CONGLOME', 'VIVIENDA', 'HOGAR', 'MIEPERHO', 'PERCEPHO', 'POBREZA', 'GASHOG2D', 'INGHOG2D']

viviendas_small = viviendas[needed]

sumaria_small = sumaria[needed1]


# 4. El módulo vivienda incluye todos los hogares que entraron en el marco muestral, incluso aquellos que no participaron en la ENAHO por diversos motivos. Para eliminar estas viviendas, quedémonos con aquellas cuyo ``` RESULT``` sea igual a 1 ó 2. Almacena este resultado para después.

# In[8]:


cond1 = viviendas_small['RESULT'] == 1

cond2 = viviendas_small['RESULT'] == 2


viviendas_smallr = viviendas_small[(cond1) | (cond2)]
viviendas_smallr


# 

# 5. Queremos calcular una serie de variables (ó columnas nuevas):  
# En sumaria: 
# - Queremos el número de miembros dependientes del hogar . Estos son el número de personas que no perciben un ingreso ó la diferencia entre el total de miembros y el total de perceptores. 
# - Queremos el ingreso mensual promedio por perceptor del hogar.
# - Queremos la diferencia  entre ingreso y gasto del hogar

# In[9]:


sumaria_small['DEPENDIENTES'] = sumaria_small['MIEPERHO'] - sumaria_small['PERCEPHO']

ingreso_mensual = sumaria_small['INGHOG2D'] / sumaria_small['PERCEPHO'] / 12 

sumaria_small['INGRESOxMES'] = ingreso_mensual

dif_ingreso_gas = (sumaria_small['INGHOG2D'] - sumaria_small['GASHOG2D'])

sumaria_small['INGRESO-GASTO'] = dif_ingreso_gas

sumaria_small 


# 6. La variable de `pobreza`, en la sumaria, está codificada como integers 1, 2 y 3. Esto corresponde a:  
# `1`: hogar pobre extremo  
# `2`: hogar pobre no extremo  
# `3`: hogar no  pobre  
# 
# En base a esta variable, crea dos variables más:
# 1. Una variable que tenga `'pobre extremo'`, `'pobre no extremo'` y `'no pobre'` en vez  de 1, 2, 3.
# 2. Una variable que tenga `'pobre'` y `'no pobre'` (ó que englobe a los hogares pobres y pobres no extremos).
# 
# 

# In[10]:


sumaria_small['tipo_pobreza'] = sumaria_small['POBREZA']

diccionario_cambios = {1: 'hogar pobre extremo',
                       2: 'hogar pobre no extremo',3: 'hogar no pobre'}

sumaria_small.replace({'tipo_pobreza' : diccionario_cambios}, inplace = True)

sumaria_small['POBRE O NO'] = sumaria_small['POBREZA']

diccionario_cambioss = {1: 'pobre',
                       2: 'pobre',3: 'no pobre'}

sumaria_small.replace({'POBRE O NO' : diccionario_cambioss}, inplace = True)

sumaria_small


# 7. Queremos saber el promedio de ingresos de los hogares (inghog2d) por nivel de pobreza. Haz un `groupby` para averiguar esto. 
# 
# 
# (Por ejemplo, todos los hogares pobres extremos tendrán un único promedio, y así con las 2 categorías de pobreza adicionales). 

# In[11]:


sumaria[['INGHOG2D', 'POBREZA']].groupby('POBREZA').mean()


# 8. ¡Ahora uniremos los datos!  
# Pero antes un check de sanidad: Verifica que el número  de filas de ambas bases de datos son las mismas (acuérdate que filtramos las observaciones por `result`).  La ENAHO recolecta información de estos 34,490 hogares a través de todos sus módulos. Para utilizar estos módulos a la vez, realizaremos una "unión" (merge).   
# 
# Une ambas bases con un _inner merge_. Recuerda que el id que identifica a cada hogar se compone de ` conglome vivienda hogar`.  

# In[12]:


viviendas_smallr.shape


# In[13]:


sumaria_small.shape


# In[14]:


resultado_merge = pd.merge(viviendas_smallr,
                     sumaria_small,
                    left_on = ['CONGLOME', 'VIVIENDA', 'HOGAR'],
                    right_on = ['CONGLOME', 'VIVIENDA', 'HOGAR'],
                    how = 'inner', indicator = True)
resultado_merge         #no restringir


# 9. Haz un ```groupby``` que agrupe (`agg`) los datos por nivel de pobreza  y la nbi1. Queremos hallar el promedio y la mediana de los ingresos (inghog2d) y los gastos (gashog2d) por el producto cartesiano de las categorías de estas 2 variables - pobreza y nbi 1 -. 
# 
# El producto cartesiano es tan sólo todas las posibles combinaciones entre categorías. 
# En este caso, tendremos:
# - pobre extremo con nbi1
# - pobre extremo sin nbi1
# - pobre no extremo con nbi1
# - pobre no extremo sin nbi1
# - no pobre con nbi1
# - no pobre sin nbi1
# 
# (Este es un  ejemplo de cómo, al cruzar un indicador de pobreza monetaria -pobreza- y pobreza multidimensional-nbis-, podemos seguir observando brechas).

# In[15]:


nueva_agregacion = resultado_merge.groupby(['tipo_pobreza', 'NBI1']).agg(
{'INGHOG2D': ['mean', 'median'], 
 'GASHOG2D': ['mean', 'median']}
).reset_index()

nueva_agregacion


# 10. Crea una variable que nos informe sobre los hogares que tienen las 5 nbis. Esta tomará el valor de 1 si tiene las 5 nbis, 0 en caso contrario (así  tenga 4, 3). 
# 
# Calcula el promedio de miembros dependientes por cada categoría de esta nueva variable. 

# In[16]:


nbiss = resultado_merge['NBI1'] + resultado_merge['NBI2'] + resultado_merge['NBI3'] + resultado_merge['NBI4'] + resultado_merge['NBI5'] 

resultado_merge['NBIs'] = nbiss

cond1 = resultado_merge['NBIs'] == '11111'

resultado_mergenbis = resultado_merge[cond1]

resultado_mergenbis


# 11. Crédito extra: 
# 
# Guarda el dataframe del resultado del ejercicio 9 como un csv. (No es necesario adjuntar este csv, con  que el bloque haya corrido está bien). 

# In[17]:


df = pd.DataFrame(nueva_agregacion)


# In[18]:


df.to_csv('ejercicioo_9.csv')


# **Tarea terminada**    ┗┃・ ■ ・┃┛ 

# (╯°□°）╯︵ ┻━┻

# ٩͡[๏̯͡๏]۶ #tarea culminada :')

# In[ ]:




