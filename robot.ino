#include <Servo.h>

Servo sA, sB, sC, sD;

int A = 0, B = 105, C = 0, D = 150;
// Inicio: 0,105,0,180

void setup() {
  Serial.begin(9600);
  sA.attach(3);
  sB.attach(5);
  sC.attach(6);
  sD.attach(9);
  sA.write(A);
  sB.write(B);
  sC.write(C);
  sD.write(D);
}

void loop() {
  if (Serial.available()) {
    A = Serial.parseInt();
    B = Serial.parseInt();
    C = Serial.parseInt();
    D = Serial.parseInt();

    if (Serial.read() == '\n') {
        Serial.print(A, DEC);
        Serial.print(",");
        Serial.print(B, DEC);
        Serial.print(",");
        Serial.print(C, DEC);
        Serial.print(",");
        Serial.println(D, DEC);
        sA.write(A);
        sB.write(B);
        sC.write(C);
        sD.write(D);
    }
  }
  delay(20);
}

