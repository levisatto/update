#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import unicodedata
import re


# In[2]:


standard_header = ['bairros', 'rotas']
zonas = pd.read_excel('zonas_bairros.xlsx', names=standard_header)
print(zonas.columns)


# In[3]:


def RemoverCaracteresEspeciais(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
bairros_sem_caracteres_especiais = []
for each in zonas['bairros']:
    clean = RemoverCaracteresEspeciais(each)
    bairros_sem_caracteres_especiais.append(clean)
zonas['bairros'] = bairros_sem_caracteres_especiais


# In[4]:


zonas['bairros'] = zonas['bairros'].str.lower().str.strip().str.replace('2', 'ii')
zonas['rotas'] = zonas['rotas'].str.lower().str.strip()
print(zonas['rotas'].unique())
bairros_unicos = zonas['bairros'].unique()
bairros_unicos = pd.DataFrame(bairros_unicos)
bairros_unicos[0].value_counts().sort_values(ascending=False)


# In[5]:


bairro_centro = zonas['rotas'] == 'centro'
zona_centro = zonas.loc[bairro_centro, 'bairros'].str.upper()
zona_centro = zona_centro.str.strip()
zona_centro = zona_centro.unique()

bairro_norte = zonas['rotas'] == 'norte'
zona_norte = zonas.loc[bairro_norte, 'bairros'].str.upper().str.strip()
zona_norte = zona_norte.unique()

bairro_leste = zonas['rotas'] == 'leste'
zona_leste = zonas.loc[bairro_leste, 'bairros'].str.upper().str.strip()
zona_leste = zona_leste.unique()

bairro_sul = zonas['rotas'] == 'sul'
zona_sul = zonas.loc[bairro_sul, 'bairros'].str.upper().str.strip()
zona_sul = zona_sul.unique()

bairro_sdc = zonas['rotas'] == 'sdc'
zona_sdc = zonas.loc[bairro_sdc, 'bairros'].str.upper().str.strip()
zona_sdc = zona_sdc.unique()

bairro_sdb = zonas['rotas'] == 'sdb'
zona_sdb = zonas.loc[bairro_sdb, 'bairros'].str.upper().str.strip()
zona_sdb = zona_sdb.unique()

bairro_timon = zonas['rotas'] == 'timon'
zona_timon = zonas.loc[bairro_timon, 'bairros'].str.upper().str.strip()
zona_timon = zona_timon.unique()


# In[6]:


zonas_final_nomes = ['SDB', 'SDC', 'SUL', 'LESTE', 'NORTE', 'CENTRO','TIMON']
zonas_final = zona_sdb, zona_sdc, zona_sul, zona_leste, zona_norte, zona_centro, zona_timon
rotas_final = pd.DataFrame(zonas_final)

rotas_final = rotas_final.T
rotas_final.columns = zonas_final_nomes
print(rotas_final)

rotas_final.to_excel('rotas_final.xlsx')


# In[ ]:




