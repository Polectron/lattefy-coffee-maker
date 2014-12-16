import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

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
GPIO.cleanup
