

from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'root'
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    print(email)
    print(senha)
    return redirect('/')


if  __name__ in "__main__":
    app.run(debug=True)