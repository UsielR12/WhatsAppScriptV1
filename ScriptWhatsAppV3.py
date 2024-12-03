import requests
import time

# URL para enviar mensajes
send_url = "https://api.whatmsg.com/msg"

# URL para consultar mensajes entrantes (ajusta si es diferente en WhatMsg)
check_url = "https://api.whatmsg.com/inbox"

# Claves de configuración
api_key = "dkKHw4XQRefJBcSenwzZzJnpmOpnuWac"
from_number = "50664425845"  # Número del remitente
to_number = "50684181246"    # Número del destinatario

# Mensajes
mensaje_inicial = "Hola hola, esto es una prueba"
mensaje_notificacion = "El destinatario ha respondido con: {respuesta}"

def enviar_mensaje(from_number, to_number, mensaje):
    """Envía un mensaje al destinatario."""
    payload = f"apikey={api_key}&from={from_number}&to={to_number}&msgbody={mensaje}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(send_url, data=payload, headers=headers)

    if response.status_code == 200:
        print(f"Mensaje enviado correctamente al número {to_number}.")
        return True
    else:
        print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")
        return False

def verificar_respuesta(to_number):
    """Consulta las respuestas para verificar si el destinatario ha respondido."""
    params = {"apikey": api_key}  # Parámetros para autenticar
    response = requests.get(check_url, params=params)

    if response.status_code != 200:
        print(f"Error al consultar mensajes: {response.status_code} - {response.text}")
        return None

    try:
        # Filtrar mensajes para obtener respuestas del destinatario
        mensajes = response.json().get("messages", [])
        for mensaje in mensajes:
            if mensaje.get("from") == to_number:  # Asegurarse de que es el destinatario
                return mensaje.get("body")  # Devuelve el contenido del mensaje recibido
    except ValueError:
        print("La respuesta del servidor no es un JSON válido.")
    return None

def notificar_respuesta(from_number, to_number, respuesta):
    """Envía una notificación sobre la respuesta recibida."""
    mensaje = mensaje_notificacion.format(respuesta=respuesta)
    return enviar_mensaje(from_number, to_number, mensaje)

# Enviar mensaje inicial
if enviar_mensaje(from_number, to_number, mensaje_inicial):
    print(f"Esperando respuesta del número {to_number}...")

    # Esperar respuesta del destinatario
    respuesta = None
    timeout = 120  # Tiempo máximo de espera (en segundos)
    intervalo = 15  # Intervalo entre verificaciones (en segundos)

    for _ in range(timeout // intervalo):
        respuesta = verificar_respuesta(to_number)
        if respuesta:
            print(f"El destinatario respondió: {respuesta}")
            break
        time.sleep(intervalo)  # Esperar antes de volver a consultar

    if respuesta:
        # Enviar notificación con la respuesta
        if notificar_respuesta(from_number, to_number, respuesta):
            print(f"Notificación enviada al número {from_number}.")
        else:
            print(f"No se pudo enviar la notificación al número {from_number}.")
    else:
        print(f"No se recibió respuesta del número {to_number}.")
else:
    print("No se pudo enviar el mensaje inicial.")