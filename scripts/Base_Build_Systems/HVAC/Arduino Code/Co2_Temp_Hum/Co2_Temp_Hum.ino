/*
  DHT11 Temp / Humidity sensor module test

  Basic code for exercising the module.
  Requires DHT library to be installed
*/
#include "dht.h"          // Include the DHT library
dht DHT;                  // Create instance of DHT object

#include "MQ135.h"      // Include the MQ135 library
#define ANALOGPIN A0    //  Define Analog PIN on Arduino Board
#define RZERO 206.85    //  Define RZERO Calibration Value

MQ135 gasSensor = MQ135(ANALOGPIN);
String calText = "MQ135 RZERO Calibration Value : " ;
String ppmtext = "CO2 ppm value : " ;

int const DHT11_PIN = 3;  // Connects to sensor I/O, use any digital pin
int sensor;               // Dummy variable for sensor read

int x; // Python submited request

//===============================================================================
//  Initialization
//===============================================================================
void setup() {
  Serial.begin(9600);
  float rzero = gasSensor.getRZero();
//  delay(3000);
//  Serial.println(calText + rzero);

}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  
  // Co2_sensor values
  if (x == 1) {
    float ppm = gasSensor.getPPM();
    digitalWrite(13,HIGH);
    Serial.println(ppmtext + ppm);
  }

  // Temp values
  else if (x == 2) {
    sensor = DHT.read11(DHT11_PIN);  // Read sensor
    Serial.print("Temperature : ");  // Printout returned results
    Serial.print(DHT.temperature);
    Serial.println(" C\t");
  }

  // Humidity values
  else if (x == 3) {
    sensor = DHT.read11(DHT11_PIN);  // Read sensor
    Serial.print("Humidity : ");
    Serial.print(DHT.humidity);
    Serial.println(" %");
  }

}
