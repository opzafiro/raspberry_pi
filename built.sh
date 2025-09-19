#!/bin/bash
mkdir -p imagenes/miniatura imagenes/originales imagenes/recortadas imagenes/originales_copy
sudo apt install libvips-tools #sistema de procesamiento de imágenes
python -m venv entorno_virtual
source entorno_virtual/bin/activate
pip install dependencias.txt