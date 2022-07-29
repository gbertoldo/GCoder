#!/usr/bin/python

G0  = "G0 "
G1  = "G1 "
G90 = "G90 "

def g2(Xf, Yf, Xoff, Yoff, feedrate):
    return "G2 X%.4f Y%.4f I%.4f J%.4f F%.4f"%(float(Xf), float(Yf), float(Xoff), float(Yoff), float(feedrate))

def g3(Xf, Yf, Xoff, Yoff, feedrate):
    return "G3 X%.4f Y%.4f I%.4f J%.4f F%.4f"%(float(Xf), float(Yf), float(Xoff), float(Yoff), float(feedrate))

def x(value):
	return " X"+"{:.4f}".format(value)

def y(value):
	return " Y"+"{:.4f}".format(value)

def z(value):
	return " Z"+"{:.4f}".format(value)

def f(value):
	return " F"+"{:.4f}".format(value)

class coordSystem(object):
	def __init__(self, E1Axis, E2Axis, E3Axis):
		self.E1Axis = E1Axis
		self.E2Axis = E2Axis
		self.E3Axis = E3Axis
	def E1(self, val):
		return " "+self.E1Axis+"%.4f"%(val)
	def E2(self, val):
		return " "+self.E2Axis+"%.4f"%(val)
	def E3(self, val):
		return " "+self.E3Axis+"%.4f"%(val)
	
