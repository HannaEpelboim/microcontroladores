# importação de bibliotecas
from gpiozero import LED, Button
from threading import Timer
from gpiozero import MotionSensor
from requests import post
from gpiozero import LightSensor
from gpiozero import DistanceSensor
from time import sleep
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask


# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/led/<int:indice>/<string:estado>")
def mostra_na_pagina(indice, estado):
    if estado == "on":
        atualiza_led(indice, True)
        texto = "Luz %d ligada!" %(indice)
    elif estado == "off":
        atualiza_led(indice, False)
        texto = "Luz %d apagada!" %(indice)
    return texto
    
    
def atualiza_led(indice, estado):
    if estado == True:
        leds[indice-1].on()
    else:
        leds[indice-1].off()
    for i in range(len(leds)):
        estados[i] = leds[i].is_lit
        
    dados = {"data": datetime.now(), "estados": estados}
    colecao.insert(dados)
    

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
cliente = MongoClient("localhost", 27017)
banco = cliente["historico"]
colecao = banco["historico"]
estados = [False]*5

atualiza_led(2, True)
app.run(port=5000, debug=False)
# rode o servidor
