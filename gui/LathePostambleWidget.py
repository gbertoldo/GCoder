#!/usr/bin/python

from Tkinter import *
from math import *
from EntryFormWidget import *

class LathePostambleWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
  
        self.fields = []
        
        self.fields.append(   TextEntry(name="Postambulo personalizado",        label="Adicionado antes dos seguintes comandos", value=""))
        self.fields.append(IntegerEntry(name="Parar o motor da fresa",          label="0 = Nao, 1 = Sim (M5)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Parar o liquido de refrigeracao", label="0 = Nao, 1 = Sim (M9)", value=1, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="Terminar o programa",             label="0 = Nao, 1 = Sim (M2), 2 = Sim (M30)", value=1, lower=0, upper=2))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        self.form.grid(sticky="E")

    @staticmethod
    def getOperationLabel():
        return "Postambulo"

    def getFields(self):
        return self.form.getFields()
    
    def setFields(self, fields):
        self.form.setFields(fields)
        return
        
    def getGCode(self):
        fields = self.getFields()
        gcode = []
        
        var = filter(lambda variable: variable['name'] == "Postambulo personalizado", fields)[0]
        if var['value'] != "":
            gcode.append(var['value'])
       
        var = filter(lambda variable: variable['name'] == "Parar o motor da fresa", fields)[0]
        if var['value'] == 1:
            gcode.append("M5; Disable spindle")

        var = filter(lambda variable: variable['name'] == "Parar o liquido de refrigeracao", fields)[0]
        if var['value'] == 1:
            gcode.append("M9; Disable coolant")
        
        var = filter(lambda variable: variable['name'] == "Terminar o programa", fields)[0]
        if var['value'] == 1:
            gcode.append("M2; End the program")
        elif var['value'] == 2:
            gcode.append("M30; Exchange pallet shuttles and end the program")
            
        return gcode


if __name__ == "__main__":
    app = LathePostambleWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
