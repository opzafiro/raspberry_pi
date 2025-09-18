from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters
from telegram import Update
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
from gpiozero import Button


ruta = 'audios'
loop =None
        
application = ApplicationBuilder().token('7392248545:AAGcbygZXKnSyjT_ySgbmbcLppCC-uQGvjk')\
    .read_timeout(60)\
    .write_timeout(60)\
    .connect_timeout(30)\
    .build()

class MiHandler(FileSystemEventHandler):
    def on_closed(self, event):
        loop.call_soon_threadsafe(lambda: loop.create_task(enviar_archivo(event.src_path)))
        print(f"Se creó: {event.src_path}")
    
async def enviar_archivo(path):
    with open(path, 'rb') as file:
        await application.bot.send_document(chat_id=-1002148727613, document= file)
        print(f"Se envió: {path}")

async def main():
    global loop
    loop = asyncio.get_running_loop()
    
    observer = Observer()
    observer.schedule(MiHandler(), ruta, recursive=False)
    observer.start()
    try:
        await asyncio.Event().wait()
    finally:
        observer.stop()
        observer.join()

    #await enviar_archivo('audios/hola copy 5.txt')

asyncio.run(main())







