from tkinter import *
from MainApp import start_nn
from ImageCapture import text2speech


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Access App!")
        master.geometry("500x500")

        self.label = Label(master, text="Bine ati venit, in cazul in care nu faceti parte din baza de date, apasati butonul <Insert in DB>!")
        self.label.pack()

        self.submitButton = Button(master, text="Start App", command=self.startGrantAccess)
        self.submitButton.pack()

        self.submitButton = Button(master, text="Insert in DB", command=self.insertInDB)
        self.submitButton.pack()

        self.trainButton = Button(master, text="Train NN", command=self.trainNN)
        self.trainButton.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def startGrantAccess(self):
        print("You start the access authentification!")
        start_nn(0)

    def trainNN(self):
        print("You start the NN training!")
        start_nn(1)

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


