#!/usr/bin/python

from GCoder import *

# Traces a zig zag path to fill a rectangle.
# The progressive motion occurs in the E1 axis at steps 'steps'. 
# The forth and back motion occurs in the E2 axis at 'feedrate'.
# coordSystem is used to choose the plane of the rectangle.
def zigZagFilled(coordSystem, E1beg, E1end, E2beg, E2end, step, feedrate):

	cs = coordSystem

	if ( E1end < E1beg ):
		step = -abs(step)

	Nstep = int((E1end-E1beg)/float(step))

	gcode = []
	
	currentE1 = E1beg
	
	for i in range(0,Nstep+1):
		currentE1 = E1beg + step * i		
		if ( i%2 == 0 ):
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2beg) + f(feedrate))
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2end) + f(feedrate))
		else:
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2end) + f(feedrate))
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2beg) + f(feedrate))
			

	if ( abs(currentE1 - E1end) > 1E-4 ):
		currentE1 = E1end
		if ( Nstep%2 == 0 ):
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2end) + f(feedrate))
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2beg) + f(feedrate))
		else: 
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2beg) + f(feedrate))
			gcode.append(G1 + cs.E1(currentE1) + cs.E2(E2end) + f(feedrate))
	return gcode

# Traces a path to fill a rectangle following its contour.
# The contourDirection defines motion in clockwise (0) or 
# counterclockwise (1) direction. The feedrate is given by 'feedrate'.
# The progressive step is given by 'step'.
# coordSystem is used to choose the plane of the rectangle.
def contourFilled(coordSystem, contourDirection, E1beg, E1end, E2beg, E2end, step, feedrate):
    # TODO
    return []
    
# Traces a path to along a rectangle contour.
# The contourDirection defines motion in clockwise (0) or 
# counterclockwise (1) direction. The feedrate is given by 'feedrate'.
# coordSystem is used to choose the plane of the rectangle.
def contour(coordSystem, contourDirection, E1beg, E1end, E2beg, E2end, feedrate):
    # TODO    
    return []



# For testing
if __name__ == "__main__":
    cs = coordSystem("X","Y","Z")
    E1beg = 0.0
    E1end = 100.0
    E2beg = 0.0
    E2end = 200.0
    step  = 10.0
    feedrate = 120.0
    gc = zigZagFilled(cs, E1beg, E1end, E2beg, E2end, step, feedrate)
    
    for line in gc:
        print(line)
