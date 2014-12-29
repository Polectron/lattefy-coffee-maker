#include <Wire.h>
#include <LiquidCrystal.h>
#include "pitches.h"

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
    
    lcd.print("Esperando orden");
    
}

void loop() {
    delay(100);
    if (number ==  3){
        lcd.print("Finalizado");
        buzz();
        number = 0;
        lcd.clear();
        lcd.print("Esperando orden");
    }
}

// callback for received data
void receiveData(int byteCount){
    while(Wire.available()) {
        number = Wire.read();
        lcd.setCursor(0, 0);
        lcd.clear();
        if (number == 1){
            lcd.print("Haciendo 1");
        }else if (number == 2){
            lcd.print("Haciendo 2");
        }
     }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

void buzz(){
    // notes in the melody:
    int melody[] = {
        NOTE_D3, NOTE_D4, NOTE_D5};

// note durations: 4 = quarter note, 8 = eighth note, etc.:
    int noteDurations[] = {
        8, 8, 8};
        
    for (int thisNote = 0; thisNote < 8; thisNote++) {
        // to calculate the note duration, take one second 
        // divided by the note type.
        //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
        int noteDuration = 1000/noteDurations[thisNote];
        tone(8, melody[thisNote],noteDuration);
    
        // to distinguish the notes, set a minimum time between them.
        // the note's duration + 30% seems to work well:
        int pauseBetweenNotes = noteDuration * 1.30;
        delay(pauseBetweenNotes);
        // stop the tone playing:
        noTone(8);
    }
}
