/* Commands sent over Serial:
 * 0 (RAWCM) - Sends the raw data over serial in centimeters
 * 1 (RAWIN) - Sends the raw data over serial in inches
 * 2 (ALARM) - Sound the alarm for 5s, for debugging
 * 3 (LIGHT) - Blink all the LEDs at 2Hz for 5s, for debugging
 * 4 (PAUSE) - Acknowledge high water level and pause alarm
 * 5 (SLEEP) - Sleep the device, stop the sensors and output
 */
 
#include <avr/sleep.h>

// Constants
#define trigPin 12
#define echoPin 13
#define vccPin 11
#define greenPin 2
#define redPin 4
#define buzzPin A2
#define greenPinGND 3
#define redPinGND 5
#define buzzPinGND A0
int duration, final_cm, final_inches;
double cm;
String command; 
bool mode = false;

void setup() {
  Serial.begin (9600);
  Serial.setTimeout(-1);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(vccPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(buzzPin, OUTPUT);
  pinMode(greenPinGND, OUTPUT);
  pinMode(redPinGND, OUTPUT);
  pinMode(buzzPinGND, OUTPUT);
  digitalWrite(vccPin, HIGH);
  digitalWrite(greenPinGND, LOW);
  digitalWrite(redPinGND, LOW);
  digitalWrite(buzzPinGND, LOW);
}
 
void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);
  cm = pow(((pow(duration, 2.0))/(3460.2041) - 1.69), 0.5);

  if (cm > 9) {
    ;
  } else if (cm > 6.5) {
    final_cm = 0;
  } else if (cm > 4.5) {
    final_cm = 1;
  } else if (cm > 3.6) {
    final_cm = 2;
  } else if (cm > 3.1) {
    final_cm = 3;
  } else if (cm > 2.2) {
    final_cm = 4;
  } else if (cm > 1.1) {
    final_cm = 5;
  } else {
    final_cm = 6;
  }

  final_inches = 2.65748 - (duration / 2.0) / 74;

  if (final_cm < 4) {
    digitalWrite(greenPin, HIGH);
    digitalWrite(redPin, LOW);
    digitalWrite(buzzPin, LOW);
  } else if (final_cm >= 4 && mode == false) {
    digitalWrite(greenPin, LOW);
    digitalWrite(redPin, HIGH);
    digitalWrite(buzzPin, HIGH);
  } else if (final_cm >= 4 && mode == true) {
    digitalWrite(greenPin, LOW);
    digitalWrite(redPin, HIGH);
    digitalWrite(buzzPin, LOW);
  }

  if (Serial.available() > 0) {
    command = Serial.readStringUntil('*');
    if (command == "0") {
      Serial.print(final_cm);
      Serial.print("/");
    } else if (command == "1") {
      Serial.print(final_inches);
      Serial.print("/");
    } else if (command == "2") {
      digitalWrite(buzzPin, HIGH);
      delay(5000);
      Serial.print("2/");
    } else if (command == "3") {     
      digitalWrite(redPin, HIGH);
      delay(500);
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      delay(500);
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      delay(500);
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      delay(500);
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      delay(500);
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      delay(500);
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      delay(500);
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      delay(500);
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      delay(500);
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      delay(500);
      Serial.print("3/");
    } else if (command == "4") {      
      mode = true;
      Serial.print("4/");
    } else if (command == "5") {      
      set_sleep_mode(SLEEP_MODE_PWR_DOWN);
      digitalWrite(greenPinGND, LOW);
      digitalWrite(redPinGND, LOW);
      digitalWrite(buzzPinGND, LOW);
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, LOW);
      digitalWrite(buzzPin, LOW);
      Serial.print("5/");
      delay(100);
      sleep_mode();
    }
  }
  
  delay(250);
}