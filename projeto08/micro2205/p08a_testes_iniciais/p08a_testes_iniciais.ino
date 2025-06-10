#include <Servo.h>
#include <EEPROM.h>
#include <GFButton.h>

GFButton botaoB(3);
GFButton botaoA(2);
GFButton botaoC(4);
int count = 0;
int endereco = 0;
int pot = A5;
int ang = 90;

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  botaoB.setPressHandler(botaoBpressed);
  EEPROM.get(endereco, count);
  pinMode(pot, INPUT);
  servo1.attach(12);
  servo2.attach(11);
}

void botaoBpressed() {
  count++;
  Serial.println(count);
  EEPROM.put(endereco, count);
}

void loop() {
  botaoB.process();
  int valor_pot = analogRead(pot);
  int valor_map = map(valor_pot, 0, 1023, 0, 180);
  servo1.write(valor_map);
  
  if (botaoA.isPressed()) {
    ang = max(--ang, 45);
    delay(15);
  }
  if (botaoC.isPressed()) {
    ang = min(135, ++ang);
    delay(15);
  }
  servo2.write(ang);
  // Serial.println(ang);
}

