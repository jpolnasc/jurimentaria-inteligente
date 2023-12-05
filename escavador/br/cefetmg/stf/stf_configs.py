SEARCH_URL = 'https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=true&sinonimo=true' \
             '&plural=true&radicais=false&buscaExata=true&page=<PAGE_NUMBER>&pageSize=1&queryString=<QUERY_STRING>' \
             '&sort=_score&sortBy=desc'
SEARCH_FIELD = '<QUERY_STRING>'
PAGE_FIELD = '<PAGE_NUMBER>'

XPATH_NUMBER_OF_RESULTS="//span[@class='pages-resume ml-0']"
XPATH_FOR_REPORTER_JUDGE = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[2]/h4[2]/span"
XPATH_FOR_JUDGMENT_DATE = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[2]/span/h4[1]/span"
XPATH_FOR_PUBLICATION_DATE = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[2]/span/h4[2]/span"
XPATH_FOR_COURT = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[2]/h4[1]/span"
XPATH_FOR_EMENTA = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[4]/div[1]/div[1]/div/div/div/p"
XPATH_FOR_DECISAO = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[4]/div[1]/div[2]/div/div/div/p"
XPATH_FOR_LEGISLACAO = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div/div[1]/div/p"
XPATH_FOR_DADOS_COMPLETOS = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/a"

XPATH_FOR_ID = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div/a/h4"
XPATH_FOR_RECURSO = "/html/body/app-root/app-home/main/app-search-detail/div/div/div[2]/mat-tab-group/div/mat-tab-body[1]/div/div/div[1]/div[1]/h4[2]"


#  Delay in seconds to wait the main page to load
HOMEPAGE_IMPLICIT_WAITING_TIME = 10
SEARCH_PAGE_IMPLICIT_WAITING_TIME = 20