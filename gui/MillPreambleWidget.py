#!/usr/bin/python

from Tkinter import *
from math import *
from EntryFormWidget import *

class MillPreambleWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
  
        self.fields = []
        
        self.fields.append(IntegerEntry(name="Unidade",                             label="0 = polegadas (G20), 1 = milimetros (G21)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Modo de taxa de corte (feedrate)",    label="0=(G93) Tempo inverso, 1=(G94) (mm ou in)/min", value=1, lower=0, upper=1))
        self.fields.append(  FloatEntry(name="Taxa de corte (feedrate)",            label="de acordo com o modo da taxa de corte", value=60.0, lower=0.0, upper=100000.0))
        self.fields.append(  FloatEntry(name="Velocidade do spindle",               label="(rev/min)", value=1000.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(IntegerEntry(name="Ativar refrigeracao",                 label="0 = Nao (M9), 1 = Sim (M7 and M8)", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Plano ativo",                         label="0 = XY (G17), 1 = ZX (G18), 2 = YZ (G19)", value=0, lower=0, upper=2))
        self.fields.append(IntegerEntry(name="Cutter - compensacao de raio",        label="0 = Nao (G40), 1 = Sim", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Cutter - compensacao de comprimento", label="0 = Nao (G49), 1 = Sim", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Sistema de coordenadas",              label="1 a 6 -> G54 a G59 e 7 a 9 -> G59.1 a G59.3", value=1, lower=1, upper=9))
        self.fields.append(IntegerEntry(name="Modo de controle de caminho",         label="0 = Exato (G61), 1 = Curvado (G64)", value=1, lower=0, upper=1))
        self.fields.append(  FloatEntry(name="Precisao do modo G64",                label="Parametro P do comando G64, se ativado", value=0.001, lower=0.0, upper=1.0))
        self.fields.append(IntegerEntry(name="Modo de distancia",                   label="0 = Absoluto (G90), 1 = Incremental (G91)", value=0, lower=0, upper=1))
        self.fields.append(   TextEntry(name="Preambulo personalizado",             label="Adicionado apos os comandos acima", value=""))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        self.form.grid(sticky="E")

    @staticmethod
    def getOperationLabel():
        return "Preambulo"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
        
        fields = self.getFields()
        
        gcode = []
        
        var = filter(lambda variable: variable['name'] == "Unidade", fields)[0]
        if var['value'] == 0:
            gcode.append("G20; inches")
        else:
            gcode.append("G21; millimiters")
            
        var = filter(lambda variable: variable['name'] == "Modo de taxa de corte (feedrate)", fields)[0]
        if var['value'] == 0:
            gcode.append("G93;  Feedrate mode: inverse time")
        else:
            gcode.append("G94; Feedrate mode: (mm or in)/min")       
            
        var = filter(lambda variable: variable['name'] == "Taxa de corte (feedrate)", fields)[0]
        gcode.append("F%.4f; Feedrate"%(var['value']))
        
        var = filter(lambda variable: variable['name'] == "Velocidade do spindle", fields)[0]
        gcode.append("M3 S%.4f; Enable spindle in the clockwise direction"%(var['value']))
        
        var = filter(lambda variable: variable['name'] == "Ativar refrigeracao", fields)[0]
        if var['value'] == 0:
            gcode.append("M9; Disable coolants")
        else:
            gcode.append("M7 M8; Enable coolants")   
            
        var = filter(lambda variable: variable['name'] == "Plano ativo", fields)[0]
        if var['value'] == 0:
            gcode.append("G17; Active plane: XY")
        elif var['value'] == 1:
            gcode.append("G18; Active plane: ZX")
        else:
            gcode.append("G19; Active plane: YZ")

        var = filter(lambda variable: variable['name'] == "Cutter - compensacao de raio", fields)[0]
        if var['value'] == 0:
            gcode.append("G40; No cutter radius compensation")
        
        var = filter(lambda variable: variable['name'] == "Cutter - compensacao de comprimento", fields)[0]
        if var['value'] == 0:
            gcode.append("G49; No cutter length compensation")
        
        var = filter(lambda variable: variable['name'] == "Sistema de coordenadas", fields)[0]
        if var['value'] == 1:
            gcode.append("G54; Sistema de coordenadas 1")
        elif var['value'] == 2:
            gcode.append("G55; Sistema de coordenadas 2")
        elif var['value'] == 3:
            gcode.append("G56; Sistema de coordenadas 3")
        elif var['value'] == 4:
            gcode.append("G57; Sistema de coordenadas 4")
        elif var['value'] == 5:
            gcode.append("G58; Sistema de coordenadas 5")
        elif var['value'] == 6:
            gcode.append("G59; Sistema de coordenadas 6")
        elif var['value'] == 7:
            gcode.append("G59.1; Sistema de coordenadas 7")
        elif var['value'] == 8:
            gcode.append("G59.2; Sistema de coordenadas 8")
        else:
            gcode.append("G59.3; Sistema de coordenadas 9")
            
        var = filter(lambda variable: variable['name'] == "Modo de controle de caminho", fields)[0]
        if var['value'] == 0:
            gcode.append("G61; Path mode: exact")        
        else:
            var = filter(lambda variable: variable['name'] == "Precisao do modo G64", fields)[0]
            gcode.append("G64 P%.4f; Path mode: blended"%(var['value']))

        var = filter(lambda variable: variable['name'] == "Modo de distancia", fields)[0]
        if var['value'] == 0:
            gcode.append("G90; Distance mode: absolute")        
        else:
            gcode.append("G91; Distance mode: relative")        
        
        var = filter(lambda variable: variable['name'] == "Preambulo personalizado", fields)[0]
        if var['value'] != "":
            gcode.append(var['value'])

        return gcode

if __name__ == "__main__":
    app = MillPreambleWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
