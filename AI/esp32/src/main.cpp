#include <Arduino.h>
#include <Wire.h>
#include <ModbusMaster.h>
 
// --- ขาของ Rain sensor ---
#define RAIN_ANALOG_PIN 35
#define RAIN_DIGITAL_PIN 25
 
// --- LDR & LED ---
#define LED_PIN 2
#define LDR_ANALOG_PIN 34
 
// --- SI7021 ---
#define SI7021_ADDR 0x40
 
// --- RS485 (MAX485) ---
#define MAX485_DE_RE 4
#define RS485_RX 16
#define RS485_TX 17
 
ModbusMaster node;
 
// --- ฟังก์ชันของ SI7021 ---
void resetSI7021() {
  Wire.beginTransmission(SI7021_ADDR);
  Wire.write(0xFE);
  Wire.endTransmission();
  delay(50);
}
 
float readHumidity() {
  Wire.beginTransmission(SI7021_ADDR);
  Wire.write(0xF5);
  Wire.endTransmission();
  delay(50);
  if (Wire.requestFrom(SI7021_ADDR, 3) == 3) {
    uint16_t humi = Wire.read() << 8 | Wire.read();
    Wire.read();
    return humi * 125.0 / 65536.0 - 6.0;
  }
  return -1;
}
 
float readTemperature() {
  Wire.beginTransmission(SI7021_ADDR);
  Wire.write(0xF3);
  Wire.endTransmission();
  delay(50);
  if (Wire.requestFrom(SI7021_ADDR, 3) == 3) {
    uint16_t temp = Wire.read() << 8 | Wire.read();
    Wire.read();
    return temp * 175.72 / 65536.0 - 46.85;
  }
  return -1;
}
 
// --- ควบคุม RS485 ---
void preTransmission() {
  digitalWrite(MAX485_DE_RE, HIGH);
  delayMicroseconds(100);
}
void postTransmission() {
  delayMicroseconds(100);
  digitalWrite(MAX485_DE_RE, LOW);
}
 
void setup() {
  Serial.begin(9600);
  Wire.begin();
 
  pinMode(LED_PIN, OUTPUT);
  pinMode(MAX485_DE_RE, OUTPUT);
  digitalWrite(MAX485_DE_RE, LOW);
 
  pinMode(RAIN_DIGITAL_PIN, INPUT);
 
  Serial2.begin(9600, SERIAL_8N1, RS485_RX, RS485_TX);
  node.begin(1, Serial2);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);
 
  resetSI7021();
  Serial.println("All sensors initialized.");
}
 
void loop() {
  // อ่าน LDR
  int valLDR = analogRead(LDR_ANALOG_PIN);
  digitalWrite(LED_PIN, valLDR < 2000 ? HIGH : LOW);
 
  // อ่าน Rain sensor
  int valRainAnalog = analogRead(RAIN_ANALOG_PIN);
  int rainState = digitalRead(RAIN_DIGITAL_PIN);
 
  // อ่าน SI7021
  float humidity = readHumidity();
  float temperature = readTemperature();
 
  // อ่าน Soil sensor ผ่าน Modbus
  uint8_t result = node.readHoldingRegisters(0x0000, 8);
  float soilTemp = -999, moisture = -999, ec = -999, ph = -999;
  float nitrogen = -999, phosphorus = -999, potassium = -999, salinity = -999;
 
  if (result == node.ku8MBSuccess) {
    soilTemp   = (int16_t)node.getResponseBuffer(0) / 10.0;
    moisture   = node.getResponseBuffer(1) / 10.0;
    ec         = node.getResponseBuffer(2);
    ph         = node.getResponseBuffer(3) / 100.0;
    nitrogen   = node.getResponseBuffer(4);
    phosphorus = node.getResponseBuffer(5);
    potassium  = node.getResponseBuffer(6);
    salinity   = node.getResponseBuffer(7);
  }
 
  // ส่งข้อมูล JSON ทาง Serial
  Serial.print("{");
  Serial.print("\"LDR\":"); Serial.print(valLDR);
  Serial.print(",\"RainAnalog\":"); Serial.print(valRainAnalog);
  Serial.print(",\"RainDigital\":"); Serial.print(rainState);
  Serial.print(",\"Humidity\":"); Serial.print(humidity);
  Serial.print(",\"Temperature\":"); Serial.print(temperature);
  Serial.print(",\"SoilTemp\":"); Serial.print(soilTemp);
  Serial.print(",\"Moisture\":"); Serial.print(moisture);
  Serial.print(",\"EC\":"); Serial.print(ec);
  Serial.print(",\"pH\":"); Serial.print(ph);
  Serial.print(",\"Nitrogen\":"); Serial.print(nitrogen);
  Serial.print(",\"Phosphorus\":"); Serial.print(phosphorus);
  Serial.print(",\"Potassium\":"); Serial.print(potassium);
  Serial.print(",\"Salinity\":"); Serial.print(salinity);
  Serial.println("}");
 
  delay(3000);
}