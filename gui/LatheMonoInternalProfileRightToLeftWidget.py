# -*- coding: utf-8 -*-
#!/usr/bin/python

from Tkinter import *
import tkFileDialog
import tkMessageBox
from math import *
import PIL.Image
from PIL import ImageTk
import os

from EntryFormWidget import *
import subroutines.LatheMonotonicPath as LatheMonotonicPath

class LatheMonoInternalProfileRightToLeftWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bd=5)
 
        self.fields = []
        
        self.fields.append(IntegerEntry(name="D/R",                                   label="0 = X=Diametro, 1 = X=Raio", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="D/R final",                             label="0 = X=Diametro, 1 = X=Raio (alterar para este modo ao concluir)", value=0, lower=0, upper=1))
        self.fields.append(  FloatEntry(name="Zi",                                    label="Coord. Z inicial (mm ou in)", value=0.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Xs",                                    label="Coord. X para movimentacao segura (mm ou in)", value=50.0, lower=FLOATLOWERBOUND, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="Rt",                                    label="Raio de curvatura da ponta da ferramenta (mm ou in)", value=1.0, lower=1E-5, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="dS",                                    label="Espessura da camada de acabamento (mm ou in)", value=0.05, lower=1E-5, upper=FLOATUPPERBOUND))
        self.fields.append(IntegerEntry(name="N",                                     label="Numero de passos de acabamento", value=1, lower=0, upper=INTUPPERBOUND))
        self.fields.append(  FloatEntry(name="dX",                                    label="Passo do corte (mm ou in)", value=0.2, lower=0.001, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="TC-Z",                                  label="Taxa de corte em Z (mm/min ou in/min)", value=60.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="TC-X",                                  label="Taxa de corte em X (mm/min ou in/min)", value=60.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(  FloatEntry(name="TC-F",                                  label="Taxa de corte de acabamento (mm/min ou in/min)", value=30.0, lower=0.01, upper=FLOATUPPERBOUND))
        self.fields.append(IntegerEntry(name="CCI",                                   label="Condicao de contorno inicial (0=tangente a Z, 1=tangente a X)", value=0, lower=0, upper=1))
        self.fields.append(IntegerEntry(name="CCF",                                   label="Condicao de contorno final (0=tangente a Z, 1=tangente a X)", value=1, lower=0, upper=1))
        
        self.form = EntryFormWidget(self, self.fields, width=10)
        
        self.form.grid(row=0, column=0, sticky="E")

        # Loading the image
        self.img = PIL.Image.open(os.path.dirname(os.path.abspath(__file__))+"/fig/TurningInternalRightToLeft.png") 
        ratio = 1.0
        maxSize = 300.0
        if self.img.width > self.img.height:
            ratio = maxSize/self.img.width
        else:
            ratio = maxSize/self.img.height

        self.img = self.img.resize((int(self.img.width*ratio),int(self.img.height*ratio)),3)

        self.img = ImageTk.PhotoImage(self.img)
        
        Label(self, image = self.img).grid(row=0,column=1,padx=20,sticky=W+E)

        self.selectFileBtn = Button(self, text="Selecionar arquivo de contorno", command=self.selectFileButtonPressed).grid(row=1,column=1, pady=2)
        Button(self, text="Ajuda", command=self.helpButtonPressed).grid(row=1,column=2, pady=2)

        self.dirname = "~/"
        self.basename = "Nenhum arquivo selecionado"

        self.setContourFileName(self.basename)


    @staticmethod
    def getOperationLabel():
        return "Perfil interno (dir. -> esq.)"

    def getFields(self):
        fields = dict()
        fields["formfields"] = self.form.getFields() 
        fields["dirname"] = self.dirname
        fields["basename"] = self.basename
        return fields
    
    def setFields(self, fields):
        self.form.setFields(fields["formfields"])
        self.dirname = fields["dirname"]
        self.basename = fields["basename"]
        self.setContourFileName(self.basename)
        return
        
    def getGCode(self):
        
        gcode = []
        fields = self.getFields()
        filename = fields["dirname"]+"/"+fields["basename"]
        formfields = fields["formfields"]

        DRMode = extractValue('D/R',formfields)
        DRModef = extractValue('D/R final',formfields)
        zi = extractValue("Zi",formfields)
        rsafe = extractValue("Xs",formfields)
        rc = extractValue("Rt",formfields)
        dsfinishing = extractValue("dS",formfields)
        Nfinishing = extractValue("N",formfields)
        stepR = extractValue("dX",formfields)
        feedrateZ = extractValue("TC-Z",formfields)
        feedrateR = extractValue("TC-X",formfields)
        feedrateFinishing = extractValue("TC-F",formfields)
        bci = extractValue("CCI",formfields)
        bcf = extractValue("CCF",formfields)

        path = self.readFile(filename)

        # If in diameter mode, converts X to radius 
        if DRMode == 0: 
            rsafe = 0.5 * rsafe
            stepR = 0.5 * stepR
            feedrateR = 0.5 * feedrateR
            for p in path:
                p[1] = 0.5 * p[1]

        gcode = LatheMonotonicPath.turnInternalProfileRightToLeft(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing)

        if DRModef == 0:
            gcode.append("G7") # diameter mode
        else: 
            gcode.append("G8") # radius mode
        return gcode

    def setContourFileName(self, filename):
        Label(self, text=filename,bg='#000', fg='#ff0').grid(row=1,column=0,padx=20,sticky=W+E) 


    def selectFileButtonPressed(self):
        filename = tkFileDialog.askopenfilename(initialdir = "~/",title = "Selecionar arquivo de contorno",filetypes = (("txt","*.txt"),("todos","*.*")))
        if filename:
            self.dirname = os.path.dirname(filename)
            self.basename = os.path.basename(filename)
        else:
            self.dirname = '~/'
            self.basename = 'Nenhum arquivo selecionado'
        self.setContourFileName(self.basename)
        self.readFile(filename)


    def helpButtonPressed(self):
        tkMessageBox.showinfo(title="Como carregar o contorno", message="Arquivo de texto simples (.txt) com os pontos (Z,X) do contorno.\n Requisitos: \n * Z na primeira coluna e X na segunda. \n * Usar espaco para separar Z e X. \n * Usar ponto como separador decimal. \n * Z monotonicamente crescente. \n * X monotonicamente decrescente. \n\n Exemplo: \n 0.0 10.0 \n 10.0 10.0 \n 10.0 0.0")

    def readFile(self, filename):
        contour = []
        try:
            with open(filename) as ifile:
                for line in ifile.readlines():
                    sline = line.split(" ")
                    contour.append([float(sline[0]),float(sline[1])])
        except:
            contour = None
        
        if contour is None:
            tkMessageBox.showerror(title="Erro de leitura", message="Verifique a formatacao do arquivo. Consulte Ajuda para mais informacoes.")
        else:
            fields = self.getFields()
            formfields = fields["formfields"]
            zi = extractValue("Zi",formfields)
            rsafe = extractValue("Xs",formfields)
            rc = extractValue("Rt",formfields)
            listOfErrors = LatheMonotonicPath.isTurnInternalProfileRightToLeftFeasible(zi, rsafe, rc, contour)
            for err in listOfErrors:
                tkMessageBox.showerror(title="Erro", message=err)
        return contour

if __name__ == "__main__":
    app = LatheMonoInternalProfileRightToLeftWidget(None)
    app.grid()
    app.master.title("Test")
    app.mainloop()
