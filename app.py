from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def db():
    return sqlite3.connect("clinic.db")

def init():
    con = db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialty TEXT,
        price REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS visits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        queue INTEGER,
        diagnosis TEXT,
        treatment TEXT
    )
    """)

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
    name = request.form["name"]
    phone = request.form["phone"]
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO patients(name, phone) VALUES (?,?)",(name,phone))
    con.commit()
    con.close()
    return redirect("/")

@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    name = request.form["name"]
    spec = request.form["spec"]
    price = request.form["price"]
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO doctors(name, specialty, price) VALUES (?,?,?)",(name,spec,price))
    con.commit()
    con.close()
    return redirect("/")

@app.route("/add_visit", methods=["POST"])
def add_visit():
    patient = request.form["patient"]
    doctor = request.form["doctor"]
    diagnosis = request.form["diagnosis"]
    treatment = request.form["treatment"]
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM visits")
    queue = cur.fetchone()[0] + 1
    cur.execute("""
    INSERT INTO visits(patient_id, doctor_id, date, queue, diagnosis, treatment)
    VALUES (?,?,?,?,?,?)
    """,(patient,doctor,datetime.now(),queue,diagnosis,treatment))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)    cur.execute("SELECT * FROM patients")
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
    app.run(host="0.0.0.0", port=5000)
