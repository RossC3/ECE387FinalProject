#Tilt Controller Script MPU 6050

#imports and runs calculations script to get rotation
import Calculations

# Orientation of the Chip. Is the X-axis the horizontal axis or is the Y-axis
xOrientation = False
yOrientation = True
zOrientation = False

#degrees of sensitivity for tilt controller
phSense = 1
pvSense = 1
nhSense = -1
nvSense = -1


# defines orientation, default is yOrientation
def setOrientation(a):
    
    global xOrientation
    global yOrientation
    global zOrientation
    if a == 0:
        yOrientation = True
        xOrientation = False
        zOrientation = False
    elif a == 1:
        xOrientation = True
        yOrientation = False
        zOrientation = False;
    else:
        xOrientation = False
        yOrientation = False
        zOrientation = True
        

#defines degree of sensitivity before notification of tilt default values are both 1
#increasing numbers decreases sensitivity
def setSensitivity(pa, na, pb, nb):
    global phSense
    global pvSense
    global nhSense
    global nvSense

    phSense = pa + 5
    nhSense = na - 5
    pvSense = pb + 2
    nvSense = nb - 5
    
#detects if the controller should move right or is past the Right degree sensitivity
def Right():
    global xOrientation
    global yOrientation
    global phSense
    global nhSense
    

    if yOrientation:
        if(Calculations.getYRotation()> phSense):
            return True
        
    elif xOrientation:
        if(Calculations.getXRotation()> phSense):
            return True
    else:
        if Calculations.getZRotation() < nhSense:
            return True
    
    return False
    
#detects if the controller should move right or is past the left degree sensitivity
def Left():
    global xOrientation
    global yOrientation
    global hSense
    global phSense
    global nhSense
    
    if yOrientation:
        if(Calculations.getYRotation() < nhSense):
            return True
        
    elif xOrientation:
        if(Calculations.getXRotation() < nhSense):
            return True

    else:
        if Calculations.getZRotation() > phSense:
            return True
    
    return False
#detects if the controller should move right or is past the +vertical or forward degree sensitivity    
def Up():
    global xOrientation
    global yOrientation
    global pvSense
    global nvSense
    
    if yOrientation:
        if(Calculations.getXRotation() < nvSense):
            return True
        
    elif xOrientation:
        if(Calculations.getYRotation() > pvSense):
            return True
    else:
        if(calculations.getYRotation() > pvSense):
            return True

    return False
#detects if the controller should move right or is past the -vertical or backward degree sensitivity    
def Down():
    global xOrientation
    global yOrientation
    global pvSense
    global nvSense
    
    if yOrientation:
        if(Calculations.getXRotation() > pvSense):
            return True
        
    elif xOrientation:
        if(Calculations.getYRotation()< nvSense):
            return True
    
    else:
        if(calculations.getYRotation() > nvSense):
            return True
    return False


