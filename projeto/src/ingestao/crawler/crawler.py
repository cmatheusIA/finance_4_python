from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import io
import requests
import json
import os

class Crawler:
    def __init__(self,indice=None) -> None:
        self.indice = indice
        self.path_driver = f'{os.path.expanduser("~")}/chromedriver/stable/chromedriver'
        self.diretorio_Atual =  os.getcwd()
        
    
    def __get_keys(self):
        #diretorio_atual = os.getcwd()

        # Subir dois níveis para o diretório "avo"
        diretorio_avo = os.path.abspath(os.path.join(self.diretorio_Atual, "../.."))
        caminho_relativo = os.path.join('utils', 'keys.json')

        # Construir o caminho relativo para 'src/utils/keys.json'
        caminho_chave_json = os.path.join(diretorio_avo, caminho_relativo)
        with open(caminho_chave_json) as f:
            api_keys = json.load(f)
        #alpha_vantage_key = api_keys['alpha_vantage']
        return api_keys

    def robot(self, sleep_num=0, driver=None,indice=None):
        print("[INFO] Iniciando robo de coleta")
        if self.indice==None:
            self.indice=indice
        
        url = f"https://sistemaswebb3-listados.b3.com.br/indexPage/day/{self.indice}?language=pt-br"
        print(f"[INFO] Dados coletados do indice {self.indice}")
        print(f"[INFO] Link onde vamos fazer download {url}")


        if driver==None:
            print("[INFO] Configurando  e iniciando  webdriver")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")

            # Set path to chromedriver as per your configuration
            #homedir = os.path.expanduser("~")
            #webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")
            service= Service(self.path_driver)
            driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f"[INFO] acesando o {url}")
        driver.get(url)
        sleep(sleep_num)
        driver.find_element(By.ID,'segment').send_keys("Setor de Atuação")
        sleep(sleep_num)

        driver.find_element(By.LINK_TEXT,"Download").click()
        sleep(sleep_num)
        print(f"[INFO] Iniciando o processo de configuração do buffer para salvar o arquivo")
        #arquivos = !ls -1t *.csv # lista todos os arquivos com a extensão ".csv" no diretório atual, em ordem decrescente de data de modificação
        #diretorio_atual = os.getcwd()

        # Lista todos os arquivos com a extensão ".csv" no diretório atual
        arquivos = [arquivo for arquivo in os.listdir(self.diretorio_Atual) if arquivo.endswith(".csv")]
        if not arquivos:
            return None
        print('[INFO] Criando diretorio')
        #diretorio_atual = os.getcwd()

        # Subir dois níveis para o diretório "avo"
        diretorio_avo = os.path.abspath(os.path.join(self.diretorio_Atual, "../.."))
        pasta_data = os.path.join(diretorio_avo,'data')
        subpasta = os.path.join(pasta_data, f'BR/{self.indice}')
        subpasta = os.path.join(pasta_data, str(self.indice))

        # Verifica se a subpasta existe e a cria se necessário
        print('[INFO] Checando se o diretorio ja existe')
        if not os.path.exists(subpasta):
            #os.chmod(subpasta, 0o777)
            os.makedirs(subpasta)

        # Move o arquivo CSV para a subpasta
        print('[INFO] Salvando os arquivos')
        arquivo_csv = arquivos[0]
        novo_caminho = os.path.join(subpasta, arquivo_csv)
        os.rename(arquivo_csv, novo_caminho)
        print(f'[INFO] Arquivos salvos no caminho = {novo_caminho}')

    
    def robot_usa_tickets(self):
        print("[INFO] Iniciando robo de coleta")
        print("[INFO] Carregando keys para usar a api alpha vantage")
        _keys = self.__get_keys()
        key = _keys['alpha_vantage']

        url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={key}'

        print("[INFO] Iniciando requisição")
        try:
            response = requests.get(url)
        except:
            return "ERROR na Requisição !! So deus sabe o motivo !!!"
        print("[INFO] Criando diretorio para salvar os dados")
        diretorio_avo = os.path.abspath(os.path.join(self.diretorio_Atual, "../.."))

        pasta_data = os.path.join(diretorio_avo,'data')
        subpasta = os.path.join(pasta_data, 'USA')

        # Verifica se a subpasta existe e a cria se necessário
        print("[INFO] Checando se o diretorio ja existe")
        if not os.path.exists(subpasta):
            os.makedirs(subpasta)
        print("[INFO] Salvando os dados")
        df = pd.read_csv(io.StringIO(response.text))
        df.to_json(f'{subpasta}/tickers.json',orient="records", default_handler=str)


        