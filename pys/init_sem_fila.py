import entrada_saida as es
import info as info
import constantes as const
import threading
import time
import acoes_personagem as acoes_person


def converter_para_segundos(tempo):
    dias, horas, minutos = tempo
    total_segundos = dias * 86400 + horas * 3600 + minutos * 60
    return total_segundos

def converter_de_segundos(segundos):
    dias = segundos // 86400
    segundos_restantes = segundos % 86400
    horas = segundos_restantes // 3600
    segundos_restantes %= 3600
    minutos = segundos_restantes // 60
    return dias, horas, minutos

# # Exemplo de uso
# tempo = [0, 2, 0]  # _ dias, _ horas, _ minutos
# segundos = converter_para_segundos(tempo)
# print(f"Total de segundos: {segundos}")

# tempo_original = converter_de_segundos(segundos)
# print(f"Tempo original: {tempo_original}")

primeira_execucao = True

def primeira_espera(espera_inicial, myEvent, myEventPausa):
    global primeira_execucao
    if primeira_execucao:
        segundos = converter_para_segundos(espera_inicial)
        if segundos > 0:
            info.printinfo("Iniciando espera inicial.")
            sleep_with_check(segundos, myEvent, myEventPausa)
            info.printinfo("Espera inicial terminou.")
        primeira_execucao = False

def iniciar(myEvent, myEventPausa):
    acoes_person.carregar_craft_categorias()
    # nicknames =        ["Jikininki", "Scalaxy", "Waxius", "Phormid", "Aqsafada", "Kobernn"]
    # tempo_restante =   [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # itens =            ["bracelete_1_10"]

    dados = es.carregar_json(f'{const.PATH_TASK}')
    nicknames = dados['nicknames']
    tempo_restante = dados['tempo_restante']
    itens = dados['itens']

    espera_inicial = dados['tempo_espera_inicial']
    primeira_espera(espera_inicial, myEvent, myEventPausa)

    personagens = es.filtrar_json(nicknames, "nickname", f'{const.PATH_CONSTS}personagens.json')
    # print(personagens)

    crafts = es.filtrar_json(itens, "item", f'{const.PATH_CONSTS}/crafts.json')
    # print(crafts)

    if not myEvent.is_set():
        return
    
    verificar_pausa(myEventPausa)

    while myEvent.is_set():
        espera_diminuida = False
        nova_duracao = [0, 0, 0]
        for i, personagem in enumerate(personagens):

            duracao = converter_para_segundos(tempo_restante[i])
            sleep_with_check(duracao, myEvent, myEventPausa)

            acoes_person.logar(personagem, myEvent, myEventPausa)
            acoes_person.fechar_popup(myEvent, myEventPausa)

            verificar_pausa(myEventPausa)

            duracao, contador = craftar(personagem, crafts[0], myEvent, myEventPausa)
            if duracao != crafts[0]['duração_dia_hora_minuto']:
                if personagem['nickname'] == nicknames[0]: ## gambiarra pois por enquanto todos tempos valem pra todos personagens
                    info.printinfo("Ajustando para esperar menos tempo.")
                    espera_diminuida = True
                    nova_duracao = duracao
            verificar_pausa(myEventPausa)

            if contador < 0 and crafts[0]['precisa_desmontar'] == True: ## nesse cenario o contador é negativo porque faltou recursos e vou verificar se tem algo para desmontar
                info.printinfo("Problema ao craftar, indo desmontar itens na bolsa para tentar novamente.")
                contador_desmontados = desmontar(crafts[0]['item'], (contador*-1), myEvent, myEventPausa)
                verificar_pausa(myEventPausa)
                info.printinfo(f"Desmontados {contador_desmontados} itens.")
                # if contador_desmontados > 0:
                #     info.printinfo("Desmontagem concluída, tentando craftar novamente.")
                duracao, contador = craftar(personagem, crafts[0], myEvent, myEventPausa)

            if(crafts[0]['precisa_desmontar'] == True and contador > 0):
                info.printinfo(f"Indo desmontar {contador} itens coletados.")
                contador_desmontados = desmontar(crafts[0]['item'], contador, myEvent, myEventPausa)
                info.printinfo(f"Desmontados {contador_desmontados} itens.")

            verificar_pausa(myEventPausa)
            acoes_person.fechar_popup(myEvent, myEventPausa)
            acoes_person.deslogar(myEvent, myEventPausa)

        verificar_pausa(myEventPausa)
        if myEvent.is_set():
            info.printinfo("Todos os personagens foram logados. Aguardando tempo restante.")
            segundos = 0
            if espera_diminuida is False:
                segundos = converter_para_segundos(crafts[0]['duração_dia_hora_minuto'])
            else:
                segundos = converter_para_segundos(nova_duracao)
            info.printinfo(f"Duração = {nova_duracao}")
            sleep_with_check(segundos, myEvent, myEventPausa)
    info.printinfo("Evento finalizado.")

def craftar(personagem, craft, myEvent, myEventPausa):
    acoes_person.abrir_menu_craft(myEvent, myEventPausa)
    duracao, contador = acoes_person.iniciar_todos_slots(personagem, craft, myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    if duracao is None and contador is None:
        info.printinfo("Erro ao craftar, ajustando para tempo original.", erro=True)
        duracao = craft['duração_dia_hora_minuto']
        contador = 0
    acoes_person.fechar_menu_craft(myEvent, myEventPausa)
    acoes_person.fechar_popup(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    return duracao, contador

def desmontar(craft, contador, myEvent, myEventPausa):
    contador_desmontados = 0
    acoes_person.abrir_menu_bolsa(myEvent, myEventPausa)
    acoes_person.abrir_aba_equipamento(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    contador_desmontados = acoes_person.encontrar_itens_e_desmontar(craft, contador, myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    acoes_person.fechar_menu_bolsa(myEvent, myEventPausa)
    # if contador_desmontados is None:
    #     contador_desmontados = 0
    return contador_desmontados


def sleep_with_check(segundos, myEvent, myEventPausa):
    if segundos == 0:
        return
    
    tempo = converter_de_segundos(segundos)
    info.printinfo(f"Aguardando por {tempo[0]} dias, {tempo[1]} horas e {tempo[2]} minutos.")
    intervalo = 1  # Intervalo de verificação em segundos
    intervalo_mensagem = 300  # Intervalo para imprimir a mensagem em segundos
    contador_mensagem = 0

    for _ in range(int(segundos / intervalo)):
        if not myEvent.is_set():
            info.printinfo("Tempo de espera foi cancelado.")
            break
        verificar_pausa(myEventPausa)
        time.sleep(intervalo)
        contador_mensagem += intervalo

        if contador_mensagem >= intervalo_mensagem:
            contador_mensagem = 0
            tempo_restante = converter_de_segundos(segundos - (_ * intervalo))
            info.printinfo(f"Tempo restante: {tempo_restante[0]} dias, {tempo_restante[1]} horas e {tempo_restante[2]} minutos.")

    if myEvent.is_set():
        info.printinfo("Tempo de espera finalizado.")

def verificar_pausa(myEventPausa):
    while myEventPausa.is_set(): pass