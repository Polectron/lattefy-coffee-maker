import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)
orders = []

def make_order(order):
    print("Calentando agua")
    print("Vertiendo {0} en el deposito".format(order))
    print("Colocando taza vacia")
    print("Vertiendo infusion en la taza")

try:
	while True:
		if (GPIO.input(3) == 1): #Cafe
			GPIO.output(7,1)
			print("Boton pulsado")
			time.sleep(1.4)
            make_order(1)
        elif (GPIO.input(1))
		else:
			GPIO.output(7,0)
except KeyboardInterrupt:
	GPIO.cleanup()
