#include "DHT.h"

#define DHTPIN 6
#define DHTTYPE DHT22   // Using DHT22 as per filename
#define LDR_PIN 4

#define R_LED 9
#define G_LED 8
#define B_LED 10

DHT dht(DHTPIN, DHTTYPE);

float temp;
float humidity;

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  pinMode(LDR_PIN, INPUT);
  pinMode(R_LED, OUTPUT);
  pinMode(G_LED, OUTPUT);
  pinMode(B_LED, OUTPUT);

  // Set a default LED state (e.g., off)
  digitalWrite(R_LED, HIGH);
  digitalWrite(G_LED, HIGH);
  digitalWrite(B_LED, HIGH);
}

void setColor(bool r, bool g, bool b) {
  digitalWrite(R_LED, !r); // Assuming common anode LEDs, LOW is ON
  digitalWrite(G_LED, !g);
  digitalWrite(B_LED, !b);
}

void RGB_LED_reaction(float current_temp, int light_value) {
    if (current_temp > 30 && light_value > 2000) {
        // Hot and bright -> Red/Orange colors
        setColor(true, false, false); // Red
    } else if (current_temp < 30 && light_value <= 2000) {
        // Cool and dim -> Green/Cyan colors
        setColor(false, true, false); // Green
    } else {
        // Other conditions -> Blue
        setColor(false, false, true); // Blue
    }
}

void loop() {
  // Wait for a request from the Python script
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'R') {
      // 1. Read sensor values
      temp = dht.readTemperature();
      humidity = dht.readHumidity();
      int lightValue = analogRead(LDR_PIN);

      // 2. Perform local actions (like controlling the LED)
      RGB_LED_reaction(temp, lightValue);

      // 3. Send data back to Python script
      if (isnan(temp) || isnan(humidity)) {
        // Do not send anything if readings are invalid
        return;
      } else {
        Serial.print(temp);
        Serial.print(",");
        Serial.println(humidity);
      }
    }
  }
  // The Arduino will now just wait for commands,
  // but you could add a small delay here if needed
  // to prevent overly rapid looping, though it's not strictly necessary.
  delay(100); 
}
