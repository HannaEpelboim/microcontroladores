# importação de bibliotecas
from os import system
from time import sleep
from requests import post, get
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button, Buzzer, LED

# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")


# parâmetros iniciais do Telegram
chave = "7653728106:AAHK6RlEQz9KMoynZ2-901NbIbkPcDiBILs"
id_da_conversa = "7158599693"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções]
def envia_foto(foto):
    endereco = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"photo": open(foto, "rb")}
    resposta = post(endereco, data=dados, files=arquivo)

def tira_foto(qtd):
    for i in range(qtd):
        comando = "fswebcam foto_%d.jpg" % (i+1)
        system(comando)
        led1.blink(n=1, on_time=0.1)
        sleep(2)
        
def envia_mensagem(texto):
    dados = {"chat_id": id_da_conversa, "text": texto}
    endereco = endereco_base + "/sendMessage"
    resposta = post(endereco, json=dados)
    print(resposta.text)

def solta_buzzer():
    buzzer.off()
    envia_mensagem("Tem alguem na porta")
    tira_foto(1)
    envia_foto("foto_1.jpg")
    
def trata_texto_mensagem(texto):
    if texto == "Abrir":
        led1.on()
    elif texto == "Soar Alarme":
        buzzer.beep(n = 5, on_time = 0.3, off_time = 0.2)
    
# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
buzzer = Buzzer(16)

botao1.when_pressed = buzzer.on
botao1.when_released = solta_buzzer
botao2.when_pressed = led1.off
# loop infinito
proximo_id_de_update = 0
while True:
    
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update}
    resposta = get(endereco, json=dados)
    dicionario_da_resposta = resposta.json()
    for resultado in dicionario_da_resposta["result"]:
        mensagem = resultado["message"]
        if "text" in mensagem:
            texto = mensagem["text"]
            trata_texto_mensagem(texto)
        elif "voice" in mensagem:
            id_do_arquivo = mensagem["voice"]["file_id"]
             # depois baixa o arquivo e faz algo com ele...
        elif "photo" in mensagem:
            foto_mais_resolucao = mensagem["photo"][-1]
            id_do_arquivo = foto_mais_resolucao["file_id"]
         # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)
