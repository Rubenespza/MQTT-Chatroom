import paho.mqtt.client as mqtt
import json
import time

# --- Configuración ---
BROKER_ADDRESS = "broker.hivemq.com"  # Broker público de prueba
PORT = 1883
QOS_LEVEL = 1

# --- Funciones de Callback ---

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Conectado al Broker MQTT en {BROKER_ADDRESS}")
        room_topic = userdata['room_topic']
        client.subscribe(room_topic, qos=QOS_LEVEL)
        print(f"🚪 Suscrito a la sala: {room_topic}")
    else:
        print(f"❌ Fallo en la conexión, código de retorno: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sender = payload.get('user', 'Desconocido')
        message = payload.get('message', '')

        if sender != userdata['username']:
            print(f"\r[{sender}]: {message}\n> Tú: ", end="")

    except Exception as e:
        print(f"\nError al procesar el mensaje: {e}")

# --- Función Principal ---
def main():
    username = input("👤 Ingresa tu nombre de usuario: ")
    room = input("💬 Ingresa el nombre de la sala: ")
    room_topic = f"chat/rooms/{room}"

    user_data = {
        'username': username,
        'room_topic': room_topic
    }

    client = mqtt.Client(userdata=user_data)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER_ADDRESS, PORT, 60)
        client.loop_start()
        print("Escribe tu mensaje y presiona Enter. Escribe 'salir' para desconectar.")

        while True:
            message_text = input(f"> Tú: ")
            if message_text.lower() == 'salir':
                break

            payload = json.dumps({
                "user": username,
                "message": message_text,
                "timestamp": time.time()
            })

            client.publish(room_topic, payload, qos=QOS_LEVEL)

    except Exception as e:
        print(f"\nOcurrió un error: {e}")
    finally:
        print("\nDesconectando...")
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()

#-- python chat_client.py