from tkinter import *

lista_nume_angajati = []


def init_gui():
    master = Tk()
    e = Entry(master)
    e.pack()
    e.focus_set()
    return master, e


def callback(master, e):
    nume_angajat = e.get()
    master.destroy()
    lista_nume_angajati.append(nume_angajat)


def start_gui():
    master, e = init_gui()
    b = Button(master, text="OK", width=10, command=callback(master, e))
    b.pack()
    mainloop()


start_gui()