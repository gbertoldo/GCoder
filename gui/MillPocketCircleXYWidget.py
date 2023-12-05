# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.MillPocketCircleXY 

class MillPocketCircleXYWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(  FloatEntry(name="Xref",                                  label="Coord. X do centro do circulo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Yref",                                  label="Coord. Y do centro do circulo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="D",                                     label="Diametro do circulo (mm ou in)", value=50.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z seguro",                              label="Altura segura para movimentacao (mm ou in)", value=5.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z inicial",                             label="Valor de Z para inicio de fresagem (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Profundidade do corte",                 label="Z inicial - Z final (mm ou in)", value=2.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em R",                            label="Passo na direcao radial (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em Z",                            label="Altura do passo em Z (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo de acabamento em R",              label="Passo de acabamento na direcao radial (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo de acabamento em Z",              label="Passo de acabamento em Z (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em Z",                    label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em X e Y",                label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Diametro da fresa",                     label="Diametro da ferramenta de corte (mm ou in)", value=5.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(  IntegerEntry(name="Sentido do corte",                    label="Sentido (0=horário, 1=anti-horario)", value=0, lower=0, upper=1))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        
    @staticmethod
    def getOperationLabel():
        return "Cavidade circular (XY)"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
        
        fields = self.getFields()
        
        gcode = []
        
        Xref = extractValue('Xref',fields)
        Yref = extractValue('Yref',fields)
        D    = extractValue('D',fields)
        Zsafe = extractValue('Z seguro',fields)
        Zi = extractValue('Z inicial',fields)
        DZ = extractValue('Profundidade do corte',fields)
        Zf = Zi-DZ
        stepR = extractValue('Passo em R',fields)
        stepZ = extractValue('Passo em Z',fields)
        dRfinishing = extractValue('Passo de acabamento em R',fields)
        dZfinishing = extractValue('Passo de acabamento em Z',fields)
        feedrateZ = extractValue('Taxa de corte em Z',fields)
        feedrateR = extractValue('Taxa de corte em X e Y',fields)
        toolDiameter = extractValue('Diametro da fresa',fields)
        contourDir = extractValue('Sentido do corte',fields)
    
        gcode = subroutines.MillPocketCircleXY.millPocketCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepR, stepZ, dRfinishing, dZfinishing, feedrateR, feedrateZ, toolDiameter, contourDir)

        return gcode

if __name__ == "__main__":
    app = MillPocketCircleXYWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
