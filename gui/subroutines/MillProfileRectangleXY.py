#!/usr/bin/python

from GCoder import *
import math


def millProfileRectangleXY(Xref, Yref, DX, DY, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir):
    """
        Cuts a rectangle on the surface XY

        Xref, Yref   = coordinates of the center of the rectangle 
        DX           = length of rectangle along X (mm)
        DY           = length of rectangle along Y (mm)
        Zi           = initial position of z (mm)
        Zf           = final position of z (mm)
        Zsafe        = z safe for motion (mm)
        stepZ        = layer height (mm)
        feedrateXY   = feedrate along XY (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
        toolDiameter = tool diameter (mm)
        isToolInside = true if tool is inside of the rectangle
        contourDir   = 0=clockwise, 1=counter-clockwise
    """

    # Changing rectangle according to the tool diameter
    if ( isToolInside ):
        DX = DX-toolDiameter
        DY = DY-toolDiameter
    else:
        DX = DX+toolDiameter
        DY = DY+toolDiameter
        
    X1=Xref-DX/2.0
    Y1=Yref-DY/2.0
    X2=Xref+DX/2.0
    Y2=Yref-DY/2.0
    X3=Xref+DX/2.0
    Y3=Yref+DY/2.0
    X4=Xref-DX/2.0
    Y4=Yref+DY/2.0   
    
    # Function to create the rectangle on a single layer in the clockwise direction
    def rectangleCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Moving to point 4
        gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))
        # Moving to point 3
        gc.append(G1 + x(X3) + y(Y3) + f(feedrateXY))
        # Moving to point 4
        gc.append(G1 + x(X2) + y(Y2) + f(feedrateXY))
        # Moving to point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        return gc

    # Function to create the rectangle on a single layer in the counter-clockwise direction
    def rectangleCCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Moving to point 2
        gc.append(G1 + x(X2) + y(Y2) + f(feedrateXY))
        # Moving to point 3
        gc.append(G1 + x(X3) + y(Y3) + f(feedrateXY))
        # Moving to point 4
        gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))
        # Moving to point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
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
            gcode = gcode + rectangleCW()
        else:
            gcode = gcode + rectangleCCW()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Yref = 0.0
    DX = 100.0
    DY = 120.0
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepZ = 1.0
    feedrateXY = 600.0 
    feedrateZ = 300.0
    toolDiameter = 3.0
    isToolInside = True
    contourDir = 0 # 0 = CW, 1 = CCW
    
    gc = millProfileRectangleXY(Xref, Yref, DX, DY, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir)

    for item in gc:
        print(item)
