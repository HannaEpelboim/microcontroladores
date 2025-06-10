# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from py_irsend.irsend import send_once
from flask import Flask,render_template, redirect
from gpiozero import LED, Button
from threading import Timer
import json

send_once("aquario", ["KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5"])
botao1=Button(11)
botao2=Button(12)
botao3=Button(13)
botao4=Button(14)

with open('data.JSON') as arquivo:
    dados = json.load(arquivo)

# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
@app.route("/power")
def mostrar_inicio():
 send_once("aquario", ["KEY_POWER"])
 return redirect("/")

@app.route("/aumentaVolume")
def aumenta_volume():
 send_once("aquario", ["KEY_VOLUMEUP"])
 return redirect("/")

@app.route("/abaixaVolume")
def abaixa_volume():
 send_once("aquario", ["KEY_VOLUMEDOWN"])
 return redirect("/")

@app.route("/mudo")
def mudo():
 send_once("aquario", ["KEY_MUTE"])
 return redirect("/")

@app.route("/canal/<string:x>")
def canal(x):
    for carac in x:
        print(carac)
        send_once("aquario", ["KEY_" + carac])
        
        
    return redirect("/")

@app.route("/powerOff/<int:x>")
def power_off(x):
    t = Timer(x, send_once, args=("aquario", ["KEY_POWER"]))
    t.start()        
        
    return redirect("/")

@app.route("/")
def canais():
    return render_template("index.html",mylist=dados)
# rode o servidor

app.run(port=5000, debug = True)





