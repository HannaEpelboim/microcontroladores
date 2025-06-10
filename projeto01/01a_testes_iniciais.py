# importação de bibliotecas
from gpiozero import LED
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep


# definição de funções
def pisca4():
    led3.blink(n=4)
    global contador
    contador +=1
    lcd.clear()
    lcd.message(str(contador))
    

# criação de componentes
contador = 0
led1 = LED(21)
led2 = LED(22)
led3 = LED(23)
led5 = LED(25)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

led1.blink(on_time=1.0, off_time=3.0)

botao2.when_pressed = led2.toggle

botao3.when_pressed = pisca4

# loop infinito
while True:
    
    if botao1.is_pressed and led1.is_lit:
         led5.on()
    else:
        led5.off()
         
        
    sleep(0.2)
    