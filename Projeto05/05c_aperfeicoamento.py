# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

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

def desligaLed1():
    atualiza_led(1,False)
    
def comeca_timer():
    global timer
    timer = Timer(10, desligaLed1)
    timer.start()

def liga_led_distancia():
    global timer
    atualiza_led(1,True)
    if timer != None:
        timer.cancel()
        
def led2_acende():
    
    atualiza_led(2,True)

def led2_apaga():
    
    atualiza_led(2,False)

def liga_leds(dicionario):
    i = 1
    for estado in dicionario["estados"]:
        atualiza_led(i, estado)
        i += 1
@app.route("/led/estados")
def faz_html():
    i = 1
    codigo = "<ul>"
    for estado in estados:
        if estado == True:
            codigo += "<li>Led %d aceso</li>" %(i)
        else:
            codigo += "<li>Led %d apagado</li>" %(i)
        i +=1
    codigo += "</ul>"
    return codigo

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
cliente = MongoClient("localhost", 27017)
banco = cliente["historico"]
colecao = banco["historico"]
estados = [False]*5
timer = None
sensor_distancia = MotionSensor(27)
sensor_luz =  LightSensor(8)
sensor_luz.threshold = 0.3
#sensor_distancia.threshold_distance = 0.1

ordenacao = [ ["data", DESCENDING] ]
busca = {}
doc = colecao.find_one(busca, sort = ordenacao)

liga_leds(doc)

sensor_distancia.when_motion = liga_led_distancia
sensor_distancia.when_no_motion = comeca_timer
#atualiza_led(2, True)
sensor_luz.when_dark = led2_acende
sensor_luz.when_light = led2_apaga

# rode o servidor
app.run(port=5000, debug=False) #sempre ultima linha

