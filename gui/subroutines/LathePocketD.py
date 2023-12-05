#!/usr/bin/python

from GCoder import *
import math


def lathePocketD(Zi, Zf, Di, Df, Dsafe, stepD, dDfinishing, feedrateD, feedrateZ):
    """
        Creates a pocket cutting along paths of constant diameters (D) 

        Zi, Zf       = initial and final values of Z (mm)
        Di, Df       = initial and final values of D (mm)
        Dsafe        = D safe for motion (mm)
        stepD        = step in the radial direction (mm)
        dDfinishing  = thickness of the finishing in D (mm)
        feedrateD    = feedrate along D (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
    """
    if Df < Di:
        stepD = -math.fabs(stepD)

    if dDfinishing < 0.0:
        dDfinishing = - dDfinishing

    Nsteps = int(math.fabs((math.fabs(Df-Di)-dDfinishing)/stepD))

    # Creating the gcode
    gcode = []

    # Setting the diameter mode (G7)
    gcode.append("G7")

    # Moving to D safe
    gcode.append(G0+x(Dsafe))

    # Moving to Z initial
    gcode.append(G0+z(Zi))

    # Creating multiple layers
    D = 0.0
    for i in range(0, Nsteps+1):
        D = Di + stepD * i
        gcode.append(G1+x(D)+f(feedrateD))
        gcode.append(G1+z(Zf)+f(feedrateZ))
        gcode.append(G1+x(D-stepD)+f(feedrateD))
        gcode.append(G0+z(Zi))
    
    if dDfinishing > 1E-4:
        if stepD < 0.0:
            D = Df+dDfinishing
        else:
            D = Df-dDfinishing
        gcode.append(G1+x(D)+f(feedrateD))
        gcode.append(G1+z(Zf)+f(feedrateZ))
        gcode.append(G1+x(D-stepD)+f(feedrateD))
        gcode.append(G0+z(Zi))

    if ( math.fabs(D-Df) > 1E-4 ):
        D = Df
        gcode.append(G1+x(D)+f(feedrateD))
        gcode.append(G1+z(Zf)+f(feedrateZ))
        gcode.append(G1+x(D-stepD)+f(feedrateD))
        gcode.append(G0+z(Zi))

    # Moving to the safe D
    gcode.append(G0+x(Dsafe))

    # Moving to the initial Z
    gcode.append(G0+z(Zi))


    return gcode



# For testing
if __name__ == "__main__":
    Zi = 10.0
    Zf = 0.0
    Di = 20.0
    Df = 16.0
    Dsafe = 22.0
    stepD = 1.0
    dDfinishing = 0.1
    feedrateD = 600.0 
    feedrateZ = 300.0
    
    gc = lathePocketD(Zi, Zf, Di, Df, Dsafe, stepD, dDfinishing, feedrateD, feedrateZ)

    for item in gc:
        print(item)
