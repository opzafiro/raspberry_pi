from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import system
from subprocess import Popen
from PIL import Image
from os.path import basename
from time import time
from datetime import datetime
import requests

ip_server= "34.60.11.63"

url_yolo = f"http://{ip_server}:2020"
url_server = f'http://{ip_server}:3030'

#decorador que mide el tiempo de ejecucion de una función
def tiempo_ejecucion(fun):
    def envoltorio(*args, **kwargs):
        t_inicio = time()  
        resultado = fun(*args, **kwargs)  
        t_fin = time()  
        print(fun.__name__, 'tardó:', t_fin - t_inicio, 'segundos')  
        return resultado  
    return envoltorio


# toma una imagen y la envia al servidor y este responde con las coordenadas
@tiempo_ejecucion
def coordenadas_imagen(nombre):
    file = {"imagen": open(f"imagenes/miniatura/{nombre}", "rb")}
    response = requests.post(url_yolo, files=file)
    coordenadas = response.text.replace('\n', '').split(' ')
    coordenadas = tuple(map(int, coordenadas))
    print('coordenadas: ',coordenadas)  
    return coordenadas

@tiempo_ejecucion
def envia_imagen(nombre):
    file = {"imagen": open(f"imagenes/recortadas/{nombre}", "rb")}
    response = requests.post(url_server, files=file)
    
@tiempo_ejecucion
def crea_miniatura(filename):
    size = 416, 416
    origen = "imagenes/captura.jpg"
    destino = f"imagenes/originales/{filename}"
    mv = Popen(f"cp {origen} {destino}", shell=True)
    mv.wait()
    miniatura_path= 'imagenes/miniatura/'+ filename
    original_path= 'imagenes/originales/' + filename
    im= Image.open(original_path)
    im.thumbnail(size)
    im.save(miniatura_path)

@tiempo_ejecucion
def recorta_imagen(filename, coordenadas):
    original_path= 'imagenes/originales/' + filename
    recortada_path= 'imagenes/recortadas/' + filename
    im= Image.open(original_path)
    region = im.crop(coordenadas)
    region.save(recortada_path)

class Handler(FileSystemEventHandler):
    def on_closed(self, event):
        print(event.src_path)
        t_0 = time()
        ahora = datetime.now()
        timestamp = ahora.strftime("%Y%m%d%H%M%S%f")
        filename = f"{timestamp}.jpg"
        recortada_path= 'imagenes/recortadas/' + filename

        crea_miniatura(filename)
        coordenadas = coordenadas_imagen(filename)
        recorta_imagen(filename, coordenadas)
        envia_imagen(filename)
        print(f'tiempo total={time()-t_0}')
        print('=========================================')
        
observer =Observer()
observer.schedule(Handler(), 'imagenes/', recursive= False)
observer.start()




try:
    while observer.is_alive():
        observer.join(1)
finally:
        observer.stop()
        observer.join()

