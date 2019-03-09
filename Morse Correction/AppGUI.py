import tkinter as tk
from Correction import *

class AppGUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        recLambda = lambda arg = "Rec" : self.getFileData(arg)
        ansLambda = lambda arg = "Ans" : self.getFileData(arg)

        self.evaluateBtn = tk.Button(self, text="Evaluate", command=self.evaluateText)
        self.getRecTextBtn = tk.Button(self, text="Find Recieved Text", command=recLambda)
        self.testBtn = tk.Button(self, text="Test", command=self.getAndCompare)
        self.getAnsTextBtn = tk.Button(self, text="Find Answer Text", command=ansLambda)
        
        self.evaluateBtn.pack(side="left")
        self.testBtn.pack(side="right")
        self.getRecTextBtn.pack(side="left")
        self.getAnsTextBtn.pack(side="right")
        
        self.quit = tk.Button(self, text="QUIT", fg="red", command = self.master.destroy)
        self.quit.pack(side="bottom")

    def getFileData(self, context):
        Correction.getFileData(Correction, context)

    def evaluateText(self):
        Correction.evaluateText(Correction)

    def getAndCompare(self):
        Correction.getAndCompare(Correction)
        
root = tk.Tk()
app = AppGUI(master=root)
app.mainloop()
