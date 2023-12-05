#!/usr/bin/python

from GCoder import *
import math


def latheThreading(Zi, Zf, Di, Dsafe, threadPitch, threadDepth, stepD, Nfinishing, taperMode, taperAngle):
    """
        Creates a pocket cutting along paths of constant diameters (D) 

        Zi, Zf       = initial and final values of Z (mm)
        Di           = D initial (mm)
        Dsafe        = D safe for motion (mm)
        threadPitch  = pitch of the thread (mm/rev)
        threadDepth  = depth of the thread (mm) 
        stepD        = initial step in the radial direction (mm)
        Nfinishing   = number of finishing steps
        taperMode    = 0 = no taper, 1=entry taper, 2=exit taper, 3=both taper
        taperAngle   = angle of the taper (deg)
    """

    Ipar = Di-Dsafe
    Epar = math.tan(math.pi/180.0*taperAngle)*threadDepth

    # Creating the gcode
    gcode = []

    # Setting the diameter mode (G7)
    gcode.append("G7")

    # Moving to D safe
    gcode.append(G0+x(Dsafe))

    # Moving to Z initial
    gcode.append(G0+z(Zi))

    gcode.append("G76 "+par("P",threadPitch)+z(Zf)+par("I",Ipar)+par("J",stepD)+par("K",threadDepth)+par("H",Nfinishing)+par("E",Epar)+"L"+str(taperMode))

    # Moving to the safe D
    gcode.append(G0+x(Dsafe))

    # Moving to the initial Z
    gcode.append(G0+z(Zi))


    return gcode



# For testing
if __name__ == "__main__":
    Zi = 0.0
    Zf = -10.0
    Di = 20.0
    Dsafe = 22.0
    threadPitch = 1.0
    threadDepth = 0.63
    stepD = 1.0
    Nfinishing = 2
    taperMode = 1
    taperAngle = 45.0

    gc = latheThreading(Zi, Zf, Di, Dsafe, threadPitch, threadDepth, stepD, Nfinishing, taperMode, taperAngle)

    for item in gc:
        print(item)
