import time
import tempo
import info
import sys

class Fila_prioridade:
    def __init__(self):
        self.queue = []
        self.nicknames = []
        self.novos_nicks = []
        self.novos_itens = []
        self.novas_tasks = False

    def init(self, nicknames, tempo_restante, itens, slots_disponiveis, reinserir_na_fila):
        for i, nickname in enumerate(nicknames):
            self.nicknames.append(nickname)
            # info.printinfo(f"Adicionando {personagem['nickname']} na fila de prioridade.")
            tempo_espera = time.time() + tempo.converter_para_segundos(tempo_restante[i])
            time.sleep(0.1)
            try:
                self.enqueue(nickname, tempo_espera+2, itens[i], slots_disponiveis[i], reinserir_na_fila[i])
            except IndexError:
                info.printinfo("Falha ao iniciar a fila. A quantidade de \"nicknames\" e \"itens\" devem ser iguais.", True, True)
                sys.exit()

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, nickname, tempo_espera, item, slots_disponiveis, reinserir_na_fila, requisisao_bot = False):
        self.queue.append([nickname, tempo_espera, item, slots_disponiveis, reinserir_na_fila])
        self.queue.sort(key=lambda x: x[1])
        if requisisao_bot:
            self.novas_tasks = True
            self.novos_nicks.append(nickname)
            self.novos_itens.append(item)


    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def size(self):
        return len(self.queue)
    
    def reset(self):
        self.queue = []

    def has_novas_tasks(self):
        return self.novas_tasks
    
    def get_novas_tasks(self):
        retorno_nicks = self.novos_nicks
        retorno_itens = self.novos_itens
        self.novas_tasks = False
        self.novos_nicks = []
        self.novos_itens = []
        return retorno_nicks, retorno_itens

    def print_queue(self, nicknames = None, fila_detalhada = False):
        nicknames = self.nicknames
        lista = []
        nicks = []
        for f in self.queue:
            personagem = f[0]
            tempo = f[1]
            item = f[2]
            slots_disponiveis = f[3]
            reinserir_na_fila = f[4]
            tempo_restante = tempo - time.time()
            if fila_detalhada == True:
                lista.append(f"\n\t\tPersonagem: {personagem},\tTempo restante: {tempo_restante:.2f} segundos.\tItem: {item},\tSlots disponíveis: {slots_disponiveis},\tReinserir na fila: {reinserir_na_fila}\n")
            else:
                lista.append(f"\n\t\tPersonagem: {personagem},\tTempo restante: {tempo_restante:.2f} segundos.")
            nicks.append(personagem)
        info.printinfo("Fila de prioridade:\n" + "".join(lista), False, True)
        #if nicks.__len__() < nicknames.__len__():
        #    for nick in nicknames:
        #        if nick not in nicks:
        #            info.printinfo(f"Personagem {nick} está sendo a prioridade.", False, True)
        #            break
        info.printinfo(f"O personagem com prioridade é: {self.queue[0][0]}.", False, True)
        time.sleep(2)
    
    