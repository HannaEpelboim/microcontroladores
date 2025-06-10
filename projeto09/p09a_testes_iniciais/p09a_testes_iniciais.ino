#include <AFMotor.h>

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
unsigned long instanteAnteriorDeDeteccao = 0;
int sensor1 = A11;
int sensor2 = A12;
int conta = 0;
bool maior = false;
int num = 0;
int valorAnalogico1, valorAnalogico2;


void setup() {
  motor3.setSpeed(0);
  motor4.setSpeed(0);
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  valorAnalogico2 = analogRead(sensor2);
  if (valorAnalogico2 <= 800) {
    maior = false;
  } else if (valorAnalogico2 > 800) {
    maior = true;
  }
}


// motorA.run(FORWARD); motorB.run(BACKWARD); motorA.run(RELEASE);

void loop() {
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    Serial.println(texto);
    if (texto.startsWith("frente ")) {
      num = texto.substring(7).toInt();
      //Serial.println(String(num));
      motor3.setSpeed(num);
      motor3.run(FORWARD);
    } else if (texto.startsWith("tras ")) {
      num = texto.substring(4).toInt();
      //Serial.println(String(num));
      motor3.setSpeed(num);
      motor3.run(BACKWARD);
    }
  }


  if (millis() > instanteAnteriorDeDeteccao + 500) {
    valorAnalogico1 = analogRead(sensor1);
    valorAnalogico2 = analogRead(sensor2);

    if (valorAnalogico2 <= 800 && maior) {
      maior = !maior;
    } else if (valorAnalogico2 > 800 && !maior) {
      conta++;
      maior = !maior;
      String st = "Contagem " + String(conta);
      Serial.println(st);
    }

    String s = String(valorAnalogico1) + ", " + String(valorAnalogico2);
    Serial.println(s);
    instanteAnteriorDeDeteccao = millis();
  }
}
