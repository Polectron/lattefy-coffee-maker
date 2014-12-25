from pushbullet import PushBullet
import RPi.GPIO as GPIO
import time
import threading
import smbus

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class lattefy():
    def __init__(self):
        #Pushbullet API data
        self.token = "w33vXv9uztYSjBDXWAH0MPrwMigEifeQ"
        self.pb = PushBullet(self.token)
        self.pb.contacts
    
        #Coffee orders array
        self.orders = []
        
        #Setting up SPI connection
        self.SPI_bus = smbus.SMBus(1)
        self.SPI_address = 0x04
        
        #Threading Pushbullet checks
        self.hilo=threading.Thread(target=self.pbCycle)
        self.hilo.start()
        
        #Threading buttons checks
        self.hilo2=threading.Thread(target=self.btnCycle)
        self.hilo2.start()
        
        while True:
            for order in self.orders:
                self.SPI_bus.write_byte(self.SPI_address, order) #Send order number to Arduino
                if order == 1: #Option 1
                    print(order)
                elif order == 2: #Option 2
                    print(order)
    def get_sender(self,sender_iden,sender_name,sender_email):
        for contact in self.pb.contacts:
            if contact.email == sender_email:
                return contact
                break
        else:
            success, contact = self.pb.new_contact(sender_name,sender_email)
            return contact
    
    def get_body(self,push):
        try:
            body = push["body"]
            return body
        except:
            return ""
    
    def get_order(self,order):
        if order == "caféconleche":
            return 1
        elif order == "cafésolo":
            return 2
        else:
            return 0
    
    def buzz():        
        p = GPIO.PWM(12, 3000)
        p.start(0)
        p.ChangeFrequency(900) #900Hz
        p.ChangeDutyCycle(70)
        time.sleep(0.1)
        p.stop()
        time.sleep(0.1)
        p.start(0)
        p.ChangeFrequency(900)
        p.ChangeDutyCycle(70)
        time.sleep(0.1)
        p.stop()
 
    def pbCycle(self):
        while True:
            success, self.pushes = self.pb.get_pushes()
            #print(self.pushes)
            for push in self.pushes:
                if push["dismissed"] == False:
                    re_body = self.get_body(push)
                    body = re_body.lower()
                    body = body.split(" ")
                    body = "".join(body)
                    sender_iden = push["sender_iden"]
                    sender_name = push["sender_name"]
                    sender_email = push["sender_email"]
                    order_result = self.get_order(body)
                    if order_result > 0:
                        if order_result == 1:
                            print("Preparando café con leche")
                        elif order_result == 2:
                            print("Preparando café solo")
                        self.get_sender(sender_iden,sender_name,sender_email).push_note("¡Orden terminada!","Ya puedes recoger tu {0}".format(re_body))
                        time.sleep(2)
                        self.orders.append(order_result)
                    else:
                        self.get_sender(sender_iden,sender_name,sender_email).push_note("Error","Servicio no reconocido, prueba a pedir un 'café con leche' o un 'café solo'")
                    success_now, pushes_now = self.pb.get_pushes()
                    self.pb.dismiss_push(pushes_now[0]["iden"])
                    self.pb.dismiss_push(push["iden"])
            time.sleep(1)
    
    def btnCycle(self):
        while True:
            if GPIO.input(11) == 1:
                self.orders.append(1)
                time.sleep(1.4)
            elif GPIO.input(12) == 1:
                self.orders.append(2)
                time.sleep(1.4)
    
latte = lattefy()
