#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>
#define SERIAL_RX_BUFFER_SIZE 256
#define OLED_RESET -1

Adafruit_SSD1306 display(-1);
 
unsigned long currentMillis;//current millis()
unsigned long messageMillis;// last time we did no data message
unsigned long goodDataInterval = 10000;// how long we wait before complaining
unsigned long messageInterval= 10000;   // how long we wait before message
unsigned long lastGoodDataMillis;// last time we got data

void setup() {
  Serial.begin(115200);
    // initialize with the I2C addr 0x3C
   display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  

   // Clear the buffer.
   display.clearDisplay();
}

void loop() {

  currentMillis = millis();

  if (Serial.available()) {
    while (Serial.available() > 0) {

      String x = Serial.readStringUntil("\0");
      Serial.print("I received: ");
      Serial.println(x);
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, x);
      // we have received and processed a string of data
      // reset the timer for how long ago we got good data
       lastGoodDataMillis = millis();

      if (error) {
        Serial.println(F("deserializeJson() failed: "));
        Serial.print(error.f_str());
        return;
      }
      else
      {
        //desirialisation of recieved json
          const char* CPU_name = doc["CPU_name"];
          const char* CPU_load = doc["CPU_load"];
          const char* RAM_percentage = doc["RAM_percentage"];
          const char* GPU_name = doc["GPU_name"];
          const char* GPU_load = doc["GPU_load"];
          const char* GPU_temp = doc["GPU_temp"];
          
          display.clearDisplay();
            display.setTextSize(1);
          display.setTextColor(WHITE);
          //CPU
          display.setCursor(0,0); 
          display.println(CPU_name);

          display.setCursor(82,0); 
          display.println(CPU_load);

           //GPU
          display.setCursor(0,10); 
          display.println(GPU_name);

          display.setCursor(82,10);
          display.println(GPU_load);

          //RAM
          display.setCursor(0,20); 
          display.println("RAM"); 

          display.setCursor(82,20);
          display.println(RAM_percentage);


          
          display.display();

      }
    }
  }

  if (millis() - lastGoodDataMillis > goodDataInterval && currentMillis - messageMillis > messageInterval ) {
        display.setTextSize(1);
        display.setTextColor(WHITE);
        display.setCursor(0,0); 
        display.clearDisplay();
        display.println("No Stats. Is your Python program running?");
        display.display();
        messageMillis = millis();
          
  }
}