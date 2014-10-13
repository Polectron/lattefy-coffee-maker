from pushbullet import PushBullet
import time
class lattefy():
    def __init__(self):
        self.token = "w33vXv9uztYSjBDXWAH0MPrwMigEifeQ"
        self.pb = PushBullet(self.token)
        self.pb.contacts
        self.cycle()
    
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
 
    def cycle(self):
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
                    else:
                        self.get_sender(sender_iden,sender_name,sender_email).push_note("Error","Servicio no reconocido, prueba a pedir un 'café con leche' o un 'café solo'")
                    success_now, pushes_now = self.pb.get_pushes()
                    self.pb.dismiss_push(pushes_now[0]["iden"])
                    self.pb.dismiss_push(push["iden"])
            time.sleep(1)
latte = lattefy()
