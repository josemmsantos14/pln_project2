from flask import Flask, render_template, request, session, redirect
import json
import re
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static')
app.secret_key = "pln_proj_2"

# file = open("merged_data.json", encoding="utf-8")
# db = json.load(file)



def load_data():
    global db
    with open("merged_data.json", encoding="utf-8") as file:
        db = json.load(file)

    global areas, diseases, info, area_disease, diseases_info
    areas = []
    diseases = []
    info = []
    area_disease = {}
    diseases_info = {}
    for a, ds in db.items():
        areas.append(a)
        dis = []  # Create a new list for each area
        for d, i in ds.items():
            diseases.append(d)
            info.append(i)
            diseases_info[d] = i
            dis.append(d)
        area_disease[a] = dis

load_data()
            

# --------------------USERS-----------------------------------------------------------------
user1 = { "name" : "user1", "pass" : "12345", "isAdmin" : "admin"}
user2 = { "name" : "user2", "pass" : "12345", "isAdmin" : "user"}
users = [user1, user2]
# ------------------------------------------------------------------------------------------
@app.route("/", methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user["name"] == username and user["pass"] == password:
                # print("user: ", username)
                # print("pass: ", password)
                session['user'] = user["name"]
                session['pass'] = user["pass"]
                session['isAdmin'] = user["isAdmin"]
                return redirect("/welcome")
            else:
                error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", error=error)


# ------------------------------------------------------------------------------------------

@app.route("/welcome")
def home():
    print(session["isAdmin"])
    return render_template("inside/welcome.html", userType = session["isAdmin"])

# ------------------------------------------------------------------------------------------

@app.route("/terms", methods=['GET','POST'])
def terms():
    load_data()
    categories_opt = None
    format_opt = None
    a_diseases = diseases
    diseases_table = {}
    # print(area_disease.items())
    if request.method == "POST":
        a_diseases.clear()
        categories_opt = request.form.get("categories")
        format_opt = request.form.get("format")
        # print("dic:",area_disease.items())
        for a, d in area_disease.items():
            if a == categories_opt:
                a_diseases = d
        print(format_opt)
        print(categories_opt)
        for disease, info in diseases_info.items():
            if disease in a_diseases:
                diseases_table[disease] = info

    return render_template('inside/terms/terms.html', dis=a_diseases, designations_table=diseases_table.items(), areas = areas, categorie = categories_opt, format_data = format_opt, userType = session["isAdmin"])

@app.route("/term/<t>")
def term_pt(t):
    for d, i in diseases_info.items():
        if d == t:
            # print(t)
            # print(d)
            value = diseases_info.get(d, None)
            value_pt = value["PT"].items()
    return render_template('inside/terms/term_pt.html', designation=t, values=value_pt, userType = session["isAdmin"])

@app.route("/term/en/<t>")
def term_en(t):
    for d, i in diseases_info.items():
        if d == t:
            # print(t)
            # print(d)
            value = diseases_info.get(d, None)
            value_en = value["EN"].items()
            term = list(value["EN"].items())[0][1]
    return render_template('inside/terms/term_en.html',designation_pt =t, designation=term, values=value_en, userType = session["isAdmin"])

@app.route("/term/es/<t>")
def term_es(t):
    for d, i in diseases_info.items():
        if d == t:
            # print(t)
            # print(d)
            value = diseases_info.get(d, None)
            value_es = value["ES"].items()
            term = list(value["ES"].items())[0][1]
    return render_template('inside/terms/term_es.html',designation_pt =t, designation=term, values=value_es, userType = session["isAdmin"])

@app.route("/addterm", methods=["GET","POST"])
def addterm():
    if request.method == "POST":
        categoria = request.form.get("areas")
        designation_disease = request.form.get("designation")
        translation_en = request.form.get("en")
        translation_es = request.form.get("es")
        description = request.form.get("description")
        # print(categoria)
        # print(designation_disease)
        # print(translation_en)
        # print(translation_es)
        # print(description,"\n")

        for area, disease in db.items():
            if designation_disease not in disease:
                info_message = "Term Added"
            else:
                info_message = "Term Updated!"

        db[categoria][designation_disease] = {
                "PT":{
                    "Termo":designation_disease,
                    "Descrição":description
                },
                "EN":{
                    "Term":translation_en
                },
                "ES":{
                    "Plazo":translation_es
                }
                }
        db[areas[0]][designation_disease] = {
                "PT":{
                    "Termo":designation_disease,
                    "Descrição":description
                },
                "EN":{
                    "Term":translation_en
                },
                "ES":{
                    "Plazo":translation_es
                }
                }

        # voltar a ordenar o dicionário depois de adicionar o novo termo
        for area, disease in db.items():
            if area == categoria:
                myKeys = list(disease.keys())
                myKeys = sorted(myKeys, key=lambda s: s.casefold())
                # print(myKeys)
                # sorted_db = {i: db[i] for i in myKeys}
                

        file_save = open("merged_data.json","w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()
        load_data()
        # return render_template("inside/terms/terms.html",  dis=diseases, designations_table=diseases_info.items(), areas = areas, userType = session["isAdmin"])
        return redirect("/terms")
    return render_template("inside/add_term.html", areas = areas, userType = session["isAdmin"])


@app.route("/delete/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    
    if request.method == "DELETE":
        for area, disease in db.items():
            if designation in disease:
                print(designation)
                #del db[disease]
                del disease[designation] 
                # print(db.get(designation))
        file_save = open("merged_data.json","w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()
        load_data()
        return redirect("/terms")

    return render_template("terms.html")


@app.route("/terms/search")
def search():
    search = request.args.get("search")
    lista = []
    if search:
        for area, disease in db.items():
            for dis, language in disease.items():
                for lan, info in language.items():
                    for title, desc in info.items():
                        if re.search(rf'\b{re.escape(search)}\b', str(desc), flags=re.IGNORECASE):
                            if dis not in lista:
                                lista.append(dis)
    print(lista)
    return render_template("inside/search.html", matched = lista, userType = session["isAdmin"])


app.run(host="localhost", port=3000, debug=True)

