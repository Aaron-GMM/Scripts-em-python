from flask import Flask, render_template, request, redirect, url_for, send_file, session
from model import ClasseCalculadora
from model import PlanilhaCliente
from model import GerarPDF
from array import *
import babel.numbers
import locale

app = Flask(__name__, template_folder="./view/")
app.secret_key = "root"

def formatar_num(numero):
     # Defina a localização para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    return str(locale.currency(numero, grouping=True, symbol=None))

@app.route("/pdf")
def download_pdf():
    GerarPDF.GerarPDF.gerar(session['plano_producao'],session['plano_vendas'],session['precos_castanhas'],session['plano_venda_amendoa_inicial'], session['preco_amendoa_inicial'] )
    return send_file("calculo_produção_de_castanha.pdf", as_attachment=True, mimetype="aplication/pdf", download_name="exemplo.pdf")

@app.route('/', methods=["GET", "POST"])
def home():
    if(request.method == "GET"):
        return render_template('home.html')
    else: # POST
        PlanilhaCliente.PlanilhaExel.criar_planilha()

        v = PlanilhaCliente.Cliente.inserir_cliente()
        if v==0:
            message = "Login successful"
            return redirect(url_for('calc', message=message))
        elif v==2:
            message = "Campo vazio"
            return render_template("home.html",message=message)
        elif v==3:
            message = "campo errado"
            return  render_template("home.html",message=message)
        else:
             message = "Email existente"
             return render_template("home.html",message=message)

@app.route('/calculadora', methods=["GET", "POST"])
def calc():

    calculadora = ClasseCalculadora.ClasseCalculadora()

    if(request.method == "GET"):
        return render_template('get_dados.html')
    else: # POST
        if request.form.get("kg_amendoa1") is not None:

            amendoa_extra = babel.numbers.parse_decimal(request.form.get("kg_amendoa1"), locale='pt')
            amendoa_comum = babel.numbers.parse_decimal(request.form.get("kg_amendoa2"), locale='pt')
            amendoa_popular = babel.numbers.parse_decimal(request.form.get("kg_amendoa3"), locale='pt')
            amendoa_comercial = babel.numbers.parse_decimal(request.form.get("kg_amendoa4"), locale='pt')
            amendoa_mista = babel.numbers.parse_decimal(request.form.get("kg_amendoa5"), locale='pt')
            
           
            plano_venda_amendoa_inicial ={
                'amendoa_extra':amendoa_extra,
                'amendoa_comum':amendoa_comum,
                'amendoa_popular':amendoa_popular,
                'amendoa_comercial':amendoa_comercial,
                'amendoa_mista':amendoa_mista
            }

            session['plano_venda_amendoa_inicial'] = plano_venda_amendoa_inicial

            preco_amendoa_extra = babel.numbers.parse_decimal(request.form.get("preco_amendoa1"), locale='pt')
            preco_amendoa_comum = babel.numbers.parse_decimal(request.form.get("preco_amendoa2"), locale='pt')
            preco_amendoa_popular = babel.numbers.parse_decimal(request.form.get("preco_amendoa3"), locale='pt')
            preco_amendoa_comercial = babel.numbers.parse_decimal(request.form.get("preco_amendoa4"), locale='pt')
            preco_amendoa_mista = babel.numbers.parse_decimal(request.form.get("preco_amendoa5"), locale='pt')
      
            preco_amendoa_inicial ={
                'preco_amendoa_extra':preco_amendoa_extra,
                'preco_amendoa_comum':preco_amendoa_comum,
                'preco_amendoa_popular':preco_amendoa_popular,
                'preco_amendoa_comercial':preco_amendoa_comercial,
                'preco_amendoa_mista':preco_amendoa_mista
            }
            session['preco_amendoa_inicial'] = preco_amendoa_inicial

            preco_cast_pequena = babel.numbers.parse_decimal(request.form.get("preco_cast1"), locale='pt')
            preco_cast_media1 = babel.numbers.parse_decimal(request.form.get("preco_cast2"), locale='pt')
            preco_cast_media2 = babel.numbers.parse_decimal(request.form.get("preco_cast3"), locale='pt')
            preco_cast_grande = babel.numbers.parse_decimal(request.form.get("preco_cast4"), locale='pt')

           
            precos_castanhas = {
                "precoCastpequena":preco_cast_pequena,
                "precoCastmedia1":preco_cast_media1,
                "precoCastmedia2":preco_cast_media2,
                "precoCastgrande":preco_cast_grande
                }
            session['precos_castanhas'] = precos_castanhas
            # Passando valores para o calculo de produção
            calculadora.calculoPlanoProducao(precos_castanhas, plano_venda_amendoa_inicial)
            
            # Resultados do calculo
            result_plano_producao = calculadora.plano_producao_kg
            kg_total_producao = calculadora.kg_total_producao
            custo_total_producao = calculadora.custo_total_producao
            custo_tipo_castanha = calculadora.custo_tipo_castanha

            session['plano_producao'] = {
                "kg_castanha_pequena": formatar_num(result_plano_producao[0]),
                "kg_castanha_media1": formatar_num(result_plano_producao[1]),
                "kg_castanha_media2": formatar_num(result_plano_producao[2]),
                "kg_castanha_grande": formatar_num(result_plano_producao[3]),
                "kg_total_producao": formatar_num(kg_total_producao),
                "custo_castanha_pequena": formatar_num(custo_tipo_castanha[0]),
                "custo_castanha_media1": formatar_num(custo_tipo_castanha[1]),
                "custo_castanha_media2": formatar_num(custo_tipo_castanha[2]),
                "custo_castanha_grande": formatar_num(custo_tipo_castanha[3]),
                "custo_total_producao": formatar_num(custo_total_producao)
            }

            classe_kg_amendoa = calculadora.classe_amendoa_kg
            estoque_kg_amendoa = calculadora.estoque_kg_amendoa

            session['plano_vendas'] = {
                "kg_amendoa_extra_estoque": formatar_num(estoque_kg_amendoa[0]),
                "kg_amendoa_comum_estoque": formatar_num(estoque_kg_amendoa[1]),
                "kg_amendoa_popular_estoque": formatar_num(estoque_kg_amendoa[2]),
                "kg_amendoa_comercial_estoque": formatar_num(estoque_kg_amendoa[3]),
                "kg_amendoa_mista_estoque": formatar_num(estoque_kg_amendoa[4]),
                "kg_amendoa_extra": formatar_num(classe_kg_amendoa[0]),
                "kg_amendoa_comum": formatar_num(classe_kg_amendoa[1]),
                "kg_amendoa_popular": formatar_num(classe_kg_amendoa[2]),
                "kg_amendoa_comarcial": formatar_num(classe_kg_amendoa[3]),
                "kg_amendoa_mista": formatar_num(classe_kg_amendoa[4])
            }
            
            

            # Apresentação do Plano de Produção e do Plano de Vendas depois do calculo
            return render_template("result_calc.html", download_pdf = download_pdf,precos_castanhas=precos_castanhas, plano_producao = session['plano_producao'], plano_vendas = session['plano_vendas'], preco_amendoa_inicial = preco_amendoa_inicial, kg_amendoa_inicial = plano_venda_amendoa_inicial)


        else:
            return render_template("get_dados.html")

if __name__ == '_main_':
    app.run()