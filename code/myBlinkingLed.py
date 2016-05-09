#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

def Blink():
	while true:
		for i in range (0,3):
			time.sleep(.25)
			GPIO.output(17,True)
			time.sleep(.25)
			GPIO.output(17,False)
		time.sleep(5)
		for i in range (0,4):
			time.sleep(.25)
			GPIO.output(17,True)
			time.sleep(.25)
			GPIO.output(17,False)
		time.sleep(5)
	GPIO.cleanup()
Blink()