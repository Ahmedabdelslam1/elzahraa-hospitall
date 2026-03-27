from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect("clinic.db")

@app.route("/")
def index():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    con.close()
    return render_template("index.html", patients=patients)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    phone = request.form["phone"]

    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO patients(name, phone) VALUES(?,?)",(name,phone))
    con.commit()
    con.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
