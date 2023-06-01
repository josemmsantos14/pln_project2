import requests, json
import re
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
    if len(titles) == 0:
        description = page_soup.find('div', class_='field--name-field-text-html').get_text()
        description= re.sub("\n"," ",description)
        results["Definição geral"] = description
    else:
        for title in titles:
            description = ''
            next_sibling = title.find_next_sibling()
            while next_sibling and next_sibling.name != 'h2' and next_sibling.name != 'h3':
                description += next_sibling.get_text()
                next_sibling = next_sibling.find_next_sibling()
            description= re.sub("\n"," ",description)
            results[title.text] = description
    return results

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

category_dict = {}

for option in options:
    category_url = url2 + option["value"]
    category_name = option.text
    if category_name not in category_dict:
        category_dict[category_name] = {}
    page_number = 0
    while True:
        urlp = f"{category_url}&page={page_number}"
        html = requests.get(urlp, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all("div", class_="views-row")
        for div in divs:
            page_url = url1 + div.div.span.a["href"]
            page_info = extractDiseasePage(page_url)
            title = extractDiseaseListPage(div)
            title = re.sub(r'\([^()]*\)', "", title).lower().strip()
            category_dict[category_name][title] = page_info
        next_page = soup.find("li", class_="pager__item pager__item--next")
        if next_page is None or not next_page.find("a", href=True):
            break
        else:
            page_number += 1
        
file = open("output/pt_diseases.json", "w", encoding="utf-8")
json.dump(category_dict, file, ensure_ascii=False, indent=4)
file.close()
