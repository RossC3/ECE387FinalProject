#Calculations Script

import math
import Setup
import statistics
import time

#Average resting degree value of the sensor used to calibrate starting point
Xrest = 0

Yrest = 0

Zrest = 0
#Calculates the distance between two points
def dist(a,b):
    return math.sqrt((a*a)+(b*b))

#Outputs +/- Y rotation from approximately zero
def getYRotation():
    global Yrest
    #calculates angle
    rads = math.atan2(Setup.getAx(), dist(Setup.getAy(),Setup.getAz()))
    
    #returns angle with adjustment for starting position
    return - round(math.degrees(rads) + Yrest)

#Outputs +/- X rotation from approximately zero
def getXRotation():
    #calculates angle
    global Xrest
    radians = math.atan2(Setup.getAy(), dist(Setup.getAx(),Setup.getAz()))

    #returns angle with adjustment for starting position
    return round(math.degrees(radians) - Xrest)


# Does not work in all orientations, need IMU with Magnometer to compensate for this
def getZRotation():
    global Zrest
    radians = math.atan2(Setup.getAz(), dist(Setup.getAx(),Setup.getAy()))
    return round(math.degrees(radians)+Zrest)

# returns X acceleration component in m/s
def getXAcceleration():
    
    return Setup.getAx()*9.81


# returns Y acceleration component in m/s    
def getYAcceleration():
    
    return Setup.getAy()*9.81


# returns Z acceleration component in m/s
def getZAcceleration():
    
    return Setup.getAz()*9.81

# returns x angular velocity in degrees per second
def getXG():

    return Setup.getGx()

# returns y angular velocity in degrees per second
def getYG():

    return Setup.getGy()

# returns z angular velocity in degrees per second
def getZG():

    return Setup.getGz()

# returns resultant force in Newtons (N)
def resultantForce(m):

    r = math.sqrt( (m *getXAcceleration()) ** 2 + (m *getYAcceleration()) ** 2 + (m *getZAcceleration()) ** 2)
    return r

# sets resting X and Y positions in order to compensate for error
def calibrate():
    global Yrest
    global Xrest
    global Zrest
    
    Xrest = 0

    Yrest = 0

    Zrest = 0
    
    Xrest = calX()
    Yrest = calY()
    Zrest = calZ()
    

# calculates average resting position for sensor on Y axis from 100 trials
def calY():
    
    sample = []
    i = 0
    while i < 100:
        sample.append(getYRotation())
        i += 1
        
    return statistics.mean(sample)

# calculates average resting position for sensor on X axis from 100 trials
def calX():
    
    sample = []
    i = 0
    while i < 100:
        sample.append(getXRotation())
        i += 1
        
    return statistics.mean(sample)

def calZ():
    
    sample = []
    i = 0
    while i < 100:
        sample.append(getXRotation())
        i += 1
        
    return statistics.mean(sample)

def getMean(a):

    return statistics.mean(a)

def getDev(a):

    return statistics.stdev(a)

def atRest():
 
    if abs(getYRotation())> 10 or abs(getXRotation())>10:
        return False
    else:
        time.sleep(1)
        return True
    
    return True

#calibrates sensor at runtime
calibrate()

