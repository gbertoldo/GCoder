#!/usr/bin/python

from GCoder import *
import math


def millPocketCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepR, stepZ, dRfinishing, dZfinishing, feedrateR, feedrateZ, toolDiameter, contourDir):
    """
        Cuts a circular pocket on the surface XY

        Xref, Yref   = coordinates of the center of the circle 
        D            = diameter of the circle (mm)
        Zi           = initial position of z (mm)
        Zf           = final position of z (mm)
        Zsafe        = z safe for motion (mm)
        stepR        = step in the radial direction (mm)
        stepZ        = layer height (mm)
        dRfinishing  = thickness of the finishing in R (mm)
        dZfinish     = thickness of the finishing in Z (mm)
        feedrateR    = feedrate along R (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
        toolDiameter = tool diameter (mm)
        contourDir   = 0=clockwise, 1=counter-clockwise
    """

    # Changing circle according to the tool diameter
    D = D-toolDiameter
    
    
    # Function to create the circumference (path)
    def circumference(X, Y, R):
        gc = []
        # Starting at point (X,Y)
        gc.append(G1 + x(X) + y(Y) + f(feedrateR))
        # Arc to point (X,Y)
        if contourDir == 0:
            gc.append(g2(X, Y, -R, 0.0, feedrateR))
        else: 
            gc.append(g3(X, Y, -R, 0.0, feedrateR))
        return gc

    # Function to create the circle (surface)
    def circle():
        gc = []
        # Starting at point Xref, Yref
        gc.append(G1 + x(Xref) + y(Yref) + f(feedrateR))

        radius = 0.0
        while (2.0*(radius + dRfinishing) < D - 1E-3):
            radius = radius + stepR
            if (2.0*(radius + dRfinishing) > D ):
                radius = D/2.0-dRfinishing
            gc = gc + circumference(Xref+radius, Yref, radius)
        if dRfinishing > 1E-4:
            radius = D/2.0
            gc = gc + circumference(Xref+radius, Yref, radius)
        return gc

    # Creating the gcode
    gcode = []
    
    # Setting the XY plane
    gcode.append("G17")

    # Moving to Z safe
    gcode.append(G0+z(Zsafe))

    # Moving to the start position
    gcode.append(G0+x(Xref)+y(Yref))

    # Moving down
    gcode.append(G0+z(Zi+0.5))

    # Creating multiple layers
    zp = Zi 
    while ( zp-(Zf+dZfinishing) > 1E-3 ):
        zp = zp - stepZ
        if zp < Zf+dZfinishing:
            zp = Zf+dZfinishing     
        gcode.append(G1+x(Xref)+y(Yref)+f(feedrateR))
        gcode.append(G1+z(zp)+f(feedrateZ))
        gcode = gcode + circle()
    if dZfinishing > 1E-4:
        zp = Zf
        gcode.append(G1+x(Xref)+y(Yref)+f(feedrateR))
        gcode.append(G1+z(zp)+f(feedrateZ))
        gcode = gcode + circle()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Yref = 0.0
    D = 10.0
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepR = 1.0
    stepZ = 1.0
    dRfinishing = 0.1
    dZfinishing = 0.1
    feedrateR = 600.0 
    feedrateZ = 300.0
    toolDiameter = 2.0
    contourDir = 0 # 0 = CW, 1 = CCW
    
    gc = millPocketCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepR, stepZ, dRfinishing, dZfinishing, feedrateR, feedrateZ, toolDiameter, contourDir)

    for item in gc:
        print(item)
