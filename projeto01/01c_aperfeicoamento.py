# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from os import system
from time import sleep
from gpiozero import LED
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from mplayer import Player


# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")


# definição de funções
def pauseSong():
    player.pause()
    
    if player.paused:
        led01.blink()
    else:
        led01.on()


def nextTrack():
    if player.speed == 2:
        player.speed = 1
    else:
        player.pt_step(1)


def previousTrack():
    if player.time_pos < 2 and player.time_pos != None:
        player.pt_step(-1)
    else:
        player.time_pos = 0

def faster():
    player.speed = 2
    
# criação de componentes
button01 = Button(11)
button02 = Button(12)
button03 = Button(13)
button04 = Button(14)
button05 = Button(15)

led01 = LED(21)
led02 = LED(22)
led03 = LED(23)
led04 = LED(24)
led05 = LED(25)

player = Player()
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

player.loadlist("playlist.txt")
led01.on()

player.volume = 70
button01.when_pressed = previousTrack
button02.when_pressed = pauseSong
button03.when_released = nextTrack
button03.when_held = faster

# loop infinito
while True:
    posicao = player.time_pos
    metadados = player.metadata
    if metadados != None and posicao != None:
        lcd.clear()
        lcd.message("%s \n" % (player.metadata["Title"]))
        lcd.message("%02d:%02d de %02d:%02d" % (posicao//60,posicao%60, player.length//60, player.length%60))
    
        
    
    
    sleep(0.2)

