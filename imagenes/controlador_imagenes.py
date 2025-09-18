from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import system
from subprocess import Popen
from PIL import Image
from os.path import basename
from time import time
from datetime import datetime
import requests

ip_server= "35.225.118.5"

url_yolo = f"http://{ip_server}:2020"
url_server = f'http://{ip_server}:3030'

# toma una imagen y la envia al servidor y este responde con las coordenadas
def coordenadas_imagen(nombre):
    file = {"imagen": open(f"imagenes/miniatura/{nombre}", "rb")}
    response = requests.post(url_yolo, files=file)
    coordenadas = response.text.replace('\n', '').split(' ')
    coordenadas = tuple(map(int, coordenadas))
    print('coordenadas: ',coordenadas)  
    return coordenadas

def envia_imagen(nombre):
    file = {"imagen": open(f"imagenes/recortadas/{nombre}", "rb")}
    response = requests.post(url_server, files=file)
    print('imagen enviada')
    

class Handler(FileSystemEventHandler):
    def on_closed(self, event):
        print(event.src_path)
        t_0 = time()
        ahora = datetime.now()
        timestamp = ahora.strftime("%Y%m%d%H%M%S%f")
        filename = f"{timestamp}.jpg"
        #system(f'mv imagenes/*.jpg imagenes/originales/{filename}')

        origen = "imagenes/captura.jpg"
        destino = f"imagenes/originales/{filename}"

        mv = Popen(f"cp {origen} {destino}", shell=True)
        mv.wait()
        miniatura_path= 'imagenes/miniatura/'+ filename
        originales_path= 'imagenes/originales/' + filename
        recortadas_path= 'imagenes/recortadas/' + filename

        size = 416, 416

        im= Image.open(originales_path)
        im.thumbnail(size)
        im.save(miniatura_path)
        print('miniatura guardada')
        coordenadas = coordenadas_imagen(filename)
        im= Image.open(originales_path)
        region = im.crop(coordenadas)
        region.save(recortadas_path)
        envia_imagen(filename)

        print(f'tiempo ={time()-t_0}')
        
observer =Observer()
observer.schedule(Handler(), 'imagenes/', recursive= False)
observer.start()




try:
    while observer.is_alive():
        observer.join(1)
finally:
        observer.stop()
        observer.join()

