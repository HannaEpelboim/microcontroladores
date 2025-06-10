#include <GFButton.h>
#include <ShiftDisplay.h>

String listaComandos[] = {"frente", "tras", "esquerda", "direita"};
int comandoAtual = 0;
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

// NÃO COPIE O IMPLEMENTAÇÃO 1 PARA CÁ NÃO!
// ESSE É UM CÓDIGO SEPARADO DA PRIMEIRA PARTE!

// ESTE É O ARQUIVO DO ARDUINO SÓ COM O SHIELD MULTIFUNÇÃO.
// NÃO TEM MOTOR E SENSOR ÓTICO.

GFButton botao1(A1);
GFButton botao2(A2);
int led1 = 13;
int led2 = 12;

void setup() {
  botao1.setPressHandler(mensagemDir);
  botao2.setPressHandler(mostraDir);
  botao2.setReleaseHandler(paraDeMostrarDir);
  display.set(listaComandos[comandoAtual]);
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(9600);
  Serial1.setTimeout(10);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
} 

void loop() {
  botao1.process();
  botao2.process();
  display.update();

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if(texto.substring(0, 1).toInt() == 1) {
      digitalWrite(led1, HIGH); 
    } 
    else if(texto.substring(0, 1).toInt() == 0) {
      digitalWrite(led1, LOW); 
    }
    if(texto.substring(3).toInt() == 1) {
      digitalWrite(led2, HIGH); 
    }
    else if(texto.substring(3).toInt() == 0) {
      digitalWrite(led2, LOW); 
    }
  }
}

void mensagemDir() {
  comandoAtual = (comandoAtual + 1) % 4;
  display.set(listaComandos[comandoAtual]);

}

void mostraDir() {
  Serial1.println(listaComandos[comandoAtual]);
}

void paraDeMostrarDir() {
  Serial1.println("parar");
}