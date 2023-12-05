#!/usr/bin/python

# -*- coding: utf-8 -*-

from Tkinter import *
from math import *
import os
from collections import OrderedDict

from EntryFormWidget import *
from subroutines.GCoder import *

class MillDrillXYWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(  FloatEntry(name="X",  label="Coord. X do centro do furo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Y",  label="Coord. Y do centro do furo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Zi", label="Valor de Z para inicio do furo (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="dZ", label="Profundidade do furo: Z inicial - Z final (mm ou in)", value=2.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="F",  label="Taxa de corte em Z (mm/min ou in/min)", value=30.0, lower=0.0, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Zs", label="Altura segura para movimentacao (mm ou in)", value=5.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        
        self.inputFrm   = Frame(self, bd=5)
        self.inputFrm.grid(row=0, column=0, sticky="E"+"W")
        self.form = EntryFormWidget(self.inputFrm, self.fields, width=10)
        self.form.grid(row=0, column=0, sticky="E"+"W")
        
        self.addButton  = Button(self.inputFrm, text="Adicionar", command=self.addButtonPressed)
        self.addButton.grid()
       
        self.drillFrm = Frame(self, bd=5)
        self.drillFrm.grid()
        
              
        self.listboxFrm = Frame(self.drillFrm, bd=5)
        self.listboxFrm.grid(row=0,column=0, sticky="W")
        self.listbox = Listbox(self.listboxFrm, selectmode=SINGLE, height=20, width=90)
        self.listboxScroll = Scrollbar(self.listboxFrm, command=self.listbox.yview)
        self.xlistboxScroll = Scrollbar(self.listboxFrm, command=self.listbox.xview)
        self.listbox.configure(yscrollcommand=self.listboxScroll.set)
        self.listbox.configure(xscrollcommand=self.xlistboxScroll.set)
        self.listbox.pack(expand=YES, side=LEFT)
        self.listboxScroll.pack(expand=YES, side=RIGHT, fill=Y)
        #self.listbox.bind('<Double-1>',lambda x: self.addOperationButtonPressed())

        self.buttonsFrm = Frame(self.drillFrm, bd=5)
        self.buttonsFrm.grid(row=0, column=1, sticky="W")
        self.moveUpButton = Button(self.buttonsFrm, text="Subir", command=self.moveUpButtonPressed)
        self.moveUpButton.grid(sticky=W+E, padx=3, pady=3)
        self.moveDwButton = Button(self.buttonsFrm, text="Descer", command=self.moveDwButtonPressed)
        self.moveDwButton.grid(sticky=W+E, padx=3, pady=3)
        Label(self.buttonsFrm, text="\n\n").grid()
        self.delButton = Button(self.buttonsFrm, text="Remover", command=self.delButtonPressed)
        self.delButton.grid(sticky=W+E, padx=3, pady=3)
        
        
    def addButtonPressed(self):
        fields = self.form.getFields()
        X  = filter(lambda variable: variable['name'] == "X", fields)[0]['value']
        Y  = filter(lambda variable: variable['name'] == "Y", fields)[0]['value']
        Zi = filter(lambda variable: variable['name'] == "Zi", fields)[0]['value']
        dZ = filter(lambda variable: variable['name'] == "dZ", fields)[0]['value']
        F  = filter(lambda variable: variable['name'] == "F", fields)[0]['value']
        Zs = filter(lambda variable: variable['name'] == "Zs", fields)[0]['value']
        entry = [] 
        entry.append(['X',  X])
        entry.append(['Y',  Y])
        entry.append(['Zi',Zi])
        entry.append(['dZ',dZ])
        entry.append(['F',  F])
        entry.append(['Zs',Zs])
        self.listbox.insert(END,str(entry))
        
    def delButtonPressed(self):
        index=-1
        try:
            index = self.listbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
        
        self.listbox.delete(index)

        
    def moveUpButtonPressed(self):
        index=-1
        try:
            index = self.listbox.curselection()[0]
        except:
            return
        if ( index < 1 ):
            return
        tmp1 = self.listbox.get(index-1)
        tmp2 = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.delete(index-1)
        self.listbox.insert(index-1,tmp2)
        self.listbox.insert(index,  tmp1)
        
        
    def moveDwButtonPressed(self):
        index=-1
        try:
            index = self.listbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
        if ( index+1 >= self.listbox.size() ):
            return
        tmp1 = self.listbox.get(index)
        tmp2 = self.listbox.get(index+1)
        self.listbox.delete(index+1)
        self.listbox.delete(index)
        self.listbox.insert(index,   tmp2)
        self.listbox.insert(index+1, tmp1)


    @staticmethod
    def getOperationLabel():
        return "Furacao (XY)"

    def getFields(self):
        data = []
        for index in range(0,self.listbox.size()):
            data.append(self.listbox.get(index))
        return [self.form.getFields(),data]
    
    def setFields(self, fields):
        self.form.setFields(fields[0])
        for item in fields[1]:
            self.listbox.insert(END, item)
        return
        
    def getGCode(self):
        def extract(var,txt):
            return txt.split("'"+var+"',")[1].split("]")[0]
        
        fields = self.getFields()
        
        gcode = []
        
        for index in range(0,self.listbox.size()):
            item = self.listbox.get(index)

            # Extracting data
            X=float(extract("X",item))
            Y=float(extract("Y",item))
            Zi=float(extract("Zi",item))
            dZ=float(extract("dZ",item))
            F=float(extract("F",item))
            Zs=float(extract("Zs",item))
            # Moving to z safe
            gcode.append(G0+z(Zs))
            # Moving to the center of the point
            gcode.append(G0+x(X)+y(Y))
            # Moving to the starting point
            gcode.append(G0+z(Zi+0.5))
            # Drilling
            gcode.append(G1+z(Zi-dZ)+f(F))
            # Moving to z safe
            gcode.append(G0+z(Zs))
            
        return gcode

if __name__ == "__main__":
    app = MillDrillXY(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
