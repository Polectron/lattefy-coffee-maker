import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
try:
    while True:
        if (GPIO.input(11) == 1 or GPIO.input(7) == 1):
            print("Boton pulsado")
            time.sleep(0.4)
except KeyboardInterrupt:
    GPIO.cleanup()
