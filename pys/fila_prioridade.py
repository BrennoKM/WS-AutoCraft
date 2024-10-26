import time
import tempo
import info
import sys

class Fila_prioridade:
    def __init__(self):
        self.queue = []
        self.next_id = 0       
        self.last_priority = None
        self.priority_droped = False
        self.nicknames = []
        self.novos_nicks = []
        self.novos_itens = []
        self.novas_tasks = False

    def init(self, nicknames, tempo_restante, itens, slots_disponiveis, reinserir_na_fila, gastar_coin):
        for i, nickname in enumerate(nicknames):
            self.nicknames.append(nickname)
            # info.printinfo(f"Adicionando {personagem['nickname']} na fila de prioridade.")
            tempo_espera = time.time() + tempo.converter_para_segundos(tempo_restante[i])
            time.sleep(0.1)
            try:
                self.enqueue(nickname, tempo_espera+2, itens[i], slots_disponiveis[i], reinserir_na_fila[i], gastar_coin[i])
            except IndexError:
                info.printinfo("Falha ao iniciar a fila. A quantidade de \"nicknames\" e \"itens\" devem ser iguais.", True, True)
                sys.exit()

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, nickname, tempo_espera, item, slots_disponiveis, reinserir_na_fila, gastar_coin, requisisao_bot = False):
        self.queue.append([nickname, tempo_espera, item, slots_disponiveis, reinserir_na_fila, gastar_coin, self.next_id])
        self.queue.sort(key=lambda x: x[1])
        if requisisao_bot:
            self.novas_tasks = True
            self.novos_nicks.append(nickname)
            self.novos_itens.append(item)
        self.next_id += 1


    def dequeue(self):
        if self.is_empty():
            return None
        self.last_priority = self.queue[0]
        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def size(self):
        return len(self.queue)
    
    def reset(self):
        self.queue = []
        self.last_priority = None

    def has_novas_tasks(self):
        return self.novas_tasks
    
    def get_novas_tasks(self):
        retorno_nicks = self.novos_nicks
        retorno_itens = self.novos_itens
        self.novas_tasks = False
        self.novos_nicks = []
        self.novos_itens = []
        return retorno_nicks, retorno_itens
    
    def drop(self, id):
        for i, t in enumerate(self.queue):
            if t[6] == id:
                task = self.queue.pop(i)
                info.printinfo(f"Task com id \"{id}\" foi removida da fila: {task}.", False, True)
                return True
        if self.last_priority != None and id == self.last_priority[6]:
            ##info.printinfo(f"Não é possível remover a task com id \"{id}\" pois ela é a prioridade.", True, True)
            ##return False
            info.printinfo(f"Task de prioridade com id \"{id}\" foi removida da fila: {self.last_priority}.", False, True)
            self.priority_droped = True
            self.last_priority = None
            return True
        info.printinfo(f"Task com id \"{id}\" não encontrada na fila.", True, True)
        return False

    def is_priority_droped(self):
        return self.priority_droped
    
    def reset_priority_droped(self):
        self.priority_droped = False

    def print_queue(self, fila_detalhada = False):
        
        lista = []
        if self.last_priority != None:# and fila_detalhada == True:
            personagem = self.last_priority[0]
            tempo = self.last_priority[1]
            item = self.last_priority[2]
            slots_disponiveis = self.last_priority[3]
            reinserir_na_fila = self.last_priority[4]
            gastar_coin = self.last_priority[5]
            id = self.last_priority[6]
            tempo_restante = tempo - time.time()
            #lista.append(f"\n\t\tPersonagem: {personagem},\tTempo restante: {tempo_restante:.2f} segundos.\tItem: {item},\tSlots disponíveis: {slots_disponiveis},\tReinserir na fila: {reinserir_na_fila},\tID na fila: {id}\n")
            if fila_detalhada == True:
                lista.append(f"\n\t\tPersonagem: {personagem},\n\t\t\tTempo restante: {tempo_restante:.2f} segundos.\n\t\t\tItem: {item},\n\t\t\tSlots disponíveis: {slots_disponiveis},\n\t\t\tReinserir na fila: {reinserir_na_fila},\n\t\t\tGastar coin: {gastar_coin},\n\t\t\tID na fila: {id}\n")
            else:
                lista.append(f"\n\t\tPersonagem: {personagem},\n\t\t\tTempo restante: {tempo_restante:.2f} segundos.")
        if not self.is_empty():
            for t in self.queue:
                personagem = t[0]
                tempo = t[1]
                item = t[2]
                slots_disponiveis = t[3]
                reinserir_na_fila = t[4]
                gastar_coin = t[5]
                id = t[6]
                tempo_restante = tempo - time.time()
                if fila_detalhada == True:
                    lista.append(f"\n\t\tPersonagem: {personagem},\n\t\t\tTempo restante: {tempo_restante:.2f} segundos.\n\t\t\tItem: {item},\n\t\t\tSlots disponíveis: {slots_disponiveis},\n\t\t\tReinserir na fila: {reinserir_na_fila},\n\t\t\tGastar coin: {gastar_coin},\n\t\t\tID na fila: {id}\n")
                else:
                    lista.append(f"\n\t\tPersonagem: {personagem},\n\t\t\tTempo restante: {tempo_restante:.2f} segundos.")
        conteudo_fila = "Fila de prioridade:\n" + "".join(lista)
        if lista == []:
            conteudo_fila = "Fila de prioridade vazia."
        if fila_detalhada == True and conteudo_fila.endswith("\n"):
            conteudo_fila = conteudo_fila[:-1]
        info.printinfo(conteudo_fila, False, True)
        if self.last_priority != None: # and fila_detalhada == True:
            info.printinfo(f"O personagem com prioridade é: {self.last_priority[0]}.", False, True)
        time.sleep(2)
    
    