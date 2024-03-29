# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.MillProfileRoundedRectangleXA

class MillProfileRoundedRectangleXAWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        
        self.fields.append(IntegerEntry(name="Corte interno/externo",               label="0 = interno, 1 = externo", value=0, lower=0, upper=1))
        self.fields.append(  FloatEntry(name="Xref",                                label="Coord. X do centro do retangulo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Aref",                                label="Coord. A do centro do retangulo (graus)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="DX",                                  label="Largura do ret. em X (mm ou in)", value=50.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="DA",                                  label="Largura do ret. em A (graus)", value=90.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Rcyl",                                label="Raio do cilindro (mm ou in)", value=50.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Rc",                                  label="Raio do canto do ret. (mm ou in)", value=10.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z seguro",                            label="Altura segura para movimentacao (mm ou in)", value=5.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z inicial",                           label="Valor de Z para inicio de fresagem (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Profundidade do corte",               label="Z inicial - Z final (mm ou in)", value=2.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em Z",                          label="Altura do passo em Z (mm ou in)", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em Z",                  label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em X e A",              label="Taxa de corte (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Diametro da fresa",                   label="Diametro da ferramenta de corte (mm ouin)", value=5.0, lower=0.01, upper=FLOATUPPERBOUND))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        # Loading the image
        self.img = PIL.Image.open(os.path.dirname(os.path.abspath(__file__))+"/fig/MillProfileRoundedRectangleFig0.png")
        ratio = 1.0
        maxSize = 300.0
        if self.img.width > self.img.height:
            ratio = maxSize/self.img.width
        else:
            ratio = maxSize/self.img.height

        self.img = self.img.resize((int(self.img.width*ratio),int(self.img.height*ratio)),3)

        self.img = ImageTk.PhotoImage(self.img)
        
        Label(self, image = self.img).grid(row=0,column=1,padx=20,sticky=W+E)

    @staticmethod
    def getOperationLabel():
        return "Perfil retangular arredondado (XA)"

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
        Aref = filter(lambda variable: variable['name'] == "Aref", fields)[0]['value']
        DX = filter(lambda variable: variable['name'] == "DX", fields)[0]['value']
        DA = filter(lambda variable: variable['name'] == "DA", fields)[0]['value']
        Rcyl = filter(lambda variable: variable['name'] == "Rcyl", fields)[0]['value']
        Rc = filter(lambda variable: variable['name'] == "Rc", fields)[0]['value']
        Zsafe = filter(lambda variable: variable['name'] == "Z seguro", fields)[0]['value']
        Zi = filter(lambda variable: variable['name'] == "Z inicial", fields)[0]['value']
        DZ = filter(lambda variable: variable['name'] == "Profundidade do corte", fields)[0]['value']
        Zf = Zi-DZ
        stepZ = filter(lambda variable: variable['name'] == "Passo em Z", fields)[0]['value']
        feedrateZ = filter(lambda variable: variable['name'] == "Taxa de corte em Z", fields)[0]['value']
        feedrateXA = filter(lambda variable: variable['name'] == "Taxa de corte em X e A", fields)[0]['value']
        toolDiameter = filter(lambda variable: variable['name'] == "Diametro da fresa", fields)[0]['value']
        dLacc=0.1
    
        gcode = subroutines.MillProfileRoundedRectangleXA.millProfileRoundedRectXA(Xref, Aref, DX, DA, Rcyl, Rc, dLacc, Zi, Zf, Zsafe, stepZ, feedrateXA, feedrateZ, toolDiameter, isToolInside)

        return gcode

if __name__ == "__main__":
    app = MillProfileRoundedRectangleXAWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
