import requests

url = "http://192.168.0.24:2020"



def envia_imagen(nombre):
    file = {"imagen": open(f"imagenes/miniatura/{nombre}", "rb")}
    response = requests.post(url, files=file)

    print(response.text)  # Respuesta ya decodificada como dict
    