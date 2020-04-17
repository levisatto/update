#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime as dt


# In[2]:


# 1° PASSO
# USUARIOS CADASTRADOS / ENTRADAS NOVAS / BAIRROS ROTAS
entrada = pd.read_excel('entrada.xlsx', sheet_name='escalados2')
usuarios = pd.read_excel('usuarios.xlsx')
rotas_bairros = pd.read_excel('rotas_final.xlsx')


# In[3]:


standard_header = ['filial', 'matricula', 'nome', 'rua', 'numero', 'bairro', 'zona', 'horario', 'status_frequencia']


# In[4]:


usuarios.columns = standard_header


# In[5]:


header_filtro = ['matricula', 'nome', 'horario', 'serviço', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'situação', 'telefone', 'tag', 'filial']


# In[6]:


# LIMPEZA E UNIFORMIZAÇÃO DOS BAIRROS


# In[7]:


import unicodedata
import re
def RemoverCaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)


# In[8]:


clean_bairros = []
for each in usuarios['bairro']:
    caracteres_especiais = RemoverCaracteresEspeciais(each)
    clean_bairros.append(caracteres_especiais)


# In[9]:


usuarios['bairro'] = clean_bairros
usuarios['bairro'] = usuarios['bairro'].str.strip().str.upper()


# In[10]:


entrada['rua'] = entrada['rua'].str.replace('Q ', 'QUADRA ')
entrada['cidade'] = entrada['cidade'].str.upper().str.strip()
entrada['filial'] = entrada['filial'].str.upper().str.strip()
entrada['matricula'] = entrada['matricula'].astype(int)


# In[11]:


# 2° PASSO
# VERIFICAR FILIAL SEMPRE

filtro_filial = entrada[entrada['filial'] == 'DIRCEU'] # FILIAL


# In[12]:


# STATUS USUARIO
usuarios_ativos = usuarios[usuarios['status_frequencia'] == 'ATIVO']
usuarios_inativos = usuarios[usuarios['status_frequencia'] == 'INATIVO']


# In[13]:


# ENTRADA NOVA FILTRO FILIAL/ATIVO
# ENTRADA NOVA FILTRO FILIAL/ATIVO
matricula_usuarios_ativos = usuarios_ativos['matricula'] # USUARIO ATIVOS NO CADASTRO FIXO
matricula_usuarios_inativos = usuarios_inativos['matricula'] # USUARIOS INATIVOS NO CADASTRO FIXO
matricula_entradas_filial = filtro_filial['matricula'] # ENTRADAS NOVAS POPR FILIAL
matricula_usuarios_todos = usuarios['matricula'] # TODAS AS ENTRADAS


# In[14]:


# ENTRADAS ATIVAS
filtro_entradas_ativas = []
filtro_entradas_inativos_novos = []
for each in matricula_usuarios_ativos:
    for num in matricula_entradas_filial:
        if num == each:
            filtro_entradas_ativas.append(num)
            
print(filtro_entradas_ativas, len(filtro_entradas_ativas))


# In[15]:


matriculas_novas_inativas = list(set(matricula_entradas_filial) - set(filtro_entradas_ativas))


# In[16]:


# ENTRADAS INATIVAS
filtro_entradas_inativas = []
for each in matricula_usuarios_inativos:
    for num in matriculas_novas_inativas:
        if num == each:
            filtro_entradas_inativas.append(num)
            
print(filtro_entradas_inativas, len(filtro_entradas_inativas))


# In[17]:


# ENTRADAS NOVAS
filtro_entradas_novas = list(set(matriculas_novas_inativas) - set(filtro_entradas_inativas))
print(filtro_entradas_novas, len(filtro_entradas_novas))


# In[18]:


entradas_ativas_dirceu = entrada[entrada['matricula'].isin(filtro_entradas_ativas)]
print(len(entradas_ativas_dirceu))
filtro_entradas_ativas_dirceu = pd.DataFrame(entradas_ativas_dirceu)
filtro_entradas_ativas_dirceu['status_frequencia'] = 'ATIVO'
filtro_entradas_ativas_dirceu = filtro_entradas_ativas_dirceu.set_index('matricula')


# In[19]:


entradas_novas_dirceu = entrada[entrada['matricula'].isin(filtro_entradas_novas)]
print(len(entradas_novas_dirceu))
filtro_entradas_novas_dirceu = pd.DataFrame(entradas_novas_dirceu)
filtro_entradas_novas_dirceu['status_frequencia'] = 'NOVO'
filtro_entradas_novas_dirceu = filtro_entradas_novas_dirceu.set_index('matricula')


# In[20]:


# DADOS DAS ENTRADAS NOVAS E ATIVAS CONCATENADAS

novos_ativos = pd.concat([filtro_entradas_novas_dirceu, filtro_entradas_ativas_dirceu])


# In[21]:


clean_bairros_novos = []
for each in novos_ativos['bairro']:
    caracteres_especiais = RemoverCaracteresEspeciais(each)
    clean_bairros_novos.append(caracteres_especiais)
novos_ativos['bairro'] = clean_bairros_novos
novos_ativos['bairro'] = novos_ativos['bairro'].str.strip().str.upper()


# In[22]:


novos_ativos.to_excel('novos_ativos.xlsx')


# In[23]:


novos_ativos['horario'].sort_values().unique()


# In[24]:


