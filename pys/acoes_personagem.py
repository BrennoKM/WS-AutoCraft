import pg_simplificado as pgs
import info as info
import entrada_saida as es
import constantes as const
import pyautogui as pg
import time
import tempo

craft_categorias = []
gastou_coin = False

def carregar_craft_categorias():
    global craft_categorias
    craft_categorias = es.carregar_json(f'{const.PATH_CONSTS}crafts_categorias.json')



## 1. Logar
def logar(personagem, myEvent, myEventPausa):
    
    if not myEvent.is_set():
            return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_JOGAR_LOGIN)
    pgs.clicar(1)
    caminho_popup_erro = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_erro_falha_conexao.png"
    while(pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_avancar_login.png', semelhanca=0.8, necessario=True, regiao=const.AREA_BOLSA) is None):
        info.printinfo(f"Aguardando a tela de notícias ser carregada para o personagem {personagem['nickname']}.")
        alvo_erro = pgs.encontrar_alvo(caminho_popup_erro, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_BOLSA)
        if alvo_erro  is not None:
            info.printinfo("Houve uma falha de conexão durante o login. Tentando se conectar novamente em breve.", erro=True)
            pg.sleep(1)
            pg.press('enter')
            pg.sleep(0.2)
            pgs.mover_para(const.POS_BOTAO_JOGAR_LOGIN)
            pg.sleep(2)
            pgs.clicar(1)
        time.sleep(2)
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)
        verificar_alerta(myEvent, myEventPausa)

    if not myEvent.is_set():
            return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_AVANCAR_LOGIN)
    pgs.clicar(1)

    caminho = f'{const.PATH_IMGS_ANCORAS_PERSON}ancora_nickname_{personagem["nickname"].lower()}.png'
    alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=True, regiao=const.AREA_NICKNAME)
    if alvo is None:
        pg.sleep(1)
        pg.press("right")
        alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=False, regiao=const.AREA_NICKNAME)
        if alvo is None:
            for _ in range(13):
                if not myEvent.is_set():
                    return
                verificar_pausa(myEventPausa)
                alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=False, regiao=const.AREA_NICKNAME)
                if alvo is None :
                    pg.sleep(0.2)
                    pg.press("left")
                else:
                    break
                
            for _ in range(13):
                if not myEvent.is_set():
                    return
                verificar_pausa(myEventPausa)
                alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=False, regiao=const.AREA_NICKNAME)
                if alvo is None :
                    pg.sleep(0.2)
                    pg.press("right")
                else:
                    break
        if alvo is None:
            return False
    info.printinfo(f"Personagem {personagem['nickname']} encontrado.")
    if not myEvent.is_set():
            return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_JOGAR)
    pgs.clicar(1)
    pg.sleep(0.3)
    caminho_popup_reconectando = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_reconectando.png"
    while pgs.encontrar_alvo(caminho_popup_reconectando, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_BOLSA) is not None:
        info.printinfo("Esperando a conexão ser concluída.")
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)
        pg.sleep(3)
    if verificar_erro_conexao(myEvent, myEventPausa): return False

    verificar_pausa(myEventPausa)
    pg.sleep(0.1)
    info.printinfo(f"Personagem {personagem['nickname']} logado com sucesso.", False, True)
    return True

