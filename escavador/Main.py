import argparse
import br.cefetmg.stf.stf_scrapper as stf_scrapper_module
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def scrape_page(scrapper, query, page_number):
    """
    Função para raspar uma única página.
    """
    return scrapper.scrape_page(query, page_number)

def main():
    # Crie o parser
    parser = argparse.ArgumentParser(description='Realize uma pesquisa no site do STF e extraia informações.')
    parser.add_argument('query', type=str, help='A query para pesquisar.')
    parser.add_argument('max_pages', type=int, help='O número máximo de páginas para pesquisar.')

    # Parse os argumentos
    args = parser.parse_args()

    # Crie o scrapper
    stf_scrapper = stf_scrapper_module.stf_scrapper()

    # Crie um ThreadPoolExecutor para gerenciar as threads
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_page = {executor.submit(scrape_page, stf_scrapper, args.query, page_number): page_number for page_number in range(1, args.max_pages + 1)}
        for future in concurrent.futures.as_completed(future_to_page):
            results.append(future.result())

    # Converta a lista de dicionários em um DataFrame
    data_frame = pd.DataFrame(results)
    print(data_frame.head(5))

    # Salve o DataFrame em um arquivo CSV
    data_frame.to_csv('resultado_pesquisa.csv', index=False)

if __name__ == "__main__":
    main()