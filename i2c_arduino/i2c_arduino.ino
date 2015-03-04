#include <Wire.h>
#include <LiquidCrystal.h>
#include "pitches.h"
#include <Servo.h> 
 
Servo myservo;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

#define SLAVE_ADDRESS 0x04
int number = 0;

void setup() {
    myservo.attach(9);
    pinMode(7, OUTPUT);
    Serial.begin(9600);// start serial for output
    lcd.begin(16, 2);
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    myservo.write(120);
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("Esperando orden");
    
}

void loop() {
    delay(100);
    if (number == 1){
      lcd.setCursor(0, 0);
      lcd.clear();
      lcd.print("Haciendo cafe");
      digitalWrite(7, HIGH);
      myservo.write(80);
      //delay(75000);
      delay(50000);
      digitalWrite(7, LOW);
      delay(30000);
      lcd.setCursor(0, 0);
      lcd.clear();
      myservo.write(120);
      lcd.print("Cafe terminado");
      //buzz();
      tone(8, 5000,1000);
      //noTone(8);
      delay(500);
      lcd.setCursor(0, 0);
      lcd.clear();
      lcd.print("Esperando orden");
    }
    number = 0;
}

// callback for received data
void receiveData(int byteCount){
    while(Wire.available()) {
        number = Wire.read();
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
