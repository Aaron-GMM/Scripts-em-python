import pandas as pd
import numpy as np

# imp a tabela do banco de dados
data = pd.read_csv('AB_NYC_2019.csv')

# imp o resultado da média dos preços
preco_aluguel = data.loc[:, "price"]

print("A média de preços:", np.mean(preco_aluguel))

# imp a contagem distinta de regioes
regiao = data.loc[:, "neighbourhood_group"]

    print("A quantidade de regioes disponiveis:", pd.unique(regiao))

# imp valor max dos alugueis
alugueis = data.loc [:, "price"]

print("Valor máximo dos alugueis:", np.max(preco_aluguel))


