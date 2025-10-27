from socket import socket
from os.path import getsize, basename, join
import json
from queue import Queue
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen
from datetime import datetime
from time import sleep



imagenes = Queue() # cola de rutas de las imagenes a enviar

with open('config.json', 'r') as f:
    config = json.load(f)

HOST= config['ip_servidor']
PORT = config['port_imagen']


def hilo_enviar():
    global imagenes
    while True:
        try:
            with socket() as sock:
                sock.connect((HOST,PORT))
                print('conexion establecida')

                while True:
                    path_imagen = imagenes.get()
                    size_imagen = getsize(path_imagen).to_bytes(4,byteorder='big')
                    name_imagen = basename(path_imagen) + '\n'

                    print('\nenviado archivo: ', name_imagen, ' de ', size_imagen,' bits')

                    with open(path_imagen, 'rb') as file:
                        sock.sendall(name_imagen.encode())
                        sock.sendall(size_imagen)
                        sock.sendfile(file)
                        print('archivo enviado\n')
        except Exception as ex:
            imagenes.put(path_imagen)
            print("Error en conexión: \n", ex)
            sleep(3)


class Handler(FileSystemEventHandler):
    def on_closed(self, event):
        ahora = datetime.now()
        timestamp = ahora.strftime("%Y%m%d%H%M%S%f")
        imagen_name = f"{timestamp}.jpg"
        path_destino = join('imagenes','originales', imagen_name)
        mv = Popen(f"cp {event.src_path} {path_destino}", shell=True)
        mv.wait()
        imagenes.put(path_destino)
        Popen(['vlc', '-I', 'dummy', '--play-and-exit', 'audios/nortificacion/canon.mp3'])




observer =Observer()
observer.schedule(Handler(), 'imagenes', recursive= False)
observer.start()

hilo = Thread(target= hilo_enviar, daemon= True)
hilo.start()


try:
    while observer.is_alive():
        observer.join(1)
finally:
        observer.stop()
        observer.join()
