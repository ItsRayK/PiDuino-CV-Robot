import time
import serial
import random
import RPi.GPIO as GPIO
import pygame
from SimplifiedRPiGPIO import Led, DigitalInput

# Display Variables
dis_width = 600
dis_height = 400

black = (0, 0, 0)
white = (255, 255, 255)
dark_grey =  (25, 25, 25)
red = (124, 0, 0)
green = (33, 124, 0)
dark_green = (0, 79, 3)
blue = (0, 52, 124)
light_blue = (58, 212, 255)
yellow = (235, 249, 34)

# Initialize Display
pygame.init()
control_display = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("PiDuino Robotics")
clock = pygame.time.Clock()

control_display.fill(black)
pygame.display.update()
clock.tick(60)

# Serial Port (Pi > Arduino)
serialPort = '/dev/ttyUSB0'
baudrate = 9600
ser = serial.Serial(serialPort, baudrate)

# GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

headlights = Led(18)
frontSensor = DigitalInput(15)

# GUI Key Parameters
key_size = 80
gap = 30

w_xpos = (dis_width/2) - (key_size/2) + 50
w_ypos = (dis_height/4)

s_xpos = w_xpos
s_ypos = w_ypos + key_size + gap

a_xpos = w_xpos - key_size - gap
a_ypos = s_ypos

d_xpos = w_xpos + key_size + gap
d_ypos = s_ypos

pressed_color = light_blue
released_color = blue

# Object Classes
class GuiKey():

    def __init__(self, xpos, ypos, boxsize, text):
        self.xpos = xpos
        self.ypos = ypos
        self.boxsize = boxsize
        self.color = released_color
        self.text = text

    def pressed(self):
        self.color = pressed_color

    def released(self):
        self.color = released_color

    def draw(self):
        pygame.draw.rect(control_display, self.color, [self.xpos, self.ypos, self.boxsize, self.boxsize]) 
        font = pygame.font.SysFont(None, 50)
        display_text = font.render(self.text, True, white)
        control_display.blit(display_text, (self.xpos + self.boxsize / 2, self.ypos + self.boxsize / 2))

class GuiKeyToggle(GuiKey):
    def __init__(self, xpos, ypos, boxsize, text, coloron, coloroff):
        super().__init__(xpos, ypos, boxsize, text)
        self.color = coloroff
        self.coloron = coloron
        self.coloroff = coloroff

    def toggleon(self):
        self.color = self.coloron

    def toggleoff(self):
        self.color = self.coloroff

class DisplayText:
    def __init__(self, text, tsize, xpos, ypos, color):
        self.text = text
        self.tsize = tsize
        self.xpos = xpos
        self.ypos = ypos
        self.color = color

    def setText(self, text):
        self.text = text

    def draw(self):
        font = pygame.font.SysFont(None, self.tsize)
        display_text = font.render(self.text, True, self.color)
        control_display.blit(display_text, (self.xpos, self.ypos))


# Send character over serial
def send_cmd(chartosend):
    ser.write(chartosend.encode())

# Create Display Graphics
wKey = GuiKey(w_xpos, w_ypos, key_size, "W")
aKey = GuiKey(a_xpos, a_ypos, key_size, "A")
sKey = GuiKey(s_xpos, s_ypos, key_size, "S")
dKey = GuiKey(d_xpos, d_ypos, key_size, "D")
eKey = GuiKeyToggle(d_xpos, w_ypos, key_size, "E", yellow, red)

infoText = DisplayText("PiDuino Control Station", 30, 10, 10, light_blue)
lightStatus = DisplayText("Lights: OFF", 30, 10, 70, white)
teleopStatus = DisplayText("Teleoperation: ON", 30, 10, 100, white)
obstacleStatus = DisplayText("Obstacle Detected: FALSE", 30, 10, 130, white)

# Main Loop
def mainloop():
    lightState = False
    teleop = True

    while True:
        obstacleDetected = frontSensor.read()
        if not obstacleDetected:
            obstacleStatus.setText("Obstacle Detected: TRUE")
        else:
            obstacleStatus.setText("Obstacle Detected: FALSE")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if teleop:
                    if event.key == pygame.K_w:
                        #print("Forward")
                        send_cmd("w")
                        wKey.pressed()

                    if event.key == pygame.K_s:
                        #print("Backward")
                        send_cmd("s")
                        sKey.pressed()

                    if event.key == pygame.K_a:
                        #print("Left")
                        send_cmd("a")
                        aKey.pressed()

                    if event.key == pygame.K_d:
                        #print("Right")
                        send_cmd("d")
                        dKey.pressed()

            if event.type == pygame.KEYUP:
                if teleop:
                    if event.key == pygame.K_w:
                        #print("Stop Forward")
                        send_cmd("i")
                        wKey.released()

                    if event.key == pygame.K_s:
                        #print("Stop Backward")
                        send_cmd("k")
                        sKey.released()

                    if event.key == pygame.K_a:
                        #print("Stop Left")
                        send_cmd("j")
                        aKey.released()

                    if event.key == pygame.K_d:
                        #print("Stop Right")
                        send_cmd("l")
                        dKey.released()

                    if event.key == pygame.K_e:
                        #print("Toggle Lights")
                        if not lightState:
                            headlights.on()
                            lightState = True
                            lightStatus.setText("Lights: ON")
                            eKey.toggleon()
                        else:
                            headlights.off()
                            lightState = False
                            lightStatus.setText("Lights: OFF")
                            eKey.toggleoff()

                if event.key == pygame.K_t:
                    #print("Toggle Teleop")
                    if not teleop:
                        teleop = True
                        teleopStatus.setText("Teleoperation: ON")

                    else:
                        teleop = False
                        teleopStatus.setText("Teleoperation: OFF")

        control_display.fill(black)
        infoText.draw()
        lightStatus.draw()
        teleopStatus.draw()
        obstacleStatus.draw()

        wKey.draw()
        aKey.draw()
        sKey.draw()
        dKey.draw()
        eKey.draw()

        pygame.display.update()

# Main
if __name__ == '__main__':
    mainloop()
