from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def db():
    return sqlite3.connect("clinic.db")

# إنشاء قاعدة البيانات
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lab(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    test TEXT,
    result TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    date TEXT
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

# إضافة مريض
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

# إضافة طبيب
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

# تسجيل زيارة + رقم انتظار
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

# إضافة تحليل
@app.route("/add_lab", methods=["POST"])
def add_lab():
    patient = request.form["patient"]
    test = request.form["test"]
    result = request.form["result"]

    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO lab(patient_id, test, result) VALUES (?,?,?)",(patient,test,result))
    con.commit()
    con.close()

    return redirect("/")

# إضافة مصروف
@app.route("/add_expense", methods=["POST"])
def add_expense():
    name = request.form["name"]
    amount = request.form["amount"]

    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO expenses(name, amount, date) VALUES (?,?,?)",(name,amount,datetime.now()))
    con.commit()
    con.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
