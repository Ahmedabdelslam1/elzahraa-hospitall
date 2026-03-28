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
