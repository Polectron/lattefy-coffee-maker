#include <Wire.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

#define SLAVE_ADDRESS 0x04
int number = 0;

void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(9600);// start serial for output
    lcd.begin(16, 2);
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");
}

void loop() {
    delay(100);
}

// callback for received data
void receiveData(int byteCount){

    while(Wire.available()) {
        number = Wire.read();
        lcd.setCursor(0, 0);
        lcd.clear();

        if (number == 1){
            lcd.print("Haciendo opcion 1");
        }
        else if (number == 2){
            lcd.print("Haciendo opcion 2");
        }
     }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}


