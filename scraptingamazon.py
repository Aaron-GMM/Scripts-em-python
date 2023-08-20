import requests
from bs4 import BeautifulSoup
url = 'https://www.amazon.com.br/s?k=samsung&crid=HCJTIS5GX7AF&sprefix=sansug%2Caps%2C188&ref=nb_sb_ss_ts-doa-p_1_6'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"}


site = requests.get(url, headers= headers)


def proximapagina(soup):
    paginas = soup.find('a',{'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
    #ir na ultima pagina com botão proximo desativado
    if not paginas.find('span',{'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
        url = "https://www.amazon.com.br/"
        prox = soup.find('a', 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator', href=True)
        url_final = (url + str(prox['href']))
        return url_final
    else:
        return 1

while True:
    site = requests.get(url,headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    url = proximapagina(soup)
    if not url:
        break
    print(url)