novos_ativos['horario'] = novos_ativos['horario'].astype(str).str.replace(':', '').str.strip().astype(int)
horarios_dirceu = novos_ativos['horario']
horarios_dirceu.unique()


# In[25]:


# HORARIOS DE SAIDA

dirceu_horario_01 = novos_ativos[(novos_ativos['horario'] >= 220000) & (novos_ativos['horario'] <= 233500)]
dirceu_horario_02 = novos_ativos[((novos_ativos['horario'] > 233500) & (novos_ativos['horario'] < 240000)|(novos_ativos['horario'] >= 0) & (novos_ativos['horario'] <= 3500) )]
dirceu_horario_03 = novos_ativos[(novos_ativos['horario'] > 3500) & (novos_ativos['horario'] <= 15500)]

# COLETA

dirceu_horario_04 = novos_ativos[(novos_ativos['horario'] > 50000) & (novos_ativos['horario'] <= 55500)] 


# In[26]:


print(dirceu_horario_01.shape[0], dirceu_horario_02.shape[0], dirceu_horario_03.shape[0], dirceu_horario_04.shape[0])


# In[27]:


norte = rotas_bairros['NORTE']
sul = rotas_bairros['SUL']
leste = rotas_bairros['LESTE']
centro = rotas_bairros['CENTRO']
sdb = rotas_bairros['SDB']
sdc = rotas_bairros['SDC']


# In[28]:


import numpy as np
dirceu_horario_01_rota_norte = dirceu_horario_01[dirceu_horario_01['bairro'].isin(norte)]
dirceu_horario_01_rota_sul = dirceu_horario_01[dirceu_horario_01['bairro'].isin(sul)]
dirceu_horario_01_rota_leste = dirceu_horario_01[dirceu_horario_01['bairro'].isin(leste)]
dirceu_horario_01_rota_centro = dirceu_horario_01[dirceu_horario_01['bairro'].isin(centro)]
dirceu_horario_01_rota_sdb = dirceu_horario_01[dirceu_horario_01['bairro'].isin(sdb)]
dirceu_horario_01_rota_sdc = dirceu_horario_01[dirceu_horario_01['bairro'].isin(sdc)]
dirceu_horario_01_rota_timon = dirceu_horario_01[dirceu_horario_01['cidade'] == 'TIMON']
dropar = ['serviço', 'complemento', 'situação', 'telefone', 'tag', 'filial']
dirceu_horario_01_rota_norte = dirceu_horario_01_rota_norte.drop(dropar , axis=1)
dirceu_horario_01_rota_sul = dirceu_horario_01_rota_sul.drop(dropar , axis=1)
dirceu_horario_01_rota_leste = dirceu_horario_01_rota_leste.drop(dropar , axis=1)
dirceu_horario_01_rota_centro = dirceu_horario_01_rota_centro.drop(dropar , axis=1)
dirceu_horario_01_rota_sdb = dirceu_horario_01_rota_sdb.drop(dropar , axis=1)
dirceu_horario_01_rota_sdc = dirceu_horario_01_rota_sdc.drop(dropar , axis=1)
dirceu_horario_01_rota_timon = dirceu_horario_01_rota_timon.drop(dropar , axis=1)


# In[29]:


dirceu_horario_01_rota_norte['zona'] = 'NORTE'
dirceu_horario_01_rota_norte['assinatura'] = np.nan


# In[30]:


dirceu_horario_01_rota_sul['zona'] = 'SUL'
dirceu_horario_01_rota_sul['assinatura'] = np.nan


# In[31]:


dirceu_horario_01_rota_leste['zona'] = 'LESTE'
dirceu_horario_01_rota_leste['assinatura'] = np.nan


# In[32]:


dirceu_horario_01_rota_centro['zona'] = 'CENTRO'
dirceu_horario_01_rota_centro['assinatura'] = np.nan


# In[33]:


dirceu_horario_01_rota_sdb['zona'] = 'SDB'
dirceu_horario_01_rota_sdb['assinatura'] = np.nan


# In[34]:


dirceu_horario_01_rota_sdc['zona'] = 'SDC'
dirceu_horario_01_rota_sdc['assinatura'] = np.nan


# In[35]:


dirceu_horario_01_rota_timon['zona'] = 'TIMON'
dirceu_horario_01_rota_timon['assinatura'] = np.nan


# In[38]:


dirceu_rotas_horario_01 = pd.ExcelWriter('dirceu_horario_01.xlsx', engine='xlsxwriter')
dirceu_horario_01_rota_sul.to_excel(dirceu_rotas_horario_01, sheet_name='SUL')
dirceu_horario_01_rota_norte.to_excel(dirceu_rotas_horario_01, sheet_name='NORTE')
dirceu_horario_01_rota_leste.to_excel(dirceu_rotas_horario_01, sheet_name='LESTE')
dirceu_horario_01_rota_centro.to_excel(dirceu_rotas_horario_01, sheet_name='CENTRO')
dirceu_horario_01_rota_sdb.to_excel(dirceu_rotas_horario_01, sheet_name='SDB')
dirceu_horario_01_rota_sdc.to_excel(dirceu_rotas_horario_01, sheet_name='SDC')
dirceu_horario_01_rota_timon.to_excel(dirceu_rotas_horario_01, sheet_name='TIMON')
dirceu_rotas_horario_01.save()


# In[ ]:




