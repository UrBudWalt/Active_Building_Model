/*
  DHT11 Temp / Humidity sensor module test

  Basic code for exercising the module.
  Requires DHT library to be installed
*/
#include "dht.h"          // Include the DHT library
dht DHT;                  // Create instance of DHT object

int const DHT11_PIN = 3;  // Connects to sensor I/O, use any digital pin
int sensor;               // Dummy variable for sensor read
//===============================================================================
//  Initialization
//===============================================================================
void setup()
{
  Serial.begin(9600);     // Initialize serial comm
}
//===============================================================================
//  Main
//===============================================================================
void loop()
{
  sensor = DHT.read11(DHT11_PIN);  // Read sensor
  Serial.print("Temperature = ");  // Printout returned results
  Serial.print(DHT.temperature);
  Serial.print(" C\t");
  Serial.print("Humidity = ");
  Serial.print(DHT.humidity);
  Serial.println(" %");
  delay(2000);  // 1 sec min read time, so using 2 to be safe
}
