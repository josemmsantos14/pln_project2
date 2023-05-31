from flask import Flask, render_template, request, session, redirect
import json
import re

app = Flask(__name__, static_folder='static')
app.secret_key = "pln_proj_2"

file = open("terms.json", encoding="utf-8")
db = json.load(file)

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
    if request.method == "POST":
        categories_opt = request.form.get("categories")
        format_opt = request.form.get("format")
        print(format_opt)
        print(categories_opt)
    return render_template('inside/terms/terms.html', designations=db.keys(), designations_table=db.items(), categorie = categories_opt, format_data = format_opt, userType = session["isAdmin"])

@app.route("/term/<t>")
def term_pt(t):
    return render_template('inside/terms/term_pt.html', designation=t, value=db.get(t,"None"), userType = session["isAdmin"])

@app.route("/term/en/<t>")
def term_en(t):
    return render_template('inside/terms/term_en.html', designation=t, value=db.get(t,"None"), userType = session["isAdmin"])

@app.route("/term/es/<t>")
def term_es(t):
    return render_template('inside/terms/term_es.html', designation=t, value=db.get(t,"None"), userType = session["isAdmin"])

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
    return render_template("inside/table.html", designations=db.items(), userType = session["isAdmin"])


@app.route("/terms/search")
def search():

    text = request.args.get("text")
    lista = []
    if text:
        for designation, description in db.items():
            if re.search(text,designation,flags=re.I) or re.search(text,description["des"],flags=re.I) or re.search(text,description["en"],flags=re.I): 
                lista.append((designation, description))
    return render_template("inside/search.html", matched = lista, userType = session["isAdmin"])


app.run(host="localhost", port=3000, debug=True)

