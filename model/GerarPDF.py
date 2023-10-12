from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file


class GerarPDF():
    def gerar(plano_producao, planos_venda, preco_castanha, plano_venda_amendoa_inicial, preco_amendoa_inicial):
        # Dados da matriz para a tabela
        dados_tabela1 = [
            ["Tipo de Castanha", "Qtde. Castanha (Kg)", "Valor (R$/Kg)"],
            ["Pequena", plano_producao["kg_castanha_pequena"],
                plano_producao["custo_castanha_pequena"]],
            ["Média 1", plano_producao["kg_castanha_media1"],
                plano_producao["custo_castanha_media1"]],
            ["Média 2", plano_producao["kg_castanha_media2"],
                plano_producao["custo_castanha_media2"]],
            ["Grande", plano_producao["kg_castanha_grande"],
                plano_producao["custo_castanha_grande"]],
        ]
        dados_tabela2 = [
            ["Classe", "Qtde. Amêndoas (Kg)", "Estoque de Produto (Kg)"],
            ["Extra", planos_venda["kg_amendoa_extra"],
                planos_venda["kg_amendoa_extra_estoque"]],
            ["Comum", planos_venda["kg_amendoa_comum"],
                planos_venda["kg_amendoa_comum_estoque"]],
            ["Popular", planos_venda["kg_amendoa_popular"],
                planos_venda["kg_amendoa_popular_estoque"]],
            ["Comercial", planos_venda["kg_amendoa_comarcial"],
                planos_venda["kg_amendoa_comercial_estoque"]],
            ["Mista", planos_venda["kg_amendoa_mista"],
                planos_venda["kg_amendoa_mista_estoque"]],
        ]

        dados_tabela3 = [
            ["Classe de Amêndoas", "Qtde. Amêndoas (Kg)", "Preço do Produto (R$/Kg)"],
            ["Extra", plano_venda_amendoa_inicial["amendoa_extra"],
                preco_amendoa_inicial["preco_amendoa_extra"]],
            ["Comum", plano_venda_amendoa_inicial["amendoa_comum"],
                preco_amendoa_inicial["preco_amendoa_comum"]],
            ["Popular", plano_venda_amendoa_inicial["amendoa_popular"],
                preco_amendoa_inicial["preco_amendoa_popular"]],
            ["Comercial", plano_venda_amendoa_inicial["amendoa_comercial"],
                preco_amendoa_inicial["preco_amendoa_comercial"]],
            ["Mista", plano_venda_amendoa_inicial["amendoa_mista"],
                preco_amendoa_inicial["preco_amendoa_mista"]],
        ]

        dados_tabela4 = [
            ["Tipo de Castanha", "Qtde. Castanha (Kg)", "Valor (R$/Kg)"],
            ["Pequena", 1, preco_castanha['precoCastPequena']],
            ["Média 1", 1, preco_castanha['precoCastMedia1']],
            ["Média 2", 1, preco_castanha['precoCastMedia2']],
            ["Grande", 1, preco_castanha['precoCastGrande']],
        ]

       # Estilo da tabela
        style = TableStyle([
            # Define a primeira linha com a cor de fundo desejada (#bb9260)
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00264c')),  # Cor da primeira linha
            # Define a cor do texto da primeira linha
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            # Alinhar o conteúdo no centro
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # Fonte em negrito para a primeira linha
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            # Espaçamento inferior da primeira linha
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Define a cor de fundo das demais células
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Adiciona grade à tabela
        ])


        # Criar um documento PDF
        doc = SimpleDocTemplate(
            "calculo_produção_de_castanha.pdf", pagesize=letter)

        # Crie um estilo para o título
        styles = getSampleStyleSheet()
        style_title = styles["Title"]
        style_title.alignment = 1  # Centralize o título

        # Crie o conteúdo do PDF
        conteudo = []

        # Adicione o título formatado de acordo com a ABNT
        titulo = Paragraph("Resultado Produção de Castanha", style_title)

        titulo2 = Paragraph("Resultado Plano de Vendas", style_title)

        titulo3 = Paragraph("Plano de Amêndoa Inicial", style_title)

        titulo4 = Paragraph("Plano de Castanhas Inicial", style_title)

        # Adicione a tabela com o estilo definido
        tabela1 = Table(dados_tabela1)
        tabela1.setStyle(style)

        tabela2 = Table(dados_tabela2)
        tabela2.setStyle(style)

        tabela3 = Table(dados_tabela3)
        tabela3.setStyle(style)

        tabela4 = Table(dados_tabela4)
        tabela4.setStyle(style)

        conteudo.append(titulo)
        conteudo.append(tabela1)

        conteudo.append(titulo4)
        conteudo.append(tabela4)

        conteudo.append(titulo2)
        conteudo.append(tabela2)

        conteudo.append(titulo3)
        conteudo.append(tabela3)

        # Construa o PDF
        doc.build(conteudo)