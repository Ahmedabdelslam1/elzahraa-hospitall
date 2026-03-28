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
