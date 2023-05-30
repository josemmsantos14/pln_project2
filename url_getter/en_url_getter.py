import requests
import json
import time
from bs4 import BeautifulSoup

#region VariblesDeclar

# URLS PRINCIPAIS
url_mayo_principal = "https://www.mayoclinic.org"
url_mayo_diseases = url_mayo_principal + "/diseases-conditions/"

# LISTA DAS LISTAS DE TODAS AS DOENÇAS DE TODAS AS LETRAS
ul_list_all_letters = []

# LISTA DE LINKS DE CADA DOENÇA
url_dic_disease = {}

# DICIONARIO DAS INFOS DE CADA DOENÇA: SINTOMAS, CAUSAS...
disease_info = {}
disease_all_info = {}

#endregion

#region ProcessFirstPage

# HTML DA PÁGINA PRINCIPAL A SER PROCESSADA
html = requests.get(url_mayo_diseases).text
html_first = BeautifulSoup(html,"html.parser")

# BUSCA DAS ANCHOR TAGS DAS DOENÇAS POR LETRA INICIAL
div_principal = html_first.find("div", class_="cmp-alphabet-facet cmp-button__inner--type-circle cmp-button__inner--color-primary-inverse")
ul_principal = div_principal.ul
#LISTA DE CADA LETRA
list_items = ul_principal.findAll("li")

# PERCORRER TODAS AS LETRAS ALFABETICAMENTE
for li in list_items[:len(list_items)-1]:
    anchor = li.div.a
    anchor_href = anchor["href"]
    # anchor_text = anchor.text

    # HTML DA PÁGINA RESPETIVA DE CADA LETRA
    diseases_by_letter = requests.get(url_mayo_principal + anchor_href).text
    diseases_by_letter_soap = BeautifulSoup(diseases_by_letter, "html.parser")
    # CONTAINER DAS DOENÇAS
    diseases_container = diseases_by_letter_soap.find("div", class_="cmp-back-to-top-container__children")
    # LISTA DAS SEGUNDAS LETRAS ALFABETICAMENTE ORGIGANIZADAS
    ul_letter = diseases_container.findAll("ul")
    for ul in ul_letter:
        ul_list_all_letters.append(ul)

#endregion

#region ProcessSecondPage

for ul_secondary in ul_list_all_letters:
    li_disease = ul_secondary.find_all("li")
    for li in li_disease:
        anchor_disease = li.div.div.find("a", class_="cmp-result-name__link")
        if anchor_disease:
            disease = anchor_disease.text
            disease_link = anchor_disease["href"]
            url_dic_disease[disease] = disease_link

#endregion

#region ProcessThirdPage


for disease, url_disease in url_dic_disease.items():
    text = ""
    title = ""
    disease_info.clear()
    
    print(disease, " : ", url_disease, "\n")
    
    disease_page = BeautifulSoup(requests.get(url_disease).text,"html.parser")
    time.sleep(1)
    print(disease_page)
    if disease_page is not None:
        infos_container = disease_page.find("div", class_="content").find("div", id= "phmaincontent_0_ctl01_divByLine").find_next_sibling("div")
        if infos_container is not None:
            for tag in infos_container.children:
                if tag.name == "h2" and tag.text != "":
                    # PARA GUARDAR OS TITLE E TEXT PELO MEIO
                    if title != "" and text != "":
                        disease_info[title] = text
                    title = tag.text
                    text = ""
                    
                    # print("HEADER_2: ", tag, "\n")
                # elif title != "" and tag.name == "h3" and tag.text != "":
                #     semi_title = tag.text
                #     text = ""
                elif (tag.name == "p" or tag.name == "ul" or tag.name == "h3") and tag.text != "":
                    text += str(tag)

            # PARA GUARDAR OS TITLE E TEXT FINAL
            disease_info[title] = text
            # PARA GUARDAR TODAS AS INFORMAÇÕES RELATIVAS A CADA DOENÇA
            disease_all_info[disease] = disease_info

        else:
            print("infos_container not found")
    else:
        print("disease_page not found")

print(disease_all_info)
#endregion 

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
# file = open("./output/en_diseases.json","w", encoding="utf8")
# json.dump(lista,file, ensure_ascii=False, indent = 4)
# file.close()

#print("\n\n".join(urls))