from flask import session
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def db():
    return sqlite3.connect("clinic.db")

def init():
    cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
password TEXT,
role TEXT
)
""")
    cur.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','1234','admin')")
    con = db()
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, name TEXT, phone TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS doctors(id INTEGER PRIMARY KEY, name TEXT, specialty TEXT, price REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS visits(id INTEGER PRIMARY KEY, patient_id INT, doctor_id INT, visit_date TEXT, queue INT, diagnosis TEXT, treatment TEXT)")

    con.commit()
    con.close()

init()

@app.route("/")
def index():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    cur.execute("SELECT * FROM visits ORDER BY id DESC")
    visits = cur.fetchall()

    con.close()
    return render_template("index.html", patients=patients, doctors=doctors, visits=visits)

@app.route("/add_patient", methods=["POST"])
def add_patient():
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO patients(name, phone) VALUES (?,?)",
                (request.form["name"], request.form["phone"]))
    con.commit()
    con.close()
    return redirect("/")

@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO doctors(name, specialty, price) VALUES (?,?,?)",
                (request.form["name"], request.form["spec"], request.form["price"]))
    con.commit()
    con.close()
    return redirect("/")

@app.route("/add_visit", methods=["POST"])
def add_visit():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM visits")
    queue = cur.fetchone()[0] + 1

    cur.execute("""
    INSERT INTO visits(patient_id, doctor_id, visit_date, queue, diagnosis, treatment)
    VALUES (?,?,?,?,?,?)
    """,(request.form["patient"], request.form["doctor"],
         datetime.now(), queue,
         request.form["diagnosis"], request.form["treatment"]))
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pw))
        data = cur.fetchone()
        con.close()

        if data:
            session["user"] = user
            session["role"] = data[3]
            return redirect("/")
        else:
            return "خطأ في البيانات"

    return render_template("login.html")
    @app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
    if "user" not in session:
    return redirect("/login")
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
