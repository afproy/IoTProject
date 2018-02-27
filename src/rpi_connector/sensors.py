import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

class Button():

    def __init__(self, pin):
        self.pin = pin
        self.state = None
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(21, GPIO.IN)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        #initialize previous input as 0 => BUTTON NOT PRESSED
        prev_input = 0        
        
        # read pin
        input = GPIO.input(self.pin)
        # wait 0.05s to debounce the button
        time.sleep(0.05)
        
        if input == 0:
            self.state = 'closed'
        elif input == 1:
            self.state = 'open'
        return self.state
            

class DHT11():

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        humidity, temperature = None, None
        wait = 0
        while (humidity == None or temperature == None and wait<100):
            
            humidity, temperature = Adafruit_DHT.read_retry(11,self.pin)
            print "temperature = %s" %temperature
            print "humidity = %s" %humidity
            wait += 1
   
        prev_temp = temperature
        prev_humi = humidity
        return temperature, humidity


if __name__ == '__main__':
    while True:
        print "----------------"
        print Button(21).read()
        print DHT11(17).read()
        time.sleep(0.5)
