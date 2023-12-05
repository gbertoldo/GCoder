#!/usr/bin/python

from GCoder import *
import math


def millProfileRoundedRectXY(Xref, Yref, DX, DY, Rc, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir):
    """
        Cuts a rounded rectangle on the surface XY

        Xref, Yref   = coordinates of the center of the rectangle 
        DX           = length of rectangle along X (mm)
        DY           = length of rectangle along Y (mm)
        Rc           = corner radius (mm)
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
    Y1=Yref-DY/2.0+Rc
    X2=Xref-DX/2.0+Rc
    Y2=Yref-DY/2.0
    X3=Xref+DX/2.0-Rc
    Y3=Yref-DY/2.0
    X4=Xref+DX/2.0
    Y4=Yref-DY/2.0+Rc
    X5=Xref+DX/2.0
    Y5=Yref+DY/2.0-Rc
    X6=Xref+DX/2.0-Rc
    Y6=Yref+DY/2.0
    X7=Xref-DX/2.0+Rc
    Y7=Yref+DY/2.0
    X8=Xref-DX/2.0
    Y8=Yref+DY/2.0-Rc
    
    
    # Function to create the rounded rectangle on a single layer in the clockwise direction
    def roundedRectangleCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Moving to point 8
        gc.append(G1 + x(X8) + y(Y8) + f(feedrateXY))
        # Arc to point 7
        gc.append(g2(X7, Y7, Rc, 0.0, feedrateXY))
        # Moving to point 6
        gc.append(G1 + x(X6) + y(Y6) + f(feedrateXY))
        # Arc to point 5
        gc.append(g2(X5, Y5, 0.0, -Rc, feedrateXY))
        # Moving to point 4
        gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))
        # Arc to point 3
        gc.append(g2(X3, Y3, -Rc, 0.0, feedrateXY))
        # Moving to point 2
        gc.append(G1 + x(X2) + y(Y2) + f(feedrateXY))
        # Arc to point 1
        gc.append(g2(X1, Y1, 0.0, Rc, feedrateXY))
        return gc

    # Function to create the rounded rectangle on a single layer in the counter-clockwise direction
    def roundedRectangleCCW():
        gc = []
        # Starting at point 1
        gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
        # Arc to point 2
        gc.append(g3(X2, Y2, Rc, 0.0, feedrateXY))
        # Moving to point 3
        gc.append(G1 + x(X3) + y(Y3) + f(feedrateXY))
        # Arc to point 4
        gc.append(g3(X4, Y4, 0.0, Rc, feedrateXY))
        # Moving to point 5
        gc.append(G1 + x(X5) + y(Y5) + f(feedrateXY))
        # Arc to point 6
        gc.append(g3(X6, Y6, -Rc, 0.0, feedrateXY))
        # Moving to point 7
        gc.append(G1 + x(X7) + y(Y7) + f(feedrateXY))
        # Arc to point 8
        gc.append(g3(X8, Y8, 0.0, -Rc, feedrateXY))
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
            gcode = gcode + roundedRectangleCW()
        else:
            gcode = gcode + roundedRectangleCCW()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Yref = 0.0
    DX = 100.0
    DY = 120.0
    Rc = 0.0
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepZ = 1.0
    feedrateXY = 600.0 
    feedrateZ = 300.0
    toolDiameter = 3.0
    isToolInside = True
    contourDir = 0 # 0 = CW, 1 = CCW
    
    gc = millProfileRoundedRectXY(Xref, Yref, DX, DY, Rc, Zi, Zf, Zsafe, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside, contourDir)

    for item in gc:
        print(item)
