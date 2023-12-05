# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.LathePocketD

class LathePocketDWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(  FloatEntry(name="Zi",                        label="Coord. Z inicial (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Zf",                        label="Coord. Z final (mm ou in)", value=-10.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Di",                        label="Diametro inicial (mm ou in)", value=21.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Df",                        label="Diametro final (mm ou in)", value=20.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="D seguro",                  label="Diametro seguro para movimentacao (mm ou in)", value=23.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em D",                label="Passo na direcao radial (mm ou in)", value=0.5, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo de acabamento em D",  label="Passo de acabamento na direcao radial (mm ou in)", value=0.1, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em Z",        label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em D",        label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        
    @staticmethod
    def getOperationLabel():
        return "Cavidade (corte longitudinal)"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
                
        gcode = []
        
        fields = self.form.getFields()

        Zi = extractValue("Zi",fields)
        Zf = extractValue("Zf",fields)
        Di = extractValue("Di",fields)
        Df = extractValue("Df",fields)
        Dsafe = extractValue("D seguro",fields)
        stepD = extractValue("Passo em D",fields)
        dDfinishing = extractValue("Passo de acabamento em D",fields)
        feedrateD = extractValue("Taxa de corte em D",fields)
        feedrateZ = extractValue("Taxa de corte em Z",fields)

        gcode = subroutines.LathePocketD.lathePocketD(Zi, Zf, Di, Df, Dsafe, stepD, dDfinishing, feedrateD, feedrateZ)

        return gcode

if __name__ == "__main__":
    app = LathePocketDWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
