import Calibrations
import Calculations

import TiltControls
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
#Calibrations.calibrateBelt()
TiltControls.setOrientation(1)

Calibrations.calibrateBelt()
TiltControls.setSensitivity(Calibrations.meanXmax+Calibrations.stdXmax, Calibrations.meanXmin-Calibrations.stdXmin, Calibrations.meanYmax+Calibrations.stdYmax, Calibrations.meanYmin-Calibrations.stdYmin)

while True:
   
    print(Calibrations.meanXmin-Calibrations.stdXmin)
    

    #print(Calculations.getXRotation())

    if TiltControls.Right():
        print('Right Tilt')
    elif TiltControls.Left():
        print('Left Tilt')
    elif TiltControls.Up():
        print('Forward')
        GPIO.output(26,True)
    elif TiltControls.Down():
        print('Back')
    else:
        GPIO.output(26,False)

    time.sleep(.5)