## 2. Fechar popup
def fechar_popup(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.sleep(2)
    if verificar_erro_conexao(myEvent, myEventPausa): return
    caminho_popup_nao = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_login_presente_nao.png'
    caminho_popup_sim = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_login_presente_sim.png'
    alvo_nao = pgs.encontrar_alvo(caminho_popup_nao, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP)
    alvo_sim = pgs.encontrar_alvo(caminho_popup_sim, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP)
    if alvo_nao is not None and alvo_sim is not None:
        info.printinfo("Popup de login diário infelizmente apareceu.", erro=True)
        pg.sleep(4)
        if verificar_tela_login(myEvent, myEventPausa): return
        pg.press('f1')
        pg.sleep(0.5)
        if verificar_tela_login(myEvent, myEventPausa): return
        pg.press('f1')
        pg.sleep(0.5)
        if verificar_tela_login(myEvent, myEventPausa): return
        pg.press('f1')
        pg.sleep(0.5)
        if verificar_tela_login(myEvent, myEventPausa): return
        pg.press('f1')
        pg.sleep(0.5)
        if verificar_tela_login(myEvent, myEventPausa): return
        pg.press('f1')
        pg.sleep(0.5)

## 2.1 Tratar erro de conexão
def verificar_erro_conexao(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.sleep(0.7)
    caminho_popup_erro = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_erro_falha_conexao.png"
    caminho_popup_reconectando = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_reconectando.png"
    
    alvo_reconectando = pgs.encontrar_alvo(caminho_popup_reconectando, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP)
    alvo_erro = pgs.encontrar_alvo(caminho_popup_erro, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP)

    if alvo_erro is not None or alvo_reconectando is not None:
        info.printinfo("Houve uma falha de conexão.", erro=True, enviar_msg=True)
        # pg.sleep(1)
        pg.press('enter')
        pg.sleep(0.2)
        # pgs.mover_para(const.POS_BOTAO_JOGAR_LOGIN)
        # pg.sleep(1)
        # pgs.clicar(1)
        return True
    if verificar_tela_login(myEvent, myEventPausa): return True
    if (verificar_alerta(myEvent, myEventPausa)):
        info.printinfo("Houve uma falha.", erro=True, enviar_msg=True)
        return True
    return False

## 2.1.1 verificando reconexao
def verificar_reconectando(myEvent, myEventPausa):
    pg.sleep(2)
    caminho_popup_reconectando = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_reconectando.png"
    while(pgs.encontrar_alvo(caminho_popup_reconectando, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP) is not None):
        info.printinfo("Esperando a conexão ser concluída.")
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)
        pg.sleep(0.2)

## 2.2 Verificar se está na tela de login
def verificar_tela_login(myEvent, myEventPausa):
    verificar_pausa(myEventPausa)
    pg.sleep(0.3)
    caminho_popup_sair = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_sair.png"
    alvo_sair = pgs.encontrar_alvo(caminho_popup_sair, semelhanca=0.8, necessario=False, regiao=const.AREA_BOTAO_SAIR)
    if alvo_sair is not None:
        return True
    return False

## 3. Abrir menu craft
def abrir_menu_craft(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.press("f2")
    pg.sleep(0.3)
    pg.press("1")
    pg.sleep(0.3)
    pg.press("7")

## 4. iniciar todos slots
def iniciar_todos_slots(personagem, craft, myEvent, myEventPausa, segunda_tentativa=False):
    global gastou_coin
    gastou_coin = False

    segundos_originais = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
    nova_duracao_original = tempo.converter_de_segundos(segundos_originais*0.1)
    if craft['especial'] == True:
        nova_duracao_original = tempo.converter_de_segundos(900)

    contador_coletados = 0
    contador_iniciados = 0
    verificou_licenca = False
    if not myEvent.is_set():
        return [nova_duracao_original, contador_coletados, contador_iniciados]
    verificar_pausa(myEventPausa)
    # info.printinfo(f'Iniciando slots para {personagem["nickname"]} com {craft["item"]}')
    # info.printinfo(craft['craft'] in personagem['crafts'])
    # print(f'personagem["crafts"]: {personagem["crafts"]}')
    # print(f'craft["craft"]: {craft["craft"]}')

    if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
    if craft['craft'] in personagem['crafts']:
        info.printinfo(f'Iniciando task para {personagem["nickname"]} com o craft {craft["item"]}')
        pg.sleep(1.5)
        verifica_aba = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_pedidos_ativos.png', semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT_PEDIDOS_ATIVOS)
        pg.sleep(0.4)
        if verifica_aba is None:
            pg.press("right")
            info.printinfo("Não estava na aba de pedidos ativos.\n\tAlternando aba", erro=True)

        
        contador_coletados = verificar_concluidos(personagem, craft, myEvent, myEventPausa)
        caminho_slot = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_slot.png'
        caminho_craft_cadeado = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_cadeado.png'

        for j in range(personagem['slots']):
            iniciou = False
            for i in range(3):
                if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
                pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
                time.sleep(1)
                if not myEvent.is_set():
                    return [nova_duracao_original, contador_coletados, contador_iniciados]
                alvo_slot = pgs.encontrar_alvo(caminho_slot, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT_SLOTS)
                if alvo_slot is not None:
                    pgs.mover_para(alvo_slot)
                    pgs.clicar(2)
                    time.sleep(0.2)
                    verificar_pausa(myEventPausa)
                    resultado = iniciar_craft(personagem, craft, verificou_licenca, myEvent, myEventPausa)
                    if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
                    if resultado is True:
                        info.printinfo("Um craft foi iniciado.")
                        contador_iniciados+=1
                        iniciou = True
                        verificou_licenca = True
                        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
                        pgs.clicar(1)
                    elif resultado is False:
                        info.printinfo("Houve algum problema ao tentar iniciar um craft.", erro=True)
                        if gastou_coin == True:
                            if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
                            info.printinfo("Problema grave aconteceu, coins foram gastas e não foi possível finalizar a task.", erro=True, enviar_msg=True)
                            return [nova_duracao_original, -1, contador_iniciados]
                        if segunda_tentativa == False:
                            if craft['especial'] == True:
                                nova_duracao = tempo.converter_de_segundos(900)
                                return [nova_duracao, (personagem['slots']*-3), contador_iniciados]
                            return [craft['duracao_dia_hora_minuto'], (personagem['slots']*-3), contador_iniciados] ## multiplicado por -3 para que o contador seja negativo
                            ## o contador negativo significa que ele vai tentar desmontar os itens para conseguir recursos
                        else:
                            return [craft['duracao_dia_hora_minuto'], contador_coletados, contador_iniciados]
                    else:
                        info.printinfo("Não foi possível iniciar o craft.", erro=True)

                    verificar_pausa(myEventPausa)
                    time.sleep(0.2)
                    break
                else:
                    alvo_cadeado = pgs.encontrar_alvo(caminho_craft_cadeado, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT_SLOTS)
                    if alvo_cadeado is not None:
                        info.printinfo("Slot bloqueado foi encontrado.")
                        break
                    for _ in range(8 if i == 0 else 4):
                        if not myEvent.is_set():
                            return [nova_duracao_original, contador_coletados, contador_iniciados]
                        verificar_pausa(myEventPausa)
                        # if(i != 0):
                        pg.sleep(0.3)
                        pg.press("down")
                        # else:
                        #     break
                pg.sleep(1)
            iniciados_menor_que_slots = contador_iniciados < j+1 ## j+1 pois o contador inicia em 0 e o contador de iniciados precisa estar sempre um passo a frente
            if iniciados_menor_que_slots and segunda_tentativa == False:
            # if iniciou == False:
                if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
                info.printinfo(f"Não foi possível iniciar {personagem['slots'] - contador_iniciados} crafts no personagem {personagem['nickname']}.\n\tO tempo será diminuído para verificar novamente mais cedo.", erro=True)
            
                segundos = tempo.converter_para_segundos(craft['duracao_dia_hora_minuto'])
                nova_duracao = tempo.converter_de_segundos(segundos*0.1)
                if craft['especial'] == True:
                    nova_duracao = tempo.converter_de_segundos(900)
                return [nova_duracao, contador_coletados, contador_iniciados]
            
        verificar_pausa(myEventPausa)
        if verificar_erro_conexao(myEvent, myEventPausa): return [nova_duracao_original, contador_coletados, contador_iniciados]
        if segunda_tentativa == False:
            info.printinfo(f'Todos os {contador_iniciados} slots foram iniciados corretamente para o personagem {personagem["nickname"]} e {contador_coletados} itens foram coletados.', False, True)
        else:
            info.printinfo(f"Iniciou {contador_iniciados} slots faltantes para o personagem {personagem['nickname']}.", False, True)
        return [craft['duracao_dia_hora_minuto'], contador_coletados, contador_iniciados]
    else:
        info.printinfo(f'O personagem {personagem["nickname"]} não possui o craft {craft["craft"]}.', True, True)
        return [nova_duracao_original, contador_coletados, contador_iniciados]
               
## 4.1 verificar conluidos (passo intermédiario)
def verificar_concluidos(personagem, craft, myEvent, myEventPausa):
    contador=0
    caminho = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_concluido.png'
    for _ in range(personagem['slots']):
        if verificar_erro_conexao(myEvent, myEventPausa): return contador
        if not myEvent.is_set():
            return
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
        pg.sleep(0.3)
        alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
        if alvo is not None:
            if not myEvent.is_set():
                return
            verificar_pausa(myEventPausa)
            pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
            pgs.clicar(1)
            pg.sleep(0.2)
            pgs.mover_para(alvo)
            pgs.clicar(1)
            pg.sleep(0.2)
            if verificar_tela_login(myEvent, myEventPausa): return
            pg.press('f2')
            contador+=1
            pg.sleep(0.2)
            if verificar_erro_conexao(myEvent, myEventPausa): return contador
            ## implementar tratamento de falha pra caso a bolsa esteja cheia e não consiga coletar o item
            info.printinfo("Coletou um craft concluído.")
        else:
            pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
            pgs.clicar(1)
            return contador
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pgs.clicar(1)
    verificar_pausa(myEventPausa)
    return contador

## 4.2 iniciar craft (passo intermédiario)
def iniciar_craft(personagem, craft, verificou_licenca, myEvent, myEventPausa):
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pg.sleep(0.2)
    pgs.clicar(1)
    pg.sleep(0.2)
    pg.press("down")
    pg.sleep(0.2)
    pg.press("up")
    pg.sleep(0.2)
    caminho_craft_alvo = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_{craft['craft']}.png'
    caminho_craft_iniciar_alvo = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_iniciar.png'
    caminho_popup_faltou_recurso = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_faltou_recurso.png'
    for i in range(3):
        if verificar_erro_conexao(myEvent, myEventPausa): return False
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
        # if i == 0:
        #     pgs.clicar(1) ## por enquanto não precisa, parece estar correto abrir a profissão já selecionada
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)
        time.sleep(0.2)
        alvo_craft = pgs.encontrar_alvo(caminho_craft_alvo, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT_SLOTS)
        time.sleep(0.3)
        if alvo_craft is not None:
            info.printinfo("Encontrou a categoria do craft.")
            pgs.mover_para(alvo_craft)
            pgs.clicar(1)
            pg.sleep(2)
            alvo_iniciar = pgs.encontrar_alvo(caminho_craft_iniciar_alvo, semelhanca=0.8, necessario=False, regiao=const.AREA_BOTAO_CRAFT_INICIAR)
            pg.sleep(1)
            if alvo_iniciar is None:
                # if verificar_erro_conexao(myEvent, myEventPausa): return False
                info.printinfo("Não entrou na categoria, clicando mais uma vez.")
                pg.sleep(0.2)
                pgs.clicar(1)
            pg.sleep(1)
            if(craft['especial'] == True):  ## implementar a seleção de crafts especiais futuramente
               return iniciar_craft_especial(personagem, craft, verificou_licenca, myEvent, myEventPausa)
            for _ in range(craft['posicao'] + (craft_categorias[craft['craft']]["slots_especiais"] - 1)):
                # if verificar_erro_conexao(myEvent, myEventPausa): return False
                if not myEvent.is_set():
                    return
                verificar_pausa(myEventPausa)
                pg.press("down")
                pg.sleep(0.15)
            pg.sleep(1)
            if(craft['melhoria'] == True):
                # implementar a verificação caso o craft seja uma melhoria, para escolher um item na bolsa a ser melhorado
                verificar_melhoria(craft, verificou_licenca, myEvent, myEventPausa)
                pg.sleep(2)
                verificou_licenca = True
            if verificou_licenca == False:
                if verificar_licenca(craft, myEvent, myEventPausa) == False:
                    return False
                pg.sleep(2)
            if (craft['melhoria'] == False):
                pg.press("f2")
                pg.sleep(0.1)
            alvo_popup_faltou_recurso = pgs.encontrar_alvo(caminho_popup_faltou_recurso, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_BOLSA)
            if alvo_popup_faltou_recurso is not None:
                if verificar_erro_conexao(myEvent, myEventPausa): return False
                info.printinfo("Faltou recurso para iniciar o craft.", erro=True, enviar_msg=True)
                pg.sleep(0.1)
                pg.press("enter")
                pg.sleep(0.1)
                pg.press("f1")
                pg.sleep(0.1)
                return False
            time.sleep(0.2)
            return True ## não acredito que eu estava esquecendo disso, passei horas procurando
        else:
            if verificar_erro_conexao(myEvent, myEventPausa): return False
            info.printinfo("Não encontrou a categoria do craft.\n\tApertando 'down' pra encontrar.", erro=True)
            # for _ in range(4):
            for _ in range(8 if i == 0 else 4):
                # if verificar_erro_conexao(myEvent, myEventPausa): return False
                if not myEvent.is_set():
                        return
                verificar_pausa(myEventPausa)
                # if(i != 0):
                pg.press("down")
                pg.sleep(0.1)
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pgs.clicar(1)
    time.sleep(0.5)
    verificar_pausa(myEventPausa)
    return False ## falso pois não inicou um craft

## 4.3 verificar licença (passo intermédiario)
def verificar_licenca(craft, myEvent, myEventPausa, primeiro_enter=True):
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    if primeiro_enter == True:
        pgs.press("enter")
    pg.sleep(1.5)
    licenca = craft['licenca']
    alvo_licenca_atual = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_LICENCA}ancora_licenca_{licenca}.png', semelhanca=0.99, necessario=True, regiao=const.AREA_BOTAO_SELECIONAR_LICENCA)
    if alvo_licenca_atual is None:
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        info.printinfo("Licença atual não é a certa. Escolhendo uma licença.")
        pgs.mover_para(const.POS_BOTAO_SELECIONAR_LICENCA)
        pg.sleep(0.3)
        pgs.clicar(1)
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        pg.sleep(1)
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
        pg.sleep(1)
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        for _ in range(30): ## supondo 30 sets de licença na bag
            if not myEvent.is_set():
                return
            verificar_pausa(myEventPausa)
            pgs.press("right")
            pg.sleep(0.3)
            alvo_licenca = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_LICENCA}ancora_licenca_{licenca}_texto.png', semelhanca=0.97, necessario=False, regiao=const.AREA_CRAFT)
            pg.sleep(0.2)
            if alvo_licenca is not None:
                info.printinfo("Licença correta encontrada.")
                pg.press("enter")
                pg.sleep(0.3)
                return True
        info.printinfo("Licença correta não encontrada, indo usar a licenca comum", erro=True)
        for _ in range(30):
            if not myEvent.is_set():
                return
            verificar_pausa(myEventPausa)
            pgs.press("right")
            pg.sleep(0.3)
            alvo_licenca = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_LICENCA}ancora_licenca_{licenca}_texto.png', semelhanca=0.97, necessario=False, regiao=const.AREA_CRAFT)
            pg.sleep(0.2)
            if alvo_licenca is not None:
                info.printinfo("Licença correta encontrada.")
                pg.press("enter")
                pg.sleep(0.3)
                return True
            pg.sleep(0.3)
            alvo_licenca_comum = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_LICENCA}ancora_licenca_1_texto.png', semelhanca=0.99, necessario=False, regiao=const.AREA_CRAFT)
            pg.sleep(0.2)
            if alvo_licenca_comum is not None:
                info.printinfo("Licença comum encontrada.")
                pg.press("enter")
                pg.sleep(0.3)
                return True
        info.printinfo("Licença comum não encontrada.", erro=True)
        return False
    if not myEvent.is_set(): return
    info.printinfo("Licença correta já estava selecionada.")
    pg.sleep(0.3)
    verificar_pausa(myEventPausa)
    return True


