# AREA_TELA_WARSPEAR = (961, 41, 957, 975)

# POS_BOTAO_JOGAR_LOGIN = (1437, 890)
# POS_BOTAO_AVANCAR_LOGIN = (1566, 817)
# AREA_BOTAO_SAIR = (962, 947, 187, 63)
# AREA_POPUP = (1153, 317, 598, 384)


# AREA_PERSONAGEM = (1219, 268, 434, 61)
# AREA_NICKNAME = (1221, 449, 248, 79)
# POS_BOTAO_JOGAR = (1570, 819)

# AREA_CRAFT = (1219, 268, 435, 513)
# AREA_CRAFT_SLOTS = (1191, 219, 121, 616)
# AREA_CRAFT_PEDIDOS_ATIVOS = (1233, 302, 402, 83)
# POS_BOTAO_CRAFT_MENU = (1438, 351)
# AREA_BOTAO_CRAFT_INICIAR = (1451, 754, 230, 113)


# AREA_BOLSA = (1217, 145, 436, 867)
# POS_BOTAO_BOLSA_MENU = (1430, 235)

import os
import sys
import json

# Diretório onde o executável ou script está sendo executado
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.join(os.path.dirname(sys.executable), 'pys')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório do script

# Caminho para o arquivo JSON
PATH_JSON = os.path.join(BASE_DIR, '..\\consts\\posicao_area.json')

# Função para carregar constantes do JSON
def carregar_constantes():
    with open(PATH_JSON, 'r') as f:
        return json.load(f)

# Função para salvar constantes no JSON
def salvar_constantes(constantes):
    with open(PATH_JSON, 'w') as f:
        json.dump(constantes, f, indent=4)

# Carregar constantes
constantes = carregar_constantes()

# Atribuir variáveis
AREA_TELA_WARSPEAR = tuple(constantes["AREA_TELA_WARSPEAR"])
POS_BOTAO_JOGAR_LOGIN = tuple(constantes["POS_BOTAO_JOGAR_LOGIN"])
POS_BOTAO_AVANCAR_LOGIN = tuple(constantes["POS_BOTAO_AVANCAR_LOGIN"])
AREA_BOTAO_SAIR = tuple(constantes["AREA_BOTAO_SAIR"])
AREA_POPUP = tuple(constantes["AREA_POPUP"])
AREA_PERSONAGEM = tuple(constantes["AREA_PERSONAGEM"])
AREA_NICKNAME = tuple(constantes["AREA_NICKNAME"])
POS_BOTAO_JOGAR = tuple(constantes["POS_BOTAO_JOGAR"])
AREA_CRAFT = tuple(constantes["AREA_CRAFT"])
AREA_CRAFT_SLOTS = tuple(constantes["AREA_CRAFT_SLOTS"])
AREA_CRAFT_PEDIDOS_ATIVOS = tuple(constantes["AREA_CRAFT_PEDIDOS_ATIVOS"])
POS_BOTAO_CRAFT_MENU = tuple(constantes["POS_BOTAO_CRAFT_MENU"])
AREA_BOTAO_CRAFT_INICIAR = tuple(constantes["AREA_BOTAO_CRAFT_INICIAR"])
AREA_BOLSA = tuple(constantes["AREA_BOLSA"])
POS_BOTAO_BOLSA_MENU = tuple(constantes["POS_BOTAO_BOLSA_MENU"])

# Caminhos para imagens
PATH_IMGS_ICON = os.path.join(BASE_DIR, '..\\imgs\\icones\\')
PATH_IMGS_ANCORAS_CRAFT = os.path.join(BASE_DIR, '..\\imgs\\ancoras\\ancoras craft\\')
PATH_IMGS_ANCORAS_PERSON = os.path.join(BASE_DIR, '..\\imgs\\ancoras\\ancoras personagens\\')
PATH_IMGS_ANCORAS_BOLSA = os.path.join(BASE_DIR, '..\\imgs\\ancoras\\ancoras bolsa\\')
PATH_IMGS_ANCORAS_POPUP = os.path.join(BASE_DIR, '..\\imgs\\ancoras\\ancoras popup\\')
PATH_IMGS_ITENS = os.path.join(BASE_DIR, '..\\imgs\\itens\\')

PATH_ITENS = os.path.join(BASE_DIR, '..\\itens\\')
PATH_CONSTS = os.path.join(BASE_DIR, '..\\consts\\')
PATH_LOGS = os.path.join(BASE_DIR, '..\\logs\\')

PATH_TASK = os.path.join(BASE_DIR, '..\\task.json')