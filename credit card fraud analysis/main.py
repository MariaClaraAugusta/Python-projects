import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import function as fc


conn, cursor = fc.conexao()


#    POSIÇÃO DOS GRÁFICOS EM CADA IMAGEM (QUADRANTES)
linhas_colunas2x1 = [2,1]
linhas_colunas3x1 = [3,1]
linhas_colunas2x2 = [2,2]

#    CONTA AS TRANSAÇÕES FRAUDULENTAS E LEGITIMAS
fraudes = fc.conta_class('dia',1)
naofraudes = fc.conta_class('dia',0)
fraudes_dia1 = fc.conta_class('dia1',1)
fraudes_dia2 = fc.conta_class('dia2',1)
naofraudes_dia1 = fc.conta_class('dia1',0)
naofraudes_dia2 = fc.conta_class('dia2',0)
amount_dia1 = fc.soma_amount('dia1')
amount_dia2 = fc.soma_amount('dia2')

# GRÁFICOS DE PIZZA

dic_fraudes_total = {
    'dados': [fraudes,naofraudes],
    'labels': [f'Fraudulentas ({fraudes})', f'Não Fraudulentas ({naofraudes})'],
    'cores': ['#FF7676', '#4CAF50'],
    'titulo': 'Porcentagem de Transações de Cartão de Crédito',
    'legenda': 'Tipo de Transação'
}

dic_fraudes_dias = {
    'dados': [fraudes_dia1,fraudes_dia2],
    'labels': [f'dia 1 ({fraudes_dia1})', f'dia 2 ({fraudes_dia2})'],
    'cores': ['#fcba03', '#035efc'],
    'titulo': 'Porcentagem de Transações Fraudulentas: Dia 1 X Dia 2',
    'legenda': 'Dia da Transação'
}

dic_amount_dias = {
    'dados': [amount_dia1,amount_dia2],
    'labels': ['dia 1 (${:.2f})'.format(amount_dia1), 'dia 2 (${:.2f})'.format(amount_dia2)],
    'cores': ['#f5e642','#9927db'],
    'titulo': 'Quantia transacionada por dia',
    'legenda': 'Dia da Transação'
}

# GRÁFICOS LINHA

dic_amount_fc_time = {
    'intervalo': 'total',
    'label_f': f'Fraudulentas ({fraudes})',
    'label_nf': f'Não Fraudulentas ({naofraudes})',
    'titulo': 'Valor das Transações em Função do Tempo'
}

dic_amount_fc_time_dia1 = {
    'intervalo': 'dia1',
    'label_f': f'Fraudulentas ({fraudes_dia1})',
    'label_nf': f'Não Fraudulentas ({naofraudes_dia1})',
    'titulo': 'Valor das Transações em Função do Tempo (Dia 1)'
}

dic_amount_fc_time_dia2 = {
    'intervalo': 'dia2',
    'label_f': f'Fraudulentas ({fraudes_dia2})',
    'label_nf': f'Não Fraudulentas ({naofraudes_dia2})',
    'titulo': 'Valor das Transações em Função do Tempo (Dia 2)'
}

# HISTOGRAMAS

dic_legitimas_ps = {
    'tipo': 'Time',
    'class': 0,
    'nbins': 45,
    'titulo': "Transações Legítimas Por Segundo",
    'xlabel': 'Tempo (Segundos)',
    'cor': '#03fcca'
}

dic_fraudulentas_ps = {
    'tipo': 'Time',
    'class': 1,
    'nbins': 45,
    'titulo': f"Transações Fraudulentas Por Segundo",
    'xlabel': 'Tempo (Segundos)',
    'cor': '#ed3978'
}

dic_fraudulentas_valor = {
    'tipo': 'Amount',
    'class': 1,
    'nbins': 10,
    'titulo': 'Transações Fraudulentas por Valor',
    'xlabel': 'Valor (USD)',
    'cor': '#ed3978'
}

dic_legitimas_valor = {
    'tipo': 'Amount',
    'class': 0,
    'nbins': 10,
    'titulo': 'Transações Legítimas por Valor',
    'xlabel': 'Valor (USD)',
    'cor': '#03fcca'
}

# HISTOGRAMAS COM FILTRO

dic_legitimas = {
    'class': 0,
    'intervalo': [500, 3000],
    'tipo': 'Time',
    'coluna': 'Time',
    'titulo': 'Transações Legítimas em intervalo de tempo',
    'cor': '#03fcca',
    'xlabel': 'Tempo (Segundos)'
}

dic_fraudes = {
    'class': 1,
    'intervalo': [500, 3000],
    'tipo': 'Amount',
    'coluna': 'Amount',
    'titulo': f'Transações Fraudulentas em intervalo de valor',
    'cor': '#ed3978',
    'xlabel': 'Valor (USD)'
}

dicionarios_pizza = [dic_fraudes_dias, dic_fraudes_total, dic_amount_dias]
dicionarios_linha = [dic_amount_fc_time, dic_amount_fc_time_dia1, dic_amount_fc_time_dia2]
dicionarios_hist = [dic_fraudulentas_ps, dic_legitimas_ps, dic_fraudulentas_valor, dic_legitimas_valor]
dicionario_hist_filtrado = [dic_legitimas, dic_fraudes]


fc.cria_tabelas()
fc.cria_grafico_pizza(dicionarios_pizza, linhas_colunas3x1)
fc.cria_grafico_linha(dicionarios_linha, linhas_colunas3x1)
fc.cria_histograma(dicionarios_hist, linhas_colunas2x2)
fc.cria_histograma_filtrado(dicionario_hist_filtrado, linhas_colunas2x1)


path = 'images base'
image_files = ['figura1.png', 'figura2.png', 'figura3.png', 'figura4.png', 'figura5.png', 'figura6.png']
posicoes_grafico = [(85, 400), (85, 400), (85,100), (85, 0), (85, 300), (85, 100)]

pdf_filename = 'gráficos_projeto.pdf'
c = canvas.Canvas(pdf_filename, pagesize=A4)
c.setFont("Helvetica", 14)
c.drawString(170, 750, "Análise de Fraudes em Cartão de Crédito")


desired_width = 400

for i in range(len(image_files)):
    image_path = os.path.join(path, image_files[i])
    
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = height / width
    desired_height = int(aspect_ratio * desired_width)
    x, y = posicoes_grafico[i]

    c.drawImage(image_path, x, y, width=desired_width, height=desired_height)
    c.showPage()

c.save()
