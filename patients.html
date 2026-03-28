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
