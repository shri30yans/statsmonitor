# Hardware Stats Monitor with Arduino
A Arduino powered OLED display which display's the Hardware stats of a computer running a Python program

### How it works?
The python program running on our computer collects and sends the Arduino, hardware statistics through Serial communication. The Python program running on our computer countinously send's data to the Arduino which then display's the information on the OLED Screen.

###Images
![Top View](https://github.com/shri30yans/statsmonitor/blob/main/statsmonitortop.png)   
*Top View*
     
![Side View](https://github.com/shri30yans/statsmonitor/blob/main/statsmonitorside.png)   
*Side View*  

### Parts needed
* An Arduino (Here, I used an Arduino nano)
* An  I2C 128 x 64 (Any OLED display can be used with a few modifications)

### Setup
* Python Libraries required:
    * psutil
    * GPUtil
    * cpuinfo
    * pyserial

* Arduino Libraries required:
    * SPI
    * Wire
    * Adafruit_GFX
    * Adafruit_SSD1306
    * ArduinoJson

* Wire Setup
    Connections for Uno, Nano
    * Vin >	5V
    * GND >	GND
    * SDA >  A4; 
    * SCL > A5
