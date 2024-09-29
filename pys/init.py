import entrada_saida as es
import info as info
import constantes as const
import threading
import time
import acoes_personagem as acoes_person
from fila_prioridade import Fila_prioridade as Filap
import tempo


# # Exemplo de uso
# tempo = [0, 2, 0]  # _ dias, _ horas, _ minutos
# segundos = converter_para_segundos(tempo)
# print(f"Total de segundos: {segundos}")

# tempo_original = converter_de_segundos(segundos)
# print(f"Tempo original: {tempo_original}")

primeira_execucao = True
fila_prioridade = Filap()
nicknames = []

def primeira_espera(espera_inicial, myEvent, myEventPausa):
    global primeira_execucao
    if primeira_execucao:
        segundos = tempo.converter_para_segundos(espera_inicial)
        if segundos > 0:
            info.printinfo("Iniciando espera inicial.")
            sleep_with_check(segundos, myEvent, myEventPausa, imprimir_fila=False)
            info.printinfo("Espera inicial terminou.")
        primeira_execucao = False

def deslogar(myEvent, myEventPausa):
    acoes_person.deslogar(myEvent, myEventPausa)

def print_fila(fila=None, fila_detalhada=False):
    fila = fila_prioridade
    fila.print_queue(fila_detalhada)

def resetar_fila():
    global fila_prioridade
    fila_prioridade.reset()
    info.printinfo("Fila de prioridade resetada.", False, True)

def drop_task(id):
    global fila_prioridade
    fila_prioridade.drop(id)

def add_task(nickname, tempo_restante, item, slots_disponiveis, reinserir_na_fila, gastar_coin, requisisao_bot=False):
    global fila_prioridade
    fila_prioridade.enqueue(nickname, tempo_restante, item, slots_disponiveis, reinserir_na_fila, gastar_coin, requisisao_bot=True)
    

