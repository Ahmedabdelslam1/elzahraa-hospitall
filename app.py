from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
def check_role(roles):
    if 'role' not in session or session['role'] not in roles:
        return False
    return True
app = Flask(__name__)
app.secret_key = 'secret123'
from werkzeug.security import generate_password_hash, check_password_hash
hashed = generate_password_hash(password)
check_password_hash(hashed, password)

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    role TEXT
)
''')
   c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1,'admin','1234','admin')")
c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (2,'doctor','1234','doctor')")
c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (3,'reception','1234','reception')")

    # إنشاء مستخدم افتراضي
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1,'admin','1234')")

    conn.commit()
    conn.close()

init_db()
#سجل العمليات
@app.route('/logs')
def logs():
    if not check_role(['admin']):
        return "🚫 غير مصرح"

    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    return render_template('logs.html', logs=data)
# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def log_action(user, action):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (user, action, time) VALUES (?,?,datetime('now'))", (user, action))
    conn.commit()
    conn.close()
        if user:
    session['user'] = user[1]
    session['role'] = user[3]
    return redirect(url_for('dashboard'))

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
    if not check_role(['admin','doctor','reception']):
        return "🚫 غير مصرح"

    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()
    conn.close()

    return render_template('patients.html', patients=data)
# إضافة مريض
@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    if not check_role(['admin','reception']):
        return "🚫 غير مصرح"

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

        log_action(session['user'], f"إضافة مريض {name}")

    
# الحجز
@app.route('/appointments', methods=['GET','POST'])
def appointments():
    if not check_role(['admin','doctor','reception']):
        return "🚫 غير مصرح"

    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    if request.method == 'POST':
        if not check_role(['admin','reception']):
            return "🚫 غير مصرح"

        name = request.form['name']
        date = request.form['date']
        c.execute("INSERT INTO appointments (patient_name,date) VALUES (?,?)",(name,date))
        conn.commit()

    c.execute("SELECT * FROM appointments")
    data = c.fetchall()
    conn.close()

    return render_template('appointments.html', appointments=data)
<h2>الحجوزات</h2>

<form method="POST">
<input name="name" placeholder="اسم المريض">
<input type="date" name="date">
<button>حجز</button>
</form>

<table border="1">
<tr><th>الاسم</th><th>التاريخ</th></tr>

{% for a in appointments %}
<tr>
<td>{{a[1]}}</td>
<td>{{a[2]}}</td>
</tr>
{% endfor %}
</table>
#الفواتير
@app.route('/invoices', methods=['GET','POST'])
def invoices():
    if not check_role(['admin','accountant']):
        return "🚫 غير مصرح"

    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']

        c.execute("INSERT INTO invoices (patient_id, amount, status, date) VALUES (?,?,?,date('now'))",
                  (patient_id, amount, 'unpaid'))
        conn.commit()

        log_action(session['user'], f"إنشاء فاتورة للمريض {patient_id}")

    c.execute("SELECT * FROM invoices")
    data = c.fetchall()
    conn.close()

    return render_template('invoices.html', invoices=data)
# تسجيل خروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
