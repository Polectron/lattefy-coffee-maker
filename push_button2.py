import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)
try:
    while True:
        if (GPIO.input(11) == 1):
            GPIO.output(7,1)
            print("Boton pulsado")
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
except KeyboardInterrupt:
    GPIO.cleanup()
