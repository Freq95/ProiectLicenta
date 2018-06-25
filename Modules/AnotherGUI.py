from tkinter import *

# daca se doresc mai multe campuri in Frame, adaugati un nume in lista de mai jos
fields = 'Nume Angajat',
lista_nume_angajati = []


def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      lista_nume_angajati.append(text)
      print('%s: "%s"' % (field, text))


def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries


#if __name__ == '__main__':
def init_gui():
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1 = Button(root, text='Adauga',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Urmatoarea poza', command=root.quit)
   b2.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()
