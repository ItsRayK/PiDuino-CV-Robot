import RPi.GPIO as GPIO

class DigitalOutput:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def high(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def low(self):
        GPIO.output(self.pin, GPIO.LOW)

class DigitalInput:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read(self):
        return GPIO.input(self.pin)

class Led(DigitalOutput):
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)


    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


class Button(DigitalInput):
    pass

class Switch(DigitalInput):
    pass
