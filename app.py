from flask import Flask, render_template

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
