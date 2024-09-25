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
                time.sleep(2)
                info.salvar_log()

            if key.char == "k":
                info.printinfo("Task iniciada.")
                if not myEvent.is_set():
                    myEvent.set()
                # th = threading.Thread(target=init.iniciar, args=(myEvent,))
                th = threading.Thread(target=lambda: init.iniciar(myEvent, myEventPausa))
                th.start()
        
            if key.char == "l":
                if myEventPausa.is_set():
                    myEventPausa.clear()
                    info.printinfo("Task despausada")
                else:
                    myEventPausa.set()
                    info.printinfo("Task pausada")
            
            # if key.char == "t":s
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
                    pgs.capturar_e_salvar_area(x_inicial, y_inicial, largura, altura, "print_gerado_da_area.png")
                else:
                    print("Não há pontos suficientes para calcular a área.")
    except AttributeError:
        pass



def sleep_with_check(duration):
    interval = 1 #Intervalo de verificação em segundos
    for _ in range(int(duration / interval)):
        if not myEvent.is_set():
            break
        time.sleep(interval)

def salvar_log_loop():
    while True:
        time.sleep(600)
        info.salvar_log(resetar=False)

global myEvent
myEvent = threading.Event()
myEvent.clear()

global myEventAtalho
myEventAtalho = threading.Event()
myEventAtalho.set()
info.printinfo("Os atalhos estão ativados:\n\tK\t => inicia a task\n\tL\t => pausa a task\n\tEsc\t => encerra a task\n\tAlt Gr\t => ativa/desativa os atalhos")

global myEventPausa
myEventPausa = threading.Event()
myEventPausa.clear()

tb.iniciar_bot(myEvent, myEventPausa)
# th = threading.Thread(target=lambda: init.iniciar(myEvent, myEventPausa))
# th.start()
# myEvent.set()

th_log = threading.Thread(target=salvar_log_loop)
th_log.start()

th_l = threading.Thread(target=listener)
th_l.start()
th_l.join()