## 4.4 verificar melhoria (passo intermédiario)
def verificar_melhoria(craft, verificou_licenca, myEvent, myEventPausa, precisa_iniciar=True):
    if verificou_licenca == False:
        verificar_licenca(craft, myEvent, myEventPausa)
    pg.sleep(1)
    pgs.press("f2")
    alvo_alerta = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_alerta.png', semelhanca=0.8, necessario=False, regiao=const.AREA_POPUP)
    if alvo_alerta is not None:
        info.printinfo("Alerta de melhoria encontrado. Escolhendo um item para melhorar.")
        pg.press("enter")
        pg.sleep(1)
        if precisa_iniciar:
            pgs.press("f2")
            pg.sleep(1)
        return True
    return False

## 4.5 iniciar craft especial (passo intermédiario)
def iniciar_craft_especial(personagem, craft, verificou_licenca, myEvent, myEventPausa, segunda_tentativa=False):
    global gastou_coin
    info.printinfo("Item especial vai ser craftado.")
    pg.sleep(2)
    slots_especiais = craft_categorias[craft['craft']]["slots_especiais"]
    # info.printinfo(f"Range: {slots_especiais}")
    caminho_recursos = f'{const.PATH_IMGS_ANCORAS_CRAFTS_ESPECIAIS}ancora_{craft['item']}_recursos.png'
    caminho_produzido = f'{const.PATH_IMGS_ANCORAS_CRAFTS_ESPECIAIS}ancora_{craft['item']}_produzido.png'
    for i in range(slots_especiais):
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        
        pgs.press("enter")
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
        pg.sleep(1)
        ## o alvo recursos é mais rigoroso porque a maioria dos crafts especiais tem um item que são muito parecidos um com outro
        alvo_recursos = pgs.encontrar_alvo(caminho_recursos, semelhanca=0.98, necessario=True, regiao=const.AREA_CRAFT)
        alvo_produzido = pgs.encontrar_alvo(caminho_produzido, semelhanca=0.90, necessario=True, regiao=const.AREA_CRAFT)
        pg.sleep(1)
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        if alvo_recursos is not None and alvo_produzido is not None:
            info.printinfo("Craft especial encontrado.")
            pg.sleep(1)
            if verificou_licenca == False:
                verificar_licenca(craft, myEvent, myEventPausa, primeiro_enter=False)
                verificou_licenca = True
            pg.sleep(2)
            if not myEvent.is_set(): return
            verificar_pausa(myEventPausa)
            tinha_melhoria = verificar_melhoria(craft, verificou_licenca, myEvent, myEventPausa, precisa_iniciar=False)
            ## verificar_melhoria também serve pra iniciar o craft, mas ele verifica o popup de alerta para selecionar um item
            if tinha_melhoria:
                pgs.press("f2")
                pg.sleep(0.3)
            return True
        pgs.press("f1")
        pg.sleep(0.3)
        pgs.press("down")
    info.printinfo("O craft especial não está disponível.", erro=True)
    if segunda_tentativa == True:
        info.printinfo("Coins foram gastas e o craft não foi encontrado, erro grave aconteceu.", erro=True, enviar_msg=True)
        return False
    if craft['gastar_coin'] == True and segunda_tentativa == False and gastou_coin == False:
        info.printinfo("Indo gastar coins para puxar o craft especial.", False, True)
        pgs.press("up")
        pg.sleep(0.3)
        pgs.press("enter")
        pg.sleep(0.3)
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        verificar_reconectando(myEvent, myEventPausa)
        pgs.press("down")
        pg.sleep(0.3)
        pgs.press("down")
        pg.sleep(0.3)
        pgs.press("enter")
        pg.sleep(1.5)
        for j in range(craft['posicao']+1):
            if not myEvent.is_set(): return
            verificar_pausa(myEventPausa)
            if j != 0:
                pgs.press("down")
            pg.sleep(0.15)
        pg.sleep(0.3)
        pgs.press("enter")
        # while True:
        #     info.printinfo("Vai pressionar f2 e substituir o craft.")
        #     pg.sleep(10)
        ## o alvo recursos é mais rigoroso porque a maioria dos crafts especiais tem um item que são muito parecidos um com outro
        alvo_recursos = pgs.encontrar_alvo(caminho_recursos, semelhanca=0.98, necessario=True, regiao=const.AREA_CRAFT)
        alvo_produzido = pgs.encontrar_alvo(caminho_produzido, semelhanca=0.90, necessario=True, regiao=const.AREA_CRAFT)
        pg.sleep(1)
        if not myEvent.is_set(): return
        verificar_pausa(myEventPausa)
        if alvo_recursos is not None and alvo_produzido is not None:
            info.printinfo("Craft especial encontrado na lista e vai ser puxado para substituição.", False, True)
            pgs.press("f2")
            pg.sleep(0.3)
            pgs.press("f2")
            gastou_coin = True
            pg.sleep(2)
            return iniciar_craft_especial(personagem, craft, verificou_licenca, myEvent, myEventPausa, segunda_tentativa=True)
        info.printinfo("Craft especial não foi encontrado para puxar e gastar coins.", erro=True, enviar_msg=True)
    return False


