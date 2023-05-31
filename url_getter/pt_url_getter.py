import requests, json
from bs4 import BeautifulSoup

def extractDiseasePage(url):
    page_html = requests.get(url, headers=headers).text
    page_soup = BeautifulSoup(page_html, "html.parser")
    titles = page_soup.find_all('h2', class_='field--name-field-title')
    if not titles:
        titles = page_soup.find_all('h2')
        others= page_soup.find_all('h3')
        titles= titles + others  
    results = {}
    for title in titles:
        description = ''
        next_sibling = title.find_next_sibling()
        while next_sibling and next_sibling.name != 'h2'and next_sibling.name != 'h3':
            description += str(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        results[title.text] = description
    return results

def extractCategory(page_soup):
    options = page_soup.find_all("option")
    selected_option = next(option for option in options if 'selected' in option.attrs)
    section_name = selected_option.text
    return section_name

def extractDiseaseListPage(div):
    title = div.div.span.a.text
    return title


url = "https://www.cuf.pt/saude-a-z"
url1 ="https://www.cuf.pt"
url2 = "https://www.cuf.pt/saude-a-z?pesquisa=&grande_area="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "html.parser")


options = soup.find_all("option")

category_urls = []

for option in options:
    category_urls.append(url2 + option["value"])

lista=[]   
urls = []
for category_url in category_urls:
    page_number = 0
    while True:
        urlp = f"{category_url}&page={page_number}"
        html = requests.get(urlp, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        categoria= extractCategory(soup)
        divs = soup.find_all("div", class_="views-row")
        for div in divs:
            page_url = url1 + div.div.span.a["href"]
            page_info = extractDiseasePage(page_url)
            title = extractDiseaseListPage(div)
            lista.append({categoria:{title:page_info}})
        next_page = soup.find("li", class_="pager__item pager__item--next")
        if next_page is None or not next_page.find("a", href=True):
            break
        else:
            page_number += 1
        
#print(lista)
file = open("output/pt_diseases.json", "w", encoding="utf-8")
json.dump(lista, file, ensure_ascii=False, indent=4)
file.close()
