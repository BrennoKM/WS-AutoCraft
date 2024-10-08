import pyautogui as pg
import random
import info as info
import os
from PIL import Image

pg.useImageNotFoundException(False)
pg.FAILSAFE = False




def capturar_e_salvar_area(x_inicial, y_inicial, largura, altura, caminho_arquivo):
    # Capturar a área especificada
    screenshot = pg.screenshot(region=(x_inicial, y_inicial, largura, altura))
    
    # Salvar a imagem
    screenshot.save(caminho_arquivo)
    print(f"Screenshot salva em: {caminho_arquivo}")

def capturar_print(x_inicial, y_inicial, largura, altura):
    screenshot = pg.screenshot(region=(x_inicial, y_inicial, largura, altura))
    return screenshot
    
def mover_para(alvo=None, var_x=0, var_y=0):
    if(alvo is not None):
        x, y = alvo
        x = x + var_x + random.uniform(-5, 5)
        y = y + var_y + random.uniform(-5, 5)
        d = 0.3
        d = 0.3 + random.uniform(-0.2, 0.2)
        t=pg.easeOutQuad
        pg.moveTo(x, y, d, t)
        return True
    return None

def clicar(qnt):
    pg.sleep(0.1)
    pg.click(clicks=qnt, interval=0.12 + random.uniform(-0.01, 0.02))

def sleep(tempo):
    pg.sleep(tempo)

def encontrar_alvo(path, semelhanca=0.8, regiao=None, center: bool = True, necessario: bool = True, alvo_problema: bool = False, mover: bool = False, myEvent=None):
    if os.path.exists(path):
        try:
            slot = pg.locateOnScreen(path, confidence=semelhanca, region=regiao)
        except Exception as e:
            info.printinfo(f'Except no PyAutoGui ao tentar localizar {path} na tela: {e}', True, True)
            pg.sleep(3)
            return None
        if myEvent is not None and not myEvent.is_set():
            return
        if(slot != None):
            if(center == True):
                slot = pg.center(slot)
            if(mover == True):
                mover_para(slot)
            if necessario is True:  ## coloquei essa condição pro log não ficar tão poluído	
                info.printinfo(f'Alvo encontrado: {path}')
            if alvo_problema is True:
                info.printinfo(f'Alvo de problema encontrado: {path}', erro=True)
            return slot
        if necessario is True:
            info.printinfo(f'Alvo não encontrado: {path}', erro=True)
        
        return None
    info.printinfo(f'Arquivo não encontrado: {path}', erro=True)
    return None

def encontrar_alvos(path, semelhanca=0.8, regiao = None, center: bool = True, necessario: bool = True, alvo_problema: bool = False, myEvent=None):
    if myEvent is not None and not myEvent.is_set():
        return
    if os.path.exists(path):
        try:
            slots = pg.locateAllOnScreen(path, confidence=semelhanca, region=regiao)
        except Exception as e:
            info.printinfo(f'Except no PyAutoGui ao tentar localizar {path} na tela: {e}', True, True)
            pg.sleep(3)
            return None
        # info.printinfo(f'Alvos encontrados: {slots}')
        retorno = []
        if(slots != None):
            if(center == True):
                for slot in slots:
                    slot = pg.center(slot)
                    retorno.append(slot)
            if necessario is True:
                info.printinfo(f'Alvo encontrado: {path}')
            if alvo_problema is True:
                info.printinfo(f'Alvo encontrado: {path}', erro=True)
                    
            return retorno
        if necessario is True:
            info.printinfo(f'Alvo não encontrado: {path}', erro=True)
        return None
    info.printinfo(f'Arquivo não encontrado: {path}', erro=True)
    return None

def press(tecla, repeticoes=1, intervalo=0.1, myEvent=None, myEventPausa=None):
    for _ in range(repeticoes):
        if myEvent is not None and not myEvent.is_set():
            return
        if myEventPausa is not None:
            while myEventPausa.is_set(): pass
        pg.press(tecla)
        pg.sleep(intervalo + random.uniform(-0.01, 0.02))