## 5. fechar menu craft
def fechar_menu_craft(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    if verificar_erro_conexao(myEvent, myEventPausa): return
    if verificar_tela_login(myEvent, myEventPausa): return
    pg.press('f1')
    pg.sleep(0.3)
        
## 6. abrir menu bolsa
def abrir_menu_bolsa(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    if verificar_erro_conexao(myEvent, myEventPausa): return
    if verificar_tela_login(myEvent, myEventPausa): return
    pg.press('f2')
    pg.sleep(0.3)
    pg.press('1')
    pg.sleep(0.3)
    pg.press('2')

## 6.1 abrir aba de equipamentos
def abrir_aba_equipamento(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)
    pgs.clicar(1)
    pg.sleep(0.3)
    if verificar_erro_conexao(myEvent, myEventPausa): return None
    alvo = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_BOLSA}ancora_bolsa_equipamento.png', semelhanca=0.8, necessario=True, regiao=const.AREA_BOLSA)
    if not myEvent.is_set():
        return
    if alvo is not None:
        pgs.mover_para(alvo)
        pg.sleep(0.2)
        pgs.clicar(1)
        pg.sleep(0.3)
    pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)

## 7. encontrar e desmontar itens
def encontrar_itens_e_desmontar(item, contador, myEvent, myEventPausa):
    contador_desmontados = 0
    caminho_popup_cancelar = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_cancelar.png"
    for _ in range(contador):
        if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
        desmontou = False
        for _ in range(3):
            if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
            pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)
            pg.sleep(0.2)
            alvo = pgs.encontrar_alvo(f'{const.PATH_IMGS_ITENS}{item}.png', semelhanca=0.99, regiao=const.AREA_BOLSA, center=True, necessario=True)
            pg.sleep(0.25)
            if not myEvent.is_set():
                return contador_desmontados
            verificar_pausa(myEventPausa)
            if alvo is None:
                if not myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                info.printinfo("Apertando 'down' para procurar no resto da bolsa", erro=True)
                pgs.press('down', 12, 0.1, myEvent, myEventPausa)
                pg.sleep(0.15)
            else:
                if not myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)
                pg.sleep(0.1)
                pgs.clicar(1)
                pg.sleep(0.1)
                pgs.clicar(1)
                pg.sleep(0.1)

                pgs.mover_para(alvo)
                pgs.clicar(1)
                if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
                if verificar_tela_login(myEvent, myEventPausa): return
                pg.press('f2')
                pg.sleep(0.15)
                pg.press('8')
                pg.sleep(0.15)
                if not myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
                if verificar_tela_login(myEvent, myEventPausa): return
                pg.press('f2')
                # pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)
                if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
                info.printinfo("Um item está sendo desmontado.")
                while (pgs.encontrar_alvo(caminho_popup_cancelar, semelhanca=0.8, necessario=False, regiao=const.AREA_BOLSA) is not None):
                    pg.sleep(1) ## espera dinamica para desmontar
                pg.sleep(1)
                verificar_pausa(myEventPausa)
                # pgs.clicar(1)
                # pg.sleep(0.1)
                # pgs.clicar(1)
                pg.sleep(0.1)
                contador_desmontados+=1
                desmontou = True
                break
        if (desmontou == False):
            info.printinfo("Todos itens foram/estão desmontados.")
            break
    if verificar_erro_conexao(myEvent, myEventPausa): return contador_desmontados
    info.printinfo(f"Desmontagem concluída. Total de itens desmontados: {contador_desmontados}")
    return contador_desmontados


