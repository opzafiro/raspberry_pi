#!/bin/bash
mkdir -p imagenes/miniatura imagenes/originales imagenes/recortadas imagenes/originales_copy
sudo apt update
sudo apt install libvips-tools #sistema de procesamiento de imágenes

#audio
sudo apt install pulseaudio pulseaudio-module-bluetooth bluez-tools
pulseaudio -k
pulseaudio --start

pactl set-default-source bluez_sink.46_60_07_6E_51_98.a2dp_sink.monitor # BT600 input predeterminado
pactl set-default-sink bluez_sink.41_42_47_71_E7_5C.a2dp_sink # Air pods output predeterminado


sudo apt install ffmpeg # de wav a mp3

# python
python -m venv entorno_virtual
source entorno_virtual/bin/activate
pip install dependencias.txt