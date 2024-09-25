import requests
import threading
from dotenv import load_dotenv
import os
import time
import info
import init


TOKEN = ''
CHAT_IDS = ''
AUTHORIZED_CHAT_IDS = ''

def verificar_variaveis_ambiente(printinfo_callback=print):
    global TOKEN, CHAT_IDS, AUTHORIZED_CHAT_IDS
    load_dotenv(dotenv_path='telegram.env')

    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_IDS = os.getenv("CHAT_IDS")
    AUTHORIZED_CHAT_IDS = os.getenv("AUTHORIZED_CHAT_IDS").split(",")
    if not TOKEN:
        if printinfo_callback:
            printinfo_callback("Aviso: TELEGRAM_TOKEN não está definido no arquivo .env", erro=True)

    if CHAT_IDS:
        CHAT_IDS = CHAT_IDS.split(",")
    else:
        if printinfo_callback:
            printinfo_callback("Aviso: CHAT_IDS não está definido no arquivo .env", erro=True)

    if not AUTHORIZED_CHAT_IDS:
        printinfo_callback("Aviso: AUTHORIZED_CHAT_IDS não está definido no arquivo .env", erro=True)
session = requests.Session()

def send_telegram_message(message, printinfo_callback=print):
    global TOKEN, CHAT_IDS
    if not TOKEN or not CHAT_IDS:
        if printinfo_callback:
            printinfo_callback("Aviso: Não é possível enviar mensagem, TOKEN ou CHAT_IDS não definidos.", erro=True)
        return
    # Inicia uma thread para cada chat_id
    for chat_id in CHAT_IDS:
        thread = threading.Thread(target=send_message, args=(chat_id, message, printinfo_callback))
        thread.start()

def send_message(chat_id, message, printinfo_callback=print):
        urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        try:
            response = session.get(urlmsg, timeout=60)  # Adiciona timeout de 60 segundos
            response.raise_for_status()  # Levanta exceção para códigos de status HTTP de erro
        except requests.exceptions.RequestException as e:
            if printinfo_callback:
                printinfo_callback(f"Erro na request para chat_id {chat_id}.", True)
            return None
        # if printinfo_callback:
            # printinfo_callback(f"Mensagem enviada para chat_id {chat_id}.")
        return response.json()

# verificar_variaveis_ambiente()

# URL TO GET CHAT_ID:
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# # ULR TO ACTUALLY SEND TELEGRAM MESSAGE:
# message = "Hello, World!"
# urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_IDS[0]}&text={message}"

# print(requests.get(url).json())

# r = requests.get(urlmsg)
# print(r.json())

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        response = session.get(url, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter atualizações.")
        return None

def process_updates(updates, myEvent, myEventPausa):
    for update in updates["result"]:
        message = update.get("message")
        if message:
            text = message.get("text")
            chat_id = message["chat"]["id"]
            if str(chat_id) in AUTHORIZED_CHAT_IDS:  # Verificar se o chat_id está autorizado
                process_command(text, chat_id, myEvent, myEventPausa)

            else:
                if text == "/start":
                    send_message(chat_id, "Bem vindo ao WS-AutoCraft, verifique o menu para enviar comandos.", info.printinfo)
                    info.printinfo(f"Novo /start no bot com chat_id: {chat_id}", False, True)
                else:
                    send_message(chat_id, "Você não está autorizado a usar este comando.")

def process_command(text, chat_id, myEvent, myEventPausa):
    ## nesse ponto já se pressupoe que o chat_id é autorizado
    if text == "/start":
        send_message(chat_id, "Bem vindo ao WS-AutoCraft, verifique o menu para enviar comandos.", info.printinfo)
        info.printinfo(f"Novo /start no bot com chat_id: {chat_id}", False, True)
    elif text == "/starttask":
        info.printinfo("Bot de craft foi iniciado remotamente.", False, True)
        send_telegram_message("Task de craft iniciado.", info.printinfo)
        if not myEvent.is_set():
            myEvent.set()
        th = threading.Thread(target=lambda: init.iniciar(myEvent, myEventPausa))
        th.start()
    elif text == "/stoptask":
        info.printinfo("Bot de craft foi encerrado remotamente.", False, True)
        send_telegram_message("Task de craft encerrado.", info.printinfo)
        myEvent.clear()
        time.sleep(2)
        info.salvar_log(resetar=False)

    elif text == "/pause":
        myEventPausa.set()
        info.printinfo("Bot foi pausado remotamente.", False, True)
        send_telegram_message("Task pausado.", info.printinfo)
    elif text == "/resume":
        myEventPausa.clear()
        info.printinfo("Bot foi despausado remotamente remotamente.", False, True)
        send_telegram_message("Task despausado.", info.printinfo)

def listen_for_commands(myEvent, myEventPausa):
    offset = None
    info.printinfo("Bot telegram iniciado.")
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            process_updates(updates, myEvent, myEventPausa)
            if updates["result"]:
                offset = updates["result"][-1]["update_id"] + 1
        time.sleep(1)


def iniciar_bot(myEvent, myEventPausa):
    verificar_variaveis_ambiente(print)
    threading.Thread(target=listen_for_commands, args=(myEvent, myEventPausa,)).start()

# Exemplo de uso
if __name__ == "__main__":
    from threading import Event
    myEvent = Event()
    myEventPausa = Event()
    iniciar_bot(myEvent, myEventPausa)