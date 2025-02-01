#include <DHT11.h>

// Define pins
const int temp_humidity_pin = 8;
const int moist_pin = A2;
const int light_pin = A3;
const int fire_pin = 3;
const int gas_sensor = 5;
const int fan_pin = 6;
const int pump_pin = 10;
const int intrusion_pin = 4;

//value vars

int temperature = 0;
int humidity = 0;
int result;

// Create DHT11 object
DHT11 dht11(temp_humidity_pin);

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(100);
  pinMode(fire_pin, INPUT);
  pinMode(gas_sensor, INPUT);
  pinMode(intrusion_pin, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int input = Serial.readString().toInt();
    processInput(input);
  }
}

void processInput(int input) {

  if(input == 1){
    // Attempt to read the temperature and humidity values from the DHT11 sensor.
      //result = dht11.readTemperatureHumidity(temperature, humidity);
      temperature = dht11.readTemperature();
      delay(500);
      Serial.println(temperature);
  }
  else if(input == 2){
    // Attempt to read the temperature and humidity values from the DHT11 sensor.
      humidity = dht11.readHumidity();
      Serial.println(humidity);
  }
  else if(input == 3){
    Serial.println(analogRead(moist_pin));
  }
  else if(input == 4){
    Serial.println(analogRead(light_pin));
  }
  else if(input == 5){
    Serial.println(digitalRead(fire_pin));
  }
  else if(input == 6){
    Serial.println(digitalRead(intrusion_pin));
  }
  else if(input == 7){
    Serial.println(digitalRead(gas_sensor));
  }
  else{
    Serial.println("error");
  }
  delay(1000);
}