## 8. fechar menu bolsa
def fechar_menu_bolsa(myEvent, myEventPausa):
    if not myEvent.is_set(): return
    verificar_pausa(myEventPausa)
    if verificar_erro_conexao(myEvent, myEventPausa): return
    if verificar_tela_login(myEvent, myEventPausa): return
    pg.press('f1')
    pg.sleep(0.3)

## 9. deslogar
def deslogar(myEvent, myEventPausa):
    if not verificar_tela_login(myEvent, myEventPausa):
        fechar_menu_craft(myEvent, myEventPausa)
        fechar_menu_bolsa(myEvent, myEventPausa)
        verificar_alerta(myEvent, myEventPausa)
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f1')
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f1')
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f1')
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f1')
    verificar_pausa(myEventPausa)
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f2')
        pg.sleep(0.3)
        pg.press('9')
        pg.sleep(0.2)
        pg.press('6')
        pg.sleep(0.2)
    if not verificar_tela_login(myEvent, myEventPausa):
        pg.press('f2')

    pg.sleep(2)
    if verificar_tela_login(myEvent, myEventPausa):
        info.printinfo("Deslogou com sucesso.", False, True)
        return True
    else:
        info.printinfo("Não conseguiu deslogar. Tentando novamente", erro=True, enviar_msg=True)
        pg.sleep(0.2)
        return deslogar(myEvent, myEventPausa)
         

## 9.1 verificando alerta
def verificar_alerta(myEvent, myEventPausa):
    caminho_alerta = f"{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_alerta.png"
    alvo_alerta = pgs.encontrar_alvo(caminho_alerta, semelhanca=0.8, necessario=False, alvo_problema=True, regiao=const.AREA_POPUP)
    if alvo_alerta is not None:
        info.printinfo("Popup de alerta foi encontrado.", True, True)
        pg.sleep(0.2)
        pg.press("enter")
        pg.sleep(0.2)
        return True
    return False

## 0. pausando (passo opcional)
def verificar_pausa(myEventPausa):
    while myEventPausa.is_set(): pass