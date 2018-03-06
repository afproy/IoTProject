import RPi.GPIO as GPIO
import Adafruit_DHT
import time


class Button:   
    def init(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def read(self):
        input_state = GPIO.input(self.pin)
        if input_state == False:
            print('Button Pressed')
            time.sleep(0.2)


class DHT11:
    def init(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2 
        self.temperature = None
        self.humidity = None


    def read(self):
        while ((self.humidity == None) || (self.temperature == None)):
            self.humidity, self.temperature = Adafruit_DHT.read_retry(self.pin1, self.pin2)
        return self.humidity, self.temperature

