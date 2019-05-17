import math
import statistics
import Calculations
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,OUT)
xMaxlist = []
xMinlist = []
yMaxlist = []
yMinlist = []
zMaxlist = []
zMinlist = []

meanXmin = 0
meanYmin = 0
meanZmin = 0
meanXmax = 0
meanYmax = 0
meanZmax = 0

stdXmin = 0
stdYmin = 0
stdZmin = 0
stdXmax = 0
stdYmax = 0
stdZmax = 0




#Calculates x, y, and z rotations of the body during rep
def calculateRep():
    
    maxX = 0
    maxY = 0
    maxZ = 0

    minX = 0
    minY = 0
    minZ = 0
    
    while not Calculations.atRest():

        print('calculating max rotation')
        print(Calculations.getYRotation())
        
        if Calculations.getYRotation() > maxY:
            maxY = Calculations.getYRotation()
        elif Calculations.getYRotation() < minY:
            minY = Calculations.getYRotation()
            
        if Calculations.getXRotation() > maxX:
            maxX = Calculations.getXRotation()
        elif Calculations.getYRotation() < minX:
            minX= Calculations.getXRotation()
            
        
        if Calculations.getZRotation() > maxZ:
            maxZ = Calculations.getZRotation()
        elif Calculations.getYRotation() < minZ:
            minZ = Calculations.getZRotation()

    xMaxlist.append(maxX)
    yMaxlist.append(maxY)
    zMaxlist.append(maxZ)
    xMinlist.append(minX)
    yMinlist.append(minY)
    zMinlist.append(minZ)

#takes calculations and finds average and standard dev of mean in all x, y, and z rotations
def calibrateBelt():
    global meanXmin, meanYmin, meanZmin, meanXmax, meanYmax, meanZmax
    global stdXmin, stdYmin, stdZmin, stdXmax, stdYmax, stdZmax
    global xMaxlist, yMaxlist, zMaxlist, xMinlist, yMinlist, zMinlist
    Calculations.calibrate()
    i = 0

    while i < 2:

        
        
        if not Calculations.atRest():
            print('Starting Rep')
            calculateRep()
            print('Finished Rep')
            GPIO.output(26,True)
            i = i+1
            time.sleep(1)
            GPIO.output(26,False)
        else:
            print('Waiting')


   
    
    meanXmin = Calculations.getMean(xMinlist)
    meanYmin = Calculations.getMean(yMinlist)
    meanZmin = Calculations.getMean(zMinlist)
    meanXmax = Calculations.getMean(xMaxlist)
    meanYmax = Calculations.getMean(yMaxlist)
    meanZmax = Calculations.getMean(zMaxlist)

    stdXmin = Calculations.getDev(xMinlist)
    stdYmin = Calculations.getDev(yMinlist)
    stdZmin = Calculations.getDev(zMinlist)
    stdXmax = Calculations.getDev(xMaxlist)
    stdYmax = Calculations.getDev(yMaxlist)
    stdZmax = Calculations.getDev(zMaxlist)
