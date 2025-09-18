from gpiozero import Button
from subprocess import Popen
from signal import pause

path_imagen = 'imagenes/captura.jpg'

pin_envia_imagen = 21
pin_reproduce_audio = 20
pin_envia_audio = 16

button_envia_imagen = Button(pin= pin_envia_imagen, bounce_time=0.1)
button_reproduce_audio = Button(pin= pin_reproduce_audio, bounce_time=0.1)
button_envia_audio = Button(pin_envia_audio, bounce_time=0.1)

proceso_camara = Popen(['rpicam-still',
                                '-n',
                                '-s',
                                '-v', '1',
                                '-t', '0',
                                '--rotation','180',
                                '--autofocus-mode', 'continuous',
                                '-o', path_imagen])


def captura_imagen():
    proceso_camara.send_signal(10)
    print('capturando imagen')


button_envia_imagen.when_pressed = captura_imagen

try:
    while True:
        pass
except:
    proceso_camara.send_signal(12)