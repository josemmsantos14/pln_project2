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
    categories_opt = None
    format_opt = None
    a_diseases = diseases
    print(area_disease.items())
    if request.method == "POST":
        a_diseases.clear()
        categories_opt = request.form.get("categories")
        format_opt = request.form.get("format")
        print("dic:",area_disease.items())
        for a, d in area_disease.items():
            if a == categories_opt:
                a_diseases = d
        print(format_opt)
        print(categories_opt)
    return render_template('inside/terms/terms.html', dis=a_diseases, designations_table=diseases_info.items(), areas = areas, categorie = categories_opt, format_data = format_opt, userType = session["isAdmin"])

@app.route("/term/<t>")
def term_pt(t):
    for d, i in diseases_info.items():
        if d == t:
            print(t)
            print(d)
            value = diseases_info.get(d, None)
            value_pt = value["PT"].items()
    return render_template('inside/terms/term_pt.html', designation=t, values=value_pt, userType = session["isAdmin"])

@app.route("/term/en/<t>")
def term_en(t):
    for d, i in diseases_info.items():
        if d == t:
            print(t)
            print(d)
            value = diseases_info.get(d, None)
            value_en = value["EN"].items()
    return render_template('inside/terms/term_en.html', designation=t, values=value_en, userType = session["isAdmin"])

@app.route("/term/es/<t>")
def term_es(t):
    for d, i in diseases_info.items():
        if d == t:
            print(t)
            print(d)
            value = diseases_info.get(d, None)
            value_es = value["ES"].items()
    return render_template('inside/terms/term_es.html', designation=t, values=value_es, userType = session["isAdmin"])

@app.route("/addterm")
def addterm():
    return render_template("inside/add_term.html", userType = session["isAdmin"])

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

    return render_template("inside/terms.html", designations=sorted_db.keys(), message = info_message, userType = session["isAdmin"])


@app.route("/term/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    
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

    return render_template("terms.html")

@app.route("/table")
def table():
    return render_template("inside/table.html", designations=db.items(), userType = session["isAdmin"])


@app.route("/terms/search")
def search():
    search = request.args.get("search")
    lista = []
    if search:
        for area, disease in db.items():
            for dis, language in disease.items():
                for lan, info in language.items():
                    for title, desc in info.items():
                        if re.search(search,str(desc),flags=re.I):
                            if dis not in lista:
                                lista.append(dis)
    print(lista)
    return render_template("inside/search.html", matched = lista, userType = session["isAdmin"])


app.run(host="localhost", port=3000, debug=True)

