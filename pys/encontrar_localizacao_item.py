import pyautogui as pg


## Encontrar a posicao de um item no menu de craft, serve apenas para facilitar a contagem

posicao = 19

slots_especiais = 3

pg.sleep(2)

for _ in range(posicao + slots_especiais - 1):
    pg.press("down")
    pg.sleep(0.15)
