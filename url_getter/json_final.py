import json
from deep_translator import GoogleTranslator

# Carregar os jsons extraídos dos sites
with open('output/pt_diseases.json',encoding='utf-8') as file1:
    data1 = json.load(file1)

with open('output/es_diseases.json',encoding='utf-8') as file2:
    data2 = json.load(file2)

with open('output/en_diseases.json',encoding='utf-8') as file3:
    data3 = json.load(file3)

#  Carregar o dicionário do trabalho 1
with open('output/final_dici_tp1.json',encoding='utf-8') as translation_file:
    translation_data = json.load(translation_file)

# Traduzir de Português para Inglês
def translate_to_english(text):
    translator = GoogleTranslator(source='pt', target='en')
    translation = translator.translate(text)
    return translation

# Traduzir de Português para Espanhol
def translate_to_spanish(text):
    translator = GoogleTranslator(source='pt', target='es')
    translation = translator.translate(text)
    return translation

# Function to check if a Portuguese key exists in the English and Spanish data
def check_translation(key):
    english_key = None
    spanish_key = None

    # Check if the translation exists in the translation JSON
    if key in translation_data:
        translations = translation_data[key]['trad']
        english_key = translations.get('en')
        spanish_key = translations.get('es')

    # If the translation doesn't exist, use Google Translate 
    if not english_key:
        english_key = translate_to_english(key)

    # If the translation doesn't exist, use Google Translate 
    if not spanish_key:
        spanish_key = translate_to_spanish(key)

    return english_key, spanish_key

# Create the merged JSON data
merged_data = {}

for area, diseases in data1.items():
    merged_data[area] = {}
    for disease, info in diseases.items():
        merged_data[area][disease] = {
            'PT': {
                'Termo': disease,
                **info
            },
            'EN': {},
            'ES': {}
        }

        # Check if the Portuguese key exists in the English and Spanish data
        english_key, spanish_key = check_translation(disease)

        # Populate the English data
        if english_key:
            merged_data[area][disease]['EN'] = {
                'Term': english_key,
                **data3.get(english_key, {})
            }
        # Populate the Spanish data
        if spanish_key:
            merged_data[area][disease]['ES'] = {
                'Plazo': spanish_key,
                **data2.get(spanish_key, {})
             }
      
# Save the merged JSON data to a file
with open('output/merged_data.json', 'w', encoding='utf-8') as merged_file:
    json.dump(merged_data, merged_file, indent=4, ensure_ascii=False)
