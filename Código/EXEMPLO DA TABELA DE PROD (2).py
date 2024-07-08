#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORTANDO AS BIBILIOTECAS NECESSÁRIAS
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# In[2]:


#DEFINE CONFIGURAÇÕES PARA O CHORME


chrome_options = webdriver.ChromeOptions()
#options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') #NÃO ABRIR JANELA
chrome_options.add_argument('--no-sabdbox')#DESABILITA MEDIDA DE SEGURANÇA
chrome_options.add_argument('--disable-dev-shm-usage')#DESATIVA O USO DE MEMÓRIA COMPARTILHADA, NÃO SEI EXATAMENTE


# In[29]:


driver = webdriver.Chrome(options=chrome_options)#INICIALIZADA O CHROME COM AS CONFIGURAÇÕES ACIMA


# In[30]:


driver.get('https://sidra.ibge.gov.br/tabela/6588#/n3/41/v/36/p/all/c48/39435/l/v,p+c48,t/resultado')#CARREGA O LINK ESCOLHIDO


# In[31]:


print(driver.page_source) #imprime o código da página


# In[32]:


#GRAVA O CÓDIGO EM UM ARQUIVO XML
with open("Prod_Hec_mes1.xml", "w") as arq:
    arq.write(driver.page_source)


# In[33]:


#GRAVA O CÓDIGO EM UM ARQUIVO DE TEXTO
#O 'w' significa write que é escrever em inglês, ou seja este arquivo esta aberto em modo de escrita 
with open("Prod_Hec_mes1.txt", "w") as arq:
    tag_td1 = soup.find_all(title='Quilogramas por Hectare')
    for tag in tag_td1:
        arq.write(tag.text)
        arq.write('\n')


# In[39]:


#ABRE O ARQUIVO XML
#O 'r' significa read que é ler em inglês, ou seja este arquivo está aberto em modo de leitura
#se está em modo de leitura não pode ser editado
arquivoXML = open('Prod_Hec_mes1.xml', 'r')
soup = BeautifulSoup(arquivoXML.read(), 'html.parser')


# In[40]:


soup


# In[41]:





#COM O SOUP CRIADO, É POSSÍVEL ENCONTRAR OS VALORES
#EXISTE MAIS DE UMA TABELA NA PÁGINA,
#TEMOS QUE ENCONTRAR A QUE PRECISAMOS


#OLHANDO A TABELA NO LINK É INDENTEFICÁVEL QUE OS VALORES ESTÃO ASSOCIADOS A HECTARES



#OLHANDO O SOUP E ENCONTRANDO A TABELA ONDE ESTÃO OS VALORES ESTE PADRÃO SE REPETIRÁ <td class="x-col-68" title="Hectares">57.800</td>
#SENDO ASSIM É SÓ PROCURAR PELO TEXTO QUE ESTÁ CONTIDO NO title = "Hectares"




tag_td = soup.find_all(class_='texto-rotulo')
for tag in tag_td:
    print(tag.text)


# In[42]:


tag_td


# In[43]:



with open("Pdata.txt", "w") as arq:
    for tag in tag_td[82:214]:
        arq.write(tag.text)
        arq.write('\n')


# In[46]:


meses_csv = []
for tag in tag_td[82:214]:
    meses_csv.append(tag.text)
    


# In[47]:


df3 = pd.DataFrame(meses_csv)
df3.to_csv('q.csv', index=False, header=False)


# In[44]:


#CADA DADO CORRENDO A UM MÊS
#PARA SABER QUANTOS MESES FORAM ENCONTRADOS
len(tag_td)


# In[ ]:


data2 = soup.find_all(title= 'rotulo coluna')
data2
for i in data2:
    print(i)


# In[ ]:



#ESCREVENDO OS DADOS DE 2013 A 2023;

with open("Prod_Hec_mes1.txt", "w") as arq:
    for tag in tag_td1[76:208]:
        arq.write(tag.text)
        arq.write('\n')


# In[ ]:


valores_mes = []
for tag in tag_td1[76:208]:
    valores_mes.append(float(tag.text))
    


# In[45]:


valores_mes


# In[ ]:


df = pd.DataFrame(valores_mes)
df.to_csv('q.csv', index=False, header=False)


# In[ ]:


lista_anos = []
tamanho_grupo = 12
for i in range(0, len(valores_mes), tamanho_grupo):
    grupo = valores_mes[i:i + tamanho_grupo]
    lista_anos.append(grupo)
    
    


# In[ ]:


lista_anos


# In[ ]:


for i in lista_anos:
    print(len(i))


# In[ ]:


with open("Prod_Hec_mes2.txt", "w") as arq:
    for meses in lista_anos:
        for mes in meses:
            arq.write(mes)
            arq.write(',')


# In[ ]:


media_meses = []
media = 0

for ano in lista_anos:
    for mes in ano:
        media = (sum(float(mes)))/(len(mes))
        media_meses.append(media)
        media = 0


# In[ ]:


#OBSERVANDO A TABELA ELA VAI DE SETEMBRO DE 2006 A ABRIL 2024
#SÃO 212 MESES
#O 424 É PORQUE EM 2 TABELAS APARECEM VALORES POR HECTARES
#NA DE ÁREA PLANTADA E ÁREA COLHIDA
#ENTÃO OS 212 PRIMEIROS DE SÃO DE ÁREA PLANTADA
#E OS OUTROS 212 DE ÁREA COLHIDA

