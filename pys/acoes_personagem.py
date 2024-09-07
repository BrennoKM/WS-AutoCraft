import pg_simplificado as pgs
import info as info
import entrada_saida as es
import constantes as const
import pyautogui as pg
import time

craft_categorias = []

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

    while(pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_avancar_login.png', semelhanca=0.8, necessario=False, regiao=const.AREA_BOLSA) is None):
        info.printinfo(f"Aguardando a tela de notícias ser carregada para o personagem {personagem['nickname']}.")
        time.sleep(2)
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)

    if not myEvent.is_set():
            return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_AVANCAR_LOGIN)
    pgs.clicar(1)

    caminho = f'{const.PATH_IMGS_ANCORAS_PERSON}ancora_nickname_{personagem["nickname"].lower()}.png'
    alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=False, regiao=const.AREA_NICKNAME)
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
    if not myEvent.is_set():
            return
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_JOGAR)
    pgs.clicar(1)
    verificar_pausa(myEventPausa)
    pg.sleep(5)

## 2. Fechar popup
def fechar_popup(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.sleep(2)
    caminho_popup_nao = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_login_presente_nao.png'
    caminho_popup_sim = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_login_presente_sim.png'
    alvo_nao = pgs.encontrar_alvo(caminho_popup_nao, semelhanca=0.8, necessario=False, regiao=const.AREA_TELA_WARSPEAR)
    alvo_sim = pgs.encontrar_alvo(caminho_popup_sim, semelhanca=0.8, necessario=False, regiao=const.AREA_TELA_WARSPEAR)
    if alvo_nao is not None and alvo_sim is not None:
        info.printinfo("Popup de login presente infelizmente apareceu.", erro=True)
        pg.sleep(8)
        pg.press('f1')
        pg.sleep(0.5)
        pg.press('f1')
        pg.sleep(0.5)
        pg.press('f1')
        pg.sleep(0.5)
        pg.press('f1')
        pg.sleep(0.5)
        pg.press('f1')
        pg.sleep(0.5)

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
def iniciar_todos_slots(personagem, craft, myEvent, myEventPausa):
    contador = 0
    if not myEvent.is_set():
        return [None, None]
    verificar_pausa(myEventPausa)
    # info.printinfo(f'Iniciando slots para {personagem["nickname"]} com {craft["item"]}')
    # info.printinfo(craft['craft'] in personagem['crafts'])
    # print(f'personagem["crafts"]: {personagem["crafts"]}')
    # print(f'craft["craft"]: {craft["craft"]}')

    if craft['craft'] in personagem['crafts']:
        info.printinfo(f'Iniciando task para {personagem["nickname"]} com o craft {craft["item"]}')
        pg.sleep(1)
        verifica_aba = pgs.encontrar_alvo(f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_pedidos_ativos.png', semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
        pg.sleep(0.4)
        if verifica_aba is None:
            pg.press("right")
            info.printinfo("Não estava na aba de pedidos ativos.\n\tAlternando aba", erro=True)

        contador = verificar_concluidos(personagem, craft, myEvent, myEventPausa)
        contador_iniciados = 0
        caminho_slot = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_slot.png'
        caminho_craft_cadeado = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_cadeado.png'

        for _ in range(personagem['slots']):
            for i in range(3):
                time.sleep(0.5)
                pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
                alvo_slot = pgs.encontrar_alvo(caminho_slot, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
                
                if alvo_slot is not None:
                    pgs.mover_para(alvo_slot)
                    pgs.clicar(2)
                    time.sleep(0.5)
                    verificar_pausa(myEventPausa)
                    resultado = iniciar_craft(personagem, craft, myEvent, myEventPausa)

                    if resultado is True:
                        info.printinfo("Um craft foi iniciado.")
                        contador_iniciados+=1
                    elif resultado is False:
                        info.printinfo("Faltou recurso para iniciar o craft.", erro=True)
                        return [craft['duração_dia_hora_minuto'], (personagem['slots']*-3)] ## multiplicado por -3 para que o contador seja negativo
                        ## o contador negativo significa que ele vai tentar desmontar os itens para conseguir recursos
                    else:
                        info.printinfo("Não foi possível iniciar o craft.", erro=True)

                    verificar_pausa(myEventPausa)
                    time.sleep(0.5)
                    break
                else:
                    alvo_cadeado = pgs.encontrar_alvo(caminho_craft_cadeado, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
                    if alvo_cadeado is not None:
                        info.printinfo("Encontrou slot bloqueado, todos estão ocupados.", erro=True)
                        return [craft['duração_dia_hora_minuto'], contador]
                    # for _ in range(4):
                    for _ in range(8 if i == 1 else 4):
                        if not myEvent.is_set():
                                return [None, None]
                        verificar_pausa(myEventPausa)
                        if(i != 0):
                            pg.sleep(0.3)
                            pg.press("down")
                pg.sleep(1)
            
    verificar_pausa(myEventPausa)
    if contador_iniciados == 0 and contador == 0:
        info.printinfo("Não foi possível iniciar nem coletar nenhum craft.\n\tO tempo de espera será diminuido.", erro=True)
        return [[0, 0, 20], 0]
    return [craft['duração_dia_hora_minuto'], contador]
                      
## 4.1 verificar conluidos (passo intermédiario)
def verificar_concluidos(personagem, craft, myEvent, myEventPausa):
    contador=0
    primeira_vez = True
    caminho = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_concluido.png'
    for _ in range(personagem['slots']):
        if not myEvent.is_set():
            return
        alvo = pgs.encontrar_alvo(caminho, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
        pg.sleep(0.3) 
        if alvo is not None:
            if not myEvent.is_set():
                return
            verificar_pausa(myEventPausa)
            if primeira_vez:
                pgs.mover_para(alvo)
                pgs.clicar(1)
                primeira_vez = False
            pg.sleep(0.3)  
            pg.press('f2')
            contador+=1
            pg.sleep(0.3)
            info.printinfo("Coletou um craft concluído.")
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pgs.clicar(1)
    verificar_pausa(myEventPausa)
    return contador

## 4.2 iniciar craft (passo intermédiario)
def iniciar_craft(personagem, craft, myEvent, myEventPausa):
    caminho_craft_alvo = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_{craft['craft']}.png'
    caminho_craft_iniciar_alvo = f'{const.PATH_IMGS_ANCORAS_CRAFT}ancora_craft_iniciar.png'
    caminho_popup_faltou_recurso = f'{const.PATH_IMGS_ANCORAS_POPUP}ancora_popup_faltou_recurso.png'
    for i in range(3):
        pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
        # if i == 0:
        #     pgs.clicar(1) ## por enquanto não precisa, parece estar correto abrir a profissão já selecionada
        if not myEvent.is_set():
            return
        verificar_pausa(myEventPausa)
        time.sleep(1.5)
        alvo_craft = pgs.encontrar_alvo(caminho_craft_alvo, semelhanca=0.8, necessario=True, regiao=const.AREA_CRAFT)
        time.sleep(1)
        if alvo_craft is not None:
            info.printinfo("Encontrou a categoria do craft.")
            pgs.mover_para(alvo_craft)
            pgs.clicar(1)
            pg.sleep(0.5)
            alvo_iniciar = pgs.encontrar_alvo(caminho_craft_iniciar_alvo, semelhanca=0.8, necessario=False, regiao=const.AREA_BOTAO_CRAFT_INICIAR)
            pg.sleep(0.3)
            if alvo_iniciar is None:
                info.printinfo("Não entrou na categoria, clicando mais uma vez.")
                pg.sleep(0.3)
                pgs.clicar(1)
                pg.sleep(0.3)
            pg.sleep(0.3)
            # slots_especiais = craft_categorias[craft['craft']]['slots_especiais']
            # info.printinfo(slots_especiais)  # imprimir o valor 2
            for _ in range(craft['posicao'] + (craft_categorias[craft['craft']]["slots_especiais"] - 1)):
                if not myEvent.is_set():
                    return
                verificar_pausa(myEventPausa)
                pg.press("down")
                pg.sleep(0.2)
            pg.press("f2")
            pg.sleep(0.3)
            alvo_popup_faltou_recurso = pgs.encontrar_alvo(caminho_popup_faltou_recurso, semelhanca=0.8, necessario=False, regiao=const.AREA_BOLSA)
            if alvo_popup_faltou_recurso is not None:
                # info.printinfo("Faltou recurso para iniciar o craft.", erro=True)
                pg.sleep(0.3)
                pg.press("enter")
                pg.sleep(0.3)
                pg.press("f1")
                pg.sleep(0.3)
                return False
            time.sleep(0.5)
            return True ## não acredito que eu estava esquecendo disso, passei horas procurando
        else:
            info.printinfo("Não encontrou a categoria do craft.\n\tApertando 'down' pra encontrar.", erro=True)
            # for j in range(4):
            for _ in range(8 if i == 1 else 4):
                if not myEvent.is_set():
                        return
                verificar_pausa(myEventPausa)
                # if(i != 0):
                pg.press("down")
                pg.sleep(0.15)
    verificar_pausa(myEventPausa)
    pgs.mover_para(const.POS_BOTAO_CRAFT_MENU)
    pgs.clicar(1)
    time.sleep(0.5)
    verificar_pausa(myEventPausa)
    return True
        
## 5. fechar menu craft
def fechar_menu_craft(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.press('f1')
    pg.sleep(0.3)
        
## 6. abrir menu bolsa
def abrir_menu_bolsa(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
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
    for _ in range(contador):
        desmontou = False
        for _ in range(3):
            pg.sleep(3)
            alvo = pgs.encontrar_alvo(f'{const.PATH_IMGS_ITENS}{item}.png', semelhanca=0.8, regiao=const.AREA_BOLSA, center=True, necessario=True)
            pg.sleep(0.35)
            if not myEvent.is_set():
                return contador_desmontados
            verificar_pausa(myEventPausa)
            if alvo is None:
                if myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                pgs.press('down', 12, 0.12, myEvent, myEventPausa)
                pg.sleep(0.35)
            else:
                if not myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                pgs.mover_para(alvo)
                pgs.clicar(1)
                pg.press('f2')
                pg.sleep(0.15)
                pg.press('8')
                pg.sleep(0.15)
                if not myEvent.is_set():
                    return contador_desmontados
                verificar_pausa(myEventPausa)
                pg.press('f2')
                pgs.mover_para(const.POS_BOTAO_BOLSA_MENU)
                info.printinfo("Um item está sendo desmontado.")
                pg.sleep(8) ## implementar a espera dinamica para desmontar
                verificar_pausa(myEventPausa)
                pgs.clicar(1)
                pg.sleep(0.3)
                pgs.clicar(1)
                pg.sleep(0.3)
                contador_desmontados+=1
                desmontou = True
                break
        if (desmontou == False):
            info.printinfo("Todos itens foram/estão desmontados.")
            break
    return contador_desmontados


## 8. fechar menu bolsa
def fechar_menu_bolsa(myEvent, myEventPausa):
    if not myEvent.is_set(): return
    verificar_pausa(myEventPausa)
    pg.press('f1')
    pg.sleep(0.3)

## 9. deslogar
def deslogar(myEvent, myEventPausa):
    if not myEvent.is_set():
        return
    verificar_pausa(myEventPausa)
    pg.press('f2')
    pg.sleep(0.3)
    pg.press('9')
    pg.sleep(0.2)
    pg.press('6')
    pg.sleep(0.2)
    pg.press('f2')

## 0. pausando (passo opcional)
def verificar_pausa(myEventPausa):
    while myEventPausa.is_set(): pass