import json
import urllib.request
import RPi.GPIO as gpio
import time

# gpio stuff
gpio.setmode(gpio.BCM)

roteLed = 21
blaueLed = 16
grueneLed = 20
servoPin = 17

#setup
gpio.setup(servoPin, gpio.OUT)
gpio.setup(roteLed, gpio.OUT)
gpio.setup(grueneLed, gpio.OUT)
gpio.setup(blaueLed, gpio.OUT)

gpio.output(grueneLed, gpio.LOW)
gpio.output(roteLed, gpio.HIGH)

# Liste aller Bojen + errechnen aller Clients
website = urllib.request.urlopen('http://foerdefunk.de/nodes.json')
websiteString = website.read().decode('utf-8')
data = json.loads(websiteString)

nodes = data['nodes']

countClients = 0;

for a in nodes:
	countClients += nodes[a]['statistics']['clients']

print (countClients)

# blinken der Status LED
gpio.output(roteLed, gpio.LOW)
time.sleep(0.5)
gpio.output(roteLed, gpio.HIGH)
time.sleep(0.5)
gpio.output(roteLed, gpio.LOW)
gpio.output(grueneLed, gpio.HIGH)


# Bewegen Servo Motor
servo = gpio.PWM(servoPin, 50)
def zeiger(val):
	# 13 Steht für die Schritte die der Servo braucht für einen Halbkreis
	# 200 Die Maximal Anzahl der Clients
	# +3 = Ist gleich der Anfangswert
	# -18 damit auch die 0 auf der Linken Seite ist. 
        return 18 -( (val*(13/200))+3)

wert = zeiger(countClients)
print(wert)
servo.start(wert)
time.sleep(60)

gpio.cleanup()
