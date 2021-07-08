#!/usr/bin/env python
# coding: utf-8

# # EC5

# 1) Lee el archivo llamado "penguins.csv". Esta es una base de pingüinos de la Antártida que viven en diferentes islas y pertenecen a 3 tipos: Adelie, Gentoo y Chinstrap.
# 
# (es una base muy adorable y pueden leer más sobre ella [aquí](https://allisonhorst.github.io/palmerpenguins/). Esta surgió como alternativa a la famosísima iris, publicada por primera vez en _Annals of Eugenics_ cuya infame historia se remonta a la defensa de la Eugenesia).

# In[1]:


import pandas as pd


# In[2]:


penguins = pd.read_csv('penguins.csv')
penguins


# 2) Elimina las observaciones que tienen valor perdido (_missing_) en `sex` y `body_mass_g`.

# In[28]:


penguinsc = penguins.copy(deep = True)

penguinsce = penguinsc.dropna(subset=['sex', 'body_mass_g'])

penguinsce


# 3) Haz una tabulación cruzada en donde cuentes el número de pingüinos, por por especie, que hay en cada una de las islas. Este nuevo dataframe tendrá como filas a las especies (_species_) y las nuevas columnas, las islas (_island_). Usa `pivot_table`.

# In[36]:


penguinsce['nueva columna'] = 1

penguinsce


# In[40]:


resumen = penguinsce.pivot_table(index='species', columns='island', values='Unnamed: 0', aggfunc='count')

resumen


# In[ ]:




