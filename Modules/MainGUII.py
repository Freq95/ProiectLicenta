from tkinter import *
from MainApp import start_nn
from ImageCapture import text2speech
from AdminPass import *
from PIL import Image, ImageTk

class MyFirstGUI:
    def __init__(self, master):
        self.master = master

        master.title("Access App!")
        #master.geometry("500x500")

        #photo = PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Adauga_Client.jpg")
        #label = Label(master, image=photo)
        #label.image = photo  # keep a reference!
        #label.grid()

        self.label = Label(master, text="Bine ați venit!\n\n\n")
        self.label.configure(font=("Times New Roman", 15, "bold"))
        self.label.pack()

        self.submitButton = Button(master, text="", command=self.startGrantAccess)
        img = PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Start_Aplicatie.jpg")
        self.submitButton.config(image=img)
        self.submitButton.image = img
        self.submitButton.pack()

        self.submitButton = Button(master, text="Insert in DB", command=self.insertInDB)
        img_1 = PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Inserati_Persoana.jpg")
        self.submitButton.config(image=img_1)
        self.submitButton.image = img_1
        self.submitButton.pack()

        self.trainButton = Button(master, text="Train NN", command=self.trainNN)
        img_2 = PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Antrenare_Retea.jpg")
        self.trainButton.config(image=img_2)
        self.trainButton.image = img_2
        self.trainButton.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        img_3 = PhotoImage(file="D:/GitLocalRepo/ProiectLicenta_git/Modules/Buttons/Inchide_Aplicatia.jpg")
        self.close_button.config(image=img_3)
        self.close_button.image = img_3
        self.close_button.pack()

    def startGrantAccess(self):
        print("You start the access authentification!")
        start_nn(0)

    def trainNN(self):
        init_gui_admin()
        try:
            if parola_introdusa[0] == "1234":
                print("You start the NN training!")
                start_nn(1)
        except:
            print("Inchide interfata grafica.")

    def insertInDB(self):
        case = 0
        print("You pressed Insert in DB!")
        text2speech(case)
        #p1 = multiprocessing.Process(target=text2speech, args=(case,))
        #p1.start()

        # trebuie conexiune la DB pt a putea vedea poza
        # showImageByDBIndex(37)

        #p1.join()
        print("Done!")


if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()





