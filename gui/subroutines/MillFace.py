#!/usr/bin/python

from GCoder import *
import Rectangle

def faceZZigZag(zigZagDir, Xref, Yref, RefPos, DX, DY, Zi, Zf, finishingHeight, Zsafe, stepXY, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside):

    # Creating the gcode
    gcode = []
	
    Xi = Xref
    Yi = Yref
    Xf = 0.0
    Yf = 0.0
	
    if ( RefPos == 0 ):
        Xf = Xref + DX
        Yf = Yref + DY
    elif ( RefPos == 1 ):
        Xf = Xref - DX
        Yf = Yref + DY
    elif ( RefPos == 2 ):
        Xf = Xref - DX
        Yf = Yref - DY
    else:
        Xf = Xref + DX
        Yf = Yref - DY
	
    # Fast move to Zsafe
    gcode.append(G0 + z(Zsafe) )

    # Defining the XY workspace according to the tool diameter
    E1beg = 0.0
    E1end = 0.0
    E2beg = 0.0
    E2end = 0.0
	
    if ( isToolInside == True ) :
        if ( abs(Xf-Xi) < toolDiameter or abs(Yf-Yi) < toolDiameter ):
            raise ValueError("Diametro da ferramenta maior que as dimensoes do retangulo")
        if ( Xi < Xf ):
            E1beg = Xi+toolDiameter/2.0
            E1end = Xf-toolDiameter/2.0
        else:
            E1beg = Xi-toolDiameter/2.0
            E1end = Xf+toolDiameter/2.0
        if ( Yi < Yf ):
            E2beg = Yi+toolDiameter/2.0
            E2end = Yf-toolDiameter/2.0
        else:
            E2beg = Yi-toolDiameter/2.0
            E2end = Yf+toolDiameter/2.0
    else:
        if ( Xi < Xf ):
            E1beg = Xi-toolDiameter/2.0
            E1end = Xf+toolDiameter/2.0	
        else:
            E1beg = Xi+toolDiameter/2.0
            E1end = Xf-toolDiameter/2.0

        if ( Yi < Yf ):
            E2beg = Yi-toolDiameter/2.0
            E2end = Yf+toolDiameter/2.0
        else:
            E2beg = Yi+toolDiameter/2.0
            E2end = Yf-toolDiameter/2.0
	
    # Defining the coordinate system
    if zigZagDir == 0:
        cs = coordSystem("X", "Y", "Z")
    else:
        cs = coordSystem("Y", "X", "Z")
        tmpB = E1beg
        tmpE = E1end
        E1beg = E2beg
        E1end = E2end
        E2beg = tmpB
        E2end = tmpE
	
    # Moving to the start cutting position
    gcode.append(G0 + cs.E1(E1beg) + cs.E2(E2beg) + z(Zsafe) )


    NZsteps = int( abs(abs(1.0*Zf-Zi)-finishingHeight) / stepZ )

    if ( Zf < Zi ):
        stepZ = - stepZ

    currentZ = Zi
	
    for i in range(1,NZsteps+1):
        currentZ = Zi + stepZ * i

        # Moving to the cutting layer position:
        gcode.append(G1 + z(currentZ) + f(feedrateZ) )

        # Cuttig a rectangle with zigzag
        gcode = gcode + Rectangle.zigZagFilled(cs, E1beg, E1end, E2beg, E2end, stepXY, feedrateXY) 

        # Moving to Zsafe
        gcode.append(G0 + z(Zsafe) )

        # Moving to the initial position
        gcode.append(G0 + cs.E1(E1beg) + cs.E2(E2beg) + z(Zsafe) )
        
    if ( abs(Zf - currentZ) > finishingHeight + 1E-4 ):
        if ( Zf < Zi ):
            currentZ = Zf+finishingHeight
        else:
            currentZ = Zf-finishingHeight

        # Moving to the cutting layer position:
        gcode.append(G1 + z(currentZ) + f(feedrateZ) )

        # Cuttig a rectangle with zigzag
        gcode = gcode + Rectangle.zigZagFilled(cs, E1beg, E1end, E2beg, E2end, stepXY, feedrateXY) 

        # Moving to Zsafe
        gcode.append(G0 + z(Zsafe) )

        # Moving to the initial position
        gcode.append(G0 + cs.E1(E1beg) + cs.E2(E2beg) + z(Zsafe) )
        
    if ( abs(Zf - currentZ) > 1E-4 ):
        currentZ = Zf
        
        # Moving to the cutting layer position:
        gcode.append(G1 + z(currentZ) + f(feedrateZ) )

        # Cuttig a rectangle with zigzag
        gcode = gcode + Rectangle.zigZagFilled(cs, E1beg, E1end, E2beg, E2end, stepXY, feedrateXY) 
        
        # Moving to Zsafe
        gcode.append(G0 + z(Zsafe) )

        # Moving to the initial position
        gcode.append(G0 + cs.E1(E1beg) + cs.E2(E2beg) + z(Zsafe) )

    return gcode

# For testing
if __name__ == "__main__":
    
    zigZagDir = 1
    Xref = 0
    Yref = 0
    RefPos = 0
    DX = 100 
    DY = 100 
    Zi = 0 
    Zf = -5
    finishingHeight = 0.1 
    Zsafe = 5
    stepXY = 10
    stepZ = 1
    feedrateXY = 120 
    feedrateZ = 30
    toolDiameter = 10
    isToolInside = False
    
    gc = faceZZigZag(zigZagDir, Xref, Yref, RefPos, DX, DY, Zi, Zf, finishingHeight, Zsafe, stepXY, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside)
    for line in gc:
        print(line)
    print("M30")
