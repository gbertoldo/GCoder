# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.LatheThreading

class LatheThreadingWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(  FloatEntry(name="Zi",                        label="Coord. Z inicial (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Zf",                        label="Coord. Z final (Zf<Zi=rosca direita; Zf>Zi=rosca invertida)(mm ou in)", value=-10.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Di",                        label="Diametro inicial (mm ou in)", value=21.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="D seguro",                  label="Diametro seguro (Ds>Di=rosca externa, Ds<Di=rosca interna) (mm ou in)", value=23.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo da rosca",            label="Passo da rosca (mm ou in)", value=1.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Profundidade da rosca",     label="Profundidade da rosca (mm ou in)", value=0.63, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo de corte",            label="Passo inicial de corte da ferramenta (mm ou in)", value=0.1, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  IntegerEntry(name="Passos de acabamento",    label="Numero de passos de acabamento", value=0, lower=0, upper=10))
        self.fields.append(  IntegerEntry(name="Modo de chanfro",         label="0=Sem chanfro, 1=entrada, 2=saida, 3=ambos", value=0, lower=0, upper=3))
        self.fields.append(  FloatEntry(name="Angulo de chanfro",         label="Angulo de chanfro (graus)", value=45.0, lower=30.0, upper=60.0))
          
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        
    @staticmethod
    def getOperationLabel():
        return "Rosqueamento"

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
        Dsafe = extractValue("D seguro",fields)
        threadPitch = extractValue("Passo da rosca",fields)
        threadDepth = extractValue("Profundidade da rosca",fields)
        stepD = extractValue("Passo de corte",fields)
        Nfinishing = extractValue("Passos de acabamento",fields)
        taperMode = extractValue("Modo de chanfro",fields)
        taperAngle = extractValue("Angulo de chanfro",fields)
        gcode = subroutines.LatheThreading.latheThreading(Zi, Zf, Di, Dsafe, threadPitch, threadDepth, stepD, Nfinishing, taperMode, taperAngle)

        return gcode

if __name__ == "__main__":
    app = LatheThreadingWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
