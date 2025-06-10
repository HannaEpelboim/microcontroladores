# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS
# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from os import system
from subprocess import Popen
from time import sleep
from requests import post, get
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button, Buzzer, LED, DistanceSensor
from urllib.request import urlretrieve
from mplayer import Player
from datetime import datetime, timedelta
from unidecode import unidecode

# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")
player = Player()
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1


# parâmetros iniciais do Telegram
chave = "CHAVE"
id_da_conversa = "ID"
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
    keyboard = {"keyboard":[[{"text":"Abrir"}],[{"text":"Ignorar"}], [{"text":"Soar Alarme"}]]}
    dados = {"chat_id": id_da_conversa, "text":"O que deseja fazer?","reply_markup":keyboard}
    endereco = endereco_base + "/sendMessage"
    resposta = post(endereco, json=dados)
     
    
def trata_texto_mensagem(texto):
    if texto == "Abrir":
        led1.on()
    elif texto == "Soar Alarme":
        buzzer.beep(n = 5, on_time = 0.3, off_time = 0.2)
    elif texto == "Ignorar":
        pass
    else:
        for i in range(2):
            lcd.clear()
            sleep(1)
            lcd.message("Msg. Recebida")
            buzzer.beep(n=1,on_time=1)
            sleep(1)
        lcd.clear()
        tam = len(texto)
        texto= unidecode(texto)
        for i in range(tam):
            lcd.clear()
            lcd.message(texto[i:])
            sleep(0.5)
        lcd.clear()
        
def inicia_gravacao():
    global aplicativo
    comando = ["arecord", "--duration", "30", "audio.wav"]
    aplicativo = Popen(comando)
    
def parar_gravacao():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        system("opusenc audio.wav audio.ogg")

        dados = {"chat_id": id_da_conversa}
        endereco = endereco_base + "/sendVoice"
        arquivo = {"voice": open("audio.ogg", "rb")}
        resposta = post(endereco, data=dados, files=arquivo)

def trata_audio(id_do_arquivo):
    endereco = endereco_base + "/getFile"
    dados = {"file_id": id_do_arquivo}
    resposta = get(endereco, json=dados)
    dicionario = resposta.json()
    final_do_link = dicionario["result"]["file_path"]
    link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
    arquivo_de_destino = "arquivo_recebido.ogg"
    urlretrieve(link_do_arquivo, arquivo_de_destino)
    player.loadfile(arquivo_de_destino)
    
def frente_porta():
    global tempo_na_porta
    if tempo_na_porta == None:
        tempo_na_porta = datetime.now()

def saiu_da_porta():
    global tempo_na_porta
    agora = datetime.now()
    intervalo = agora - tempo_na_porta
    segundos = intervalo.total_seconds()
    if segundos >= 10:
       envia_mensagem("Pessoa saiu")
    print("\n Tempo na porta foi:")
    print(segundos)
    tempo_na_porta = None
    
# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
buzzer = Buzzer(16)
aplicativo = None
tempo_na_porta = datetime.now()

botao1.when_pressed = buzzer.on
botao1.when_released = solta_buzzer
#botao2.when_pressed = led1.off
botao3.when_pressed = inicia_gravacao
botao3.when_released = parar_gravacao
sensor.when_in_range = frente_porta
sensor.when_out_of_range = saiu_da_porta
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
            trata_audio(id_do_arquivo)
        elif "photo" in mensagem:
            foto_mais_resolucao = mensagem["photo"][-1]
            id_do_arquivo = foto_mais_resolucao["file_id"]
         # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)


