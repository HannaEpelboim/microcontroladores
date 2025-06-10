#include <meArm.h>
#include <EEPROM.h>
#include <GFButton.h>
#include <LinkedList.h>

struct Posicao {
 int x;
 int y;
 int z;
 bool garraAberta;
};

int base = 12, ombro = 11, cotovelo = 10, garra = 9;
meArm braco(
 180, 0, -pi/2, pi/2, // ângulos da base
 135, 45, pi/4, 3*pi/4, // ângulos do ombro
 180, 90, 0, -pi/2, // ângulos do cotovelo
 30, 0, pi/2, 0 // ângulos da garra
);

GFButton botaoB(3);
GFButton botaoA(2);
GFButton botaoC(4);
GFButton botaoD(5);
GFButton botaoE(6);
int count = 0;
int endereco = 0;
int pot = A5;
int y = A1;
int x = A0;
int ang = 90;
bool garra_aberta = false;
bool modo_absoluto = true;
int ultimo_x = 0;
int ultimo_y = 130;

LinkedList<Posicao> listaDeEstruturas;

void setup() {
  Serial.begin(9600);
  botaoA.setPressHandler(botaoApressed);
  botaoB.setPressHandler(botaoBpressed);
  botaoC.setPressHandler(botaoCpressed);
  botaoD.setPressHandler(botaoDpressed);
  botaoE.setPressHandler(botaoEpressed);
  pinMode(pot, INPUT);
  pinMode(x, INPUT);
  pinMode(y, INPUT);
  braco.begin(base, ombro, cotovelo, garra);
  braco.gotoPoint(0, 130, 0);
  braco.closeGripper();

  int total;

  EEPROM.get(endereco, total);

  Posicao var;
  for (int i = 0; i < total; i++) {
    EEPROM.get(endereco + 2 + sizeof(Posicao) * i, var);
    listaDeEstruturas.add(var);
  }
}

void botaoApressed() {
  if (garra_aberta) {
        braco.closeGripper();
  } else {
    braco.openGripper();
  }
  garra_aberta = !garra_aberta;
}

void botaoBpressed() {
  modo_absoluto = !modo_absoluto;

  if (!modo_absoluto) {
      Serial.println("Modo Relativo");
  } else {
    Serial.println("Modo Absoluto");
  }
  
}

void botaoCpressed(){
  Posicao novaPosicao;
  novaPosicao.x = braco.getX();
  novaPosicao.y = braco.getY();
  novaPosicao.z = braco.getZ();
  novaPosicao.garraAberta = garra_aberta; 
  listaDeEstruturas.add(novaPosicao);

  int total = listaDeEstruturas.size();

  EEPROM.put(endereco, total);
  EEPROM.put(endereco + 2 + sizeof(Posicao) * (total - 1), listaDeEstruturas.get(total - 1));

  Serial.println("Salvou!");
  
}

void botaoDpressed(){
  int total;
  EEPROM.get(endereco, total);

  listaDeEstruturas.clear();

  Posicao var;
  for (int i = 0; i < total; i++) {
      EEPROM.get(endereco + 2 + sizeof(Posicao) * i, var);
      listaDeEstruturas.add(var);
    }

  for(int i = 0; i<total; i++){
    braco.gotoPoint(listaDeEstruturas.get(i).x, listaDeEstruturas.get(i).y, listaDeEstruturas.get(i).z);
    if (!listaDeEstruturas.get(i).garraAberta) {
      braco.closeGripper();
    } else {
      braco.openGripper();
    }
    delay( 500);
  }
}

void botaoEpressed() {
  EEPROM.put(endereco, 0);
  listaDeEstruturas.clear();
}

void loop() {
  botaoE.process();
  botaoD.process();
  botaoC.process();
  botaoB.process();
  botaoA.process();
  int valor_pot = analogRead(pot);
  int valor_x = analogRead(x);
  int valor_y = analogRead(y);

  valor_x = map(valor_x, 0, 1023, -150, 150);
  valor_y = map(valor_y, 0, 1023, 100, 200);
  int valor_z = map(valor_pot, 0, 1023, -30, 100);
  

  if (modo_absoluto) {
    braco.gotoPoint(valor_x, valor_y, valor_z);
  } else {
    valor_x = map(valor_x, -150, 150, -10, 10);
    valor_y = map(valor_y, 100, 200, -10, 10);
    valor_x = max(-150, min(150, valor_x + ultimo_x + 1));
    valor_y = max(100, min(200, valor_y + ultimo_y + 1));
    braco.gotoPoint(valor_x, valor_y, valor_z);
    
  }

  ultimo_x = valor_x;
  ultimo_y = valor_y;
}


