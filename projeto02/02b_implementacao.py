# importação de bibliotecas
from py_irsend.irsend import send_once
from flask import Flask
from gpiozero import LED, Button
from threading import Timer 
send_once("aquario", ["KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5"])
botao1=Button(11)
botao2=Button(12)
botao3=Button(13)
botao4=Button(14)



# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
@app.route("/power")
def mostrar_inicio():
 send_once("aquario", ["KEY_POWER"])
 return "Bem-vindo!"

@app.route("/aumentaVolume")
def aumenta_volume():
 send_once("aquario", ["KEY_VOLUMEUP"])
 return "Volume aumentado!"

@app.route("/abaixaVolume")
def abaixa_volume():
 send_once("aquario", ["KEY_VOLUMEDOWN"])
 return "Volume abaixado!"

@app.route("/mudo")
def mudo():
 send_once("aquario", ["KEY_MUTE"])
 return "Mutado!"

@app.route("/canal/<string:x>")
def canal(x):
    for carac in x:
        print(carac)
        send_once("aquario", ["KEY_" + carac])
        
        
    return "canal"

@app.route("/powerOff/<int:x>")
def power_off(x):
    t = Timer(x, send_once, args=("aquario", ["KEY_POWER"]))
    t.start()        
        
    return "desligando em" + str(x) + "segundos"

# rode o servidor

app.run(port=5000, debug = True)



