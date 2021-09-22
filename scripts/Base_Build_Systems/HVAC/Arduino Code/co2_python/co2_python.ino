#include "MQ135.h"
#define ANALOGPIN A0    //  Define Analog PIN on Arduino Board
#define RZERO 206.85    //  Define RZERO Calibration Value
MQ135 gasSensor = MQ135(ANALOGPIN);
String calText = "MQ135 RZERO Calibration Value : " ;
String ppmtext = "CO2 ppm value : " ;

void setup(){
  Serial.begin(9600);
  float rzero = gasSensor.getRZero();
  delay(3000);
  Serial.println(calText + rzero);
}

void loop() {
  float ppm = gasSensor.getPPM();
  delay(1000);
  digitalWrite(13,HIGH);
  Serial.println(ppmtext + ppm);
}
