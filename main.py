#!/usr/bin/python

from Tkinter import *
import tkMessageBox
import PIL.Image
from PIL import ImageTk
import os
import copy
import pickle

from gui.MillPreambleWidget import *
from gui.MillPostambleWidget import *
from gui.LathePreambleWidget import *
from gui.LathePostambleWidget import *
from gui.widgetList import *

#
# Importing milling operations
#
for widget in millWidgetList:
    try:
        exec("import gui."+widget)
    except:
        print(";Erro fatal: impossivel importar "+"gui."+widget)
        exit()
    
#
# Importing turning operations
#
for widget in latheWidgetList:
    try:
        exec("import gui."+widget)
    except:
        print(";Erro fatal: impossivel importar  "+"gui."+widget)
        exit()


#
# The main application
#        
class Application(Frame):
    def __init__(self, master=None):
        #
        # Initializes the main application
        #
        Frame.__init__(self, master, bd=5)
        
        ################################################################
        #
        # Main variables
        #
        self.softwareVersion = 0

        # The job list is the set of operations selected and configured
        # by the user from the available list of operations
        self.millingJobList = []
        self.turningJobList = []
        
        # machineNumer: 0 = mill, 1 = lathe
        self.machineNumber = IntVar()
        self.machineNumber.set(0)
        
        # The operation of the millingJobList or turningJobList that is 
        # under edition by the user
        self.operationUnderEdition = None
        
        # Check variables to include or not the preamble and postamble (0=no, 1=yes)
        self.includePreamble = IntVar()
        self.includePostamble = IntVar()
        self.includePreamble.set(1)
        self.includePostamble.set(1)
        
        tmp = MillPreambleWidget(None)
        self.millPreambleOperation  = {"label":MillPreambleWidget.getOperationLabel(),  "className":"MillPreambleWidget",   "fields":tmp.getFields()}
        tmp.destroy()
        tmp = MillPostambleWidget(None)
        self.millPostambleOperation = {"label":MillPostambleWidget.getOperationLabel(),"className":"MillPostambleWidget", "fields":tmp.getFields()}
        tmp.destroy()
        tmp = LathePreambleWidget(None)
        self.lathePreambleOperation  = {"label":LathePreambleWidget.getOperationLabel(),  "className":"LathePreambleWidget",   "fields":tmp.getFields()}
        tmp.destroy()
        tmp = LathePostambleWidget(None)
        self.lathePostambleOperation = {"label":LathePostambleWidget.getOperationLabel(),"className":"LathePostambleWidget", "fields":tmp.getFields()}
        tmp.destroy()
        
        # projectFile contains the name of the file where the snapshot
        # of the last use of the application
        self.projectFile = os.path.dirname(os.path.abspath(__file__))+"/project.gcoder"
        
        # Trying to load snapshot from previous use
        if (os.path.exists(self.projectFile)):
            try:
                self.loadProject()
            except:
                print(";Impossivel carregar as ultimas configuracoes. Usando configuracoes predefinidas...")
                
        ################################################################
        #
        # LEFT FRAME
        #
        self.leftFrm  = Frame(self, bd = 5)
        self.leftFrm.grid(row=0, column=0)
        
        # Loading the LOGO image
        self.img = PIL.Image.open(os.path.dirname(os.path.abspath(__file__))+"/fig/logo.png")
        ratio = 1.0
        maxSize = 300.0
        if self.img.width > self.img.height:
            ratio = maxSize/self.img.width
        else:
            ratio = maxSize/self.img.height

        self.img = self.img.resize((int(self.img.width*ratio),int(self.img.height*ratio)),3)

        self.img = ImageTk.PhotoImage(self.img)
        
        Label(self.leftFrm, image = self.img).grid(row=0,column=0,sticky=W+E)
        
        # Creating the machine selector frame
        #---------------------------------------
        self.machineFrm = Frame(self.leftFrm, bd=15)
        
        self.machineFrm.grid()
        
        Radiobutton(self.machineFrm, text="Fresadora", value=0, var=self.machineNumber, command=self.machineSelected,indicatoron=0, bd=3).grid(row=0, column=0, ipadx=40, ipady=10)
        Radiobutton(self.machineFrm, text="Torno", value=1, var=self.machineNumber, command=self.machineSelected,indicatoron=0, bd=3).grid(row=0, column=1, ipadx=50, ipady=10)
        
        
        # Creating the operation selector frame
        #---------------------------------------
        self.operationsFrm = Frame(self.leftFrm, bd=5)
        
        self.operationsFrm.grid()
        
        self.preamblePostambleFrm = Frame(self.operationsFrm, bd=5)
        
        self.preamblePostambleFrm.grid(row=0,column=0)
               
        Checkbutton(self.preamblePostambleFrm, text='',variable=self.includePreamble, onvalue=1, offvalue=0, command=self.checkPreamblePressed).grid(row=0,column=0)        
        self.preambleButton  = Button(self.preamblePostambleFrm, text="Cabecalho", command=self.preambleButtonPressed)
        self.preambleButton.grid(row=0,column=1, padx=5)

        Checkbutton(self.preamblePostambleFrm, text='',variable=self.includePostamble, onvalue=1, offvalue=0, command=self.checkPostamblePressed).grid(row=0,column=2)
        self.postambleButton = Button(self.preamblePostambleFrm, text="Rodape", command=self.postambleButtonPressed)
        self.postambleButton.grid(row=0,column=3, ipadx=8, padx=5)
        
        
        Label(self.operationsFrm, text="Selecione uma operacao:").grid(row=1,column=0, sticky=W+E)
        
        self.operationListboxFrm = Frame(self.operationsFrm)
        self.operationListboxFrm.grid(row=2,column=0, sticky=W+E+N+S)
        self.operationListbox = Listbox(self.operationListboxFrm, selectmode=SINGLE, height=10, width=40)
        self.operationListboxScroll = Scrollbar(self.operationListboxFrm, command=self.operationListbox.yview)
        self.operationListbox.configure(yscrollcommand=self.operationListboxScroll.set)
        self.operationListbox.pack(expand=YES, side=LEFT)
        self.operationListboxScroll.pack(expand=YES, side=RIGHT, fill=Y)
        self.operationListbox.bind('<Double-1>',lambda x: self.addOperationButtonPressed())
                
        self.createOperations()

        self.selectOperationButton= Button(self.operationsFrm, text="Adicionar", command=self.addOperationButtonPressed).grid(row=3,column=0, sticky=W+E, pady=2)

        # Creating the job frame
        #--------------------------
        
        self.jobFrm = Frame(self.leftFrm, bd=5)
        
        self.jobFrm.grid()
                
        Label(self.jobFrm, text="Operacoes selecionadas:").grid(row=0,column=0, sticky=W+E)
                
        self.jobListboxFrm = Frame(self.jobFrm)
        self.jobListboxFrm.grid(row=1,column=0, sticky=W+E)
        self.jobListbox = Listbox(self.jobListboxFrm, selectmode=SINGLE, height=10, width=40)
        self.jobListboxScroll = Scrollbar(self.jobListboxFrm, command=self.jobListbox.yview)
        self.jobListbox.configure(yscrollcommand=self.jobListboxScroll.set)
        self.jobListbox.pack(side=LEFT)
        self.jobListboxScroll.pack(side=RIGHT, fill=Y)
        
        self.jobButtonsFrm = Frame(self.jobFrm, bd=5)
        self.jobButtonsFrm.grid()
                
        self.upjobButton= Button(self.jobButtonsFrm, text="Subir", command=self.upJobButtonPressed).grid(row=0,column=0, sticky=W+E, padx=3, pady=3)
        self.downjobButton= Button(self.jobButtonsFrm, text="Descer", command=self.downJobButtonPressed).grid(row=0,column=1, sticky=W+E, padx=3, pady=3)
        self.duplicatejobButton= Button(self.jobButtonsFrm, text="Duplicar", command=self.duplicateJobButtonPressed).grid(row=0,column=2, sticky=W+E, padx=3, pady=3)
        self.editjobButton= Button(self.jobButtonsFrm, text="Editar", command=self.editJobButtonPressed).grid(row=1,column=0, sticky=W+E, padx=3, pady=3)
        self.deletejobButton= Button(self.jobButtonsFrm, text="Apagar", command=self.deleteJobButtonPressed).grid(row=1,column=1, sticky=W+E, padx=3, pady=3)
        self.clearjobButton= Button(self.jobButtonsFrm, text="Limpar", command=self.clearJobButtonPressed).grid(row=1,column=2, sticky=W+E, padx=3, pady=3)
        
        self.savejobButton= Button(self.jobFrm, text="Salvar o GCode", command=self.saveJobButtonPressed).grid(row=3,column=0, sticky=W+E)
    
        self.jobListbox.bind('<Double-1>',lambda x: self.editJobButtonPressed())
        
        ################################################################
        #
        # RIGHT FRAME
        #
        self.rightFrm = Frame(self, bd = 5)
        self.rightFrm.grid(row=0, column=1, sticky=W+E+N)
        
        self.operationEditorFrm = Frame(self.rightFrm)
        self.operationEditorFrm.grid(sticky=W+E+N)
        
        self.widgetFrm = Frame(self.operationEditorFrm)
        self.widgetFrm.grid(row=0)

        self.buttonsEditorFrm = Frame(self.operationEditorFrm)
        self.buttonsEditorFrm.grid(row=1)
        
        self.saveEditorFrmButton = Button(self.buttonsEditorFrm, text="Salvar", command=self.saveEditorFrmButtonPressed)
        self.saveEditorFrmButton.grid(row=0,column=0,ipadx=5,padx=5)
        self.closeEditorFrmButton = Button(self.buttonsEditorFrm, text="Fechar", command=self.closeEditorFrmButtonPressed)
        self.closeEditorFrmButton.grid(row=0,column=1,ipadx=5, padx=5)
        
        self.setOperationEditor(None)

        ################################################################
        self.updateJobListBox()

        self.pack(expand=True, fill=BOTH)
    
    
    # Changes the machine selection (mill or lathe)
    def machineSelected(self):
        self.createOperations()
        self.updateJobListBox()
        self.setOperationEditor(None)
        return


    # Callback function for the check button for enable/disable Preamble
    def checkPreamblePressed(self):
        if ( self.includePreamble.get() == 0 ):
            self.preambleButton["state"]  = "disabled"
        else:
            self.preambleButton["state"]  = "normal"
        return

    # Callback function for the check button for enable/disable Postamble
    def checkPostamblePressed(self):
        if ( self.includePostamble.get() == 0 ):
            self.postambleButton["state"] = "disabled"
        else:
            self.postambleButton["state"] = "normal"
        return

    # Callback function for the preamble button
    def preambleButtonPressed(self):
        if self.machineNumber.get() == 0: # mill
            operationWidget = MillPreambleWidget(self.operationEditorFrm)
            operationWidget.setFields(self.millPreambleOperation["fields"])
            self.setOperationEditor(operationWidget)
            self.operationUnderEdition = self.millPreambleOperation
        else: # lathe
            operationWidget = LathePreambleWidget(self.operationEditorFrm)
            operationWidget.setFields(self.lathePreambleOperation["fields"])
            self.setOperationEditor(operationWidget)
            self.operationUnderEdition = self.lathePreambleOperation
        return

    # Callback function for the postamble button
    def postambleButtonPressed(self):
        if self.machineNumber.get() == 0: # mill
            operationWidget = MillPostambleWidget(self.operationEditorFrm)
            operationWidget.setFields(self.millPostambleOperation["fields"])
            self.setOperationEditor(operationWidget)
            self.operationUnderEdition = self.millPostambleOperation
        else: # lathe
            operationWidget = LathePostambleWidget(self.operationEditorFrm)
            operationWidget.setFields(self.lathePostambleOperation["fields"])
            self.setOperationEditor(operationWidget)
            self.operationUnderEdition = self.lathePostambleOperation
        return

    # Creates the list of operations for milling and turning based on 
    # the millWidgetList and latheWidgetList.
    def createOperations(self):
        self.millingOperations = []
        self.turningOperations = []
        
        for widget in millWidgetList:
            exec("label=gui."+widget+"."+widget+".getOperationLabel()")
            self.millingOperations.append({"label":label,"className":widget, "fields":[]})

        for widget in latheWidgetList:
            exec("label=gui."+widget+"."+widget+".getOperationLabel()")
            self.turningOperations.append({"label":label,"className":widget, "fields":[]})

        self.operationListbox.delete(0,END) 
        
        if self.machineNumber.get() == 0:
            for item in self.millingOperations:
                self.operationListbox.insert(END, item["label"])        
        else:
            for item in self.turningOperations:
                self.operationListbox.insert(END, item["label"])


    # Sets the operation editor frame to edit the current selected
    # operation. If None, the operation editor is hidden.
    def setOperationEditor(self, frm):
        if frm is None:
            self.operationEditorFrm.grid_forget()
            self.operationUnderEdition = None
        else:
            self.widgetFrm.destroy()
            self.widgetFrm = frm
            self.widgetFrm.grid(row=0)
            self.operationEditorFrm.grid()


    # Adds the selected operation from the list of operations
    # to the job list. Then, opens the editor.
    def addOperationButtonPressed(self):
        index=-1
        try:
            index = self.operationListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
            
        jobList = None
        optList = None
        prefix = ""
        
        if self.machineNumber.get() == 0: # mill
            prefix = "gui."
            jobList = self.millingJobList
            optList = self.millingOperations           
        else: # lathe
            prefix = "gui."
            jobList = self.turningJobList
            optList = self.turningOperations

        exec("operationWidget = "+prefix+optList[index]["className"]+"."+optList[index]["className"]+"(self.operationEditorFrm)")
        self.setOperationEditor(operationWidget)
        optList[index]["fields"] = operationWidget.getFields()
        jobList.append(copy.deepcopy(optList[index]))
        self.operationUnderEdition = jobList[-1]

        self.updateJobListBox()

        return


    # Updates the job list box
    def updateJobListBox(self):
        self.jobListbox.delete(0,END)
        
        if self.machineNumber.get() == 0:
            jobList = self.millingJobList
        else:
            jobList = self.turningJobList
        
        for item in jobList:
            self.jobListbox.insert(END, item["label"])
       
            
    # Moves up the selected operation from the job list
    def upJobButtonPressed(self):
        index=-1
        try:
            index = self.jobListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
            
        if index == 0:
            return

        if self.operationUnderEdition is not None:
            self.setOperationEditor(None)
            
        jobList = None
        
        if self.machineNumber.get() == 0:
            jobList = self.millingJobList
        else:
            jobList = self.turningJobList

        tmp = jobList[index]
        jobList[index] = jobList[index-1]
        jobList[index-1] = tmp

        self.updateJobListBox()
        return
            
            
    # Moves down the selected operation from the job list
    def downJobButtonPressed(self):
        index=-1
        try:
            index = self.jobListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
            
        jobList = None
        
        if self.machineNumber.get() == 0:
            jobList = self.millingJobList
        else:
            jobList = self.turningJobList
            
        if index == len(jobList)-1:
            return

        if self.operationUnderEdition is not None:
            self.setOperationEditor(None)
            
        tmp = jobList[index]
        jobList[index] = jobList[index+1]
        jobList[index+1] = tmp

        self.updateJobListBox()
        return


    # Duplicates the selected operation from the job list
    def duplicateJobButtonPressed(self):
        index=-1
        try:
            index = self.jobListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
            
        jobList = None
        
        if self.machineNumber.get() == 0:
            jobList = self.millingJobList
        else:
            jobList = self.turningJobList

        duplicated = copy.deepcopy(jobList[index])
        jobList.insert(index,duplicated)

        self.updateJobListBox()
        return
        

    # Edits the selected operation from the job list
    def editJobButtonPressed(self):
        index=-1
        try:
            index = self.jobListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
            
        if self.operationUnderEdition is not None:
            self.setOperationEditor(None)
        
        jobList = None
        if self.machineNumber.get() == 0:
            prefix = "gui."
            jobList = self.millingJobList           
        else:
            prefix = "gui."
            jobList = self.turningJobList

        exec("operationWidget = "+prefix+jobList[index]["className"]+"."+jobList[index]["className"]+"(self.operationEditorFrm)")
        operationWidget.setFields(jobList[index]["fields"])
        self.operationUnderEdition = jobList[index]
        self.setOperationEditor(operationWidget)

        self.updateJobListBox()
        return
        
    # Deletes the selected operation from the job list
    def deleteJobButtonPressed(self):
        index=-1
        try:
            index = self.jobListbox.curselection()[0]
        except:
            return
        if ( index < 0 ):
            return
        
        jobList = None
        if self.machineNumber.get() == 0:
            jobList = self.millingJobList
        else:
            jobList = self.turningJobList

        if self.operationUnderEdition == jobList[index]:
            self.setOperationEditor(None)
            
        jobList.remove(jobList[index])

        self.updateJobListBox()
        return
    
    
    # Clears the entire job list
    def clearJobButtonPressed(self):
        if self.operationUnderEdition is not None:
            self.setOperationEditor(None)
        
        answer = tkMessageBox.askyesno(title='Confirmacao', message='Apagar tudo?')
        
        if answer:
            if self.machineNumber.get() == 0:
                for i in reversed(range(0, len(self.millingJobList))):
                    self.millingJobList.remove(self.millingJobList[i])
            else:
                for i in reversed(range(0, len(self.turningJobList))):
                    self.turningJobList.remove(self.turningJobList[i])

            self.updateJobListBox()
        return
        
        
    # Saves the current configuration and generates the gcode
    def saveJobButtonPressed(self):
        self.saveProject()
        sys.stdout.write(self.generateGcode())
        return
    
    
    # Saves the operation under edition
    def saveEditorFrmButtonPressed(self):
        self.operationUnderEdition["fields"] = self.widgetFrm.getFields()
        
        
    # Closes the operation editor
    def closeEditorFrmButtonPressed(self):
        self.setOperationEditor(None)


    # Saves the current application configuration
    def saveProject(self):
        with open(self.projectFile, 'wb') as fp:
            pickle.dump([self.softwareVersion, self.machineNumber.get(),self.millingJobList, self.turningJobList], fp)


    # Loads the current application configuration
    def loadProject(self):
        with open(self.projectFile, 'rb') as fp:
            softwareVersion, mNumber, millingJobList, turningJobList = pickle.load(fp)
            if ( self.softwareVersion != softwareVersion ):
                print(";Incompatibilidade de versoes do programa.")
                return
            self.machineNumber.set(mNumber)
            self.millingJobList = millingJobList
            self.turningJobList = turningJobList
       
       
    # Generates the GCode from the operations of the job list
    def generateGcode(self):
        jobList = None
        if self.machineNumber.get() == 0:
            prefix = "gui."
            jobList = self.millingJobList
        else:
            prefix = "gui."
            jobList = self.turningJobList
        
        gcodeTxt = ""
        
        # Including preamble (if enable)
        if ( self.includePreamble.get() == 1 ):
            if self.machineNumber.get() == 0:
                operationWidget = MillPreambleWidget(self.operationEditorFrm)
                operationWidget.setFields(self.millPreambleOperation["fields"])
            else:
                operationWidget = LathePreambleWidget(self.operationEditorFrm)
                operationWidget.setFields(self.lathePreambleOperation["fields"])
            gcode = operationWidget.getGCode()
            operationWidget.destroy()
            for line in gcode:
                gcodeTxt = gcodeTxt + line + "\n" 
                    
        # Including the GCode from the jobList
        for item in jobList:
            exec("operationWidget = "+prefix+item["className"]+"."+item["className"]+"(self.operationEditorFrm)")
            operationWidget.setFields(item["fields"])
            gcode = operationWidget.getGCode()
            operationWidget.destroy()
            for line in gcode:
                gcodeTxt = gcodeTxt + line + "\n" 
        
        # Including postamble (if enable)
        if ( self.includePostamble.get() == 1 ):
            if self.machineNumber.get() == 0:
                operationWidget = MillPostambleWidget(self.operationEditorFrm)
                operationWidget.setFields(self.millPostambleOperation["fields"])
            else:
                operationWidget = LathePostambleWidget(self.operationEditorFrm)
                operationWidget.setFields(self.lathePostambleOperation["fields"])
            gcode = operationWidget.getGCode()
            operationWidget.destroy()
            for line in gcode:
                gcodeTxt = gcodeTxt + line + "\n" 
                
        return gcodeTxt
               


app = Application()
app.master.title("GCODER - UTFPR-FB")
app.master.geometry('1400x870')
#app.master.geometry("{0}x{1}+0+0".format(app.master.winfo_screenwidth(), app.master.winfo_screenheight()))
app.mainloop()
