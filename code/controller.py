#!/usr/bin/python
#If this file is called by the user through the terminal, it must follow the format:
#	moveSensor.py <direction> <time>
#direction might be 1 - move down or 2 - move up
#time is how long the sensor will be moving

import sys
import os
import datetime
import sqlite3
import RPi.GPIO as GPIO
import time

PORT_DOWN=23
PORT_UP=24
DELAY_DOWN=3 #time while the motor is going to be running
DELAY_UP=3
DELAY_TEMP=10 #time to wait the temperature to stablish after the sensor moves

#position = 0 -> surface
#position = 1 -> middle
#position = 2 -> deepest
position = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PORT_DOWN, GPIO.OUT)
GPIO.setup(PORT_UP, GPIO.OUT)

#this funciton controls directly the motor and make the sensor go down
def moveDown():
	GPIO.output(PORT_DOWN, True)
	GPIO.output(PORT_UP, False)
	time.sleep(DELAY_DOWN)
	GPIO.output(PORT_DOWN,False)

#this function controles directly the motor and make the sensor go up
def moveUp():
        GPIO.output(PORT_UP, True)
        GPIO.output(PORT_DOWN, False)
        time.sleep(float(DELAY_UP))
        GPIO.output(PORT_UP,False)

#return the actual depth of the sensor
def getPosition():
	return position

#set a new depth to the sensor
def setPosition(newPosition):
	global position
	if (newPosition - position) > 0:
		while (position != newPosition):
			moveDown()
			position += 1
	else:
		while (position != newPosition):
			moveUp()
			position -= 1

#this function access the file "w1_slave", where the temperature
# is written and split it to get the temperature
def readTemp(unit):
        tempfile = open("/sys/bus/w1/devices/28-0000069757fc/w1_slave") #access the file w1_slave
        tempfile_text = tempfile.read() #copy the text of the file to the variable tempfile_text
        tempfile.close() #close the file
        tempC = float(tempfile_text.split("\n")[1].split("t=")[1]) #get only the number that represents the temperature from the variable and convert it to integer
	tempC = tempC /1000
	tempF = (((tempC*9)/5)+32)
	
	if unit == 0:
        	return tempC
	elif unit == 1:
		return tempF
	else:
		return 999 #invalid parameter

#this function saves the temperature and the respective date/time and depth in the database
def saveTemp(date, depth, tempC, tempF):
	conn = sqlite3.connect("buoy.db")
	c = conn.cursor()
	c.execute("INSERT INTO buoy VALUES ('%s', '%s', '%s', '%s')" % (date, depth, tempC, tempF))
	conn.commit()
	conn.close()

#this function gets the date and time and returns it in the format 'YYYY-MM-DD H:M
def getDateTime():
	date = "%s-%s-%s" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
	time = "%s:%s"% (datetime.datetime.today().hour, datetime.datetime.today().minute)
	return "%s %s"% (date, time)

#this is the main function. This function calls the others in order to make the measurements. It measure the temperature
#in the surface (position 0) and save it in the save it in the database. Then the function does the same for the
#positions 1 and 2
def controller():
	if getPosition() != 0:
		setPosition(0)
	saveTemp(getDateTime(), getPosition(), readTemp(0), readTemp(1))

	setPosition(1)
	time.sleep(DELAY_TEMP)
	saveTemp(getDateTime(), getPosition(), readTemp(0), readTemp(1))

	setPosition(2)
	time.sleep(DELAY_TEMP)
	saveTemp(getDateTime(), getPosition(), readTemp(0), readTemp(1))
	
	setPosition(0)

controller()
