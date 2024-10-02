import requests
import threading
from dotenv import load_dotenv
import os
import time
import tempo
import info
import init
import entrada_saida as es
import constantes as const
import json
import threading
import pg_simplificado as pgs
import tempfile
from datetime import datetime


TOKEN = ''
CHAT_IDS = ''
AUTHORIZED_CHAT_IDS = ''

bot_start_time = 0

def verificar_variaveis_ambiente(printinfo_callback=print):
    global TOKEN, CHAT_IDS, AUTHORIZED_CHAT_IDS
    try:
        load_dotenv(dotenv_path=const.PATH_ENV)

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
    except Exception as e:
        if printinfo_callback:
            printinfo_callback(f"Erro ao verificar variáveis de ambiente no arquivo 'telegram.env'.", erro=True)


session = requests.Session()

def send_telegram_message(message, printinfo_callback=print):
    global TOKEN, CHAT_IDS
    if not TOKEN or not CHAT_IDS:
        # if printinfo_callback:
        #     printinfo_callback("Aviso: Não é possível enviar mensagem, TOKEN ou CHAT_IDS não definidos.", erro=True)
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
                printinfo_callback(f"Erro na request para chat_id {chat_id}.", True, True)
                # printinfo_callback(f"Erro na request para chat_id {chat_id}: {e}", True)
            return None
        # if printinfo_callback:
            # printinfo_callback(f"Mensagem enviada para chat_id {chat_id}.")
        return response.json()

def send_image(chat_id, image_path, printinfo_callback):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    legenda_hora_atual = datetime.now().strftime("%H:%M:%S")
    with open(image_path, 'rb') as image_file:
        files = {'photo': image_file}
        data = {'chat_id': chat_id, 'caption': f"Printscreen tirada às {legenda_hora_atual}"}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            printinfo_callback("Printscreen enviada com sucesso.")
        else:
            printinfo_callback(f"Falha ao enviar printscreen: {response.text}", True, True)
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
        # info.printinfo(f"Erro ao obter atualizações.")
        return None

def process_updates(updates, myEvent, myEventPausa):
    global bot_start_time
    for update in updates["result"]:
        message = update.get("message")
        if message:
            update_time = update["message"]["date"]
            if update_time < bot_start_time:
                info.printinfo(f"Ignorando comando que foi submetido antes do bot iniciar.", True)
                continue
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

def listen_for_commands(myEvent, myEventPausa):
    global bot_start_time
    offset = None
    if not TOKEN or not CHAT_IDS:
        info.printinfo("Aviso: Não foi possível iniciar o bot do telegram, TOKEN ou CHAT_IDS não definidos.", erro=True)
        return
    info.printinfo("Bot telegram iniciado.", False, True)
    bot_start_time = int(time.time())
    # info.printinfo(f"Bot iniciado em: {bot_start_time}")
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            process_updates(updates, myEvent, myEventPausa)
            if updates["result"]:
                offset = updates["result"][-1]["update_id"] + 1
        time.sleep(1)

