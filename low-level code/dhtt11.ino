#include <DHT.h>

#define DHTPIN 6      // Digital pin connected to DHT11
#define DHTTYPE DHT11 // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 test starting...");
  dht.begin();
}

void loop() {
  delay(2000); // DHT11 needs ~2 seconds between readings

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // Celsius

  // Check if reading failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);
}