def iniciar(myEvent, myEventPausa):
    global fila_prioridade
    global nicknames
    global primeira_execucao
    primeira_execucao = True
    if fila_prioridade.has_novas_tasks() == False:
        fila_prioridade.reset()
    acoes_person.carregar_craft_categorias()

    dados = es.carregar_json(f'{const.PATH_TASK}')
    try:
        nicknames = dados['nicknames']
        tempo_restante = dados['tempo_restante']
        itens = dados['itens']
        slots_disponiveis = dados['slots_disponiveis']
        reinserir_na_fila = dados['reinserir_na_fila']
        gastar_coin = dados['gastar_coin']
        espera_inicial = dados['tempo_espera_inicial']
    except KeyError:
        info.printinfo("Erro ao carregar os dados da task. Verifique se os campos estão corretos.", True, True)
        return

    if tempo_restante.__len__() < nicknames.__len__():
        for _ in range(nicknames.__len__() - tempo_restante.__len__()):
            tempo_restante.append([0, 0, 0])
    
    if slots_disponiveis.__len__() < nicknames.__len__():
        for _ in range(nicknames.__len__() - slots_disponiveis.__len__()):
            slots_disponiveis.append(-1)
    
    if reinserir_na_fila.__len__() < nicknames.__len__():
        for _ in range(nicknames.__len__() - reinserir_na_fila.__len__()):
            reinserir_na_fila.append(False)

    if gastar_coin.__len__() < nicknames.__len__():
        for _ in range(nicknames.__len__() - gastar_coin.__len__()):
            gastar_coin.append(False)

    primeira_espera(espera_inicial[0], myEvent, myEventPausa)

    personagens = es.filtrar_json(nicknames, "nickname", f'{const.PATH_CONSTS}personagens.json')
    # print(personagens)

    crafts = es.filtrar_json(itens, "item", f'{const.PATH_CONSTS}/crafts.json')
    # print(crafts)

    if not myEvent.is_set():
        return
    
    verificar_pausa(myEventPausa)

    fila_prioridade.init(nicknames, tempo_restante, itens, slots_disponiveis, reinserir_na_fila, gastar_coin)
  
    time.sleep(0.1)

    # info.printinfo(f"Fila de prioridade: {fila_prioridade}")
    # fila_prioridade.sort(key=lambda x: x[1])
    # info.printinfo(f"Fila de prioridade ordenada: {fila_prioridade}")

    while myEvent.is_set():
        if fila_prioridade.has_novas_tasks() == True:
            info.printinfo("Nova(s) task(s) adicionada(s), atualizando a lista de personagens e itens.")
            novos_nicks, novos_itens = fila_prioridade.get_novas_tasks()
            for nick in novos_nicks:
                nicknames.append(nick)
            for item in novos_itens:
                itens.append(item)
            # info.printinfo(f"Nicknames: {nicknames}")
            # info.printinfo(f"Itens: {itens}")
            personagens = es.filtrar_json(nicknames, "nickname", f'{const.PATH_CONSTS}personagens.json')
            # info.printinfo(personagens)

            crafts = es.filtrar_json(itens, "item", f'{const.PATH_CONSTS}/crafts.json')
            # info.printinfo(crafts)

        
        # fila_prioridade.sort()

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return

        prioridade = fila_prioridade.dequeue()
        print_fila(fila_prioridade)
        # info.printinfo(f"Prioridade da vez: {prioridade[0]}")
        # info.printinfo(f"Prioridade: {prioridade}")
        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        time.sleep(0.1)
        tempo_sleep = prioridade[1] - time.time()
        info.printinfo(f"Tempo de espera para {prioridade[0]}: {tempo_sleep:.2f} segundos.", False, True)
        finalizou, tempo_restante_sleep = sleep_with_check(tempo_sleep, myEvent, myEventPausa)
        if finalizou == False:
            info.printinfo(f"Tempo de espera foi interrompido. Restam {tempo_restante_sleep:.2f} segundos para o personagem {prioridade[0]}.", False, True)
            # fila_prioridade.dequeue()
            fila_prioridade.enqueue(prioridade[0], time.time() + tempo_restante_sleep, prioridade[2], prioridade[3], prioridade[4], prioridade[5])
            continue
        if fila_prioridade.is_priority_droped() == True:
            fila_prioridade.reset_priority_droped()
            info.printinfo(f"Prioridade {prioridade[0]} foi dropada da fila.", erro=True, enviar_msg=True)
            continue

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        index_persoangem = -1
        for i, personagem in enumerate(personagens):
            if personagem['nickname'] == prioridade[0]:
                index_persoangem = i
                break
        index_craft = -1
        # info.printinfo(f"Prioridade[2]: {prioridade[2]}")
        for i, craft in enumerate(crafts):
            # info.printinfo(f"Craft: {craft}")
            # info.printinfo(f"Item: {itens[index]}")
            if craft['item'] == prioridade[2]:
                index_craft = i
                break

        personagem = personagens[index_persoangem]
        craft = crafts[index_craft]
        craft["gastar_coin"] = prioridade[5]
        personagem["reinserir_na_fila"] = prioridade[4]
        personagem['slots'] = personagem['slots'] if prioridade[3] == -1 else prioridade[3]

        info.printinfo(f"Personagem:\t{personagem['nickname']},\n\tCraft: {craft['item']},\n\tSlots: {personagem['slots']},\n\tReinserir na fila: {prioridade[4]},\n\tGastar coin: {craft["gastar_coin"]}", False, True)
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
        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, True): continue
        acoes_person.fechar_popup(myEvent, myEventPausa)

        # contador_desmontados = desmontar(personagem, craft['item'], (5), myEvent, myEventPausa) ## apenas para testes, não descomentar

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
            acoes_person.deslogar(myEvent, myEventPausa)
            return
        # info.printinfo(f"Indo craftar o item: {craft}")

        duracao, contador_coletados, contador_iniciados = craftar(personagem, craft, myEvent, myEventPausa)

        espera_diminuida = False
        houve_falha_conexao = False
        nova_duracao = [0, 0, 0]
        slots_totais_disponiveis = personagem['slots']
        qnt_faltantes = personagem['slots'] - contador_iniciados
        info.printinfo(f"Slots totais disponíveis: {slots_totais_disponiveis}, Slots iniciados: {contador_iniciados}, Slots faltantes: {qnt_faltantes}", False, True)
        

        if duracao != craft['duracao_dia_hora_minuto']:
            info.printinfo("Ajustando para esperar menos tempo.")
            espera_diminuida = True
            nova_duracao = duracao

        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, False): 
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=True)
            continue

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
            acoes_person.deslogar(myEvent, myEventPausa)
            return
        
        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, False): 
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=True)
            continue

        if contador_coletados < 0 and craft['precisa_desmontar'] == False:
            segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
            temp_duracao = tempo.converter_de_segundos(segundos*0.1)
            if craft['especial'] == True:
                info.printinfo("Problema ao craftar porque o craft especial não estava disponível, ajustando para tempo para esperar menos.", erro=True, enviar_msg=True)
                temp_duracao = tempo.converter_de_segundos(900)
            else:
                info.printinfo("Problema ao craftar por falta de recursos, ajustando para tempo para esperar menos.", erro=True)
            espera_diminuida = True
            nova_duracao = temp_duracao


        if contador_coletados < 0 and craft['precisa_desmontar'] == True: ## nesse cenario o contador é negativo porque faltou recursos e vou verificar se tem algo para desmontar
            info.printinfo("Problema ao craftar, indo desmontar itens na bolsa para tentar novamente.")
            contador_desmontados = desmontar(personagem, craft['item'], (contador_coletados*-1), myEvent, myEventPausa)
            acoes_person.fechar_popup(myEvent, myEventPausa)
            verificar_pausa(myEventPausa)
            info.printinfo(f"Foram desmontados {contador_desmontados} itens.")
            
            segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
            temp_duracao = tempo.converter_de_segundos(segundos*0.1)
            if contador_desmontados > 0: ## as vezes retorna None e ainda não entendi o motivo
                info.printinfo("Desmontagem concluída, tentando craftar novamente.")
                temp_duracao, temp_contador_coletados, temp_contador_iniciados = craftar(personagem, craft, myEvent, myEventPausa, segunda_tentativa=True) ## por causa do comentario acima, eu executo isso fora do if as vezes até descobrir a causa
                qnt_faltantes = personagem['slots'] - temp_contador_iniciados - contador_iniciados
                if temp_contador_coletados < 0:
                    segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
                    temp_duracao = tempo.converter_de_segundos(segundos*0.1)
            if temp_duracao != craft['duracao_dia_hora_minuto']:
                info.printinfo("Ajustando para esperar menos tempo.")
                espera_diminuida = True
                nova_duracao = temp_duracao


        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, False): 
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=True)
            continue

        if(craft['precisa_desmontar'] == True and contador_coletados > 0):
            info.printinfo(f"Indo desmontar {contador_coletados} itens coletados.")
            contador_desmontados = desmontar(personagem, craft['item'], contador_coletados, myEvent, myEventPausa)
            info.printinfo(f"Desmontados {contador_desmontados} itens.")

        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, False): 
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=True)
            continue

        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
            acoes_person.deslogar(myEvent, myEventPausa)
            return
        acoes_person.fechar_popup(myEvent, myEventPausa)
        if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, False): 
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=True)
            continue
        acoes_person.deslogar(myEvent, myEventPausa)


        verificar_pausa(myEventPausa)
        if not myEvent.is_set():
                return
        if myEvent.is_set():
            procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa)
            if not myEvent.is_set():
                return
    info.printinfo("Evento finalizado.")
    acoes_person.deslogar(myEvent, myEventPausa)

