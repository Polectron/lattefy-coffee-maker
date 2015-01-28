from pushbullet import PushBullet
import RPi.GPIO as GPIO
import time
import threading
import smbus
from collections import deque

btn1 = 7
btn2 = 11
buzzer = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(btn1, GPIO.IN)
GPIO.setup(btn2, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)


class lattefy():
    def __init__(self):
        #Pushbullet API data
        self.token = "w33vXv9uztYSjBDXWAH0MPrwMigEifeQ"
        self.pb = PushBullet(self.token)
        self.pb.contacts
    
        #Coffee orders array
        self.orders = deque([])
        
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
            if True:
                if len(self.orders) > 0:
                    try:
                        self.SPI_bus.write_byte(self.SPI_address, self.orders[0]) #Send order number to Arduino
                    except:
                        pass
                    self.makeOrder(self.orders[0])
                    self.orders.popleft()
                    time.sleep(5)
                    self.SPI_bus.write_byte(self.SPI_address, 3) #Ask Arduino to buzz
                    time.sleep(1)
                #else:
                    #self.SPI_bus.write_byte(self.SPI_address, 0) #Send blank
                    #time.sleep(1.5)
            else:
                print("No hay tazas libres")

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
    
    def buzz(self):        
        p = GPIO.PWM(buzzer, 3000)
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
            if GPIO.input(btn1) == 1:
                self.orders.append(1)
                time.sleep(0.4)
            elif GPIO.input(btn2) == 1:
                self.orders.append(2)
                time.sleep(0.4)
                
    def makeOrder(self,order):
        time.sleep(1)
        if order == 1:
            print("Café")
            print("Liberar café en el filtro")
            self.SPI_bus.write_byte(self.SPI_address, 4) #Servo 0 
            time.sleep(1)
            print("Calentar agua")
            print("Abrir filtro")
            print("Comprobar nivel de la taza")
            time.sleep(1)
            self.SPI_bus.write_byte(self.SPI_address, 5) #Servo 170
            time.sleep(1)
        elif order == 2:
            print("Té")
    
latte = lattefy()
