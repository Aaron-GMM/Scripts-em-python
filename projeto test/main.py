from flask import Flask, render_template, request
from model.planilhaExcel import Cliente,Planinha
app = Flask(__name__)
app.config['SECRET_KEY'] = 'root'
Planinha.criar_planilha()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
     v = Cliente.Inserir_Cliente()
     if v==0:
      message  = "deu certo"
      return render_template('index.html',message=message)
     else:
         message  = "deu errado"
         return render_template('index.html',message=message)
if __name__ in "__main__":
    app.run(debug=True)
