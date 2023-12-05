#!/usr/bin/env python
import logging

from .stf_configs import SEARCH_URL, SEARCH_FIELD, HOMEPAGE_IMPLICIT_WAITING_TIME, PAGE_FIELD, \
SEARCH_PAGE_IMPLICIT_WAITING_TIME, XPATH_NUMBER_OF_RESULTS, XPATH_FOR_REPORTER_JUDGE, \
XPATH_FOR_DADOS_COMPLETOS, XPATH_FOR_ID

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class stf_scrapper():

    def __init__(self):
        pass

    def create_webdriver_instance(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')  # disabling extensions
        chrome_options.add_argument("--remote-debugging-port=9222")  # enable debug port
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
        chrome_options.add_argument(f'--user-agent={user_agent}')
        return webdriver.Chrome(options=chrome_options)

    def clean_search_query(self, query):
        """
        Clean the query, transform it into a valid url parameter
        """
        return query.replace(' ', '%20')

    def formatUrl(self, query, page):
        URL = SEARCH_URL.replace(SEARCH_FIELD, query)
        URL = URL.replace(PAGE_FIELD, page)
        return URL

    def parse_string_number_of_results(self, string_number):
        list_string = string_number.split(' ')
        result = list_string[1]
        result = result.replace('.', '')
        return int(result)

    def get_search_result_info(self, query, driver):
        search_url = self.formatUrl(query, '1')  # First page
        print(f'Using base url: {search_url}.')
        driver.get(search_url)
        driver.implicitly_wait(SEARCH_PAGE_IMPLICIT_WAITING_TIME)
        
        try:
            # Espera até que o elemento esteja presente na página
            wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
            result_number = wait.until(
                EC.presence_of_element_located((By.XPATH, XPATH_NUMBER_OF_RESULTS))
            )
        except TimeoutException as e:
            driver.save_screenshot('screenshot.png')  # Salva uma captura de tela
            raise e  # Re-lança a exceção para ser tratada posteriormente ou interromper a execução
        
        print(self.parse_string_number_of_results(result_number.text))
        return result_number.text

    def get_id(self, driver):
        try:
            element = driver.find_element_by_xpath(XPATH_FOR_ID)
            return element.text
        except Exception as e:
            logging.error(f'Failed to extract judgment date: {e}')
            return None

    def get_botao_dados_completos(self, driver):
        try:
            element = driver.find_element_by_xpath(XPATH_FOR_DADOS_COMPLETOS)
            return element.text
        except Exception as e:
            logging.error(f'Failed to extract menu: {e}')
            return None

    def extract_text_by_topic_with_child_span(self, topic_text, driver):
        try:
            # Localiza o <h4> que contém o texto do tópico
            topic_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[contains(., '{topic_text}')]/span"))
            )
            # Extrai o texto dentro do <span> que é filho do <h4>
            return topic_element.text.strip()  # Usar strip() para remover espaços em branco extra
        except NoSuchElementException:
            print(f"Não foi possível encontrar o tópico '{topic_text}' na página.")
            return ""  # Retorna uma string vazia se o tópico não for encontrado
        except Exception as e:
            print(f"Ocorreu um erro ao extrair texto para o tópico '{topic_text}': {e}")
            return ""  # Retorna uma string vazia se ocorrer um erro

    def extract_text_by_topic(self, topic_text, driver):
        try:
            # Localiza o tópico pela tag e texto do tópico
            topic_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[contains(., '{topic_text}')]"))
            )
            # Localiza o elemento contendo o texto associado ao tópico
            text_element = topic_element.find_element(By.XPATH, "./following-sibling::div")
            return text_element.text
        except NoSuchElementException:
            print(f"Não foi possível encontrar o tópico '{topic_text}' na página.")
        except Exception as e:
            print(f"Ocorreu um erro ao extrair texto para o tópico '{topic_text}': {e}")
        
        # Retorna uma string vazia se o elemento não for encontrado ou ocorrer um erro
        return ""

    def extract_text_by_h4_topic(self, topic_text), driver:
        try:
            # Localiza o <h4> que contém o texto do tópico
            topic_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[contains(text(), '{topic_text}')]"))
            )
            # O texto desejado está no mesmo <h4> que o tópico, então retornamos o texto do elemento.
            # Se o texto desejado estiver em um elemento após o <h4>, você deve ajustar o seletor abaixo.
            return topic_element.text.strip()  # Retira espaços em branco do início e do fim
        except NoSuchElementException:
            print(f"Não foi possível encontrar o tópico '{topic_text}' na página.")
            return ""  # Retorna uma string vazia se o tópico não for encontrado
        except Exception as e:
            print(f"Ocorreu um erro ao extrair texto para o tópico '{topic_text}': {e}")
            return ""  # Retorna uma string vazia se ocorrer um erro

    def extract_information(self):
        info = {
            'id' : self.get_id()
        }
        return info

    def extract_complete_data(self):
        info = {
            'relator' : self.extract_text_by_h4_topic("Relator"),
            'redator' : self.extract_text_by_h4_topic("Redator"),
            'data_julgamento' : self.extract_text_by_h4_topic("Julgamento:"),
            'data_publicacao' : self.extract_text_by_h4_topic("Publica"),
            'orgao_julgador' : self.extract_text_by_h4_topic("Órgão julgador"),
            'publicacao': self.extract_text_by_h4_topic("Public"),
            'Partes': self.extract_text_by_topic("Partes"),
            'ementa' : self.extract_text_by_topic("Ementa"),
            'decisao' : self.extract_text_by_topic("Decisão"),
            'indexacao' : self.extract_text_by_topic("Indexação"),
            'legislacao': self.extract_text_by_topic("Legislação"),
            'observacao' :self.extract_text_by_topic("Observação"),
            'acordaos_no_mesmo_sentido' :self.extract_text_by_topic("Acórdãos no mesmo sentido"),
            'intero_teor' :self.extract_text_by_topic("Inteiro teor"),
        }
        return info

    def load_search_results_page(self, query, page_number,driver):
        page_loaded = False
        while not page_loaded:
            try:
                search_url = self.formatUrl(query, str(page_number))
                print(f'Using base url: {search_url}.')
                driver.get(search_url)
                self.wait_for_element(XPATH_FOR_REPORTER_JUDGE)
                page_loaded = True
            except TimeoutException:
                print(f'Failed to load page {page_number}. Retrying.')

    def wait_for_element(self, xpath, driver):
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_dados_completos(self, driver):
        try:
            # Clica no botão que leva à página com os dados completos
            botao = driver.find_element_by_xpath(XPATH_FOR_DADOS_COMPLETOS)
            botao.click()

            # Espera pela nova página com os dados completos
            self.wait_for_element(XPATH_FOR_ID)
            
            # Raspa os dados da nova página
            dados_completos = self.extract_complete_data()
            
            # Fecha a nova página ou volta para os resultados da busca
            driver.back()
            self.wait_for_element(XPATH_FOR_REPORTER_JUDGE)
            
            return dados_completos
        except Exception as e:
            logging.error(f'Failed to extract complete data: {e}')
            return None

    def scrape_page(self, query, page_number):
        driver = self.create_webdriver_instance()
        driver.implicitly_wait(HOMEPAGE_IMPLICIT_WAITING_TIME)

        search_url = self.formatUrl(query, str(page_number))
        print(f'Loading search results page {page_number} at {search_url}...')
        driver.get(search_url)
        
        self.wait_for_element(driver, XPATH_FOR_REPORTER_JUDGE)
        info = self.extract_information(driver)
        dados_completos = self.get_dados_completos(driver)

        if info and dados_completos:
            info.update(dados_completos)

        driver.quit()
        return info if info and dados_completos else None
