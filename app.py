from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        notes TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        patient_name TEXT,
        date TEXT
    )
    ''')

    # إنشاء مستخدم افتراضي
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1,'admin','1234')")

    conn.commit()
    conn.close()

init_db()

# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = u
            return redirect(url_for('dashboard'))
        else:
            return "بيانات غير صحيحة"

    return render_template('login.html')

# لوحة التحكم
@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# المرضى
@app.route('/patients')
def patients():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()
    conn.close()
    return render_template('patients.html', patients=data)

# إضافة مريض
@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        notes = request.form['notes']

        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, phone, notes) VALUES (?,?,?)",(name,phone,notes))
        conn.commit()
        conn.close()

        return redirect('/patients')

    return render_template('add_patient.html')

# الحجز
@app.route('/appointments', methods=['GET','POST'])
def appointments():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        c.execute("INSERT INTO appointments (patient_name,date) VALUES (?,?)",(name,date))
        conn.commit()

    c.execute("SELECT * FROM appointments")
    data = c.fetchall()
    conn.close()

    return render_template('appointments.html', appointments=data)

# تسجيل خروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
