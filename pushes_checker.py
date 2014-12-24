from pushbullet import PushBullet
import RPi.GPIO as GPIO
import time
import threading
import smbus
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
class lattefy():
    def __init__(self):
        #Pushbullet API data
        self.token = "w33vXv9uztYSjBDXWAH0MPrwMigEifeQ"
        self.pb = PushBullet(self.token)
        self.pb.contacts
    
        #Coffee orders array
        self.orders = []
        
        #Setting up SPI connection
        self.bus = smbus.SMBus(1)
        self.address = 0x04
        
        #Threading Pushbullet checks
        self.hilo=threading.Thread(target=self.pbCycle)
        self.hilo.start()
        
        #Threading buttons checks
        self.hilo2=threading.Thread(target=self.btnCycle)
        self.hilo2.start()
    
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
                    self.orders.append(order_result)
                    if order_result > 0:
                        if order_result == 1:
                            print("Preparando café con leche")
                        elif order_result == 2:
                            print("Preparando café solo")
                        self.get_sender(sender_iden,sender_name,sender_email).push_note("¡Orden terminada!","Ya puedes recoger tu {0}".format(re_body))
                        time.sleep(2)
                    else:
                        self.get_sender(sender_iden,sender_name,sender_email).push_note("Error","Servicio no reconocido, prueba a pedir un 'café con leche' o un 'café solo'")
                    success_now, pushes_now = self.pb.get_pushes()
                    self.pb.dismiss_push(pushes_now[0]["iden"])
                    self.pb.dismiss_push(push["iden"])
            time.sleep(1)
    
    def btnCycle(self):
        while True:
            if (GPIO.input(11) == 1):
                GPIO.output(7,1)
                print("Botón pulsado")
                time.sleep(1.4)
                p = GPIO.PWM(12, 3000)  # channel=12 frequency=3000Hz
                p.start(0)
                p.ChangeFrequency(900)
                p.ChangeDutyCycle(70)
                time.sleep(0.1)
                p.stop()
                time.sleep(0.1)
                p.start(0)
                p.ChangeFrequency(900)
                p.ChangeDutyCycle(70)
                time.sleep(0.1)
                p.stop()
            else:
                GPIO.output(7,0)
    
latte = lattefy()
