#include "BluetoothSerial.h"

BluetoothSerial SerialBT;  // Bluetooth Serial object

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT_Login"); // Bluetooth device name
  Serial.println("✅ Bluetooth device ready. Pair and send data.");
}

void loop() {
  if (SerialBT.available()) {
    String input = SerialBT.readStringUntil('\n'); // Read until newline
    input.trim();

    int comma = input.indexOf(',');
    if (comma > 0) {
      String user = input.substring(0, comma);
      String pass = input.substring(comma + 1);

      Serial.println("Received:");
      Serial.println("User: " + user);
      Serial.println("Pass: " + pass);

      // ✅ Check credentials
      if (user == "admin" && pass == "1234") {
        SerialBT.println("✅ Login success!");
      } else {
        SerialBT.println("❌ Invalid credentials");
      }
    } else {
      SerialBT.println("⚠️ Format: username,password");
    }
  }
}
