
#include "BluetoothSerial.h"
#include <stdio.h>
#include <M5StickC.h>
#include "3D_vector.c"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


//::::::::: VARIABLES :::::::::::::
// serial
BluetoothSerial SerialBT;





static D_vect gyrom={-2.305,2450.0,0.0};
static D_vect accel={0.0,0.0,0.0};


float temp = 0.0F;

void setup() {
  // :: INIT M5 Stick C
  M5.begin();
    // -- LCD
  M5.Lcd.setRotation(3); // mise de l'ecran en paysage
  M5.Lcd.fillScreen(BLUE);
  M5.Lcd.setTextSize(1);
  M5.Lcd.setCursor(40, 0);
  M5.Lcd.println("Mesure Gyroscope");
  M5.Lcd.setCursor(0, 15);
  M5.Lcd.println("  X       Y       Z");



  // ::  INIT gyroscope IMU
  M5.IMU.Init();

  // ::  INIT BLT
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
}


void loop() {
  M5.IMU.getGyroData(&gyrom.X, &gyrom.Y, &gyrom.Z);
  M5.IMU.getAccelData(&accel.X, &accel.Y, &accel.Z);
  M5.IMU.getTempData(&temp);

  char s_Gyro[21];
  char s_Acce[21];
  char s_Temp[6];
  char str_data[64]="\0";





  M5.Lcd.setCursor(0, 30);
  M5.Lcd.printf("%6.2f  %6.2f  %6.2f      ", gyrom.X, gyrom.Y, gyrom.Z);
  M5.Lcd.setCursor(140, 30);
  M5.Lcd.print("o/s");
  M5.Lcd.setCursor(0, 45);
  M5.Lcd.printf(" %5.2f   %5.2f   %5.2f   ", accel.X, accel.Y, accel.Z);
  M5.Lcd.setCursor(140, 45);
  M5.Lcd.print("G");
  M5.Lcd.setCursor(0, 60);
  M5.Lcd.printf("Temperature : %.2f C", temp);
  delay(1000);

   strcat(str_data,D_vect_to_str(s_Gyro,gyrom,(char)','));
    strcat(str_data,",\0");

    strcat(str_data,D_vect_to_str(s_Acce,accel,(char)','));
    strcat(str_data,",\0");



    String data = "Hello\r\n";

  SerialBT.println(str_data);
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    Serial.write(SerialBT.read());
  }
  delay(5000);
}
