import pygame
import Calibrations
import TiltControls
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,OUT)
pygame.init()

sWidth = 1000
sHeight = 750
win = pygame.display.set_mode((sWidth, sHeight))
bx1 = 200
by1 = 325

bx2 = sWidth - 400
by2 = 325

bx3 = 400
by3 = 500
blength = 200
bheight = 100
pygame.display.set_caption("Smart Belt GUI")

squatting = False
deadLifting = False
squatcal = False

squatList = [];

LTilt = 0
RTilt = 0
FTilt = 0
BTilt = 0

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline= None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


run = True
squatButton = button((0, 255, 0), bx1, by1, blength, bheight, 'Squats')
deadLiftButton = button((0, 255, 0), bx2, by2, blength, bheight, 'Dead Lift')
quitButton = button((255, 0, 0), bx3, by3, blength, bheight, 'Quit')



def redrawWindow():
    win.fill((135, 206, 250))
    squatButton.draw(win, (0, 0, 0))
    deadLiftButton.draw(win, (0, 0, 0))
    quitButton.draw(win, (0, 0, 0))

def calibrationScreen():
    global cal, bx1, by1, by2, bx3, by3, blength, bheight, LTilt, RTilt, FTilt, BTilt

    startRep = button((0, 255, 0), bx3, by1, blength, bheight, 'Start')
    #endRep = button((0, 255, 0), bx2, by2, blength, bheight, 'End Rep')
    backButton = button((255, 0, 0), bx3, by3, blength, bheight, 'Back')
    t = True

    while t:
        win.fill((135, 206, 250))
        startRep.draw(win, (0, 0, 0))
        #endRep.draw(win, (0, 0, 0))
        backButton.draw(win, (0, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startRep.isOver(pos):
                    i = 10
                    while i > -1:
                        text = str(i)
                        font = pygame.font.SysFont('comicsans', 60)
                        text = font.render(text, 1, (0, 0, 0))
                        
                        win.fill((135, 206, 250))
                        win.blit(text, (bx3+100, by1-100))
                        startRep.draw(win, (0, 0, 0))
                        backButton.draw(win, (0, 0, 0))
                        pygame.display.update()
                        i = i -1
                        time.sleep(1)
                    
                    Calibrations.calibrateBelt()
                    print('DONE')
                    cal = True
                    t= True
                    LTilt = Calibrations.meanXmin-Calibrations.stdXmin
                    RTilt = Calibrations.meanXmax+Calibrations.stdXmax
                    FTilt = Calibrations.meanYmax+Calibrations.stdYmax
                    BTilt = Calibrations.meanYmin-Calibrations.stdYmin
                    

                if backButton.isOver(pos) and cal:
                    t = False

def liftScreen():
    global cal, bx1, by1, by2, bx3, by3, blength, bheight, LTilt, RTilt, FTilt, BTilt
    TiltControls.setOrientation(1)
    TiltControls.setSensitivity(RTilt, LTilt, FTilt, BTilt)
    startRep = button((0, 255, 0), bx3, by1, blength, bheight, 'Lift')
    #endRep = button((0, 255, 0), bx2, by2, blength, bheight, 'End Rep')
    backButton = button((255, 0, 0), bx3, by3, blength, bheight, 'Back')
    t = True
    lift = False
    while t:
        win.fill((135, 206, 250))
        startRep.draw(win, (0, 0, 0))
        #endRep.draw(win, (0, 0, 0))
        backButton.draw(win, (0, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startRep.isOver(pos):
                    t= True
                    lift = True
                if backButton.isOver(pos):
                    t = False
                    lift = False
        if lift:
            if TiltControls.Right():
                print('Right Tilt')
                GPIO.output(26,True)
            elif TiltControls.Left():
                print('Left Tilt')
                GPIO.output(26,True)
            elif TiltControls.Up():
                print('Forward')
                GPIO.output(26,True)
            elif TiltControls.Down():
                print('Back')
                GPIO.output(26,True)
            else:
                GPIO.output(26,False)

    time.sleep(.5)
            
def exerciseScreen():
    global cal, bx1, by1, by2, bx3, by3, blength, bheight,squatting, deadLifting,run
    liftButton = button((0, 255, 0), bx1, by1, blength, bheight, 'Lift')
    calibrateButton = button((0, 255, 0), bx2, by2, blength, bheight, 'Calibrate')
    backButton = button((255, 0, 0), bx3, by3, blength, bheight, 'Back')
    t = True
    while t:
        win.fill((135, 206, 250))
        liftButton.draw(win, (0, 0, 0))
        calibrateButton.draw(win, (0, 0, 0))
        backButton.draw(win, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if liftButton.isOver(pos) and cal:
                    print('Lifting Selected')
                    liftScreen()
                if calibrateButton.isOver(pos):
                    print('Calibration Selected')
                    calibrationScreen()
                if backButton.isOver(pos):
                    squatting = False
                    deadLifting = False
                    t = False
        
        


while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:

            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if squatButton.isOver(pos):
                print('Squats Selected')
                squatting = True
                exerciseScreen()
            if deadLiftButton.isOver(pos):
                print('Dead Lift Selected')
                deadLifting = True
                exerciseScreen()
            if quitButton.isOver(pos):

                run = False
                pygame.quit()
