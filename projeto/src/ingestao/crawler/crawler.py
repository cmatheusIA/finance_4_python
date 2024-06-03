from time import sleep
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import io
import requests
import json
import os
import investpy as invpy
from bs4 import BeautifulSoup as bs

# Definindo os headers com um User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

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

        
        caminho_chave_json = os.path.join(diretorio_avo, caminho_relativo)
        with open(caminho_chave_json) as f:
            api_keys = json.load(f)
        #alpha_vantage_key = api_keys['alpha_vantage']
        return api_keys

    def robot_indices(self, sleep_num=0, driver_flag=False,indice=None):
        """
            This function performs the following tasks:
            
            * Prints information messages to the console.
            * Sets the index number for the current run.
            * Builds the URL for the index page based on the index number.
            * Downloads the HTML content of the index page using WebDriver.
            * Enters the sector name into a search box on the page.
            * Clicks the 'Download' button on the page.
            * Waits for the download to complete.
            * Moves the downloaded file to a directory based on the index number.
            
            Parameters:
            -----------
            sleep_num: int (optional)
                The number of seconds to wait between actions. Default is 0.
            driver_flag: bool (optional)
                Whether to use headless mode with WebDriver. Default is False.
            indice: int (optional)
                The index number for the current run. If not provided, it will be set to the value of `self.indice`.
            
            Returns:
            -------
            None
        """
        print("[INFO] Iniciando robo de coleta")
        if self.indice==None:
            self.indice=indice
        
        url = f"https://sistemaswebb3-listados.b3.com.br/indexPage/day/{self.indice}?language=pt-br"
        print(f"[INFO] Dados coletados do indice {self.indice}")
        print(f"[INFO] Link onde vamos fazer download {url}")

        print("[INFO] Configurando  e iniciando  webdriver")
        if driver_flag==True:
            driver = webdriver.Chrome()
        else:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")


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
        pasta_data = os.path.join(diretorio_avo,'data/BR')
        subpasta = os.path.join(pasta_data, f'{self.indice}')
        subpasta = os.path.join(pasta_data, str(self.indice))

        # Verifica se a subpasta existe e a cria se necessário
        print('[INFO] Checando se o diretorio ja existe')
        if not os.path.exists(subpasta):
            os.makedirs(subpasta)

        # Move o arquivo CSV para a subpasta
        print('[INFO] Salvando os arquivos')
        arquivo_csv = arquivos[0]
        novo_caminho = os.path.join(subpasta, arquivo_csv)
        os.rename(arquivo_csv, novo_caminho)
        print(f'[INFO] Arquivos salvos no caminho = {novo_caminho}')
        return arquivo_csv

    
    def robot_usa_tickets(self):
        """
            Method that retrieves all daily stock prices for the US stock market,
            over the last 20 years using Alpha Vantage API.

            Returns:
                None: The function does not return anything, but instead exports a JSON file 
                containing the stock data to a folder named "USA" in the current working directory.
        """
        print("[INFO] Iniciando robo de coleta")
        print("[INFO] Carregando keys para usar a api alpha vantage")
        _keys = self.__get_keys()
        key = _keys['alpha_vantage']

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&state=active&apikey={key}'

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
    


    def get_countries(self):
        return invpy.stocks.get_stock_countries()


    def get_symbol_by_country(self, country: str) -> Tuple[pd.DataFrame, List[str]]:
        """
        Retrieves the symbols of stocks in a given country.
        
        Parameters
        ----------
        country : str
            The country whose stock symbols are desired.
        
        Returns
        -------
        stocks : DataFrame
            A DataFrame with columns 'name', 'full_name', and 'symbol' for each stock in the country.
            The 'symbol' column will be appended with '.SA' for convenience.
        list_of_symbols : List[str]
            A list of the unique stock symbols found in the country.
        """
        stocks = invpy.stocks.get_stocks(country=country)
        stocks = stocks[['name', 'full_name', 'symbol']]
        stocks['symbol'] = stocks['symbol'] + '.SA'
        list_of_symbols = stocks['symbol'].tolist()
        
        return stocks, list_of_symbols
    
    def getFIIS(self) -> Tuple[pd.DataFrame, List[str]]:
        url = "https://fiis.com.br/lista-de-fundos-imobiliarios/"
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "html.parser")
        divs = soup.find_all("div" ,attrs= {"class":"tickerBox"} )
        fiis = []
        for fii in divs:

            fiis.append(
                {
                    "symbol" : fii.find("div" ,attrs = {"class":"tickerBox__title"}).text,
                    "type" : fii.find("span" ,attrs= {"class":"tickerBox__type"}).text,
                    "desc" : fii.find("div" ,attrs= {"class":"tickerBox__desc"}).text
                }
            )
        df = pd.DataFrame(fiis)
        df["type"] = df["type"].apply(lambda x: str(x).replace(":",""))
        df_fii = df.iloc[5:]
        df_fii['symbol']=df_fii['symbol'] + '.SA'
        list_of_symbols = df_fii['symbol'].tolist()
        return df_fii, list_of_symbols