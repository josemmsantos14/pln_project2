import requests
import json
from bs4 import BeautifulSoup

def extractDiseasePage(url):
    page_html = requests.get(url).text
    page_soup = BeautifulSoup(page_html, "html.parser")

    page_div = page_soup.find("div", class_="field-name-body")
    res = page_div.div.div
    res.name = "page"
    res.attrs = {}
    return str(res)

def extractDiseaseList(div):
    desc = div.find("div", class_="field-content").text
    title = div.div.h3.a.text
    #print(div, end="\n\n")
    return title, desc


url_mayo = "https://www.mayoclinic.org/diseases-conditions/"
search_select = "index?letter="
html = requests.get(url_mayo).text

# print("html:" + html)

soup = BeautifulSoup(html,"html.parser")

div_principal = soup.find("div", class_="cmp-alphabet-facet cmp-button__inner--type-circle cmp-button__inner--color-primary-inverse")
ul = div_principal.ul
list_items = ul.findAll("li")

for li in list_items:
    


# urls = []
# for div in divs:
#     url = "https://www.atlasdasaude.pt"
#     urls.append(url + div.a["href"])

# lista = []
# for url in urls:
#     html_ = requests.get(url).text
#     soup_ = BeautifulSoup(html_, "html.parser")

#     divs = soup_.find_all("div", class_="views-row")
#     for div in divs:
        
#         page_url = url2 + div.div.h3.a["href"]
#         page_info = extractDiseasePage(page_url)
#         title, desc = extractDiseaseList(div)
#         lista.append({title.strip():{"desc":desc.strip(),"page":page_info}})

        
# print(lista)
# file = open("Aula9/doencas.json","w", encoding="utf8")
# json.dump(lista,file, ensure_ascii=False, indent = 4)
# file.close()

#print("\n\n".join(urls))