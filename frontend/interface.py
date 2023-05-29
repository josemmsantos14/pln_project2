from flask import Flask, render_template, request

import json

app = Flask(__name__)

file = open("terms.json", encoding="utf-8")

db = json.load(file)


@app.route("/")
def home():
    return render_template("home.html", title="Welcome!")

@app.route("/terms")
def terms():
    return render_template("terms.html", designations=db.keys())

@app.route("/term/<t>")
def term(t):
    return render_template("term.html", designation = t, value= db.get(t, "None"))

@app.route("/term", methods=["POST"])
def addTerm():
    print(request.form)
    designation = request.form['designation'] 
    description = request.form['description']

    if designation not in db:
        db[designation] = {"desc": description}
        file_save = open("terms.json", "w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        info_message = "Term Added correctly"

    else:
        info_message = "Term Already Exists"

    return render_template("terms.html", designations=db.keys(), message= info_message)


@app.route("/term/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    desc = db[designation]
    if designation in db:
        del db[designation]
        file_save = open("terms.json", "w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)

    return {designation: {"desc": desc}}


app.run(host="localhost", port=3000, debug=True)