import pyautogui as pg
from pynput import keyboard
import threading
import time
from collections import namedtuple
import pg_simplificado as pgs
import init as init
import info as info
import constantes as const
import telegram_bot as tb



def listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

def calcular_posicao_e_dimensoes(ponto1, ponto2):
    x_inicial = min(ponto1.x, ponto2.x)
    y_inicial = min(ponto1.y, ponto2.y)
    largura = abs(ponto2.x - ponto1.x)
    altura = abs(ponto2.y - ponto1.y)
    return (x_inicial, y_inicial), largura, altura

Point = namedtuple('Point', ['x', 'y'])
pontos = []

def on_release(key):
    # try:
    #     vk_code = key.vk  # Obtém o VK code
    #     print(f'Tecla pressionada: {key.char}, VK code: {vk_code}')
    # except AttributeError:
    #     vk_code = key.value.vk if hasattr(key, 'value') else None
    #     print(f'Tecla especial pressionada: {key}, VK code: {vk_code}')
    try:
        if key == keyboard.Key.ctrl_r:
            if myEventAtalho.is_set():
                myEventAtalho.clear()
                info.printinfo("Atalhos desativados (Ctrl_r para ativar/desativar)", erro=True)
            else:
                myEventAtalho.set()
                info.printinfo("Atalhos ativados (Ctrl_r para ativar/desativar)")
        if myEventAtalho.is_set():
            
            if key == keyboard.Key.esc:
                info.printinfo("Task encerrada.")
                myEvent.clear()
                threading.Thread(target=lambda: deslogar_com_excecao(myEvent, myEventPausa)).start()
                time.sleep(2)
                info.salvar_log()

            if key.char == "k":
                th_login = threading.Thread(target=lambda: verificar_tela_login_com_excecao(myEvent, myEventPausa))
                th_login.start()
                th_login.join()
                info.printinfo("Task iniciada.")
                if not myEvent.is_set():
                    myEvent.set()
                
                th = threading.Thread(target=lambda: iniciar_com_excecao(myEvent, myEventPausa))
                th.start()

            if key.char == "l":
                if myEventPausa.is_set():
                    myEventPausa.clear()
                    info.printinfo("Task despausada", False, True)
                else:
                    myEventPausa.set()
                    info.printinfo("Task pausada", False, True)
            
            if key.char == "g":
                alvo = pgs.encontrar_alvo(f"{const.PATH_PRINT}", semelhanca=0.90, necessario=True, regiao=const.AREA_TELA_WARSPEAR, mover=True)
                pass
            if key.char == "d":
                pos = pg.position()
                pontos.append(Point(x=pos.x, y=pos.y))
                print(f"Registrado ponto: ({pos.x}, {pos.y})")

            if key.char == "f":
                if len(pontos) >= 2:
                    ponto1 = pontos[-2]
                    ponto2 = pontos[-1]
                    (x_inicial, y_inicial), largura, altura = calcular_posicao_e_dimensoes(ponto1, ponto2)
                    print(f"Area na tela: ({x_inicial}, {y_inicial}, {largura}, {altura})")
                    try:
                        pgs.capturar_e_salvar_area(x_inicial, y_inicial, largura, altura, "print_gerado_da_area.png")
                    except Exception as e:
                        print(f"Erro ao capturar e salvar a área: {e}")
                else:
                    print("Não há pontos suficientes para calcular a área.")
    except AttributeError:
        pass

def verificar_tela_login_com_excecao(myEvent, myEventPausa):
    try:
        if (init.verificar_tela_login(myEvent, myEventPausa) == False):
            info.printinfo("Não estava na tela de login, deslogando agora.")
            init.deslogar(myEvent, myEventPausa)
    except Exception as e:
        info.printinfo(f"Erro ao verificar tela de login: {e}", erro=True, enviar_msg=True)

def iniciar_com_excecao(myEvent, myEventPausa):
    try:
        init.iniciar(myEvent, myEventPausa)
    except Exception as e:
        info.printinfo(f"Erro ao iniciar a task: {e}", erro=True, enviar_msg=True)

def deslogar_com_excecao(myEvent, myEventPausa):
    try:
        init.resetar_fila()
        init.deslogar(myEvent, myEventPausa)
    except Exception as e:
        info.printinfo(f"Erro ao deslogar a task: {e}", erro=True, enviar_msg=True)

def iniciar_telegram_bot(myEvent, myEventPausa):
    try:
        tb.iniciar_bot(myEvent, myEventPausa)
    except Exception as e:
        info.printinfo(f"Erro ao iniciar o bot do telegram: {e}", erro=True, enviar_msg=True)

def sleep_with_check(duration):
    interval = 1 #Intervalo de verificação em segundos
    for _ in range(int(duration / interval)):
        if not myEvent.is_set():
            break
        time.sleep(interval)

def salvar_log_loop():
    while True:
        time.sleep(3600)
        info.salvar_log(resetar=True)

global myEvent
myEvent = threading.Event()
myEvent.clear()

global myEventAtalho
myEventAtalho = threading.Event()
myEventAtalho.set()
info.printinfo("Os atalhos estão ativados:\n\tK\t => inicia a task\n\tL\t => pausa a task\n\tEsc\t => encerra a task\n\tCtrl_r\t => ativa/desativa os atalhos")

global myEventPausa
myEventPausa = threading.Event()
myEventPausa.clear()

th_tb = threading.Thread(target=lambda: iniciar_telegram_bot(myEvent, myEventPausa))
th_tb.start()

th_log = threading.Thread(target=salvar_log_loop)
th_log.start()

th_l = threading.Thread(target=listener)
th_l.start()
th_l.join()
