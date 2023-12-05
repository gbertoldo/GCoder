#!/usr/bin/python

from GCoder import *
import math


def millProfileCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir):
    """
        Cuts a circle on the surface XY

        Xref, Yref   = coordinates of the center of the circle 
        D            = diameter of the circle (mm)
        Zi           = initial position of z (mm)
        Zf           = final position of z (mm)
        Zsafe        = z safe for motion (mm)
        stepZ        = layer height (mm)
        feedrateXY   = feedrate along XY (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
        toolDiameter = tool diameter (mm)
        isToolInside = true if tool is inside of the circle
        contourDir   = 0=clockwise, 1=counter-clockwise
    """

    # Changing circle according to the tool diameter
    if ( isToolInside ):
        D = D-toolDiameter
    else:
        D = D+toolDiameter
        
    X1=Xref-D/2.0
    Y1=Yref
    
    
    # Function to create the circunference on a single layer in the clockwise direction
    def circunferenceCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Arc to point 1
        gc.append(g2(X1, Y1, D/2.0, 0.0, feedrateXY))
        return gc

    # Function to create the circunference on a single layer in the counter-clockwise direction
    def circunferenceCCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Arc to point 1
        gc.append(g3(X1, Y1, D/2.0, 0.0, feedrateXY))
        return gc
    
    # Creating the gcode
    gcode = []
    
    # Setting the XY plane
    gcode.append("G17")

    # Moving to Z safe
    gcode.append(G0+z(Zsafe))

    # Moving to the start position
    gcode.append(G0+x(X1)+y(Y1))

    # Moving down
    gcode.append(G0+z(Zi+0.5))

    # Creating multiple layers
    zp = Zi 
    while ( zp-Zf > 1E-3 ):
        zp = zp - stepZ
        if zp < Zf:
            zp = Zf     
        gcode.append(G1+z(zp)+f(feedrateZ))
        if contourDir == 0:
            gcode = gcode + circunferenceCW()
        else:
            gcode = gcode + circunferenceCCW()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Yref = 0.0
    D = 100.0
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepZ = 1.0
    feedrateXY = 600.0 
    feedrateZ = 300.0
    toolDiameter = 3.0
    isToolInside = True
    contourDir = 0 # 0 = CW, 1 = CCW
    
    gc = millProfileCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir)

    for item in gc:
        print(item)
