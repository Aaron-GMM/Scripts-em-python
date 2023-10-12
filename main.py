from flask import Flask, render_template, request, redirect, url_for, send_file, session
from model import ClasseCalculadora, PlanilhaCliente, GerarPDF
import babel.numbers
import locale
import re

app = Flask(__name__, template_folder="./view/")
app.secret_key = "root"

def formatar_numero(numero):
    # Define a localização para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    return str(locale.currency(numero, grouping=True, symbol=None))


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else: 
        a = PlanilhaCliente.login.get_login()
        if a == 0:
            message = "Login successful"
            return redirect(url_for('calc', message=message))
        elif a == 1:
            message = "Campo vazio"
        elif a == 2:
            message = "Campo errado"
        else:
           message = "Email não existente"
    return render_template('login.html', message=message)



@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template('cadastro.html')
    else: # POST
        PlanilhaCliente.PlanilhaExcel.criar_planilha()
        v = PlanilhaCliente.Cliente.inserir_cliente()
        if v == 0:
            message = "Login successful"
            return redirect(url_for('calc', message=message))
        elif v == 2:
            message = "Campo vazio"
        elif v == 3:
            message = "Campo errado"
        else:
            message = "Email existente"
        return render_template("cadastro.html", message=message)



@app.route("/pdf")
def download_pdf():
    GerarPDF.GerarPDF.gerar(
        session['plano_producao'],
        session['plano_vendas'],
        session['precos_castanhas'],
        session['plano_venda_amendoa_inicial'],
        session['preco_amendoa_inicial']
    )
    return send_file("calculo_produção_de_castanha.pdf", as_attachment=True, mimetype="application/pdf", download_name="calculo_produção_de_castanha.pdf")



