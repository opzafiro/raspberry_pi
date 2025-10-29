from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters
from telegram import Update
from datetime import datetime
from gpiozero import Button
from queue import Queue
from subprocess import Popen
import json
import asyncio

with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

token= config['bot_token']

audios = []
len_audios = 0
index = -1
reproduciendo= None


pin_reproduce_audio = config['pin_respuesta']
button_reproduce_audio = Button(pin= pin_reproduce_audio, bounce_time=0.1, hold_time=1)

def reproducir_audio_siguiente():
    global audios, index, len_audios, reproduciendo
    try:
        reproduciendo.kill()
    except Exception as ex:
        print('Error al cerrar reproductor: \n', ex)

    if len_audios > 0:
        index = (index+1)% len_audios
        #reproduciendo = Popen(['cvlc', '-I', 'dummy', '--play-and-exit', audios[index]])
        reproduciendo = Popen(['mpg123', audios[index]])
        

def reproducir_audio_anterior():
    global audios, index, len_audios, reproduciendo

    try:
        reproduciendo.kill()
    except Exception as ex:
        print('Error al cerrar reproductor: \n', ex)
    
    if len_audios > 0:
        index = (index-2)% len_audios
        #reproduciendo = Popen(['cvlc', '-I', 'dummy', '--play-and-exit', audios[index]])
        reproduciendo = Popen(['mpg123', audios[index]])
        



button_reproduce_audio.when_pressed = reproducir_audio_siguiente
button_reproduce_audio.when_held = reproducir_audio_anterior


        
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    global audios, len_audios, index
    voice_file = await update.message.voice.get_file()  # Obtener el archivo de voz
    # nombre unico al archivo de audio 
    ahora = datetime.now()
    timestamp = ahora.strftime("%Y%m%d%H%M%S%f")
    audio_name = f"{timestamp}.ogg"
    file_path = f'audios/recibidos/{audio_name}'
    # Descargar el archivo
    await voice_file.download_to_drive(file_path)

    Popen(['ffmpeg', '-i', file_path, file_path.replace('.ogg', '.mp3')])
    file_path = file_path.replace('.ogg', '.mp3')


    audios.append(file_path)
    len_audios +=1
    
    Popen(['mpg123', 'audios/nortificacion/011-c6-98517.mp3'])

    # Responder al usuario
    #await update.message.reply_text("Recibido")
    #system('vlc -I dummy --play-and-exit /home/bicycle/Desktop/virus/mensajes/voz/recibido.ogg')

    # responder mensaje
    #await update.message.reply_text(text=f"Recibí tu mensaje")
    
async def limpiar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global audios, len_audios, index, reproduciendo
    audios = []
    len_audios = 0
    index = -1
    reproduciendo = None

    await update.message.reply_text("Lista de audios limpiada ✅")

async def set_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global config

    if not context.args:
        await update.message.reply_text("Uso: /ip <dirección_ip>")
        return
    ip = context.args[0]
    ip = ip.replace(' ', '') 

    config['ip_servidor']=ip

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    try:
        Popen(['sudo', 'systemctl', 'restart', 'zafiro_audio.service'])
        Popen(['sudo', 'systemctl', 'restart', 'zafiro_imagen.service'])
    except Exception as ex:
        print('error al reiniciar demonios:', ex)
        await update.message.reply_text('error al reiniciar los demonios')
        return
    
    await update.message.reply_text(f'ip cambiada con exito:\n{ip}')

async def reinicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:

        Popen(['sudo', 'systemctl', 'restart', 'zafiro_audio.service'])
        Popen(['sudo', 'systemctl', 'restart', 'zafiro_imagen.service'])
        Popen(['sudo', 'systemctl', 'restart', 'zafiro_proceso_camara.service'])
        await update.message.reply_text('reinicio exitoso')

    except Exception as ex:
        print('error al reiniciar demonios:', ex)
        await update.message.reply_text('error al reiniciar los demonios')
        return

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/l limpiar audios\n/ip cambiar ip server\n/r reiniciar demonios')

async def on_startup(application):
    await application.bot.send_message(chat_id='-1002148727613', text='Hola ya vamos a comenzar 😊')



application = ApplicationBuilder().token(token).post_init(on_startup).build()
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
application.add_handler(CommandHandler('l', limpiar))
application.add_handler(CommandHandler('ip', set_ip))
application.add_handler(CommandHandler('r', reinicio))
application.add_handler(CommandHandler('help', help))

application.run_polling()

