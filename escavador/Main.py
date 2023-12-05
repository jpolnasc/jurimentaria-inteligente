import argparse
import br.cefetmg.stf.stf_scrapper as stf_scrapper_module
import pandas as pd
from threading import Thread

def scrape_page_and_collect(scrapper, query, page_number, results):
    """
    Raspagem de uma única página e coleta os resultados.
    """
    result = scrapper.scrape_page(query, page_number)
    if result:
        results.append(result)

def main():
    # Crie o parser
    parser = argparse.ArgumentParser(description='Realize uma pesquisa no site do STF e extraia informações.')

    # Adicione os argumentos
    parser.add_argument('query', type=str, help='A query para pesquisar.')
    parser.add_argument('max_pages', type=int, help='O número máximo de páginas para pesquisar.')

    # Parse os argumentos
    args = parser.parse_args()

    # Crie o scrapper
    stf_scrapper = stf_scrapper_module.stf_scrapper()

    # Lista para armazenar os resultados de cada thread
    results = []

    # Cria uma thread para cada página a ser raspada
    threads = []
    for page_number in range(1, args.max_pages + 1):
        t = Thread(target=scrape_page_and_collect, args=(stf_scrapper, args.query, page_number, results))
        t.start()
        threads.append(t)

    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()

    # Converta a lista de dicionários em um DataFrame
    data_frame = pd.DataFrame(results)
    print(data_frame.head(5))

    # Salve o DataFrame em um arquivo CSV
    data_frame.to_csv('resultado_pesquisa.csv', index=False)

if __name__ == "__main__":
    main()

# python3 Main.py "licita$" 7460
## python3 Main.py "licita$" 100