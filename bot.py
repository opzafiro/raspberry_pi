from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters
from telegram import Update
from datetime import datetime
from gpiozero import Button
from queue import Queue
from subprocess import Popen

token= '7392248545:AAGcbygZXKnSyjT_ySgbmbcLppCC-uQGvjk'

audios = []
len_audios = 0
index = -1
reproduciendo= None

pin_reproduce_audio = 20
button_reproduce_audio = Button(pin= pin_reproduce_audio, bounce_time=0.1, hold_time=1)

def reproducir_audio_siguiente():
    global audios, index, len_audios, reproduciendo
    try:
        reproduciendo.kill()
    except Exception as ex:
        print('Error al cerrar reproductor: \n', ex)

    if len_audios > 0:
        index = (index+1)% len_audios
        reproduciendo = Popen(['vlc', '-I', 'dummy', '--play-and-exit', audios[index]])
        

def reproducir_audio_anterior():
    global audios, index, len_audios, reproduciendo

    try:
        reproduciendo.kill()
    except Exception as ex:
        print('Error al cerrar reproductor: \n', ex)
    
    if len_audios > 0:
        index = (index-2)% len_audios
        reproduciendo = Popen(['vlc', '-I', 'dummy', '--play-and-exit', audios[index]])







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

    audios.append(file_path)
    len_audios +=1
    
    Popen(['vlc', '-I', 'dummy', '--play-and-exit', 'audios/nortificacion/011-c6-98517.mp3'])

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



application = ApplicationBuilder().token(token).build()
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
application.add_handler(CommandHandler('l', limpiar))

application.run_polling()