@app.route('/calculadora', methods=["GET", "POST"])
def calc():
    calculadora = ClasseCalculadora.ClasseCalculadora()
    verify = True

    if request.method == "GET":
        return render_template('get_dados_calc.html')
    else: # POST

        for names_inputs in ['kg_amendoa1', 'kg_amendoa2', 'kg_amendoa3', 'kg_amendoa4', 'kg_amendoa5', 'preco_amendoa1', 'preco_amendoa2', 'preco_amendoa3', 'preco_amendoa4', 'preco_amendoa5', 'preco_cast1', 'preco_cast2', 'preco_cast3', 'preco_cast4']:
            if request.form.get(names_inputs) == "":
                verify = "Input vazio!"

        if verify == True:
         padrao = r'^[0-9.,]+$'
         for names_inputs in ['kg_amendoa1', 'kg_amendoa2', 'kg_amendoa3', 'kg_amendoa4', 'kg_amendoa5', 'preco_amendoa1', 'preco_amendoa2', 'preco_amendoa3', 'preco_amendoa4', 'preco_amendoa5', 'preco_cast1', 'preco_cast2', 'preco_cast3', 'preco_cast4']:
            if not re.match(padrao, request.form.get(names_inputs)):
                verify = "Input errado!"
                return render_template("get_dados_calc.html", mensagem = verify)
            else:
                plano_venda_amendoa_inicial = {
                    'amendoa_extra': babel.numbers.parse_decimal(request.form.get("kg_amendoa1"), locale='pt'),
                    'amendoa_comum': babel.numbers.parse_decimal(request.form.get("kg_amendoa2"), locale='pt'),
                    'amendoa_popular': babel.numbers.parse_decimal(request.form.get("kg_amendoa3"), locale='pt'),
                    'amendoa_comercial': babel.numbers.parse_decimal(request.form.get("kg_amendoa4"), locale='pt'),
                    'amendoa_mista': babel.numbers.parse_decimal(request.form.get("kg_amendoa5"), locale='pt')
                }

                session['plano_venda_amendoa_inicial'] = plano_venda_amendoa_inicial

                preco_amendoa_inicial = {
                    'preco_amendoa_extra': babel.numbers.parse_decimal(request.form.get("preco_amendoa1"), locale='pt'),
                    'preco_amendoa_comum': babel.numbers.parse_decimal(request.form.get("preco_amendoa2"), locale='pt'),
                    'preco_amendoa_popular': babel.numbers.parse_decimal(request.form.get("preco_amendoa3"), locale='pt'),
                    'preco_amendoa_comercial': babel.numbers.parse_decimal(request.form.get("preco_amendoa4"), locale='pt'),
                    'preco_amendoa_mista': babel.numbers.parse_decimal(request.form.get("preco_amendoa5"), locale='pt')
                }

                session['preco_amendoa_inicial'] = preco_amendoa_inicial

                precos_castanhas = {
                    "precoCastPequena": babel.numbers.parse_decimal(request.form.get("preco_cast1"), locale='pt'),
                    "precoCastMedia1": babel.numbers.parse_decimal(request.form.get("preco_cast2"), locale='pt'),
                    "precoCastMedia2": babel.numbers.parse_decimal(request.form.get("preco_cast3"), locale='pt'),
                    "precoCastGrande": babel.numbers.parse_decimal(request.form.get("preco_cast4"), locale='pt')
                }

                session['precos_castanhas'] = precos_castanhas

                # Passando valores para o calculo de produção
                calculadora.calculoPlanoProducao(precos_castanhas, plano_venda_amendoa_inicial)

                # Resultados do calculo
                session['plano_producao'] = {
                    "kg_castanha_pequena": formatar_numero(calculadora.plano_producao_kg[0]),
                    "kg_castanha_media1": formatar_numero(calculadora.plano_producao_kg[1]),
                    "kg_castanha_media2": formatar_numero(calculadora.plano_producao_kg[2]),
                    "kg_castanha_grande": formatar_numero(calculadora.plano_producao_kg[3]),
                    "kg_total_producao": formatar_numero(calculadora.kg_total_producao),
                    "custo_castanha_pequena": formatar_numero(calculadora.custo_tipo_castanha[0]),
                    "custo_castanha_media1": formatar_numero(calculadora.custo_tipo_castanha[1]),
                    "custo_castanha_media2": formatar_numero(calculadora.custo_tipo_castanha[2]),
                    "custo_castanha_grande": formatar_numero(calculadora.custo_tipo_castanha[3]),
                    "custo_total_producao": formatar_numero(calculadora.custo_total_producao)
                }

                session['plano_vendas'] = {
                    "kg_amendoa_extra_estoque": formatar_numero(calculadora.estoque_kg_amendoa[0]),
                    "kg_amendoa_comum_estoque": formatar_numero(calculadora.estoque_kg_amendoa[1]),
                    "kg_amendoa_popular_estoque": formatar_numero(calculadora.estoque_kg_amendoa[2]),
                    "kg_amendoa_comercial_estoque": formatar_numero(calculadora.estoque_kg_amendoa[3]),
                    "kg_amendoa_mista_estoque": formatar_numero(calculadora.estoque_kg_amendoa[4]),
                    "kg_amendoa_extra": formatar_numero(calculadora.classe_amendoa_kg[0]),
                    "kg_amendoa_comum": formatar_numero(calculadora.classe_amendoa_kg[1]),
                    "kg_amendoa_popular": formatar_numero(calculadora.classe_amendoa_kg[2]),
                    "kg_amendoa_comarcial": formatar_numero(calculadora.classe_amendoa_kg[3]),
                    "kg_amendoa_mista": formatar_numero(calculadora.classe_amendoa_kg[4])
                }

                # Apresentação do Plano de Produção e do Plano de Vendas depois do cálculo
                return render_template(
                    "result_calc.html",
                    download_pdf=download_pdf,
                    precos_castanhas=precos_castanhas,
                    plano_producao=session['plano_producao'],
                    plano_vendas=session['plano_vendas'],
                    preco_amendoa_inicial=preco_amendoa_inicial,
                    kg_amendoa_inicial=session['plano_venda_amendoa_inicial']
                )

        else:
            return render_template("get_dados_calc.html", mensagem = verify)

if __name__ == '__main__':
    app.run()