def procedimento_pos_task(personagem, craft, prioridade, espera_diminuida, nova_duracao, qnt_faltantes, myEvent, myEventPausa, houve_falha_conexao=False):
    global fila_prioridade
    slots_totais_disponiveis = personagem['slots']

    if houve_falha_conexao and fila_prioridade.is_empty() == False:
        tempo_maior_prioridade_na_fila = fila_prioridade.peek()[1]
        segundos_temp = (tempo_maior_prioridade_na_fila - time.time()) * 1.2 ## 20% a mais prioridade para furar a fila
        segundos_temp = segundos_temp if segundos_temp < 0 else segundos_temp * -1 ## se for positivo, multiplica por -1 para ficar negativo
        nova_duracao = tempo.converter_de_segundos(segundos_temp)

    if prioridade[4] == False and espera_diminuida == False: ## não é para reinserir na fila
        info.printinfo(f"Serviço para {personagem['nickname']} finalizado. Sem reinserção na fila.", False, True)
        # fila_prioridade.dequeue()
        return
    segundos = 0
    if espera_diminuida is False:
        segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
    else:
        segundos = tempo.converter_para_segundos(nova_duracao)
    tempo_temp = tempo.converter_de_segundos(segundos)

    # info.printinfo(f"Foram iniciados {slots_totais_disponiveis - qnt_faltantes} slots com sucesso.", erro=False, enviar_msg=True)
    # info.printinfo(f"qnt_faltantes: {qnt_faltantes}")
    if qnt_faltantes == 0:
        segundos_originais = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
        temp_segundos = craft['duracao_dia_hora_minuto']
        info.printinfo(f"Serviço para {personagem['nickname']} finalizado.\n\tVoltando em: {temp_segundos[0]} dias, {temp_segundos[1]} horas e {temp_segundos[2]} minutos.\n\tTempo em segundos: {segundos_originais:.2f}.", False, True)
        temp_segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
        
        fila_prioridade.enqueue(personagem['nickname'], time.time() + temp_segundos, prioridade[2], personagem['slots'], prioridade[4], prioridade[5])

    else:
        iniciou_algum = slots_totais_disponiveis - qnt_faltantes > 0
        if iniciou_algum:
            info.printinfo(f"Foram iniciados {slots_totais_disponiveis - qnt_faltantes} slots com sucesso e {qnt_faltantes} slots não foram inciados.", erro=True, enviar_msg=True)
            if segundos > 0:
                info.printinfo(f"Serviço para {personagem['nickname']} parcialmente finalizado.\n\tVoltando em: {tempo_temp[0]} dias, {tempo_temp[1]} horas e {tempo_temp[2]} minutos.\n\tTempo em segundos: {segundos:.2f}.", False, True)
            else:
                info.printinfo(f"Serviço para {personagem['nickname']} parcialmente finalizado.\n\tVoltando em imediatamente.\n\tTempo em segundos: {segundos:.2f}.", False, True)
                
        else:
            info.printinfo(f"Nenhum slot foi iniciado com sucesso.", erro=True, enviar_msg=True)
            if segundos > 0:
                info.printinfo(f"Serviço para {personagem['nickname']} não foi finalizado com sucesso.\n\tVoltando em: {tempo_temp[0]} dias, {tempo_temp[1]} horas e {tempo_temp[2]} minutos.\n\tTempo em segundos: {segundos:.2f}.", True, True)
            else:
                info.printinfo(f"Serviço para {personagem['nickname']} não foi finalizado.\n\tVoltando em imediatamente.\n\tTempo em segundos: {segundos:.2f}.", False, True)
              
        fila_prioridade.enqueue(personagem['nickname'], time.time() + segundos, prioridade[2], qnt_faltantes, prioridade[4], prioridade[5])
        
        if iniciou_algum and prioridade[4] == True:
            info.printinfo(f"A fila foi bifurcada para o personagem {personagem['nickname']}.", erro=False, enviar_msg=True)
            temp_segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
            fila_prioridade.enqueue(personagem['nickname'], time.time() + temp_segundos, craft['item'], slots_totais_disponiveis - qnt_faltantes, prioridade[4], prioridade[5])

    time.sleep(3)
    verificar_pausa(myEventPausa)

