from scipy.optimize import linprog
from pulp import *
from array import *
from math import floor

class Calculadora:
    # Classes de amêndoas de castanhas de caju (ACC)
    # castanha pequena
    extra_p = 0.0000
    comum_p = 0.0468
    popular_p = 0.0672
    comercial_p = 0.0300
    mista_p = 0.0148
    
    # castanha media 1
    extra_m1 = 0.0153
    comum_m1 = 0.0418
    popular_m1 = 0.0095
    comercial_m1 = 0.0254
    mista_m1 = 0.0378

    # castanha media 2
    extra_m2 = 0.0542
    comum_m2 = 0.2323
    popular_m2 = 0.0000
    comercial_m2 = 0.0230
    mista_m2 = 0.0382

    # grande
    extra_g = 0.0570
    comum_g = 0.0108
    popular_g = 0.0000
    comercial_g = 0.0230
    mista_g = 0.0382

    def __init__(self):
        self.plano_producao_kg = array('d', [0.0,0.0,0.0,0.0])
        self.plano_venda_kg = array('d', [0.0,0.0,0.0,0.0,0.0])
        self.estoque_kg = array('d', [0.0,0.0,0.0,0.0,0.0])

    def calculoPlanoProducao(self, precos_castanha, plano_venda_amendoa):
        def formatar_numero(num:float):
            p_inteira, p_decimal = str(num).split(".")
            p_decimal = p_decimal[:2]
            numero = f"{p_inteira}.{p_decimal}"
            numero = round(float(numero))
            return numero


        # Cria o problema
        prob = LpProblem("Problema da Castanha", LpMinimize)

        # Cria as variaveis
        x1 = LpVariable("0_kgCastanhaPequena", 0) #índice 0
        x2 = LpVariable("1_kgCastanhaMedia1", 0) #índice 1
        x3 = LpVariable("2_kgCastanhaMedia2", 0) #índice 2
        x4 = LpVariable("3_kgCastanhaGrande", 0) #índice 3

        # Cria a funcao objetivo
        prob += precos_castanha[0] * x1 + precos_castanha[1] * x2 + precos_castanha[2] * x3 + precos_castanha[3] * x4, "Total custos"

        # Restricoes
        prob += self.extra_p * x1 + self.extra_m1 * x2 + self.extra_m2 * x3 + self.extra_g * x4 >= plano_venda_amendoa[0], "kg Amendoa - Extra"
        prob += self.comum_p * x1 + self.comum_m1 * x2 + self.comum_m2 * x3 + self.comum_g * x4 >= plano_venda_amendoa[1], "kg Amendoa - Comum"
        prob += self.popular_p * x1 + self.popular_m1 * x2 + self.popular_m2 * x3 + self.popular_g * x4 >= plano_venda_amendoa[2], "kg Amendoa - Popular"
        prob += self.comercial_p * x1 + self.comercial_m1 * x2 + self.comercial_m2 * x3 + self.comercial_g * x4 >= plano_venda_amendoa[3], "kg Amendoa - Comercial"
        prob += self.mista_p * x1 + self.mista_m1 * x2 + self.mista_m2 * x3 + self.mista_g * x4 >= plano_venda_amendoa[4], "kg Amendoa - Mista"

        # Escreve o modelo no arquivo
        prob.writeLP("CastanhaModelo.lp")

        # Resolve o problema
        prob.solve()

        # Solucoes otimas das variaveis
        for variable in prob.variables():
            index = variable.name.split("_")
            self.plano_producao_kg.insert(int(index[0]),float(variable.varValue))

        #Calcular Plano de Venda com base na qtde de castanha, no rendimento.
        # Extra
        qtde_kg_amendoa_extra_p = self.plano_producao_kg[0] * self.extra_p
        qtde_kg_amendoa_extra_m1 = self.plano_producao_kg[1] * self.extra_m1
        qtde_kg_amendoa_extra_m2 = self.plano_producao_kg[2] * self.extra_m2
        qtde_kg_amendoa_extra_g = self.plano_producao_kg[3] * self.extra_g

        soma_kg_amendoa_extra = qtde_kg_amendoa_extra_p + qtde_kg_amendoa_extra_m1 + qtde_kg_amendoa_extra_m2 + qtde_kg_amendoa_extra_g
        soma_kg_amendoa_extra_format = formatar_numero(soma_kg_amendoa_extra)
        
        # Comum
        qtde_kg_amendoa_comum_p = self.plano_producao_kg[0] * self.comum_p
        qtde_kg_amendoa_comum_m1 = self.plano_producao_kg[1] * self.comum_m1
        qtde_kg_amendoa_comum_m2 = self.plano_producao_kg[2] * self.comum_m2
        qtde_kg_amendoa_comum_g = self.plano_producao_kg[3] * self.comum_g

        soma_kg_amendoa_comum = qtde_kg_amendoa_comum_p + qtde_kg_amendoa_comum_m1 + qtde_kg_amendoa_comum_m2 + qtde_kg_amendoa_comum_g
        soma_kg_amendoa_comum_format = formatar_numero(soma_kg_amendoa_comum)
        
        # Popular
        qtde_kg_amendoa_popular_p = self.plano_producao_kg[0] * self.popular_p
        qtde_kg_amendoa_popular_m1 = self.plano_producao_kg[1] * self.popular_m1
        qtde_kg_amendoa_popular_m2 = self.plano_producao_kg[2] * self.popular_m2
        qtde_kg_amendoa_popular_g = self.plano_producao_kg[3] * self.popular_g
        
        soma_kg_amendoa_popular = qtde_kg_amendoa_popular_p + qtde_kg_amendoa_popular_m1 + qtde_kg_amendoa_popular_m2 + qtde_kg_amendoa_popular_g
        soma_kg_amendoa_popular_format = formatar_numero(soma_kg_amendoa_popular)

        # Comercial
        qtde_kg_amendoa_comercial_p = self.plano_producao_kg[0] * self.comercial_p
        qtde_kg_amendoa_comercial_m1 = self.plano_producao_kg[1] * self.comercial_m1
        qtde_kg_amendoa_comercial_m2 = self.plano_producao_kg[2] * self.comercial_m2
        qtde_kg_amendoa_comercial_g = self.plano_producao_kg[3] * self.comercial_g
        
        soma_kg_amendoa_comercial = qtde_kg_amendoa_comercial_p + qtde_kg_amendoa_comercial_m1 + qtde_kg_amendoa_comercial_m2 +qtde_kg_amendoa_comercial_g
        soma_kg_amendoa_comercial_format = formatar_numero(soma_kg_amendoa_comercial)

        # Mista
        qtde_kg_amendoa_mista_p = self.plano_producao_kg[0] * self.mista_p
        qtde_kg_amendoa_mista_m1 = self.plano_producao_kg[1] * self.mista_m1
        qtde_kg_amendoa_mista_m2 = self.plano_producao_kg[2] * self.mista_m2
        qtde_kg_amendoa_mista_g = self.plano_producao_kg[3] * self.mista_g



        soma_kg_amendoa_mista = qtde_kg_amendoa_mista_p + qtde_kg_amendoa_mista_m1 + qtde_kg_amendoa_mista_m2 + qtde_kg_amendoa_mista_g 
        soma_kg_amendoa_mista_format = formatar_numero(soma_kg_amendoa_mista)

        result_plano_venda_amendoa_extra = plano_venda_amendoa[0] - soma_kg_amendoa_extra
        result_plano_venda_amendoa_comum = plano_venda_amendoa[1] - soma_kg_amendoa_comum
        result_plano_venda_amendoa_popular = plano_venda_amendoa[2] - soma_kg_amendoa_popular
        result_plano_venda_amendoa_comercial = plano_venda_amendoa[3] - soma_kg_amendoa_comercial
        result_plano_venda_amendoa_mista = plano_venda_amendoa[4] - soma_kg_amendoa_mista

        result_plano_venda_amendoa_extra = formatar_numero(result_plano_venda_amendoa_extra)
        result_plano_venda_amendoa_comum = formatar_numero(result_plano_venda_amendoa_comum)
        result_plano_venda_amendoa_popular = formatar_numero(result_plano_venda_amendoa_popular)
        result_plano_venda_amendoa_comercial = formatar_numero(result_plano_venda_amendoa_comercial)
        result_plano_venda_amendoa_mista = formatar_numero(result_plano_venda_amendoa_mista)
        
        self.plano_venda_kg = [
            result_plano_venda_amendoa_extra, 
            result_plano_venda_amendoa_comum, 
            result_plano_venda_amendoa_popular, 
            result_plano_venda_amendoa_comercial, 
            result_plano_venda_amendoa_mista,
            soma_kg_amendoa_extra_format,
            soma_kg_amendoa_comum_format,
            soma_kg_amendoa_popular_format,
            soma_kg_amendoa_comercial_format,
            soma_kg_amendoa_mista_format
        ]

        return self

        


        
