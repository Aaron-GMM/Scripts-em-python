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
        self.plano_venda_kg = array('d', [0.0, 0.0, 0.0, 0.0])

        # Classes de amêndoas de castanhas de caju (ACC)
        self.valores_classe_amendoas = {
            "pequena": {'extra': 0.0000, 'comum': 0.0468, 'popular': 0.0672, 'comercial': 0.0300, 'mista': 0.0148},
            "media1": {'extra': 0.0153, 'comum': 0.0418, 'popular': 0.0095, 'comercial': 0.0254, 'mista': 0.0378},
            "media2": {'extra': 0.0542, 'comum': 0.2323, 'popular': 0.0000, 'comercial': 0.0230, 'mista': 0.0382},
            "grande": {'extra': 0.0570, 'comum': 0.0108, 'popular': 0.0000, 'comercial': 0.0230, 'mista': 0.0382}
        }

    def calculoPlanoProducao(self, preco_castanha, plano_venda_amendoa):
        # Criar o problema
        prob = LpProblem("Problema da Castanha", LpMinimize)

        # Cria as variaveis x1, x2, x3 e x4 que representa os tipos de castanhas
        x1 = LpVariable("0_precoCastPequena", 0)
        x2 = LpVariable("1_precoCastMedia1", 0)
        x3 = LpVariable("2_precoCastMedia2", 0)
        x4 = LpVariable("3_precoCastGrande", 0)

        # Cria função objetivo do calculo
        prob += preco_castanha["precoCastPequena"] * x1 + preco_castanha["precoCastMedia1"] * x2 + preco_castanha["precoCastMedia2"] * x3 + preco_castanha["precoCastGrande"] * x4, "Custo Total"

        # Restrições para o calculo
        prob += self.valores_classe_amendoas['pequena']['extra'] * x1 + self.valores_classe_amendoas['media1']['extra'] * x2 + self.valores_classe_amendoas['media2']['extra'] * x3 + self.valores_classe_amendoas['grande']['extra'] * x4 >= float(plano_venda_amendoa['amendoa_extra']), "Kg Amendo - Extra"
        prob += self.valores_classe_amendoas['pequena']['comum'] * x1 + self.valores_classe_amendoas['media1']['comum'] * x2 + self.valores_classe_amendoas['media2']['comum'] * x3 + self.valores_classe_amendoas['grande']['comum'] * x4 >= float(plano_venda_amendoa['amendoa_comum']), "Kg Amendo - Comum"
        prob += self.valores_classe_amendoas['pequena']['popular'] * x1 + self.valores_classe_amendoas['media1']['popular'] * x2 + self.valores_classe_amendoas['media2']['popular'] * x3 + self.valores_classe_amendoas['grande']['popular'] * x4 >= float(plano_venda_amendoa['amendoa_popular']), "Kg Amendo - Popular"
        prob += self.valores_classe_amendoas['pequena']['comercial'] * x1 + self.valores_classe_amendoas['media1']['comercial'] * x2 + self.valores_classe_amendoas['media2']['comercial'] * x3 + self.valores_classe_amendoas['grande']['comercial'] * x4 >= float(plano_venda_amendoa['amendoa_comercial']), "Kg Amendo - Comecial"
        prob += self.valores_classe_amendoas['pequena']['mista'] * x1 + self.valores_classe_amendoas['media1']['mista'] * x2 + self.valores_classe_amendoas['media2']['mista'] * x3 + self.valores_classe_amendoas['grande']['mista'] * x4 >= float(plano_venda_amendoa['amendoa_mista']), "Kg Amendo - Mista"

        # Escreve o modelo no arquivo CastanhaModelo.lp
        prob.writeLP("CastanhaModelo.lp")

        # Resolve o problema
        prob.solve()
        
        for variavel in prob.variables():
            index = variavel.name.split("_")
            index_0 = int(index[0])
            index_1 = index[1]
            
            plano_producao_kg_value = float(variavel.varValue)
            preco_castanha_value = float(preco_castanha[index_1])

            self.plano_producao_kg.insert(index_0, plano_producao_kg_value)
            self.custo_tipo_castanha.insert(index_0, plano_producao_kg_value * preco_castanha_value)
            
            self.kg_total_producao += plano_producao_kg_value
            self.custo_total_producao += plano_producao_kg_value * preco_castanha_value

        # Calcular plano de Venda
        soma_qtde_amendoa = [
            float(self.plano_producao_kg[0] * self.valores_classe_amendoas['pequena']['extra']) + float(self.plano_producao_kg[1] * self.valores_classe_amendoas['media1']['extra']) + float(self.plano_producao_kg[2] * self.valores_classe_amendoas['media2']['extra']) + float(self.plano_producao_kg[3] * self.valores_classe_amendoas['grande']['extra']),
            float(self.plano_producao_kg[0] * self.valores_classe_amendoas['pequena']['comum']) + float(self.plano_producao_kg[1] * self.valores_classe_amendoas['media1']['comum']) + float(self.plano_producao_kg[2] * self.valores_classe_amendoas['media2']['comum']) + float(self.plano_producao_kg[3] * self.valores_classe_amendoas['grande']['comum']),
            float(self.plano_producao_kg[0] * self.valores_classe_amendoas['pequena']['popular']) + float(self.plano_producao_kg[1] * self.valores_classe_amendoas['media1']['popular']) + float(self.plano_producao_kg[2] * self.valores_classe_amendoas['media2']['popular']) + float(self.plano_producao_kg[3] * self.valores_classe_amendoas['grande']['popular']),
            float(self.plano_producao_kg[0] * self.valores_classe_amendoas['pequena']['comercial']) + float(self.plano_producao_kg[1] * self.valores_classe_amendoas['media1']['comercial']) + float(self.plano_producao_kg[2] * self.valores_classe_amendoas['media2']['comercial']) + float(self.plano_producao_kg[3] * self.valores_classe_amendoas['grande']['comercial']),
            float(self.plano_producao_kg[0] * self.valores_classe_amendoas['pequena']['mista']) + float(self.plano_producao_kg[1] * self.valores_classe_amendoas['media1']['mista']) + float(self.plano_producao_kg[2] * self.valores_classe_amendoas['media2']['mista']) + float(self.plano_producao_kg[3] * self.valores_classe_amendoas['grande']['mista'])
        ]

        # Calcule o estoque de amêndoas
        classes_amendoas_dicionario = ['amendoa_extra', 'amendoa_comum', 'amendoa_popular', 'amendoa_comercial', 'amendoa_mista']
        estoque_amendoa = [soma_qtde_amendoa[i] - float(plano_venda_amendoa[classes_amendoas_dicionario[i]]) for i in range(5)]
        
        # Calcule os resultados do plano de venda
        resultados_plano_venda = [float(float(plano_venda_amendoa[classes_amendoas_dicionario[i]]) - soma_qtde_amendoa[i]) for i in range(5)]

        # Atribua aos atributos correspondentes
        self.estoque_kg_amendoa = estoque_amendoa
        self.classe_amendoa_kg = soma_qtde_amendoa
        self.plano_venda_kg = resultados_plano_venda

        return self