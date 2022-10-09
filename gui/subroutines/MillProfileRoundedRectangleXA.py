#!/usr/bin/python

from GCoder import *
import math


def millProfileRoundedRectXA(Xref, Aref, DX, DA, Rcyl, Rc, dLacc, Zi, Zf, Zsafe, stepZ, feedrateXA, feedrateZ, toolDiameter, isToolInside):
    """
        Cuts a rounded rectangle on the surface of a cylinder with 
        the axis along the X axis.

        Xref, Aref   = coordinates of the center of the rectangle 
        DX           = length of rectangle along X (mm)
        DA           = length of rectangle along A (deg)
        Rcyl         = radius of the cylinder (mm)
        Rc           = corner radius (mm)
        dLacc        = length of the segments of arc (mm). Affects the accuracy of the arc.
        Zi           = initial position of z (mm)
        Zf           = final position of z (mm)
        Zsafe        = z safe for motion (mm)
        stepZ        = layer height (mm)
        feedrateXA   = feedrate along XA (mm/min)
        feedrateZ    = feedrate along Z (mm/min)
        toolDiameter = tool diameter (mm)
        isToolInside = true if tool is inside of the rectangle
    """

    # Changing rectangle according to the tool diameter
    if ( isToolInside ):
        DX = DX-toolDiameter
        DA = DA-toolDiameter
    else:
        DX = DX+toolDiameter
        DA = DA+toolDiameter

    # Coefficient for conversion between arc length and angle: S=A*alpha
    pi = math.acos(-1.0)
    alpha = pi * Rcyl / 180.0

    Sref = Aref*alpha
    DS = DA*alpha

    def angle(length):
        return " A"+"{:.4f}".format(length/alpha)
    
    # Creating the gcode
    gcode = []

    # Function to create the rounded rectangle on a single layer
    def roundedRectangle():
        # Rotating toward the first corner
        gcode.append(G1+angle(Sref-DS/2.0+Rc)+f(feedrateXA))

        # Moving around the first corner
        arcLength = pi*Rc/2.0
        dl = dLacc
        N = int(arcLength/dl)
        if ( N == 0 ):
            N=1
        dphi = pi/2.0/N
        phibeg = pi
        xbeg = Xref-DX/2.0+Rc
        sbeg = Sref-DS/2.0+Rc
        for i in range(0,N+1):
            phi = phibeg + dphi * i
            xp = xbeg + Rc*math.cos(phi)
            sp = sbeg + Rc*math.sin(phi)
            gcode.append(G1+x(xp)+angle(sp)+f(feedrateXA))

        # Moving toward the second corner
        gcode.append(G1+x(Xref+DX/2.0-Rc)+f(feedrateXA))
        
        # Moving around the second corner
        phibeg = 1.5*pi
        xbeg = Xref+DX/2.0-Rc
        sbeg = Sref-DS/2.0+Rc
        for i in range(0,N+1):
            phi = phibeg + dphi * i
            xp = xbeg + Rc*math.cos(phi)
            sp = sbeg + Rc*math.sin(phi)
            gcode.append(G1+x(xp)+angle(sp)+f(feedrateXA))

        # Rotating toward the third corner
        gcode.append(G1+angle(Sref+DS/2.0-Rc)+f(feedrateXA))

        # Moving around the third corner
        phibeg = 0.0
        xbeg = Xref+DX/2.0-Rc
        sbeg = Sref+DS/2.0-Rc
        for i in range(0,N+1):
            phi = phibeg + dphi * i
            xp = xbeg + Rc*math.cos(phi)
            sp = sbeg + Rc*math.sin(phi)
            gcode.append(G1+x(xp)+angle(sp)+f(feedrateXA))

        # Moving toward the fourth corner
        gcode.append(G1+x(Xref-DX/2.0+Rc)+f(feedrateXA))

        # Moving around the fourth corner
        phibeg = pi/2.0
        xbeg = Xref-DX/2.0+Rc
        sbeg = Sref+DS/2.0-Rc
        for i in range(0,N+1):
            phi = phibeg + dphi * i
            xp = xbeg + Rc*math.cos(phi)
            sp = sbeg + Rc*math.sin(phi)
            gcode.append(G1+x(xp)+angle(sp)+f(feedrateXA))

    # Moving to Z safe
    gcode.append(G0+z(Zsafe))

    # Moving to the start position
    gcode.append(G0+x(Xref-DX/2)+angle(Sref+DS/2.0-Rc))

    # Moving down
    gcode.append(G0+z(Zi+0.5))

    # Creating multiple layers
    zp = Zi 
    while ( zp-Zf > 1E-3 ):
        zp = zp - stepZ
        if zp < Zf:
            zp = Zf     
        gcode.append(G1+z(zp)+f(feedrateZ))
        roundedRectangle()

    # Moving up to the safe z
    gcode.append(G0+z(Zsafe))

    return gcode



# For testing
if __name__ == "__main__":
    Xref = 0.0
    Aref = 0.0
    DX = 100.0
    DA = 120.0
    Rcyl = 75.0
    Rc = 20.0
    dLacc = 0.1
    Zi = 0.0
    Zf = -3.0
    Zsafe = 5.0
    stepZ = 1.0
    feedrateXA = 60.0 
    feedrateZ = 30.0
    toolDiameter = 3.0
    isToolInside = True
    gc = millProfileRoundedRectXA(Xref, Aref, DX, DA, Rcyl, Rc, dLacc, Zi, Zf, Zsafe, stepZ, feedrateXA, feedrateZ, toolDiameter, isToolInside)

    for item in gc:
        print(item)
