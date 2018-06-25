from tkinter import *

# daca se doresc mai multe campuri in Frame, adaugati un nume in lista de mai jos
fields = 'Parola admin: ',
parola_introdusa = []


def fetch_admin(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      parola_introdusa.append(text)
      print('%s: "%s"' % (field, text))


def makeform_admin(aroot, fields):
   entries = []
   for field in fields:
      row = Frame(aroot)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row, show="*")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries


#if __name__ == '__main__':
def init_gui_admin():
   aroot = Tk()
   ents = makeform_admin(aroot, fields)
   aroot.bind('<Return>', (lambda event, e=ents: fetch_admin(e)))
   b1 = Button(aroot, text='Valideaza',
          command=(lambda e=ents: fetch_admin(e)))
   b1.pack(side=LEFT, padx=5, pady=5)

   b2 = Button(aroot, text='Antreneaza', command=aroot.quit)
   b2.pack(side=LEFT, padx=5, pady=5)
   aroot.mainloop()


