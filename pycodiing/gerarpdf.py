from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors 
from model.calculadora import Calculadora
class PDF():
    def gerar_pdf():
# Nome do arquivo PDF de saída
      pdf_file = 'meu_documento_com_tabela.pdf'

# Dados da tabela
      result_plano_producao = Calculadora.plano_producao_kg
      result_plano_venda = Calculadora.plano_venda_kg
      result_estoque = Calculadora.estoque_kg
         
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
      dados_tabela = [
         ["Tipo de Castanha", "Qtde. de Castanha (Kg)", "Valor da Castanha (R$/Kg)"],
         ["Grande", plano_producao["kg_tipo_castanha1"] , plano_producao["custo_tipo_castanha1"]],
         ["Média 1", plano_producao["kg_tipo_castanha2"], plano_producao["custo_tipo_castanha2"]],
         ["Média 2", plano_producao["kg_tipo_castanha3"], plano_producao["custo_tipo_castanha3"]],
         ["Pequena", plano_producao["kg_tipo_castanha4"], plano_producao["custo_tipo_castanha4"]],
         ["Total",   plano_producao["kg_total"], plano_producao["custo_total"] ]
                    ]

# Configurações do PDF
      doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# Crie a tabela
      tabela = Table(dados_tabela)

# Estilize a tabela
      estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

      tabela.setStyle(estilo_tabela)

# Crie o documento PDF e adicione a tabela
      conteudo = []
      conteudo.append(tabela)
      doc.build(conteudo)

      print(f'PDF gerado com sucesso: {pdf_file}')