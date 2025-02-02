#include <Adafruit_Sensor.h>
#include <DHT.h>

// Define pins
#define DHTPIN 7     // Pin connected to DHT sensor
#define DHTTYPE DHT11
#define BAUDRATE 115200
const int moist_pin = A0;
const int light_pin = A1;
const int fire_pin = 4;
const int gas_sensor = 12;
//const int fan_pin = 7; // Not used in the provided code, but defined
const int intrusion_pin = 12;
const int led_pin = 6;
const int pump_pin = 8;
const int cooler_fan = 9;
const int heater_fan = 10;
const int cooler = 11;

//value vars

int temperature = 0;
int humidity = 0;
// Removed 'result' as it's not used correctly.  DHT11 library usage is simplified.

// Create DHT11 object
DHT dht(DHTPIN, DHT11);

void setup() {
  Serial.begin(BAUDRATE);
  dht.begin();
  //Serial.setTimeout(100); // Commented out, generally not needed
  pinMode(fire_pin, INPUT);
  pinMode(gas_sensor, INPUT);
  pinMode(intrusion_pin, INPUT);
  pinMode(moist_pin, INPUT); // Added pinMode for moisture sensor
  pinMode(light_pin, INPUT); // Added pinMode for light sensor
  pinMode(led_pin, OUTPUT);
  pinMode(pump_pin, OUTPUT);
  pinMode(cooler_fan, OUTPUT);
  pinMode(heater_fan, OUTPUT);
  pinMode(cooler, OUTPUT);
  digitalWrite(pump_pin, 1);
  digitalWrite(cooler_fan, 1);
  digitalWrite(heater_fan, 1);
  digitalWrite(cooler, 1);



}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readString(); // Read until newline
    int input = inputString.toInt(); // Convert to integer

    processInput(input);
  }
}

void processInput(int input) {

  switch (input) {  // Using a switch statement for clarity and efficiency
    case 1:
      temperature = dht.readTemperature();
      Serial.println(temperature);
      break;
    case 2:
      humidity = dht.readHumidity();
      Serial.println(humidity);
      break;

    case 3:
      Serial.println(analogRead(moist_pin));
      break;

    case 4:
      Serial.println(analogRead(light_pin));
      break;

    case 5:
      Serial.println(digitalRead(fire_pin));
      break;

    case 6:
      Serial.println(digitalRead(intrusion_pin));
      break;

    case 7:
      Serial.println(digitalRead(gas_sensor));
      break;
    
    case 8: //turn on pump
      Serial.println(1);
      digitalWrite(pump_pin, LOW);
      break;

    case 9: //turn off pump
      Serial.println(0);
      digitalWrite(pump_pin, HIGH);
      //digitalWrite(xyz_pin, xyz_s);
      break;
    
    case 10: //turn on fan, cooler
      Serial.println(1);
      digitalWrite(cooler_fan, LOW);
      break;

    case 11: //turn off fan, cooler
      Serial.println(0);
      digitalWrite(cooler_fan, HIGH);
      break;
    
    case 12: //turn on cooler
      digitalWrite(cooler, LOW);
      Serial.println(1);
      
      break;
    
    case 13: //turn off cooler
      Serial.println(0);
      digitalWrite(cooler, HIGH);
      break;

    case 14: //heater fan turned on
      Serial.println(1);
      digitalWrite(heater_fan, LOW);
      break;

    case 15: //heater fan turned off
      Serial.println(0);
      digitalWrite(heater_fan, HIGH);
      break;

    case 16:
      Serial.println(1);
      while (Serial.available() == 0) {
      }

      if (Serial.available() > 0) {
        String inputString = Serial.readStringUntil('\n');
        inputString.trim();

        if (inputString.length() > 0) {
          if (inputString.charAt(0) == '-' || (inputString.charAt(0) >= '0' && inputString.charAt(0) <= '9')) {
            int pwm_value = inputString.toInt();

            if (pwm_value >= 0 && pwm_value <= 255) {
              Serial.println(pwm_value);
              analogWrite(led_pin, pwm_value);
            } else {
              Serial.println(256);
            }
          } else {
            Serial.println(257);
          }
        }
      }else{
        analogWrite(led_pin, 0);
      }
      break;


    default:
      Serial.println("Invalid input");
  }
  delay(1000);
}