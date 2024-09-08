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
fila_prioridade = []
nicknames = []

def primeira_espera(espera_inicial, myEvent, myEventPausa):
    global primeira_execucao
    if primeira_execucao:
        segundos = converter_para_segundos(espera_inicial)
        if segundos > 0:
            info.printinfo("Iniciando espera inicial.")
            sleep_with_check(segundos, myEvent, myEventPausa, imprimir_fila=False)
            info.printinfo("Espera inicial terminou.")
        primeira_execucao = False

def print_fila(fila):
    global nicknames
    lista = []
    nicks = []
    for f in fila:
        personagem = f[0]
        tempo = f[1]
        tempo_restante = tempo - time.time()
        lista.append(f"\n\t\tPersonagem: {personagem},\tTempo restante: {tempo_restante:.2f} segundos")
        nicks.append(personagem)
    info.printinfo("Fila de prioridade:" + "".join(lista))
    if nicks.__len__() < nicknames.__len__():
        for nick in nicknames:
            if nick not in nicks:
                info.printinfo(f"Personagem {nick} está sendo a prioridade.")
                break
    time.sleep(2)

def iniciar(myEvent, myEventPausa):
    global fila_prioridade
    global nicknames
    fila_prioridade = []
    acoes_person.carregar_craft_categorias()
    # nicknames =        ["Jikininki", "Scalaxy", "Waxius", "Phormid", "Aqsafada", "Kobernn"]
    # tempo_restante =   [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # itens =            ["bracelete_1_10"]

    dados = es.carregar_json(f'{const.PATH_TASK}')
    nicknames = dados['nicknames']
    tempo_restante = dados['tempo_restante']
    itens = dados['itens']

    if tempo_restante.__len__() < nicknames.__len__():
        for _ in range(nicknames.__len__() - tempo_restante.__len__()):
            tempo_restante.append([0, 0, 0])
    

    espera_inicial = dados['tempo_espera_inicial']
    primeira_espera(espera_inicial, myEvent, myEventPausa)

    personagens = es.filtrar_json(nicknames, "nickname", f'{const.PATH_CONSTS}personagens.json')
    # print(personagens)

    crafts = es.filtrar_json(itens, "item", f'{const.PATH_CONSTS}/crafts.json')
    # print(crafts)

    if not myEvent.is_set():
        return
    
    verificar_pausa(myEventPausa)

    
    for i, personagem in enumerate(personagens):
        tempo_espera = time.time() + converter_para_segundos(tempo_restante[i])
        time.sleep(0.1)
        fila_prioridade.append([personagem['nickname'], tempo_espera+2])

    # info.printinfo(f"Fila de prioridade: {fila_prioridade}")
    fila_prioridade.sort(key=lambda x: x[1])
    # info.printinfo(f"Fila de prioridade ordenada: {fila_prioridade}")

    while myEvent.is_set():
        espera_diminuida = False
        houve_falha_conexao = False
        nova_duracao = [0, 0, 0]
        
        fila_prioridade.sort(key=lambda x: x[1])

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        print_fila(fila_prioridade)

        prioridade = fila_prioridade[0]
        info.printinfo(f"Prioridade da vez: {prioridade[0]}")
        fila_prioridade.pop(0)
        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        time.sleep(0.1)
        tempo_sleep = prioridade[1] - time.time()
        info.printinfo(f"Tempo de espera para {prioridade[0]}: {tempo_sleep:.2f} segundos.")
        sleep_with_check(tempo_sleep, myEvent, myEventPausa)

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        index = -1
        for i, personagem in enumerate(personagens):
            if personagem['nickname'] == prioridade[0]:
                index = i
                break
        index_craft = -1
        for i, craft in enumerate(crafts):
            # info.printinfo(f"Craft: {craft}")
            # info.printinfo(f"Item: {itens[index]}")
            if craft['item'] == itens[index]:
                index_craft = i
                break

        personagem = personagens[index]
        craft = crafts[index_craft]
        ##
        ##
        ##
        ##
        ##
        ## tudo pra cima é sobre fila de prioridade, tudo pra baixo é sobre o personagem atual
        ##
        ##
        ##
        ##
        ##
        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        acoes_person.logar(personagem, myEvent, myEventPausa)
        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue
        acoes_person.fechar_popup(myEvent, myEventPausa)

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        duracao, contador = craftar(personagem, craft, myEvent, myEventPausa)

        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue

        if duracao != craft['duração_dia_hora_minuto']:
            # if personagem['nickname'] == nicknames[0]: ## gambiarra pois por enquanto todos tempos valem pra todos personagens
            info.printinfo("Ajustando para esperar menos tempo.")
            espera_diminuida = True
            nova_duracao = duracao
        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        
        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue

        if contador < 0 and craft['precisa_desmontar'] == True: ## nesse cenario o contador é negativo porque faltou recursos e vou verificar se tem algo para desmontar
            info.printinfo("Problema ao craftar, indo desmontar itens na bolsa para tentar novamente.")
            contador_desmontados = desmontar(personagem, craft['item'], (contador*-1), myEvent, myEventPausa)
            acoes_person.fechar_popup(myEvent, myEventPausa)
            verificar_pausa(myEventPausa)
            info.printinfo(f"Foram desmontados {contador_desmontados} itens.")
            if contador_desmontados > 0: ## as vezes retorna None e ainda não entendi o motivo
                info.printinfo("Desmontagem concluída, tentando craftar novamente.")
                duracao, contador = craftar(personagem, craft, myEvent, myEventPausa) ## por causa do comentario acima, eu executo isso fora do if as vezes até descobrir a causa


        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue

        if(craft['precisa_desmontar'] == True and contador > 0):
            info.printinfo(f"Indo desmontar {contador} itens coletados.")
            contador_desmontados = desmontar(personagem, craft['item'], contador, myEvent, myEventPausa)
            info.printinfo(f"Desmontados {contador_desmontados} itens.")

        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        acoes_person.fechar_popup(myEvent, myEventPausa)
        if verificar_erro_conexao(personagem, myEvent, myEventPausa, True): continue
        acoes_person.deslogar(myEvent, myEventPausa)


        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        if myEvent.is_set():
            segundos = 0
            if espera_diminuida is False:
                segundos = converter_para_segundos(craft['duração_dia_hora_minuto'])
            else:
                segundos = converter_para_segundos(nova_duracao)
            tempo_temp = converter_de_segundos(segundos)
            info.printinfo(f"Serviço para {personagem['nickname']} finalizado.\n\tVoltando em: {tempo_temp[0]} dias, {tempo_temp[1]} horas e {tempo_temp[2]} minutos.\n\tTempo em segundos: {segundos:.2f}.")
            # info.printinfo(f"Duração = {nova_duracao}")
            # sleep_with_check(segundos, myEvent, myEventPausa)
            fila_prioridade.append([personagem['nickname'], time.time() + segundos])
            time.sleep(3)
            verificar_pausa(myEventPausa)
            if not myEvent.is_set():
                return
    info.printinfo("Evento finalizado.")
    info.salvar_log()

