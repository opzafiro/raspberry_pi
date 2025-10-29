from gpiozero import Button
from subprocess import Popen, CalledProcessError
from time import sleep
import json

with open('config.json', 'r') as f:
    config = json.load(f)


path_imagen = 'imagenes/captura.jpg'

pin_envia_imagen = config['pin_imagen']


button_envia_imagen = Button(pin= pin_envia_imagen, bounce_time=0.1)

while True:

    try:
        proceso_camara = Popen(['rpicam-still',
                                        '-n',
                                        '-s',
                                        '-v', '1',
                                        '-t', '11000000',
                                        '--rotation','180',
                                        '--autofocus-mode', 'continuous',
                                        '-o', path_imagen],
                                        )
        print('camara iniciada correctamente:')
        break

    except CalledProcessError as e:
        print('Error al iniciar la camara: ',e)
        sleep(10)



def captura_imagen():
    global proceso_camara
    proceso_camara.send_signal(10)
    print('capturando imagen')


button_envia_imagen.when_pressed = captura_imagen

try:
    while True:
        sleep(10)
finally:
    proceso_camara.send_signal(12)