def verificar_erro_conexao(personagem, craft, myEvent, myEventPausa, reinserir_na_fila=False):
    global fila_prioridade
    if not myEvent.is_set():
        acoes_person.deslogar(myEvent, myEventPausa)
        return True
    verificar_pausa(myEventPausa)
    houve_falha_conexao = acoes_person.verificar_erro_conexao(myEvent, myEventPausa)
    if houve_falha_conexao:
        if reinserir_na_fila:
            info.printinfo(f"Houve falha de conexão durante a execução do personagem {personagem['nickname']}, relogando para tentar novamente...", erro=True, enviar_msg=True)
            tempo_maior_prioridade_na_fila = fila_prioridade.peek()[1]
            segundos = (tempo_maior_prioridade_na_fila - time.time()) * 1.2 ## 20% a mais prioridade para furar a fila
            segundos = segundos if segundos < 0 else segundos * -1 ## se for positivo, multiplica por -1 para ficar negativo
            # tempo_temp = converter_de_segundos(segundos)

            info.printinfo(f"O {personagem['nickname']} foi reinserido na fila com prioridade em segundos: {segundos:.2f}.")
            # info.printinfo(f"Duração = {nova_duracao}")
            # sleep_with_check(segundos, myEvent, myEventPausa)
            # fila_prioridade.dequeue()
            fila_prioridade.enqueue(personagem['nickname'], time.time() + segundos, craft['item'], personagem['slots'], personagem["reinserir_na_fila"], craft['gastar_coin'])
        return True
    return False