def process_command(text, chat_id, myEvent, myEventPausa):
    ## nesse ponto já se pressupoe que o chat_id é autorizado
    if text == "/start":
        send_message(chat_id, "Bem vindo ao WS-AutoCraft, verifique o menu para enviar comandos.", info.printinfo)
        info.printinfo(f"Novo /start no bot com chat_id: {chat_id}", False, True)
    elif text == "/starttask":
        send_telegram_message("Task de craft iniciada.", info.printinfo)
        info.printinfo("Bot de craft foi iniciado remotamente.", False, True)
        if not myEvent.is_set():
            myEvent.set()
        th_login = threading.Thread(target=lambda: verificar_tela_login_com_excecao(myEvent, myEventPausa))
        th_login.start()
        th_login.join()
        th = threading.Thread(target=lambda: init.iniciar(myEvent, myEventPausa))
        th.start()
    elif text == "/stoptask":
        send_telegram_message("Task de craft encerrada.", info.printinfo)
        info.printinfo("Bot de craft foi encerrado remotamente.", False, True)
        myEvent.clear()
        # myEventPausa.clear()
        init.resetar_fila()
        threading.Thread(target=lambda: init.deslogar(myEvent, myEventPausa)).start()
        # init.deslogar(myEvent, myEventPausa)
        time.sleep(2)
        info.salvar_log(resetar=False)

    elif text == "/pause":
        send_telegram_message("Task pausada.", info.printinfo)
        info.printinfo("Bot foi pausado remotamente.", False, True)
        myEventPausa.set()
    elif text == "/resume":
        send_telegram_message("Task despausada.", info.printinfo)
        info.printinfo("Bot foi despausado remotamente.", False, True)
        myEventPausa.clear()

    elif text == "/printqueue":
        info.printinfo("Comando de printqueue foi acionado remotamente.")
        init.print_fila(fila_detalhada=True)
    
    elif text == "/printtask":
        info.printinfo("Comando de printtask foi acionado remotamente.")
        dados = es.carregar_json(f'{const.PATH_TASK}')
        formatted_dados = json.dumps(dados, separators=(',', ':'))
        formatted_dados = formatted_dados.replace('],"', '\n\t],\n"')\
                                            .replace(':[',':\n\t[\n\t\t')\
                                            .replace(',', ', ')\
                                            .replace('{','{\n')\
                                            .replace(']}','\n\t]\n}\n')\
                                            .replace(', \n',',\n')
        

        send_message(chat_id, formatted_dados, info.printinfo)

    elif text.startswith("/edittask"):

        info.printinfo("Comando de edittask foi acionado remotamente.")
        json_str = text[len("/edittask"):].strip()
        
        try:
            novos_dados = json.loads(json_str)
        except json.JSONDecodeError:
            exemplo_json = {
                "nicknames": ["nomePersonagem"],
                "tempo_restante": [[0, 0, 0]],
                "itens": ["nome_item"],
                "slots_disponiveis": [2],
                "reinserir_na_fila": [True],
                "gastar_coin": [False],
                "tempo_espera_inicial": [[0, 0, 0]]
            }
            formatted_dados = json.dumps(exemplo_json, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('],"', '\n\t],\n"')\
                                                .replace(':[',':\n\t[\n\t\t')\
                                                .replace(',', ', ')\
                                                .replace('{','{\n')\
                                                .replace(']}','\n\t]\n}\n')\
                                                .replace(', \n',',\n')
            send_message(
                chat_id,
                f"Formato de JSON inválido.\nUse: /edittask {formatted_dados}",
                info.printinfo
            )
            return
        
        dados = es.carregar_json(f'{const.PATH_TASK}')
        
        dados.update(novos_dados)
        
        with open(f'{const.PATH_TASK}', 'w') as f:
            formatted_dados = json.dumps(dados, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('],"', '\n\t],\n"')\
                                            .replace(':[',':\n\t[\n\t\t')\
                                            .replace(',', ', ')\
                                            .replace('{','{\n')\
                                            .replace(']}','\n\t]\n}\n')\
                                            .replace(', \n',',\n')
            f.write(formatted_dados)
        
        send_message(chat_id, "Tasks foram atualizadas.", info.printinfo)
        info.printinfo("Tasks foram atualizadas.")
    
    elif text.startswith("/addtask"):
        info.printinfo("Comando de addtask foi acionado remotamente.")
        json_str = text[len("/addtask"):].strip()

        try:
            nova_tarefa = json.loads(json_str)
        except json.JSONDecodeError:
            exemplo_json = {
                "nicknames": ["nomePersonagem"],
                "tempo_restante": [[0, 0, 0]],
                "itens": ["nome_item"],
                "slots_disponiveis": [2],
                "reinserir_na_fila": [True],
                "gastar_coin": [False],
            }
            formatted_dados = json.dumps(exemplo_json, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('],"', '\n\t],\n"')\
                                            .replace(':[',':\n\t[\n\t\t')\
                                            .replace(',', ', ')\
                                            .replace('{','{\n')\
                                            .replace(']}','\n\t]\n}\n')\
                                            .replace(', \n',',\n')
            send_message(
                chat_id,
                f"Formato de JSON inválido.\nUse: /addtask {formatted_dados}",
                info.printinfo
            )
            return

        try:
            for i in range(len(nova_tarefa["nicknames"])):
                nick = nova_tarefa["nicknames"][i]
                tempo_restante = nova_tarefa["tempo_restante"][i]
                tempo_espera = time.time() + tempo.converter_para_segundos(tempo_restante)
                time.sleep(0.1)
                item = nova_tarefa['itens'][i]
                slots_disponiveis = nova_tarefa["slots_disponiveis"][i]
                reinserir_na_fila = nova_tarefa["reinserir_na_fila"][i]
                gastar_coin = nova_tarefa["gastar_coin"][i]
                init.add_task(nick, tempo_espera+2, item, slots_disponiveis, reinserir_na_fila, gastar_coin, requisisao_bot=True)
        except IndexError as e:
            info.printinfo(f"Falha ao adicionar a nova task. A quantidade de atributos devem ser iguais.\nErro: {e}", True, True)
            return
        except KeyError as e:
            info.printinfo(f"Falha ao adicionar a nova task. O JSON deve conter os campos: nicknames, tempo_restante, itens, slots_disponiveis e reinserir_na_fila.\nErro: {e}", True, True)
            return

        send_message(chat_id, "Nova(s) task(s) adicionada(s).", info.printinfo)
        info.printinfo("Uma ou mais tasks foram adicionadas via bot do telegram.")
        time.sleep(2)
        init.print_fila()

    elif text.startswith("/droptask"):
        info.printinfo("Comando de droptask foi acionado remotamente.")
        try:
            ids = json.loads(text[len("/droptask "):])
            if isinstance(ids, list):
                for task_id in ids:
                    
                    # send_message(chat_id, f"Task {task_id} removida.", info.printinfo)
                    init.drop_task(task_id)
                    # else:
                    #     send_message(chat_id, f"Task {task_id} não encontrada.", info.printinfo)
            else:
                send_message(chat_id, "Formato inválido. Use /droptask [id1, id2, ...]", info.printinfo)
        except json.JSONDecodeError:
            send_message(chat_id, "Formato inválido. Use /droptask [id1, id2, ...]", info.printinfo)

    elif text == "/printcraftname":
        info.printinfo("Comando de printcraftnames foi acionado remotamente.")
        dados = es.carregar_json(f'{const.PATH_CONSTS}crafts.json')

        # dados = [{"item": entry["item"]} for entry in dados]
        dados = [entry["item"] for entry in dados]

        formatted_dados = json.dumps(dados, separators=(',', ':'), indent=4)
        # formatted_dados = formatted_dados.replace('[{','[\n\t{\n\t\t')\
        #                                 .replace('}]','\n\t}\n]')\
        #                                 .replace('},{','\n\t},\n\t{\n\t\t')\
        #                                 .replace(',\"',',\n\t\t\"')\
        #                                 .replace(',',', ')\
        #                                 .replace(':',': ')\
        #                                 .replace(', \n',',\n')

                                        
        
        send_message(chat_id, formatted_dados, info.printinfo)

    elif text.startswith("/printcraft"):
        info.printinfo("Comando de printcrafts foi acionado remotamente.")
        
        json_str = text[len("/printcraft"):].strip()
        
        try:
            items_to_filter = json.loads(json_str)
        except json.JSONDecodeError:
            exemplo_json = [
                    "material_bracelete_1_2",
                    "material_bracelete_1_3"
                ]
            
            formatted_dados = json.dumps(exemplo_json, separators=(',', ':'), indent=4)
            
            send_message(
                chat_id,
                f"Formato de JSON inválido.\nUse: /printcraft {formatted_dados}",
                info.printinfo
            )
            return
        
        dados = es.carregar_json(f'{const.PATH_CONSTS}crafts.json')

        filtered_dados = [entry for entry in dados if entry["item"] in items_to_filter]

        formatted_dados = json.dumps(filtered_dados, separators=(',', ':'))
        formatted_dados = formatted_dados.replace('[{','[\n\t{\n\t\t')\
                                        .replace('}]','\n\t}\n]')\
                                        .replace('},{','\n\t},\n\t{\n\t\t')\
                                        .replace(',\"',',\n\t\t\"')\
                                        .replace(',',', ')\
                                        .replace(':',': ')\
                                        .replace(', \n',',\n')

        send_message(chat_id, formatted_dados, info.printinfo)


    elif text.startswith("/editcraft") or text.startswith("/addcraft"):
        if text.startswith("/addcraft"):
            info.printinfo("Comando de addcraft foi acionado remotamente.")
            json_str = text[len("/addcraft"):].strip()
        else:
            info.printinfo("Comando de editcrafts foi acionado remotamente.")
            json_str = text[len("/editcraft"):].strip()
            
        
        try:
            novos_dados = json.loads(json_str)
        except json.JSONDecodeError:
            exemplo_json = [
                    {
                        "item": "material_bracelete_1_2",
                        "craft": "bracelete",
                        "especial": False,
                        "melhoria": False,
                        "precisa_desmontar": False,
                        "posicao": 2,
                        "licenca": 1,
                        "duracao_dia_hora_minuto": [0, 0, 15] 
                    }
                ]
            
            formatted_dados = json.dumps(exemplo_json, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('[{','[\n\t{\n\t\t')\
                                        .replace('}]','\n\t}\n]')\
                                        .replace('},{','\n\t},\n\t{\n\t\t')\
                                        .replace(',\"',',\n\t\t\"')\
                                        .replace(',',', ')\
                                        .replace(':',': ')\
                                        .replace(', \n',',\n')
            
            if text.startswith("/addcraft"):
                msg_saida = f"Formato de JSON inválido.\nUse: /addcraft {formatted_dados}"
            else:
                msg_saida = f"Formato de JSON inválido.\nUse: /editcraft {formatted_dados}",
            send_message(
                chat_id,
                msg_saida,
                info.printinfo
            )
            return
        
        dados = es.carregar_json(f'{const.PATH_CONSTS}crafts.json')
        
        for novo_item in novos_dados:
            item_encontrado = False
            for i, item_existente in enumerate(dados):
                if item_existente["item"] == novo_item["item"]:
                    dados[i] = novo_item
                    item_encontrado = True
                    break
            if not item_encontrado:
                dados.append(novo_item)
        
        with open(f'{const.PATH_CONSTS}crafts.json', 'w') as f:
            formatted_dados = json.dumps(dados, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('[{','[\n\t{\n\t\t')\
                                        .replace('}]','\n\t}\n]')\
                                        .replace('},{','\n\t},\n\t{\n\t\t')\
                                        .replace(',\"',',\n\t\t\"')\
                                        .replace(',',', ')\
                                        .replace(':',': ')\
                                        .replace(', \n',',\n')
            
            f.write(formatted_dados)
        
        if text.startswith("/addcraft"):
            send_message(chat_id, "Craft(s) adicionado(s).", info.printinfo)
            info.printinfo("Craft(s) adicionado(s).")
        else:
            send_message(chat_id, "Crafts foram atualizados.", info.printinfo)
            info.printinfo("Crafts foram atualizados.")
    
    elif text.startswith("/dropcraft"):
        info.printinfo("Comando de dropcraft foi acionado remotamente.")
        json_str = text[len("/dropcraft"):].strip()
        try:
            items_to_remove = json.loads(json_str)
        except json.JSONDecodeError:
            exemplo_json = [
                    "material_bracelete_1_2",
                    "material_bracelete_1_3"
                ]
            
            formatted_dados = json.dumps(exemplo_json, separators=(',', ':'), indent=4)
            
            send_message(
                chat_id,
                f"Formato de JSON inválido.\nUse: /dropcraft {formatted_dados}",
                info.printinfo
            )
            return
        
        dados = es.carregar_json(f'{const.PATH_CONSTS}crafts.json')
        dados = [item for item in dados if item["item"] not in items_to_remove]

        with open(f'{const.PATH_CONSTS}crafts.json', 'w') as f:
            formatted_dados = json.dumps(dados, separators=(',', ':'))
            formatted_dados = formatted_dados.replace('[{','[\n\t{\n\t\t')\
                                        .replace('}]','\n\t}\n]')\
                                        .replace('},{','\n\t},\n\t{\n\t\t')\
                                        .replace(',\"',',\n\t\t\"')\
                                        .replace(',',', ')\
                                        .replace(':',': ')\
                                        .replace(', \n',',\n')
            
            f.write(formatted_dados)

        send_message(chat_id, "Craft(s) removido(s).", info.printinfo)
        info.printinfo("Craft(s) removido(s).")

    elif text == "/printscreen":
        info.printinfo("Comando de printscreen foi acionado remotamente.")
        screenshot = pgs.capturar_print(*const.AREA_TELA_WARSPEAR)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            screenshot_path = tmp_file.name
            screenshot.save(screenshot_path)
        send_image(chat_id, screenshot_path, info.printinfo)
        os.remove(screenshot_path)

def verificar_tela_login_com_excecao(myEvent, myEventPausa):
    try:
        if (init.verificar_tela_login(myEvent, myEventPausa) == False):
            info.printinfo("Não estava na tela de login, deslogando agora.")
            init.deslogar(myEvent, myEventPausa)
    except Exception as e:
        info.printinfo(f"Erro ao verificar tela de login: {e}", erro=True, enviar_msg=True)
        
def iniciar_bot(myEvent, myEventPausa):
    verificar_variaveis_ambiente(info.printinfo)
    threading.Thread(target=listen_for_commands, args=(myEvent, myEventPausa,)).start()

# Exemplo de uso
if __name__ == "__main__":
    from threading import Event
    myEvent = Event()
    myEventPausa = Event()
    iniciar_bot(myEvent, myEventPausa)