def verificar_erro_conexao(personagem, myEvent, myEventPausa, reinserir_na_fila=False):
    global fila_prioridade
    if not myEvent.is_set():
        return True
    verificar_pausa(myEventPausa)
    houve_falha_conexao = acoes_person.verificar_erro_conexao(myEvent, myEventPausa)
    if houve_falha_conexao:
        if reinserir_na_fila:
            info.printinfo(f"Houve falha de conexão durante a execução do personagem {personagem['nickname']}, relogando para tentar novamente...", erro=True)
            tempo_maior_prioridade_na_fila = fila_prioridade[0][1]
            segundos = (tempo_maior_prioridade_na_fila - time.time()) * 1.2 ## 20% a mais prioridade para furar a fila
            segundos = segundos if segundos < 0 else segundos * -1 ## se for positivo, multiplica por -1 para ficar negativo
            # tempo_temp = converter_de_segundos(segundos)

            info.printinfo(f"O {personagem['nickname']} foi reinserido na fila com prioridade em segundos: {segundos:.2f}.")
            # info.printinfo(f"Duração = {nova_duracao}")
            # sleep_with_check(segundos, myEvent, myEventPausa)
            fila_prioridade.append([personagem['nickname'], time.time() + segundos])
        return True
    return False

def craftar(personagem, craft, myEvent, myEventPausa):
    acoes_person.abrir_menu_craft(myEvent, myEventPausa)
    duracao, contador = acoes_person.iniciar_todos_slots(personagem, craft, myEvent, myEventPausa)
    if verificar_erro_conexao(personagem, myEvent, myEventPausa): return duracao, contador
    verificar_pausa(myEventPausa)
    if duracao is None and contador is None:
        info.printinfo("Erro ao craftar, ajustando para tempo original.", erro=True)
        duracao = craft['duração_dia_hora_minuto']
        contador = 0
    acoes_person.fechar_menu_craft(myEvent, myEventPausa)
    acoes_person.fechar_popup(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    return duracao, contador

def desmontar(personagem, craft, contador, myEvent, myEventPausa):
    contador_desmontados = 0
    acoes_person.abrir_menu_bolsa(myEvent, myEventPausa)
    acoes_person.abrir_aba_equipamento(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    contador_desmontados = acoes_person.encontrar_itens_e_desmontar(craft, contador, myEvent, myEventPausa)
    if verificar_erro_conexao(personagem, myEvent, myEventPausa): return contador_desmontados
    verificar_pausa(myEventPausa)
    acoes_person.fechar_menu_bolsa(myEvent, myEventPausa)
    # if contador_desmontados is None:
    #     contador_desmontados = 0
    return contador_desmontados


def sleep_with_check(segundos, myEvent, myEventPausa, imprimir_fila=True):
    global fila_prioridade
    if segundos <= 0:
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
            if imprimir_fila:
                print_fila(fila_prioridade)
                info.printinfo(f"Tempo restante: {tempo_restante[0]} dias, {tempo_restante[1]} horas e {tempo_restante[2]} minutos.")

    if myEvent.is_set():
        info.printinfo("Tempo de espera finalizado.")

def verificar_pausa(myEventPausa):
    while myEventPausa.is_set(): pass