from socket import socket
from time import sleep
from os.path import basename,join ,getsize
from gpiozero import Button
from subprocess import Popen, PIPE
from datetime import datetime
from threading import Thread
import json

with open('config.json', 'r') as f:
    config = json.load(f)

IP_server= config['ip_servidor']
PORT = config['port_audio']


pin_audio= 21

boton = Button(pin_audio, bounce_time=0.1)

grabacion= None # objeto del proceso que va a grabar
client_socket= None 
creando_socket = False # bandera para identificar cuando se esta creando un nuevo socket
notificacion_grabacion = None # proceso para saber el momento en que se graba

def crea_socket(audio_name:str):
    global client_socket, creando_socket
    audio_name = audio_name + '\n'

    try:
        client_socket.close()
    except:
        pass

    try:
        client_socket = socket()
        print('conectando ...')
        client_socket.connect((IP_server, PORT))
        client_socket.sendall(audio_name.encode('utf-8'))
        print('Conexión establecida')
        creando_socket= False

    except Exception as ex:
        print('error en la conexion:\n',ex)


def grabar_y_enviar(audio_name):
    global grabacion, grabando, client_socket, creando_socket
    audio_path = join('audios', 'enviar',audio_name)
    
    with open(audio_path, 'wb') as file:

        crea_socket(audio_name)

        while True:
            data = grabacion.stdout.read(17408)
            if not data:
                grabando= False
                client_socket.close()
                print('conexion cerrada')
                break
            file.write(data)
            try:
                client_socket.sendall(data)
            except Exception as ex:
                if creando_socket == False:
                    creando_socket= True
                    hilo_socket= Thread(target=crea_socket, args=(audio_name,))
                    hilo_socket.start()
                    print('Error al enviar datos.\n', ex)

            
            
def iniciar_grabacion():
    global grabacion, grabando, notificacion_grabacion
    grabando = True
    notificacion_grabacion = Popen(['vlc', '-I', 'dummy', '--loop', 'audios/nortificacion/soft-piano-72454.mp3'])

    ahora = datetime.now()
    timestamp = ahora.strftime("%Y%m%d%H%M%S%f")
    audio_name = f"{timestamp}.mp3"

    comando_grabacion = ['ffmpeg', '-f', 'alsa', '-i', 'default', '-acodec', 'libmp3lame', '-b:a', '16k', '-ac', '1', '-ar', '11025', '-compression_level', '2', '-f', 'mp3', 'pipe:1']

    grabacion =Popen(comando_grabacion, stdout= PIPE)

    hilo_grabar_y_enviar = Thread(target=grabar_y_enviar, args=(audio_name,), daemon=True)

    hilo_grabar_y_enviar.start()

    
    

def terminar_grabacion():
    global grabacion, grabando, notificacion_grabacion
    grabando = False
    grabacion.send_signal(2)
    notificacion_grabacion.kill()
    print('fin grabacion')
    
boton.when_pressed = iniciar_grabacion
boton.when_released = terminar_grabacion

while True:
    sleep(1)