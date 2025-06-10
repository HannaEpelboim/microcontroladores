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
    player.pt_step(1)


def previousTrack():
    if player.time_pos < 2:
        player.pt_step(-1)
    else:
        player.time_pos = 0


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
button03.when_pressed = nextTrack


# loop infinito
while True:
    
    if player.metadata["Artist"]:
        lcd.clear()
        lcd.message(player.metadata["Artist"])
    
    
    sleep(0.2)
