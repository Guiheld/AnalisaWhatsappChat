import pandas as pd
import matplotlib.pyplot as plt


def resumo_conversas(df):
    mensagens_por_remetente = separar_msg_por_remetente(df)
    quantidade_mensagens = [(remetente, len(mensagens)) for remetente, mensagens in mensagens_por_remetente.items()]
    quantidade_mensagens.sort(key=lambda x: x[1], reverse=True)
    for remetente, quantidade in quantidade_mensagens:
        print(f"Remetente: {remetente}, Quantidade de mensagens: {quantidade}")
        print()

def historico_remetente(df):
    remetentes_unicos = df['remetente'].unique()
    print("Remetentes:")
    for remetente in remetentes_unicos:
        print(remetente)
    print("Digite o nome do remetente para puxar o historico, o nome deve ser igual")
    remetente_especifico = input()
    if remetente_especifico:
        df_filtrado = df[df['remetente'] == remetente_especifico]
    else:
        df_filtrado = df
    if df_filtrado.empty:
        print(f"Nenhuma mensagem encontrada para o remetente: {remetente_especifico}")
        return

    for index, row in df_filtrado.iterrows():
        print(f"Data: {row['data']}, Hora: {row['hora']}, Mensagem: {row['mensagem']}")

def separar_msg_por_remetente(df):
    mensagens_por_remetente = {}
    for index, row in df.iterrows():
        remetente = row['remetente']
        mensagem = row['mensagem']
        if remetente in mensagens_por_remetente:
            # Adiciona a nova mensagem à lista existente
            mensagens_por_remetente[remetente].append(mensagem)
        else:
            # Cria uma nova entrada no dicionário com a primeira mensagem
            mensagens_por_remetente[remetente] = [mensagem]
    return mensagens_por_remetente

def histograma(df):
    df = df[df['mensagem'].notnull() & (df['mensagem'] != '')]
    mensagens_por_dia = df.groupby(['data', 'remetente']).size().reset_index(name='quantidade')
    print(mensagens_por_dia)
    plt.figure(figsize=(12, 6))

    remetentes = mensagens_por_dia['remetente'].unique()
    for remetente in remetentes:
        # Filtrar dados do remetente atual
        dados_remetente = mensagens_por_dia[mensagens_por_dia['remetente'] == remetente]
        # Plotar o gráfico de barras para o remetente
        plt.bar(dados_remetente['data'], dados_remetente['quantidade'], label=remetente)

    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.title('Quantidade de Mensagens por Dia para Cada Remetente')
    plt.xticks(rotation=45)
    plt.legend(title='Remetente')
    plt.tight_layout()
    plt.show()
    print("Data Frame gerado para o grafico:")
    print(mensagens_por_dia)
