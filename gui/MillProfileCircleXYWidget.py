# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.MillProfileCircleXY 

class MillProfileCircleXYWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        
        self.fields.append(IntegerEntry(name="Corte interno/externo",                 label="0 = interno, 1 = externo", value=0, lower=0, upper=1))
        self.fields.append(  FloatEntry(name="Xref",                                  label="Coord. X do centro do circulo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Yref",                                  label="Coord. Y do centro do circulo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="D",                                     label="Diametro do circulo (mm ou in)", value=50.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z seguro",                              label="Altura segura para movimentacao (mm ou in)", value=5.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z inicial",                             label="Valor de Z para inicio de fresagem (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Profundidade do corte",                 label="Z inicial - Z final (mm ou in)", value=2.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em Z",                            label="Altura do passo em Z (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em Z",                    label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em X e Y",                label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Diametro da fresa",                     label="Diametro da ferramenta de corte (mm ou in)", value=5.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(  IntegerEntry(name="Sentido do corte",                    label="Sentido (0=horário, 1=anti-horario)", value=0, lower=0, upper=1))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        
    @staticmethod
    def getOperationLabel():
        return "Perfil circular (XY)"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
        
        fields = self.getFields()
        
        gcode = []
        
        toolPosition = filter(lambda variable: variable['name'] == "Corte interno/externo", fields)[0]['value']

        if (toolPosition == 0):
            isToolInside = True
        else:
            isToolInside = False
                   
        Xref = filter(lambda variable: variable['name'] == "Xref", fields)[0]['value']
        Yref = filter(lambda variable: variable['name'] == "Yref", fields)[0]['value']
        D = filter(lambda variable: variable['name'] == "D", fields)[0]['value']
        Zsafe = filter(lambda variable: variable['name'] == "Z seguro", fields)[0]['value']
        Zi = filter(lambda variable: variable['name'] == "Z inicial", fields)[0]['value']
        DZ = filter(lambda variable: variable['name'] == "Profundidade do corte", fields)[0]['value']
        Zf = Zi-DZ
        stepZ = filter(lambda variable: variable['name'] == "Passo em Z", fields)[0]['value']
        feedrateZ = filter(lambda variable: variable['name'] == "Taxa de corte em Z", fields)[0]['value']
        feedrateXA = filter(lambda variable: variable['name'] == "Taxa de corte em X e Y", fields)[0]['value']
        toolDiameter = filter(lambda variable: variable['name'] == "Diametro da fresa", fields)[0]['value']
        contourDir = filter(lambda variable: variable['name'] == "Sentido do corte", fields)[0]['value']
    
        gcode = subroutines.MillProfileCircleXY.millProfileCircleXY(Xref, Yref, D, Zi, Zf, Zsafe, stepZ, feedrateXA, feedrateZ, toolDiameter, isToolInside, contourDir)

        return gcode

if __name__ == "__main__":
    app = MillProfileCircleXYWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
