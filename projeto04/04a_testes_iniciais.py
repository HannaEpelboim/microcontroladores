# importação de bibliotecas
from os import system
from time import sleep
from requests import post
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button, LED
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# parâmetros iniciais do Telegram
chave = 'COLOQUE A CHAVE'
id_da_conversa = "COLOQUE O ID"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
def inicia_gravacao():
    lcd.clear()
    lcd.message("Gravando...")
    system("arecord --duration 5 teste_iniciais04.wav")
    lcd.clear()
    
def tira_foto():
    for i in range(5):
        comando = "fswebcam foto_%d.jpg" % (i+1)
        system(comando)
        led1.blink(n=1, on_time=0.1)
        sleep(2)
        
def envia_mensagem():
    dados = {"chat_id": id_da_conversa, "text": "Ola teste ola!"}
    endereco = endereco_base + "/sendMessage"
    resposta = post(endereco, json=dados)
    print(resposta.text)
    


# criação de componentes
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)


botao1.when_pressed = inicia_gravacao
botao2.when_pressed = tira_foto
botao3.when_pressed = envia_mensagem
