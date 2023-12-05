#!/usr/bin/python

from Tkinter import *
import tkMessageBox

# Constants
INTLOWERBOUND = -10000000
INTUPPERBOUND =  10000000
FLOATLOWERBOUND = -1E15
FLOATUPPERBOUND =  1E15

def IntegerEntry(name, label, value=0, lower=INTLOWERBOUND, upper=INTUPPERBOUND):
    """
        Returns a dictionary for collecting integer data in the EntryFormWidget class.
    """
    return {"name": name, "type": "int", "label": label, "value": value, "lower": lower, "upper": upper}
    

def FloatEntry(name, label, value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND):
    """
        Returns a dictionary for collecting float data in the EntryFormWidget class.
    """
    return {"name": name, "type": "float", "label": label, "value": value, "lower": lower, "upper": upper}


def TextEntry(name, label, value=""):
    """
        Returns a dictionary for collecting text data in the EntryFormWidget class.
    """
    return {"name": name, "type": "text", "label": label, "value": value}

def extractValue(name, fields):
    """
        Extracts the value of variable 'name' from fields
    """
    return filter(lambda variable: variable['name'] == name, fields)[0]['value']

class EntryFormWidget(Frame):
    """
        EntryFormWidget simplify the creation of forms.
    """
    def __init__(self, master, fields, width=15):
        """
            Initializing the class
        """
        Frame.__init__(self, master)
        self.fields = fields
        
        crow = 0
        ccol = 0
        self.data = []
        for field in fields:
            self.data.append(StringVar())
            self.data[crow].set(field["value"])
            Label(self,text=field["name"]).grid(row=crow,column=ccol,sticky=E)
            Entry(self, textvariable=self.data[crow], width=width, justify="right").grid(row=crow,column=ccol+1)
            Label(self,text=field["label"]).grid(row=crow,column=ccol+2,sticky=W)
            crow = crow+1

    def getFields(self):
        """
            Return a list of fields
        """
        crow = 0;
        for field in self.fields:
            if ( field["type"] == "float" ):
                try:
                    field["value"] = float(self.data[crow].get())
                    if ( field["value"] < field["lower"] or field["value"] > field["upper"] ):
                        tkMessageBox.showerror('Intervalo incorreto', "A variavel " + field["name"] + " esta fora do intervalo: ["+str(field["lower"])+";"+str(field["upper"])+"].")
                        return []
                except:
                    tkMessageBox.showerror('Tipo incorreto', "A variavel " + field["name"] + " deve ser real.")
                    return []
            elif ( field["type"] == "int" ):
                try:
                    field["value"] = int(self.data[crow].get())
                    if ( field["value"] < field["lower"] or field["value"] > field["upper"] ):
                        tkMessageBox.showerror('Intervalo incorreto', "A variavel " + field["name"] + " esta fora do intervalo: ["+str(field["lower"])+";"+str(field["upper"])+"].")
                        return []
                except:
                    tkMessageBox.showerror('Tipo incorreto', "A variavel " + field["name"] + " deve ser inteira.")
                    return []
            else:
                field["value"] = str(self.data[crow].get())
            crow = crow+1
        return self.fields

    def setFields(self, fields):
        """
            Sets the fields
        """
        crow = 0;
        for field in fields:
            if ( field["type"] == "float" ):
                try:
                    self.data[crow].set(float(field["value"]))
                    if ( field["value"] < field["lower"] or field["value"] > field["upper"] ):
                        tkMessageBox.showerror('Range error', "Variable " + field["name"] + " is out of range: ["+str(field["lower"])+";"+str(field["upper"])+"].")
                        return []
                except:
                    tkMessageBox.showerror('Type error', "Variable " + field["name"] + " must be a float.")
                    return []
            elif ( field["type"] == "int" ):
                try:
                    self.data[crow].set(int(field["value"]))
                    if ( field["value"] < field["lower"] or field["value"] > field["upper"] ):
                        tkMessageBox.showerror('Range error', "Variable " + field["name"] + " is out of range: ["+str(field["lower"])+";"+str(field["upper"])+"].")
                        return []
                except:
                    tkMessageBox.showerror('Type error', "Variable " + field["name"] + " must be an integer.")
                    return []
            else:
                self.data[crow].set(str(field["value"]))
            crow = crow+1
        return
