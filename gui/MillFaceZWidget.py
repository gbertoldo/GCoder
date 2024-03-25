#!/usr/bin/python

from Tkinter import *
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.MillFace

class MillFaceZWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(IntegerEntry(name="Direcao do zigue-zague",              label="0 = X, 1 = Y", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Ponto de referencia",                 label="0 a 3", value=0, lower=0, upper=3))
        self.fields.append(  FloatEntry(name="Xref",                                label="Coord. X do ponto de referencia", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Yref",                                label="Coord. Y do ponto de referencia", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Lx",                                  label="Comprimento do retangulo em X", value=100.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Ly",                                  label="Comprimento do retangulo em Y", value=100.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Diametro da fresa",                   label="Diametro da ferramenta de corte", value=5.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z seguro",                            label="Altura segura para movimentacao", value=5.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Z inicial",                           label="Valor de Z de inicio do faceamento", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Profundidade do faceamento",          label="Z inicial - Z final", value=10.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em X e Y",                      label="Passo do zigue-zague em X e Y", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo em Z",                          label="Altura do passo em Z", value=1.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Passo de acabamento em Z",            label="Passo de acabamento", value=0.2, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em Z",                  label="Taxa de corte", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Taxa de corte em X e Y",              label="Taxa de corte", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))

        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        # Loading the image
        self.img = PIL.Image.open(os.path.dirname(os.path.abspath(__file__))+"/fig/MillFaceZFig0.png")
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
        return "Faceamento em Z"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
        
        fields = self.getFields()
        
        gcode = []
                        
        zigZagDir = filter(lambda variable: variable['name'] == "Direcao do zigue-zague", fields)[0]['value']
        RefPos = filter(lambda variable: variable['name'] == "Ponto de referencia", fields)[0]['value']
        Xref = filter(lambda variable: variable['name'] == "Xref", fields)[0]['value']
        Yref = filter(lambda variable: variable['name'] == "Yref", fields)[0]['value']
        DX = filter(lambda variable: variable['name'] == "Lx", fields)[0]['value']
        DY = filter(lambda variable: variable['name'] == "Ly", fields)[0]['value']
        toolDiameter = filter(lambda variable: variable['name'] == "Diametro da fresa", fields)[0]['value']
        Zsafe = filter(lambda variable: variable['name'] == "Z seguro", fields)[0]['value']
        Zi = filter(lambda variable: variable['name'] == "Z inicial", fields)[0]['value']
        DZ = filter(lambda variable: variable['name'] == "Profundidade do faceamento", fields)[0]['value']
        Zf = Zi-DZ
        stepXY = filter(lambda variable: variable['name'] == "Passo em X e Y", fields)[0]['value']
        stepZ = filter(lambda variable: variable['name'] == "Passo em Z", fields)[0]['value']
        finishingHeight = filter(lambda variable: variable['name'] == "Passo de acabamento em Z", fields)[0]['value']
        feedrateXY = filter(lambda variable: variable['name'] == "Taxa de corte em X e Y", fields)[0]['value']
        feedrateZ = filter(lambda variable: variable['name'] == "Taxa de corte em Z", fields)[0]['value']
        isToolInside = False
    
        gcode = subroutines.MillFace.faceZZigZag(zigZagDir, Xref, Yref, RefPos, DX, DY, Zi, Zf, finishingHeight, Zsafe, stepXY, stepZ, feedrateXY, feedrateZ, toolDiameter, isToolInside)

        return gcode

if __name__ == "__main__":
    app = MillFaceZWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
