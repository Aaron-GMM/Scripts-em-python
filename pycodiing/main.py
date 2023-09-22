from flask import Flask, render_template, request,redirect
from model.calculadora import Calculadora
from model.planilhacliente import Cliente,Planilha
from model.gerarpdf import PDF
from array import *
import babel.numbers
import openpyxl
from openpyxl import Workbook
import pandas as pd
import pathlib

app = Flask(__name__)
if __name__ == '__main__':
    app.run()

Planilha.criar_planilha()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pdf')
def pdf():
   PDF.gerar_pdf()
   return render_template('home.html')
@app.route('/calc', methods=["GET", "POST"])
def calc():
    calculadora = Calculadora()

    if request.method == "GET": 
        return render_template('dados_pessoais.html')
    else: # POST
        # v = Cliente.inserir_client()
        # if v==0:      
        #     message = "Login successful"
        #     return render_template("home.html",message=message)
        # elif v==2:
        #     message = "Campo vazio"
        #     return render_template("home.html",message=message)
        # elif v==3:
        #     message = "campo errado"
        #     return  render_template("home.html",message=message)
        # else:
        #      message = "Email existente"
        #      return render_template("home.html",message=message)
        if request.form.get("kg_amendoa1") is not None: 

            kg_amendoa1 = babel.numbers.parse_decimal(request.form.get("kg_amendoa1"), locale='pt')
            kg_amendoa2 = babel.numbers.parse_decimal(request.form.get("kg_amendoa2"), locale='pt')
            kg_amendoa3 = babel.numbers.parse_decimal(request.form.get("kg_amendoa3"), locale='pt')
            kg_amendoa4 = babel.numbers.parse_decimal(request.form.get("kg_amendoa4"), locale='pt')
            kg_amendoa5 = babel.numbers.parse_decimal(request.form.get("kg_amendoa5"), locale='pt')

            preco_cast1 = babel.numbers.parse_decimal(request.form.get("preco_cast1"), locale='pt')
            preco_cast2 = babel.numbers.parse_decimal(request.form.get("preco_cast2"), locale='pt')
            preco_cast3 = babel.numbers.parse_decimal(request.form.get("preco_cast3"), locale='pt')
            preco_cast4 = babel.numbers.parse_decimal(request.form.get("preco_cast4"), locale='pt')

            # Calculo
            # Obtendo valores dados pelo usuário
            precos_castanha = array('d', [preco_cast1, preco_cast2, preco_cast3, preco_cast4])
            plano_venda_amendoa = array('d', [kg_amendoa1, kg_amendoa2, kg_amendoa3, kg_amendoa4, kg_amendoa5])
            
            # Passando valores para cálculo
            calculadora.calculoPlanoProducao(precos_castanha, plano_venda_amendoa)

            #obtendo resultados
            result_plano_producao = calculadora.plano_producao_kg
            result_plano_venda = calculadora.plano_venda_kg
            result_estoque = calculadora.estoque_kg
            

            kg_total_producao = result_plano_producao[0] + result_plano_producao[1] + result_plano_producao[2] + result_plano_producao[3]

            custo_tipo_castanha1 = result_plano_producao[0] * precos_castanha[0]
            custo_tipo_castanha2 = result_plano_producao[1] * precos_castanha[1]
            custo_tipo_castanha3 = result_plano_producao[2] * precos_castanha[2]
            custo_tipo_castanha4 = result_plano_producao[3] * precos_castanha[3]

            custo_total_producao = custo_tipo_castanha1 + custo_tipo_castanha2 + custo_tipo_castanha3 + custo_tipo_castanha4

            plano_venda_amendoa_ajustado = calculadora.plano_producao_kg

            plano_producao = {
                "kg_tipo_castanha1": str(result_plano_producao[0]),
                "kg_tipo_castanha2": str(result_plano_producao[1]),
                "kg_tipo_castanha3": str(result_plano_producao[2]),
                "kg_tipo_castanha4": str(result_plano_producao[3]),
                "kg_total": str(kg_total_producao),
                "custo_tipo_castanha1": str(custo_tipo_castanha1),
                "custo_tipo_castanha2": str(custo_tipo_castanha2),
                "custo_tipo_castanha3": str(custo_tipo_castanha3),
                "custo_tipo_castanha4": str(custo_tipo_castanha4),
                "custo_total": str(custo_total_producao)
            }

            plano_venda = {
                "kg_amendoa1_estoque": str(result_plano_venda[0]),
                "kg_amendoa2_estoque": str(result_plano_venda[1]),
                "kg_amendoa3_estoque": str(result_plano_venda[2]), 
                "kg_amendoa4_estoque": str(result_plano_venda[3]),
                "kg_amendoa5_estoque": str(result_plano_venda[4]),
                "kg_amendoa1": str(result_plano_venda[5]),
                "kg_amendoa2": str(result_plano_venda[6]),
                "kg_amendoa3": str(result_plano_venda[7]), 
                "kg_amendoa4": str(result_plano_venda[8]),
                "kg_amendoa5": str(result_plano_venda[9])
            }

            #Apresentacao do Plano de Produção e Plano de Vendas calculado
            return render_template('calc_multistep_result.html', plano_producao=plano_producao, plano_venda=plano_venda)
        
        else: 
            return render_template('calc_multistep.html')

@app.route('/<string:nome>')
def error(nome):
    variavel = f'{nome}'
    return render_template("error.html", variavel2=variavel)