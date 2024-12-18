import requests
import time

# Configuración de UltraMsg
INSTANCE_ID = "instance101509"  # Instance ID de UltraMsg
TOKEN = "bywdbhoco4mliq9v"      # Token de UltraMsg
CHAT_ID = "50688482272@c.us"    # ID del chat del destinatario (número + "@c.us")
NUMERO_DESTINATARIO = "50688482272"  # Número del destinatario
NUMERO_NOTIFICACION = "50684657373"  # Número para enviar la notificación
MENSAJE_INICIAL = "Hola."

# URLS
URL_ENVIO = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
URL_CONSULTA = f"https://api.ultramsg.com/{INSTANCE_ID}/chats/messages"

def enviar_mensaje(chat_id, mensaje):
    """Envía un mensaje al destinatario."""
    payload = f"token={TOKEN}&to={chat_id}&body={mensaje}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(URL_ENVIO, data=payload, headers=headers)

    if response.status_code == 200:
        print(f"Mensaje enviado correctamente al chat {chat_id}.")
        mensaje_data = response.json()
        return mensaje_data.get("timestamp", time.time())  # Marca de tiempo del mensaje enviado
    else:
        print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")
        return None

def verificar_respuesta(chat_id, timestamp_envio):
    """Consulta los mensajes de un chat específico para buscar respuestas posteriores."""
    querystring = {
        "token": TOKEN,
        "chatId": chat_id,
        "limit": 50
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.get(URL_CONSULTA, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Error al consultar mensajes: {response.status_code} - {response.text}")
        return None

    try:
        mensajes = response.json()
        for mensaje in mensajes:
            # Filtrar mensajes que sean respuestas posteriores al envío
            if not mensaje["fromMe"] and mensaje["timestamp"] > timestamp_envio:
                return mensaje["body"]  # Contenido del mensaje recibido
    except ValueError:
        print("La respuesta del servidor no es un JSON válido.")
    except KeyError:
        print("La respuesta del servidor no contiene las claves esperadas.")
    return None

def notificar_respuesta(chat_id, respuesta):
    """Envía una notificación con la respuesta recibida."""
    mensaje_notificacion = f"El destinatario {NUMERO_DESTINATARIO} respondió: '{respuesta}'"
    payload = f"token={TOKEN}&to={chat_id}&body={mensaje_notificacion}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(URL_ENVIO, data=payload, headers=headers)

    if response.status_code == 200:
        print(f"Notificación enviada al chat {chat_id}.")
        return True
    else:
        print(f"Error al enviar la notificación: {response.status_code} - {response.text}")
        return False

# Paso 1: Enviar mensaje inicial
timestamp_envio = enviar_mensaje(CHAT_ID, MENSAJE_INICIAL)
if timestamp_envio:
    print(f"Esperando respuesta del chat {CHAT_ID}...")

    # Paso 2: Esperar respuesta del destinatario
    respuesta = None
    timeout = 120  # Tiempo máximo de espera (en segundos)
    intervalo = 15  # Intervalo entre consultas (en segundos)

    for _ in range(timeout // intervalo):
        respuesta = verificar_respuesta(CHAT_ID, timestamp_envio)
        if respuesta:
            print(f"El destinatario respondió: {respuesta}")
            break
        time.sleep(intervalo)

    # Paso 3: Notificar respuesta
    if respuesta:
        if notificar_respuesta(NUMERO_NOTIFICACION, respuesta):
            print(f"Notificación enviada al número {NUMERO_NOTIFICACION}.")
        else:
            print(f"No se pudo enviar la notificación al número {NUMERO_NOTIFICACION}.")
    else:
        print(f"No se recibió respuesta del chat {CHAT_ID}.")
else:
    print("No se pudo enviar el mensaje inicial.")