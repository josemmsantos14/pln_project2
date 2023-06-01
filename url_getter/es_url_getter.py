import requests
import json, re
from bs4 import BeautifulSoup

def content(heading):
    content = ""
    if heading:
        next_tag = heading.find_next()
        while next_tag and next_tag.name != "h2":
            content += next_tag.get_text()
            #content += str(next_tag)
            next_tag = next_tag.find_next()
    content = re.sub("\n", " ", content)
    return content

url_es = "https://middlesexhealth.org/learning-center/espanol/enfermedades-y-afecciones"
url_es_1 = "https://middlesexhealth.org"

html = requests.get(url_es).text
soup = BeautifulSoup(html, "html.parser")

divs = soup.find_all("div", class_="service-content")

urls = []
for div in divs:
    url = url_es_1 + div.findAll("p")[1].a["href"]
    urls.append(url)

dici = {}
for u in urls:
    html_ = requests.get(u).text
    soup_ = BeautifulSoup(html_, "html.parser")

    term = soup_.find("div", class_="col-12").text.strip()
    term = re.sub(r'\([^()]*\)', "", term).lower().strip()
    info = soup_.find("div", class_="edit-module").text

    description_heading = soup_.find("h2", string="Perspectiva general")
    diagnosis_heading = soup_.find("h2", string="Diagnóstico")
    causes_heading = soup_.find("h2", string="Causas")
    symptoms_heading = soup_.find("h2", string="Síntomas")
    treatment_heading = soup_.find("h2", string="Tratamiento")
    prevention_heading = soup_.find("h2", string="Prevención")

    description = content(description_heading)
    symptoms = content(symptoms_heading)
    causes = content(causes_heading)
    diagnosis = content(diagnosis_heading)
    treatment = content(treatment_heading)
    prevention = content(prevention_heading)

    dici[term] = {  "Descripción": description,
                    "Síntomas": symptoms, 
                    "Causas": causes, 
                    "Diagnóstico": diagnosis, 
                    "Tratamiento": treatment, 
                    "Prevención": prevention
    }

print(dici)

file = open("output/es_diseases.json", "w", encoding="utf-8")
json.dump(dici, file, ensure_ascii=False, indent=4)
file.close()