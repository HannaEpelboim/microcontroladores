# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from py_irsend.irsend import send_once
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)


# definição de funções
send_once("mini", ["KEY_1", "KEY_2","KEY_3","KEY_4","KEY_5"])
init("aula", blocking=False)
def acende_todos():
    global leds
    for led in leds:
        led.on()

def apaga_todos():
    global leds
    for led in leds:
        led.off()
        
def escreve_led():
    global n_led
    lcd.clear()
    lcd.message("LED"+str(n_led)+"\nselecionado")

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]

botao1=Button(11)
botao2=Button(12)
botao1.when_pressed=acende_todos
botao2.when_pressed=apaga_todos
# loop infinito

while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
        codigo = lista_com_codigo[0]
        if (codigo=="KEY_1"):
            n_led=1
            escreve_led()
        elif (codigo=="KEY_2"):
            n_led=2
            escreve_led()
        elif (codigo=="KEY_3"):
            n_led=3
            escreve_led()
        elif (codigo=="KEY_4"):
            n_led=4
            escreve_led()
        elif (codigo=="KEY_5"):
            n_led=5
            escreve_led()
        elif(codigo=="KEY_OK"):
            leds[n_led-1].toggle()
        elif (codigo=="KEY_UP"):
            if (n_led!=5):
                n_led+=1
            else:
                n_led=1
            escreve_led()
        elif (codigo=="KEY_DOWN"):
            if (n_led!=1):
                n_led-=1
            else:
                n_led=5
            escreve_led()
    sleep(0.2)