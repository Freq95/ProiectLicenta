from tkinter import *
import tkinter as ttk

""" Setting The Main GUI """

GUI = Tk()

F1=Frame(GUI)
F1=Frame(GUI,width=400,height=450)
F1.place(height=7000, width=4000, x=100, y=100)
F1.config()


F1.grid(columnspan=10,rowspan=10)

F1.grid_rowconfigure(0,weight=1)
F1.grid_columnconfigure(0,weight=1)


photo=PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Meridian.jpg")
label = Label(GUI,image = photo)
label.image = photo # keep a reference!
label.grid(row=0,column=0,columnspan=20,rowspan=20)

b=ttk.Button(GUI,text="Start")
b.grid(row=8,column=8)

GUI.mainloop()