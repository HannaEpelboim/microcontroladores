// COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO 01
// DEPOIS FAÇA OS NOVOS RECURSOS

#include <AFMotor.h>
// ESTE É O ARQUIVO DO ARDUINO COM OS MOTORES E OS SENSORES ÓTICOS.
// NÃO TEM BOTÃO, NEM LED E NEM DISPLAY AQUI.

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
int sensor1 = A11;
int sensor2 = A12;
int valorDig1, valorDig2;
bool automatic = false;
unsigned long instanteAnteriorDeDeteccao = 0;

void setup() {
  motor3.setSpeed(160);
  motor4.setSpeed(160);
  
  Serial.begin(9600);
  Serial.setTimeout(10);

  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  Serial1.begin(9600);
  Serial1.setTimeout(10);
}

void loop() {
  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if (texto.startsWith("frente")) {
      frente();
    } else if (texto.startsWith("tras")) {
      tras();
    } else if (texto.startsWith("esquerda")) {
      esquerda();
    } else if (texto.startsWith("direita")) {
      direita();
    } else if (texto.startsWith("parar")) {
      parar();
    }else if(texto.startsWith("auto")){
      automatic = true;
    }
  }

  if (millis() > instanteAnteriorDeDeteccao + 100) {
    valorDig1 = digitalRead(sensor1);
    valorDig2 = digitalRead(sensor2);
    String txt = String(valorDig1) + ", " + String(valorDig2);
    Serial1.println(txt);
  }

  if(automatic){
    if(valorDig1 && valorDig2){
      tras();
    }
    else if(!valorDig1 && !valorDig2){
      frente();
    }
    else if(valorDig1 && !valorDig2){
      esquerda();
    }
    else if(!valorDig1 && valorDig2){
      direita();
    }
  }
} 


void frente() {
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void tras() {
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void esquerda() {
  motor3.run(BACKWARD);
  motor4.run(FORWARD);

}

void direita() {
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void parar() {
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  automatic = false;
}
