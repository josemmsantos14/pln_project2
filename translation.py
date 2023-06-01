from deep_translator import GoogleTranslator
import json

translator = GoogleTranslator(source='pt', target='en')

file_in = open("exemplo_teste.json",encoding="utf-8")

dici = json.load(file_in)

new_dici = {}

for designation, description in dici.items():
    new_dici[designation] = {
                                "des": description,
                                "en": translator.translate(designation)
                            }

file_out = open("dicionario_translation.json","w",encoding="utf-8")
json.dump(new_dici,file_out,ensure_ascii=False, indent=4)
file_out.close()

#translator.translate("hoje está um dia bonito")

re.sub(r'\([^()]*\)', "", text)