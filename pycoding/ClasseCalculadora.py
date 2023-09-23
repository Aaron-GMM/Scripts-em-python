from scipy.optimize import linprog
from pulp import *
from array import *

class ClasseCalculadora:
    def __init__(self):
        self.plano_producao_kg = array('d', [0.0,0.0,0.0,0.0])
        self.classe_amendoa_kg = array('d', [0.0,0.0,0.0,0.0, 0.0])
        self.estoque_kg_amendoa = array('d', [0.0,0.0,0.0,0.0,0.0])
        self.kg_total_producao = 0.0
        self.custo_total_producao = 0.0
        self.custo_tipo_castanha = array('d', [0.0, 0.0, 0.0, 0.0])

        # Classes de amêndoas de castanhas de caju (ACC)
        # castanha pequena
        self.extra_p = 0.0000
        self.comum_p = 0.0468
        self.popular_p = 0.0672
        self.comercial_p = 0.0300
        self.mista_p = 0.0148
        
        # castanha media 1
        self.extra_m1 = 0.0153
        self.comum_m1 = 0.0418
        self.popular_m1 = 0.0095
        self.comercial_m1 = 0.0254
        self.mista_m1 = 0.0378

        # castanha media 2
        self.extra_m2 = 0.0542
        self.comum_m2 = 0.2323
        self.popular_m2 = 0.0000
        self.comercial_m2 = 0.0230
        self.mista_m2 = 0.0382

        # grande
        self.extra_g = 0.0570
        self.comum_g = 0.0108
        self.popular_g = 0.0000
        self.comercial_g = 0.0230
        self.mista_g = 0.0382

    def calculoPlanoProducao(self, preco_castanha, plano_venda_amendoa):
        

        # Criar o problema
        prob = LpProblem("Problema da Castanha", LpMinimize)

        # Cria as variaveis x1, x2, x3 e x4 que representa os tipos de castanhas
        x1 = LpVariable("0_precoCastpequena", 0)
        x2 = LpVariable("1_precoCastmedia1", 0)
        x3 = LpVariable("2_precoCastmedia2", 0)
        x4 = LpVariable("3_precoCastgrande", 0)
        
        # Cria função objetivo do calculo
        prob += preco_castanha["precoCastpequena"] * x1 + preco_castanha["precoCastmedia1"] * x2 + preco_castanha["precoCastmedia2"] * x3 + preco_castanha["precoCastgrande"] * x4, "Custo Total"

        # Restrições para o calculo
        prob += self.extra_p * x1 + self.extra_m1 * x2 + self.extra_m2 * x3 + self.extra_g * x4 >= float(plano_venda_amendoa['amendoa_extra']), "Kg Amendo - Extra"
        prob += self.comum_p * x1 + self.comum_m1 * x2 + self.comum_m2 * x3 + self.comum_g * x4 >= float(plano_venda_amendoa['amendoa_comum']), "Kg Amendo - Comum"
        prob += self.popular_p * x1 + self.popular_m1 * x2 + self.popular_m2 * x3 + self.popular_g * x4 >= float(plano_venda_amendoa['amendoa_popular']), "Kg Amendo - Popular"
        prob += self.comercial_p * x1 + self.comercial_m1 * x2 + self.comercial_m2 * x3 + self.comercial_g * x4 >=float(plano_venda_amendoa['amendoa_comercial']), "Kg Amendo - Comecial"
        prob += self.mista_p * x1 + self.mista_m1 * x2 + self.mista_m2 * x3 + self.mista_g * x4 >= float(plano_venda_amendoa['amendoa_mista']), "Kg Amendo - Mista"

        # Escreve o modelo no arquivo CastanhaModelo.lp
        prob.writeLP("CastanhaModelo.lp")

        # Resolve o problema
        prob.solve()

        for vaiavel in prob.variables():
            index = vaiavel.name.split("_")
            self.plano_producao_kg.insert(int(index[0]), float(vaiavel.varValue))
            
            # Calcular kg total da produção
            self.kg_total_producao += self.plano_producao_kg[int(index[0])]

            # Custo Total da Produção
            self.custo_total_producao += self.plano_producao_kg[int(index[0])] * float(preco_castanha[index[1]])

            # Custo por tipo de castanha
            self.custo_tipo_castanha.insert(
                int(index[0]),
                self.plano_producao_kg[int(index[0])] * float(preco_castanha[index[1]])
            )




        # Calcular plano de Venda
        # Amendoa - Extra
        qtde_kg_amendoa_extra_p = self.plano_producao_kg[0] * self.extra_p
        qtde_kg_amendoa_extra_m1 = self.plano_producao_kg[1] * self.extra_m1
        qtde_kg_amendoa_extra_m2 = self.plano_producao_kg[2] * self.extra_m2
        qtde_kg_amendoa_extra_g = self.plano_producao_kg[3] * self.extra_g

        soma_kg_amendoa_extra = qtde_kg_amendoa_extra_p + qtde_kg_amendoa_extra_m1 + qtde_kg_amendoa_extra_m2 + qtde_kg_amendoa_extra_g
        
        # Amendoa - Comum
        qtde_kg_amendoa_comum_p = self.plano_producao_kg[0] * self.comum_p
        qtde_kg_amendoa_comum_m1 = self.plano_producao_kg[1] * self.comum_m1
        qtde_kg_amendoa_comum_m2 = self.plano_producao_kg[2] * self.comum_m2
        qtde_kg_amendoa_comum_g = self.plano_producao_kg[3] * self.comum_g

        soma_kg_amendoa_comum = qtde_kg_amendoa_comum_p + qtde_kg_amendoa_comum_m1 + qtde_kg_amendoa_comum_m2 + qtde_kg_amendoa_comum_g
        
        # Amendoa - Popular
        qtde_kg_amendoa_popular_p = self.plano_producao_kg[0] * self.popular_p
        qtde_kg_amendoa_popular_m1 = self.plano_producao_kg[1] * self.popular_m1
        qtde_kg_amendoa_popular_m2 = self.plano_producao_kg[2] * self.popular_m2
        qtde_kg_amendoa_popular_g = self.plano_producao_kg[3] * self.popular_g
        
        soma_kg_amendoa_popular = qtde_kg_amendoa_popular_p + qtde_kg_amendoa_popular_m1 + qtde_kg_amendoa_popular_m2 + qtde_kg_amendoa_popular_g

        # Amendoa - Comercial
        qtde_kg_amendoa_comercial_p = self.plano_producao_kg[0] * self.comercial_p
        qtde_kg_amendoa_comercial_m1 = self.plano_producao_kg[1] * self.comercial_m1
        qtde_kg_amendoa_comercial_m2 = self.plano_producao_kg[2] * self.comercial_m2
        qtde_kg_amendoa_comercial_g = self.plano_producao_kg[3] * self.comercial_g
        
        soma_kg_amendoa_comercial = qtde_kg_amendoa_comercial_p + qtde_kg_amendoa_comercial_m1 + qtde_kg_amendoa_comercial_m2 +qtde_kg_amendoa_comercial_g

        # Amendoa - Mista
        qtde_kg_amendoa_mista_p = self.plano_producao_kg[0] * self.mista_p
        qtde_kg_amendoa_mista_m1 = self.plano_producao_kg[1] * self.mista_m1
        qtde_kg_amendoa_mista_m2 = self.plano_producao_kg[2] * self.mista_m2
        qtde_kg_amendoa_mista_g = self.plano_producao_kg[3] * self.mista_g

        soma_kg_amendoa_mista = qtde_kg_amendoa_mista_p + qtde_kg_amendoa_mista_m1 + qtde_kg_amendoa_mista_m2 + qtde_kg_amendoa_mista_g


        # Quantidade no Estoque
        self.estoque_kg_amendoa[0] = soma_kg_amendoa_extra - float(plano_venda_amendoa['amendoa_extra'])
        self.estoque_kg_amendoa[1] = soma_kg_amendoa_comum - float(plano_venda_amendoa['amendoa_comum'])
        self.estoque_kg_amendoa[2] = soma_kg_amendoa_popular - float(plano_venda_amendoa['amendoa_popular'])
        self.estoque_kg_amendoa[3] = soma_kg_amendoa_comercial - float(plano_venda_amendoa['amendoa_comercial'])
        self.estoque_kg_amendoa[4] = soma_kg_amendoa_mista - float(plano_venda_amendoa['amendoa_mista'])
        
        # Kg de amendoas por classe
        self.classe_amendoa_kg[0] = soma_kg_amendoa_extra
        self.classe_amendoa_kg[1] = soma_kg_amendoa_comum
        self.classe_amendoa_kg[2] = soma_kg_amendoa_popular
        self.classe_amendoa_kg[3] = soma_kg_amendoa_comercial
        self.classe_amendoa_kg[4] = soma_kg_amendoa_mista

        
        #Calcular Plano de Venda com base na qtde de castanha, no rendimento.
        # Extra
        qtde_kg_amendoa_extra_p = self.plano_producao_kg[0] * self.extra_p
        qtde_kg_amendoa_extra_m1 = self.plano_producao_kg[1] * self.extra_m1
        qtde_kg_amendoa_extra_m2 = self.plano_producao_kg[2] * self.extra_m2
        qtde_kg_amendoa_extra_g = self.plano_producao_kg[3] * self.extra_g

        soma_kg_amendoa_extra = qtde_kg_amendoa_extra_p + qtde_kg_amendoa_extra_m1 + qtde_kg_amendoa_extra_m2 + qtde_kg_amendoa_extra_g
        
        # Comum
        qtde_kg_amendoa_comum_p = self.plano_producao_kg[0] * self.comum_p
        qtde_kg_amendoa_comum_m1 = self.plano_producao_kg[1] * self.comum_m1
        qtde_kg_amendoa_comum_m2 = self.plano_producao_kg[2] * self.comum_m2
        qtde_kg_amendoa_comum_g = self.plano_producao_kg[3] * self.comum_g

        soma_kg_amendoa_comum = qtde_kg_amendoa_comum_p + qtde_kg_amendoa_comum_m1 + qtde_kg_amendoa_comum_m2 + qtde_kg_amendoa_comum_g
        
        # Popular
        qtde_kg_amendoa_popular_p = self.plano_producao_kg[0] * self.popular_p
        qtde_kg_amendoa_popular_m1 = self.plano_producao_kg[1] * self.popular_m1
        qtde_kg_amendoa_popular_m2 = self.plano_producao_kg[2] * self.popular_m2
        qtde_kg_amendoa_popular_g = self.plano_producao_kg[3] * self.popular_g
        
        soma_kg_amendoa_popular = qtde_kg_amendoa_popular_p + qtde_kg_amendoa_popular_m1 + qtde_kg_amendoa_popular_m2 + qtde_kg_amendoa_popular_g

        # Comercial
        qtde_kg_amendoa_comercial_p = self.plano_producao_kg[0] * self.comercial_p
        qtde_kg_amendoa_comercial_m1 = self.plano_producao_kg[1] * self.comercial_m1
        qtde_kg_amendoa_comercial_m2 = self.plano_producao_kg[2] * self.comercial_m2
        qtde_kg_amendoa_comercial_g = self.plano_producao_kg[3] * self.comercial_g
        
        soma_kg_amendoa_comercial = qtde_kg_amendoa_comercial_p + qtde_kg_amendoa_comercial_m1 + qtde_kg_amendoa_comercial_m2 +qtde_kg_amendoa_comercial_g

        # Mista
        qtde_kg_amendoa_mista_p = self.plano_producao_kg[0] * self.mista_p
        qtde_kg_amendoa_mista_m1 = self.plano_producao_kg[1] * self.mista_m1
        qtde_kg_amendoa_mista_m2 = self.plano_producao_kg[2] * self.mista_m2
        qtde_kg_amendoa_mista_g = self.plano_producao_kg[3] * self.mista_g



        soma_kg_amendoa_mista = qtde_kg_amendoa_mista_p + qtde_kg_amendoa_mista_m1 + qtde_kg_amendoa_mista_m2 + qtde_kg_amendoa_mista_g 

        result_plano_venda_amendoa_extra = float(plano_venda_amendoa['amendoa_extra']) - soma_kg_amendoa_extra
        result_plano_venda_amendoa_comum = float(plano_venda_amendoa['amendoa_comum']) - soma_kg_amendoa_comum
        result_plano_venda_amendoa_popular = float(plano_venda_amendoa['amendoa_popular']) - soma_kg_amendoa_popular
        result_plano_venda_amendoa_comercial = float(plano_venda_amendoa['amendoa_comercial']) - soma_kg_amendoa_comercial
        result_plano_venda_amendoa_mista = float(plano_venda_amendoa['amendoa_mista']) - soma_kg_amendoa_mista

        result_plano_venda_amendoa_extra = result_plano_venda_amendoa_extra
        result_plano_venda_amendoa_comum = result_plano_venda_amendoa_comum
        result_plano_venda_amendoa_popular = result_plano_venda_amendoa_popular
        result_plano_venda_amendoa_comercial = result_plano_venda_amendoa_comercial
        result_plano_venda_amendoa_mista = result_plano_venda_amendoa_mista

        self.plano_venda_kg = [
            result_plano_venda_amendoa_extra, 
            result_plano_venda_amendoa_comum, 
            result_plano_venda_amendoa_popular, 
            result_plano_venda_amendoa_comercial, 
            result_plano_venda_amendoa_mista,
            soma_kg_amendoa_extra,
            soma_kg_amendoa_comum,
            soma_kg_amendoa_popular,
            soma_kg_amendoa_comercial,
            soma_kg_amendoa_mista
        ]
        return self