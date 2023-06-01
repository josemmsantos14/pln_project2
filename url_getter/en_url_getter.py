import requests
import json
import time
import random
import re
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

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    # "Referer": "https://www.example.com",
    # Add more headers if required
}
for disease, url_disease in list(url_dic_disease.items()):
    text = ""
    title = ""
    infos_container = None
    # disease_info.clear()
    
    # print("\n", disease, " : ", url_disease, "\n")

    disease_page = BeautifulSoup(requests.get(url_disease, headers=header).text,"html.parser")
    infos_container = disease_page.find("div", class_="content").find("div", id= "phmaincontent_0_ctl01_divByLine").find_next_sibling("div", class_=None)
    # print(infos_container)

    disease_info = {}

    for tag in infos_container.children:
        if tag.name == "h2" and tag.text != "":
            # PARA GUARDAR OS TITLE E TEXT PELO MEIO
            if title != "" and text != "":
                disease_info[title] = text
            title = tag.text
            text = ""

        elif (tag.name == "p" or tag.name == "ul" or tag.name == "h3"): # and tag.text != "":
            text += str(tag.text)
            # print(text)

    # PARA GUARDAR OS TITLE E TEXT FINAL
    disease_info[title] = text
    # PARA GUARDAR TODAS AS INFORMAÇÕES RELATIVAS A CADA DOENÇA
    disease = re.sub(r'\([^()]*\)', "", disease).lower().strip()
    disease_all_info[disease] = disease_info

# print(disease_all_info)

#endregion 

#region SaveFile

file = open("output/en_diseases.json","w", encoding="utf8")
json.dump(disease_all_info,file, ensure_ascii=False, indent = 4)
file.close()

#endregion