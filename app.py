from flask import Flask, render_template
from flask import request, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # بيانات تجريبية
        if username == 'admin' and password == '1234':
            return redirect(url_for('home'))
        else:
            return "بيانات غير صحيحة"

    return render_template('login.html')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return "<h1>صفحة المرضى</h1>"

@app.route('/appointments')
def appointments():
    return "<h1>صفحة الحجز</h1>"

if __name__ == '__main__':
    app.run(debug=True)
