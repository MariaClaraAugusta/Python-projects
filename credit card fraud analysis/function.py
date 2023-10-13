
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def conexao():
    conn = sqlite3.connect('database\\database.db')
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = conexao()


def conta_class(dia,classe):
    cursor.execute(f"SELECT COUNT(Class) FROM transacoes WHERE dia LIKE '%{dia}%' and Class = '{classe}'")
    result = cursor.fetchone()[0]
    
    return result


def soma_amount(dia):
    cursor.execute(f"SELECT SUM(Amount) FROM transacoes WHERE dia LIKE '%{dia}%'")
    result = cursor.fetchone()[0]
    
    return result


def cria_tabelas():
    df = pd.read_sql('SELECT Time, V1, V28, Amount, Class FROM transacoes', conn)

    descricao = df.describe()
    primeiras_linhas = df.head(10)

    indicesdf = descricao.index.tolist()

    # Adicionar os indices como a primeira coluna do DataFrame
    descricao.insert(0, '', indicesdf)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')  

    ax.table(cellText=descricao.values,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 1]
            )

    plt.savefig('images base\\figura1.png', dpi=300, bbox_inches='tight')

    ax.table(cellText=primeiras_linhas.values,
            colLabels=primeiras_linhas.columns,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 1]
            )

    plt.savefig('images base\\figura2.png', dpi=300, bbox_inches='tight')


def cria_grafico_pizza(dicionario,lc):
    figura = plt.figure(figsize=(20,30)) 
    
    for i in range(len(dicionario)):
        dados = dicionario[i]['dados']
        labels = dicionario[i]['labels']
        cores = dicionario[i]['cores'] 
        titulo = dicionario[i]['titulo']
        legenda = dicionario[i]['legenda']
        
        figura.add_subplot(lc[0],lc[1],i+1)
        plt.pie(dados, labels=labels, autopct='%1.1f%%', colors=cores, startangle=90)
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.legend(title=legenda, labels=labels, loc='best', fontsize=12)
        plt.axis('equal')

    plt.tight_layout()
    plt.savefig('images base\\figura3.png')
    

def cria_grafico_linha(dicionario,lc):
    figura = plt.figure(figsize=(20,45))
    
    for i in range(len(dicionario)):
        label_f = dicionario[i]['label_f']
        label_nf = dicionario[i]['label_nf']
        titulo = dicionario[i]['titulo']
        intervalo = dicionario[i]['intervalo']

        if intervalo == 'total':
            query = ("SELECT Amount, Time, Class FROM transacoes")
        else:
            query = (f"SELECT Amount, Time, Class FROM transacoes WHERE dia = '{intervalo}'")

        df = pd.read_sql_query(query, conn)
    
        nao_fraudes = df[df['Class'] == 0]
        fraudes = df[df['Class'] == 1]

        figura.add_subplot(lc[0],lc[1],i+1)
        plt.plot(nao_fraudes['Time'], nao_fraudes['Amount'], label=label_nf)
        plt.plot(fraudes['Time'], fraudes['Amount'], color='red', linestyle='--', marker='o', label=label_f)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Valor (USD)')
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc='upper center')
    
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('images base\\figura4.png')


def cria_histograma(dicionario,lc):
    fig = plt.figure(figsize=(20,20))

    for i in range(len(dicionario)):
        tipo = dicionario[i]['tipo']
        classe = dicionario[i]['class']
        nbins = dicionario[i]['nbins']
        titulo = dicionario[i]['titulo']
        cor = dicionario[i]['cor']
        xlabel = dicionario[i]['xlabel']

        cursor.execute(f"SELECT {tipo} FROM transacoes WHERE Class = {classe}")
        result = cursor.fetchall()

        x = [a[0] for a in result]

        fig.add_subplot(lc[0],lc[1],i+1)
        bins = np.linspace(min(x), max(x), nbins)
        plt.hist(x, bins=bins, color=cor, edgecolor='black')
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.ylabel('Transações')
        plt.xlabel(xlabel)
        plt.grid(True, linestyle='--', alpha=0.5)

    plt.subplots_adjust(hspace=0.5)
    plt.savefig('images base\\figura5.png')


def cria_histograma_filtrado(dicionario,lc):
    fig = plt.figure(figsize=(20,30))

    for i in range(len(dicionario)):
        tipo = dicionario[i]['tipo']
        classe = dicionario[i]['class']
        coluna = dicionario[i]['coluna']
        intervalo = dicionario[i]['intervalo']
        titulo = dicionario[i]['titulo']
        cor = dicionario[i]['cor']
        xlabel = dicionario[i]['xlabel']

        cursor.execute(f"SELECT {tipo} FROM transacoes WHERE Class = {classe} AND {coluna} >= {intervalo[0]} AND {coluna} <= {intervalo[1]}")
        result = cursor.fetchall()

        x = [a[0] for a in result]

        fig.add_subplot(lc[0],lc[1],i+1)
        plt.hist(x, bins=10, color=cor, edgecolor='black')
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.ylabel('Transações')
        plt.xlabel(xlabel)
        plt.grid(True, linestyle='--', alpha=0.5)
        
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('images base\\figura6.png')