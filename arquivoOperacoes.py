import logging
import os
import shutil
from logging import exception
import pandas as pd

def start():
    from main import PATH_BACKUP, PATH_PROJETO
    while True:
        try:
            print("==================== ATENÇÃO! =====================")
            print("| informe o path absoluto do arquivo de conversas |")
            PATH_DIR = input()
            PATH_TXT = os.path.join(PATH_DIR, "_chat.txt")
            print("===================================================")
            if verifica_existencia_arquivo(PATH_DIR, PATH_TXT):
                copiar_arquivo(PATH_PROJETO, PATH_BACKUP, PATH_TXT)
                break
        except exception as e:
            logging.error(e)
    df = ler_txt(PATH_PROJETO, PATH_TXT)
    print(df)
    return df

def verifica_existencia_arquivo(PATH_DIR, PATH_TXT):
    if os.path.exists(PATH_DIR) and os.path.exists(PATH_TXT):
        return True
    else:
        logging.error("Existencia do arquivo nao pode ser confirmada!")
        return False

def copiar_arquivo(PATH_PROJETO, PATH_BACKUP, PATH_TXT):
    try:
        gerenciar_backup(PATH_PROJETO, PATH_BACKUP)
        shutil.copy(PATH_TXT, PATH_PROJETO)
    except exception as e:
        logging.error(e)

def gerenciar_backup(PATH_PROJETO, PATH_BACKUP):
    arquivoAntigo = os.path.join(PATH_PROJETO, "_chat.txt")
    if os.path.isfile(arquivoAntigo): #outro arquivo de chat dentro do projeto
        if os.path.exists(PATH_BACKUP): #existe dir de backup
            shutil.copy(arquivoAntigo, PATH_BACKUP) #faz backup
            os.remove(arquivoAntigo)
        else: #cria outro
            logging.error("diretorio de backup de conversas nao existe, outro foi criado")
            os.makedirs(PATH_BACKUP)
            shutil.copy(arquivoAntigo, PATH_BACKUP)  # faz backup
            os.remove(arquivoAntigo)

def ler_txt(PATH_PROJETO, PATH_TXT):
    try:
        dados = []
        with open(PATH_TXT, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                partes = linha.split('] ')
                if len(partes) == 2:
                    data_hora = partes[0].strip('[')  # Remove o colchete inicial
                    remetente_mensagem = partes[1].split(': ', 1)  # Divide o remetente da mensagem
                    if len(remetente_mensagem) == 2:
                        remetente = remetente_mensagem[0]
                        mensagem = remetente_mensagem[1].strip()
                        data, hora = data_hora.split(' ')
                        dados.append([data, hora, remetente, mensagem])
        df = pd.DataFrame(dados, columns=['data', 'hora', 'remetente', 'mensagem'])
        df = df.drop([0]).reset_index(drop=True) # a primeira linha eh info do zap
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        if df.size < 0:
            logging.error("Historico de chat vazio")
        elif df.size < 2:
            logging.warn("Historico de chat pequeno, possivel erro!")
        return df
    except exception as e:
        logging.error(e)