def craftar(personagem, craft, myEvent, myEventPausa, segunda_tentativa=False):
    acoes_person.abrir_menu_craft(myEvent, myEventPausa)
    duracao, contador_coletados, contador_iniciados = acoes_person.iniciar_todos_slots(personagem, craft, myEvent, myEventPausa, segunda_tentativa)
    if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa): return duracao, contador_coletados, contador_iniciados
    verificar_pausa(myEventPausa)
    if duracao is None:
        info.printinfo("Erro ao craftar, ajustando para tempo original.", erro=True)
        duracao = craft['duracao_dia_hora_minuto']
    acoes_person.fechar_menu_craft(myEvent, myEventPausa)
    acoes_person.fechar_popup(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    return duracao, contador_coletados, contador_iniciados

def desmontar(personagem, craft, contador, myEvent, myEventPausa):
    contador_desmontados = 0
    acoes_person.abrir_menu_bolsa(myEvent, myEventPausa)
    acoes_person.abrir_aba_equipamento(myEvent, myEventPausa)
    verificar_pausa(myEventPausa)
    contador_desmontados = acoes_person.encontrar_itens_e_desmontar(craft, contador, myEvent, myEventPausa)
    if verificar_erro_conexao(personagem, craft, myEvent, myEventPausa): return contador_desmontados
    verificar_pausa(myEventPausa)
    acoes_person.fechar_menu_bolsa(myEvent, myEventPausa)
    # if contador_desmontados is None:
    #     contador_desmontados = 0
    return contador_desmontados


def sleep_with_check(segundos, myEvent, myEventPausa, imprimir_fila=True):
    global fila_prioridade
    if segundos <= 0:
        return True, 0

    temp_tempo = tempo.converter_de_segundos(segundos)
    info.printinfo(f"Aguardando por {temp_tempo[0]} dias, {temp_tempo[1]} horas e {temp_tempo[2]} minutos.", False, True)
    intervalo = 1  # Intervalo de verificação em segundos
    intervalo_mensagem = 300  # Intervalo para imprimir a mensagem em segundos
    contador_mensagem = 0

    tempo_inicial = time.time()
    tempo_decorrido = 0

    while tempo_decorrido < segundos:
        if not myEvent.is_set():
            info.printinfo("Tempo de espera foi cancelado.")
            return True, segundos - int(tempo_decorrido)

        time.sleep(intervalo)
        tempo_decorrido = time.time() - tempo_inicial

        if fila_prioridade.has_novas_tasks() == True:
            info.printinfo("Nova(s) task(s) adicionada(s) enquanto está em espera. Atualizando fila de prioridade.")
            return False, segundos - int(tempo_decorrido)
        
        if fila_prioridade.is_priority_droped() == True:
            info.printinfo("Prioridade dropada enquanto está em espera.", erro=True, enviar_msg=True)
            return True, segundos - int(tempo_decorrido)

        contador_mensagem += intervalo
        if contador_mensagem >= intervalo_mensagem:
            contador_mensagem = 0
            tempo_restante = tempo.converter_de_segundos(segundos - int(tempo_decorrido))
            if imprimir_fila:
                print_fila(fila_prioridade)
            info.printinfo(f"Tempo restante: {tempo_restante[0]} dias, {tempo_restante[1]} horas e {tempo_restante[2]} minutos.", False, True)

        # Verificar pausa
        if myEventPausa.is_set():
            info.printinfo("Pausa detectada durante a espera. Aguardando despausar...", False, True)
            while myEventPausa.is_set():
                if not myEvent.is_set():
                    info.printinfo("Tempo de espera foi cancelado durante a pausa.")
                    return False, segundos - int(tempo_decorrido)
                time.sleep(intervalo)
                tempo_decorrido = time.time() - tempo_inicial
                contador_mensagem += intervalo

    if myEvent.is_set():
        info.printinfo("Tempo de espera finalizado.", False, True)
        return True, 0

def verificar_pausa(myEventPausa):
    while myEventPausa.is_set(): pass