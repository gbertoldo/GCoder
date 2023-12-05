#!/usr/bin/python

from GCoder import *
import math


def millPocketRectangleXY(Xref, Yref, LX, LY, Zi, Zf, Zsafe, stepXY, stepZ, dXYfinishing, dZfinishing, feedrateXY, feedrateZ, toolDiameter, contourDir):
    """
        Cuts a rectangle pocket on the surface XY

        Xref, Yref   = coordinates of the center of the circle 
        LX           = length of the rectangle along x (mm)
        LY           = length of the rectangle along y (mm)
        Zi           = initial position of z (mm)
        Zf           = final position of z (mm)
        Zsafe        = z safe for motion (mm)
        stepXY       = step (maximum) in the X and Y direction (mm)
        stepZ        = layer height (mm)
        dXYfinishing = thickness of the finishing in the X and the Y direction (mm)
        dZfinish     = thickness of the finishing in Z (mm)
        feedrateXY   = feedrate along X and Y (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
        toolDiameter = tool diameter (mm)
        contourDir   = 0=clockwise, 1=counter-clockwise
    """

    # Changing rectangle according to the tool diameter and finishing surface
    LX = LX-toolDiameter-2.0*dXYfinishing
    LY = LY-toolDiameter-2.0*dXYfinishing

    stepX = stepXY
    stepY = stepXY

    if LX > LY:
        Nsteps = int(0.5*LX/stepXY)
    else:
        Nsteps = int(0.5*LY/stepXY)
    
    if Nsteps > 0:
        stepX = 0.5*LX/Nsteps
        stepY = 0.5*LY/Nsteps
    
    
    # Function to create the rectangular (path)
    def rectanglePath(DX, DY, isFinishing):
        gc = []
        X0=Xref-DX
        Y0=Yref
        X1=Xref-DX
        Y1=Yref-DY
        X2=Xref+DX
        Y2=Yref-DY
        X3=Xref+DX
        Y3=Yref+DY
        X4=Xref-DX
        Y4=Yref+DY

        if ( contourDir == 1 ): # CCW
            gc.append(G1 + x(X0) + y(Y0) + f(feedrateXY))
            gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
            gc.append(G1 + x(X2) + y(Y2) + f(feedrateXY))
            gc.append(G1 + x(X3) + y(Y3) + f(feedrateXY))
            gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))
            gc.append(G1 + x(X0) + y(Y0) + f(feedrateXY))
            if isFinishing:
                gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))

        else:
            gc.append(G1 + x(X0) + y(Y0) + f(feedrateXY))
            gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))
            gc.append(G1 + x(X3) + y(Y3) + f(feedrateXY))
            gc.append(G1 + x(X2) + y(Y2) + f(feedrateXY))
            gc.append(G1 + x(X1) + y(Y1) + f(feedrateXY))
            gc.append(G1 + x(X0) + y(Y0) + f(feedrateXY))
            if isFinishing:
                gc.append(G1 + x(X4) + y(Y4) + f(feedrateXY))

        return gc

    # Function to create the rectangle (surface)
    def rectangleSurface():
        gc = []
        isFinishing = False
        for i in range(1,Nsteps+1):
            DX = stepX * i
            DY = stepY * i
            if i == Nsteps and dXYfinishing < 1E-4:
                isFinishing = True
            gc = gc + rectanglePath(DX, DY, isFinishing)
        if dXYfinishing > 1E-4:
            isFinishing = True
            gc = gc + rectanglePath(LX/2.0+dXYfinishing, LY/2.0+dXYfinishing, isFinishing)
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
        gcode.append(G1+x(Xref)+y(Yref)+f(feedrateXY))
        gcode.append(G1+z(zp)+f(feedrateZ))
        gcode = gcode + rectangleSurface()
    if dZfinishing > 1E-4:
        zp = Zf
        gcode.append(G1+x(Xref)+y(Yref)+f(feedrateXY))
        gcode.append(G1+z(zp)+f(feedrateZ))
        gcode = gcode + rectangleSurface()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Yref = 0.0
    LX = 10.0
    LY = 6.0
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepXY = 1.0
    stepZ = 1.0
    dXYfinishing = 0.1
    dZfinishing = 0.1
    feedrateXY = 600.0 
    feedrateZ = 300.0
    toolDiameter = 2.0
    contourDir = 0 # 0 = CW, 1 = CCW
    
    gc = millPocketRectangleXY(Xref, Yref, LX, LY, Zi, Zf, Zsafe, stepXY, stepZ, dXYfinishing, dZfinishing, feedrateXY, feedrateZ, toolDiameter, contourDir)

    for item in gc:
        print(item)
