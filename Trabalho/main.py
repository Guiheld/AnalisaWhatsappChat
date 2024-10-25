import logging
import os

from analiseDados import resumo_conversas, histograma, historico_remetente, grafico_pizza, grafico_linha
from arquivoOperacoes import start

PATH_PROJETO = os.getcwd()
PATH_BACKUP = os.path.join(PATH_PROJETO, "backups")

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato das mensagens de log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato da data e hora
)

def main():
    df = start()
    while True:
        print("==================== ATENÇÃO! =====================")
        print("|                ESCOLHA UMA OPCAO                |")
        print("| 1. Resumo de conversas                          |")
        print("| 2. Historico de remetente                       |")
        print("| 3. Grafico do historico de remetente            |")
        print("| 4. Grafico de 'Pizza'                           |")
        print("| 5. Grafico de 'linhas'                          |")
        print("===================================================")
        opt = int(input())
        if opt == 1:
            resumo_conversas(df)
        if opt == 2:
            historico_remetente(df)
        if opt == 3:
            histograma(df)
        if opt == 4:
            grafico_pizza(df)
        if opt == 5:
            grafico_linha(df)


if __name__ == '__main__':
    main()


