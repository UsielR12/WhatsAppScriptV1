from twilio.rest import Client
import time
from datetime import datetime

# Credenciales de Twilio
account_sid = 'AC9f12c000be13be440e04f3cdb93226cf'
auth_token = '6be42b6d090ec0db2f7affabcdc40119'
client = Client(account_sid, auth_token)


# Función para enviar mensaje
def send_message(to, body):
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número de Twilio
        body=body,
        to=f'whatsapp:{to}'
    )
    print(f"Mensaje enviado con SID: {message.sid}")
    return message.sid


# Función para verificar respuesta
from datetime import datetime


def check_response(to, date_sent):
    print("Esperando respuesta...")
    while True:
        # Obtener mensajes recientes desde Twilio
        messages = client.messages.list(limit=20)

        for message in messages:
            # Filtrar solo mensajes entrantes del número esperado
            if message.direction == 'inbound' and message.from_ == f'whatsapp:{to}':
                # Convertir la fecha del mensaje entrante
                message_time = datetime.strptime(str(message.date_sent).split('+')[0], '%Y-%m-%d %H:%M:%S')

                # Verificar si el mensaje se recibió después del envío original
                if message_time > date_sent:
                    print(f"Respuesta recibida: {message.body}")
                    return message.body

        # Esperar 10 segundos antes de volver a consultar
        time.sleep(3)


# Programa principal
if __name__ == "__main__":
    # Configura los números
    to = '+50684181246'  # Número que recibirá el mensaje original
    to_notify = '+50684181246'    # Número al que se notificará la respuesta
    body = '¡Hola! Esto es una prueba.'

    # Enviar mensaje y capturar su fecha de creación
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to=f'whatsapp:{to}'
    )
    print(f"Mensaje enviado con SID: {message.sid}")
    date_sent = datetime.strptime(str(message.date_created).split('+')[0], '%Y-%m-%d %H:%M:%S')

    # Esperar respuesta y notificar
    respuesta = check_response(to, date_sent)
    print(f"Respuesta final recibida: {respuesta}")

    # Enviar notificación de la respuesta
    notification_body = f"Se recibió una respuesta: '{respuesta}'"
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=notification_body,
        to=f'whatsapp:{to_notify}'
    )

