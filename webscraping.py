from bs4 import BeautifulSoup
import pandas as pd
import re


# Carrega o arquivo HTML com BeautifulSoup
with open("nomearquivo.html", "r", encoding="ISO-8859-1") as file:
    soup = BeautifulSoup(file, "html.parser")

# Encontra a tabela desejada no HTML
table = soup.find("table", {"id": "nomeid"})

# Inicializa listas para os cabeçalhos e dados da tabela
headers = []
data = []

# Encontra a linha de cabeçalho da tabela e extrai os cabeçalhos
header_row = table.find("tr")
for header_cell in header_row.find_all("th"):
    headers.append(header_cell.get_text(strip=True))

# Itera pelas linhas da tabela (começa da segunda linha para evitar o cabeçalho novamente)
for row in table.find_all("tr")[1:]:
    row_data = [cell.get_text(strip=True) for cell in row.find_all("td")]
    data.append(row_data)

# Cria um DataFrame do Pandas com os dados e cabeçalhos
df = pd.DataFrame(data, columns=headers)

# Substitui o caractere não legível por "-" em toda a DataFrame
df = df.replace("", "-")
df.to_csv("exemplo.csv", index=False)

# Formata o arquivo CSV novamente

# Carrega o arquivo CSV
df = pd.read_csv("exemplo.csv")

# Remove espaços em branco extras de dentro das células de todas as colunas
for coluna in df.columns:
    if df[coluna].dtype == 'object':
        df[coluna] = df[coluna].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())

# Substitui "nan" por espaços em branco
df = df.replace("nan", "")

# Salva o DataFrame formatado em um arquivo CSV
df.to_csv("exemplo_formatado.csv", index=False)
df = pd.read_csv("exemplo_formatado.csv.csv")

# Dividir os valores e repetir as linhas de acordo com os números dentro dos parênteses


