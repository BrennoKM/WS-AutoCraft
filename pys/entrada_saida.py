import os
import constantes as constantes
from datetime import datetime
import json

def carregar_json(caminho_arquivo_json):
    with open(caminho_arquivo_json, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def filtrar_json(lista, atributo ,caminho_arquivo_json):
    with open(caminho_arquivo_json, 'r', encoding='utf-8') as arquivo:
        personagens = json.load(arquivo)
    
    personagens_filtrados = [personagem for personagem in personagens if personagem[atributo] in lista]
    
    return personagens_filtrados


def salvar_log(log):
    if not os.path.exists(constantes.PATH_LOGS):
        os.makedirs(constantes.PATH_LOGS)
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo_log = os.path.join(constantes.PATH_LOGS, f"log_{data_hora_atual}.txt")
    
    with open(nome_arquivo_log, 'w', encoding='utf-8') as arquivo_log:
        arquivo_log.write(f'{log}\n')
        