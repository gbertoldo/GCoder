#!/usr/bin/python

from Tkinter import *
from math import *
from gui.EntryFormWidget import *

class PreamblePostambleWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
 
        self.fields = []
        
        self.fields.append(IntegerEntry(name="Unit", label="0 = inches (G20), 1 = millimeters (G21)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Feedrate mode", label="0=(G93) Inverse time, 1=(G94) (mm or in)/min", value=1, lower=0, upper=1))
        self.fields.append(FloatEntry(name="Feedrate", label="according to the feedrate mode", value=60.0, lower=0.0, upper=100000.0))
        self.fields.append(FloatEntry(name="Spindle speed", label="(rev/min)", value=1000.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(IntegerEntry(name="Enable coolant", label="0 = No (M9), 1 = Yes (M7 and M8)", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Active plane", label="0 = XY (G17), 1 = ZX (G18), 2 = YZ (G19)", value=0, lower=0, upper=2))
        self.fields.append(IntegerEntry(name="Cutter radius compensation", label="0 = Off (G40), 1 = On", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Cutter length compensation", label="0 = Off (G49), 1 = On", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Coordinate system", label="1 to 9 = G54 to G59 and G59.1 to G59.3", value=1, lower=1, upper=9))
        self.fields.append(IntegerEntry(name="Path control mode", label="0 = Exact (G61), 1 = Blending (G64)", value=1, lower=0, upper=1))
        self.fields.append(FloatEntry(name="Path blending precision", label="Parameter P of G64, if G64 enable", value=0.001, lower=0.0, upper=1.0))
        self.fields.append(IntegerEntry(name="Distance mode", label="0 = Absolute (G90), 1 = Incremental (G91)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Stop spindle when finished", label="0 = No, 1 = Yes (M5)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Stop coolant when finished", label="0 = No, 1 = Yes (M9)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Program finished", label="0 = No, 1 = Yes (M2), 2 = Yes (M30)", value=1, lower=0, upper=2))
        self.fields.append(TextEntry(name="Custom preamble", label="Added after the generated preamble", value=""))
        self.fields.append(TextEntry(name="Custom postamble", label="Added before the generated postamble", value=""))

        EntryFormWidget(self, self.fields, width=10).grid(sticky="E")


    def feedrateModeSelected(self):
        print("feedrate mode selected")
    
    def coolantModeSelected(self):
        print("coolant mode selected")


