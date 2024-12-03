import requests
import time

# Configura la URL de la API
api_url = "https://script.google.com/macros/s/AKfycbyoBhxuklU5D3LTguTcYAS85klwFINHxxd-FroauC4CmFVvS0ua/exec"

# Configura el token de acceso
token = "GA241203154824"

# Configura los números
numero_destinatario = "50684181246"  # Número al que se enviará el primer mensaje
numero_notificacion = "50684181246"  # Número al que se notificará la respuesta
mensaje_inicial = "Hola, este es un mensaje de prueba desde Python."

# Enviar mensaje inicial
payload = {
    "op": "registermessage",
    "token_qr": token,
    "mensajes": [
        {"numero": numero_destinatario, "mensaje": mensaje_inicial}
    ]
}

response = requests.post(api_url, json=payload)

if response.status_code == 200:
    print(f"Mensaje enviado correctamente al número {numero_destinatario}.")
else:
    print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")
    exit()

# Esperar respuesta del destinatario
print(f"Esperando respuesta del número {numero_destinatario}...")

def check_response():
    """Consulta las respuestas para verificar si el destinatario ha respondido."""
    payload_check = {
        "op": "getmessages",  # Operación para verificar mensajes entrantes
        "token_qr": token
    }
    try:
        response_check = requests.post(api_url, json=payload_check)

        # Imprime el estado y el contenido del servidor
        print(f"Estado del servidor: {response_check.status_code}")
        print(f"Contenido del servidor: '{response_check.text}'")  # Incluye las comillas para ver si está vacío

        if response_check.status_code != 200:
            print("Error al consultar la API. Verifica la URL o el payload.")
            return None

        # Intentar parsear como JSON
        messages = response_check.json().get("mensajes", [])
        return messages

    except ValueError:
        print("La respuesta del servidor no es un JSON válido.")
        print(f"Respuesta recibida: '{response_check.text}'")  # Verifica el contenido exacto
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")
        return None

# Verifica periódicamente si el destinatario ha respondido
respuesta = None
timeout = 60  # Tiempo máximo de espera (en segundos)
intervalo = 10  # Intervalo entre verificaciones (en segundos)

for _ in range(timeout // intervalo):
    respuesta = check_response()
    if respuesta:
        print(f"El destinatario respondió: {respuesta}")
        break
    time.sleep(intervalo)  # Esperar antes de volver a consultar

if not respuesta:
    print(f"No se recibió respuesta del número {numero_destinatario}.")
    exit()

# Enviar notificación al número configurado
mensaje_notificacion = f"El destinatario {numero_destinatario} respondió: '{respuesta}'"
payload_notificacion = {
    "op": "registermessage",
    "token_qr": token,
    "mensajes": [
        {"numero": numero_notificacion, "mensaje": mensaje_notificacion}
    ]
}

response_notificacion = requests.post(api_url, json=payload_notificacion)

if response_notificacion.status_code == 200:
    print(f"Notificación enviada correctamente al número {numero_notificacion}.")
else:
    print(f"Error al enviar la notificación: {response_notificacion.status_code} - {response_notificacion.text}")