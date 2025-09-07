#define DHTPIN 6
#define DHTTYPE DHT11
#define LDR_PIN 4

#define R_LED 9
#define G_LED 8
#define B_LED 10

#include "DHT.h"
DHT hung_and_hung_anh_dht(DHTPIN, DHTTYPE);

//set global variables

float temp;
float humidity;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  hung_and_hung_anh_dht.begin();
  pinMode(R_LED, OUTPUT);
  pinMode(G_LED, OUTPUT);
  pinMode(B_LED, OUTPUT);
  pinMode(4, INPUT);

  digitalWrite(9,HIGH);
  digitalWrite(8,HIGH);
  digitalWrite(10,HIGH);
  
  
}

int ReadandPrintDHT() {
  temp = hung_and_hung_anh_dht.readTemperature(); // doc nhiet do
  humidity= hung_and_hung_anh_dht.readHumidity();   // doc do am 
  if (isnan(temp)|| isnan(humidity)) {
    Serial.print("Lỗi kết quả thu được là nan rồi con chó ngu!!!");
    return 0;
  }
  else {
    Serial.print("\nTemp: ");
    Serial.print(temp);
    Serial.print(" °C | Humid: ");
    Serial.print(humidity);
    return 1;

  }

}

int readLightvalue() {
  float Lightvalue = analogRead(4);
  Serial.println("\nGiá trị ánh sáng thu được là : ");
  Serial.print(Lightvalue);
  return Lightvalue;

}
void RGB_LED_reaction(float temp1, int Light) {
    if (temp1>30 && Light>2000) {
    Serial.println("\n Mau thu duoc la mau do va Cam");
    setColor(0,1,1);
    delay(500);
    setColor(0,0,1);

      }
    else if (temp1 < 30 && Light <=2000) {

    Serial.println("\nMau thu duoc la xanh la cay va cyan");
    setColor(1,0,1);
    setColor(1,0,0);


      }
   else {
    Serial.println("\n Mau nay la mau gi tao deo biet ngoai blue hehhehehe");
    setColor(1,1,0);
    setColor(0,1,0);
      }

  }
void setColor( bool a, bool b, bool c) {      // từ đoạn code này bạn hoàn toàn có thể code điều kiện khi phản ứng và đặt giá trị a b c tương ứng cho từng trường hợp 
// cái này thì tổng quát hơn nhiều so với cái LED_reaction bên trên
  digitalWrite(R_LED, a);
  digitalWrite(G_LED, b);
  digitalWrite(B_LED, c);

}

void loop() {
  // put your main code here, to run repeatedly:
  int success = ReadandPrintDHT();
  if (!success) {
    setColor(1,1,1);
    Serial.println(" Bỏ qua toàn bộ loop này vì lỗi dữ liệu ");
    return;   // get out of the whole loop
  }

  delay(1000);
  int Lightvalue_in_loop = readLightvalue();
  delay(1000);
  RGB_LED_reaction(temp, Lightvalue_in_loop);

  delay(2000);

}