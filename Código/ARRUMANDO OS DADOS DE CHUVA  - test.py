import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

def iniciar_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=service, options=options)

def obter_dados_chuva(driver, data_inicio, data_fim):
    url = "https://www.worldweatheronline.com/guarapuava-weather-history/parana/br.aspx"
    driver.get(url)

    elementos_agrupados = [[] for _ in range(365)]
    cont = 0

    while data_inicio <= data_fim:
        search_field = driver.find_element(By.ID, 'ctl00_MainContentHolder_txtPastDate')
        search_field.clear()
        search_field.send_keys(data_inicio.strftime('%d/%m/%Y'))

        search_button = driver.find_element(By.ID, 'ctl00_MainContentHolder_butShowPastWeather')
        search_button.click()
        time.sleep(5)

        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//div[@class="col mr-1" and contains(text(), "mm")]')))

        elementos = driver.find_elements(By.XPATH, '//div[@class="col mr-1" and contains(text(), "mm")]')

        for i in elementos:
            elementos_agrupados[cont].append(i.text[:-3])

        data_inicio += timedelta(days=1)
        cont += 1

    return elementos_agrupados

def salvar_dados(elementos_agrupados):
    with open("dados_chuva.txt", "w") as arq:
        for dia in elementos_agrupados:
            arq.write(','.join(dia))
            arq.write('\n')

def processar_dados(elementos_agrupados):
    elementos_anos_c = []

    for i in elementos_agrupados:
        if len(i) == 16:
            sub_lista = i[4:-1]
        elif len(i) == 15:
            sub_lista = i[4:]
        else:
            continue
        elementos_anos_c.append(sub_lista)

    valores_ano = [[] for _ in range(len(elementos_anos_c[0]))]

    for lista in elementos_anos_c:
        for i, elemento in enumerate(lista):
            valores_ano[i].append(elemento)

    return valores_ano

def agrupar_por_mes(valores_ano):
    def cria_mes(valores_ano):
        data_1 = datetime(2023, 1, 1)
        data_2 = datetime(2023, 12, 31)
        lista_meses = []
        mes = data_1.strftime("%m")
        dias = []

        while data_1 <= data_2:
            for i in valores_ano:
                dias.append(i)
                data_1 += timedelta(days=1)

                if mes != data_1.strftime("%m"):
                    lista_meses.append(dias)
                    dias = []
                    mes = data_1.strftime("%m")

            if dias:
                lista_meses.append(dias)

        return lista_meses

    return [cria_mes(i) for i in valores_ano]

def calcular_media_mensal(meses_certo):
    media_meses = []

    for ano in meses_certo:
        for mes in ano:
            media = sum(float(dia) for dia in mes) / len(mes)
            media_meses.append(round(media, 2))

    return media_meses

def agrupar_por_ano(media_meses_round):
    lista_anos = []
    tamanho_grupo = 12
    for i in range(0, len(media_meses_round), tamanho_grupo):
        grupo = media_meses_round[i:i + tamanho_grupo]
        lista_anos.append(grupo)
    return lista_anos

def main():
    driver = iniciar_driver()
    data_inicio = datetime(2023, 1, 1)
    data_fim = datetime(2023, 12, 31)

    elementos_agrupados = obter_dados_chuva(driver, data_inicio, data_fim)
    salvar_dados(elementos_agrupados)

    valores_ano = processar_dados(elementos_agrupados)
    meses_certo = agrupar_por_mes(valores_ano)
    media_meses_round = calcular_media_mensal(meses_certo)
    lista_anos = agrupar_por_ano(media_meses_round)

    df = pd.DataFrame(media_meses_round)
    df.to_csv('chuva_mes.csv', index=False, header=False)

    print(lista_anos)

if __name__ == "__main__":
    main()
