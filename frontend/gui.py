from flask import Flask, render_template, request
import json
import re

app = Flask(__name__)

file = open("terms.json", encoding="utf-8")
db = json.load(file)

@app.route("/")
def home():
    return render_template("welcome.html", title="Welcome!")

@app.route("/dicionario")
def dicionario_medico():
    return render_template('dicionario_medico.html')

@app.route("/terms")
def terms():
    return render_template('terms.html', designations=db.keys())

@app.route("/term/<t>")
def term(t):
    return render_template('term.html', designation=t, value=db.get(t,"None"))

@app.route("/addterm")
def addterm():
    return render_template("add_term.html")

@app.route("/terms", methods=["POST"])
def addTerm():
    print(request.form)
    designation = request.form["designation"]
    translation = request.form["translation"]
    description = request.form["description"]

    if designation not in db:
        info_message = "Term Added"
    else:
        info_message = "Term Updated!"

    db[designation] = {"des": description, "en": translation}

    # voltar a ordenar o dicionário depois de adicionar o novo termo
    myKeys = list(db.keys())
    myKeys = sorted(myKeys, key=lambda s: s.casefold())
    sorted_db = {i: db[i] for i in myKeys}

    file_save = open("terms.json","w", encoding="utf-8")
    json.dump(sorted_db, file_save, ensure_ascii=False, indent=4)
    file_save.close()

    return render_template("terms.html", designations=sorted_db.keys(), message = info_message)


@app.route("/term/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    desc = db[designation]
    if designation in db:
        print(designation)
        del db[designation] 
        print(db.get(designation))
        file_save = open("terms.json","w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()
        
    return {designation: {"des":desc}}


@app.route("/table")
def table():
    return render_template("table.html", designations=db.items())


@app.route("/terms/search")
def search():

    text = request.args.get("text")
    lista = []
    if text:
        for designation, description in db.items():
            if re.search(text,designation,flags=re.I) or re.search(text,description["des"],flags=re.I) or re.search(text,description["en"],flags=re.I): 
                lista.append((designation, description))
    return render_template("search.html", matched = lista)


app.run(host="localhost", port=3000, debug=True)

