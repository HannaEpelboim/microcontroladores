# importação de bibliotecas
from threading import Timer
from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
from requests import post
from gpiozero import LightSensor
from gpiozero import DistanceSensor
# definição de funções

def escreve_ola():
    print("Ola")
    global timer
    timer = Timer(2, escreve_ola)
    timer.start()    

def ligar1e2():
    global timer2
    if timer2 != None:
        timer2.cancel()
    led1.on()
    led2.on()
    
def desligaLed():
    global timer2
    timer2 = Timer(8, led2.off)
    timer2.start()
    led1.off()

def mandaInfo():
    print("Entrei")
    url = "https://cloud.activepieces.com/api/v1/webhooks/e0takSkFPnArNTmQXdYUH"
    texto  = "%d%% de luz/ %dcm\n" %(sensorLuz.value*100, sensorDist.distance*100)
    dados ={"texto": texto}
    post(url, params=dados)

    
# criação de componentes
global timer
global timer2
timer = None
timer2 = None
escreve_ola()

led1 = LED(21)
led2 = LED(22)
btn1 = Button(11)
sensor = MotionSensor(27)

sensor.when_motion = ligar1e2
sensor.when_no_motion = desligaLed
sensorDist = DistanceSensor(trigger=17, echo=18)
sensorLuz = LightSensor(8)

btn1.when_pressed = mandaInfo

# loop infinito
