from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
from parsel import Selector

class Scraper:
    def __init__(self):
        dados = []
        driver = self.iniciar_driver("https://www.amazon.com.br")
        # Realizando a pesquisa no site da Amazon
        self.pesquisar(driver, "smartphone xiaomi")
        # Colentando as informações
        self.coletar_dados(driver, dados)
        # Passando por outras paginas
        self.navegar_paginas(driver, dados)
        # Salvando os resultadosg
        self.salvar_dados(dados)
        self.fechar(driver)

    def iniciar_driver(self, site):
        driver = webdriver.Chrome()
        driver.get(site)
        sleep(1)
        return driver

    def pesquisar(self, driver, texto): 
        pesquisa = driver.find_element(By.CSS_SELECTOR, "input#twotabsearchtextbox")
        pesquisa.send_keys(texto)
        sleep(2)
        pesquisa.send_keys(Keys.ENTER)
        print('pesquisa realizada com sucesso !')       
        sleep(1)

    def coletar_dados(self, driver, dados):
            print("Coletando dados...")
            sleep(2)
            response = Selector(driver.page_source)
            # Divs com informações de cada produto
            produtos = response.xpath('//div[@class="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"]')
            for produto in produtos:
                # Nomes
                nome = produto.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").extract_first()
                # Preços
                preco = produto.xpath('.//div[@data-cy="price-recipe"]//span[@class="a-price"]//span[@aria-hidden="true"]')\
                                    .xpath('string()').extract_first()
                # Avaliação
                avaliacao = produto.xpath('.//div[@class="a-row a-size-small"]/span[1]//text()').extract_first()
                avaliacao = " ".join(avaliacao.split(" ")[0:3]) if avaliacao != None else avaliacao
                dados.append({ "Nome" : nome,
                        "Preço" : preco,
                        "Avaliação" : avaliacao
                        })
    
    def navegar_paginas(self, driver, dados):
        # Percorrer cada página:
        while True:
            try:
                # Localizar o botão Próximo
                btn_proximo = driver.find_element(By.CSS_SELECTOR,
                                    "a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
                sleep(2)
                print("Indo para a próxima página...")
                btn_proximo.click()
                self.coletar_dados(driver, dados)
                driver.implicitly_wait(5)
            except:
                break

    def salvar_dados(self, dados):
        print("Salvando os dados....")
        with open("dados.csv", "w", newline="", encoding='utf-8') as arquivo_csv:
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
            # Escrever cabeçalho
            escritor_csv.writeheader()
            # Escrever dados
            for linha in dados:
                escritor_csv.writerow(linha)
        sleep(1)
        print("Dados salvos com sucesso")
    
    def fechar(self, driver):
        return driver.quit()

Scraper()