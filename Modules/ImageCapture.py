import cv2
import os
from dummyDB import *
from AnotherGUI import *
from MainApp import *
import _thread
import time
import multiprocessing
from speechToTextTest import *


def text2speech():
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("Please say take a picture and look into the camera, after that please insert your name!")
    p3 = multiprocessing.Process(target=speech2text)
    p3.start()
    p3.join()

def captureImage():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    picture_counter = 0
    # TODO: inform the user that a photo will be taken in 4 seconds
    #text2speech()

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        #    comanda == "take a photo":
        elif k%256 == 32:
            # no SPACE press needed
            path = 'D:/GitLocalRepo/ProiectLicenta_git/Image_DataBase/train/'
            os.chdir(path)
            # start simple GUI
            init_gui()

            # numele ultimului angajat introdus in lista
            numeCandidat = lista_nume_angajati[len(lista_nume_angajati) - 1]

            # creaza un nou director pentru noul angajat
            if not os.path.exists(numeCandidat):
                os.makedirs(numeCandidat)
                path = 'D:/GitLocalRepo/ProiectLicenta_git/Image_DataBase/train/' + numeCandidat
            else:
                print("Numele introdus face parte din baza noastra de date.")

            img_name = (numeCandidat + "{}.jpg").format(img_counter)
            cv2.imwrite(os.path.join(path, img_name), frame)
            imagePath = path + '/' + img_name
            print("{} salvata!".format(img_name))

            # insert a person picture in DB // create connection with DB
            conn = create_or_open_db('picture_db.sqlite')
            insert_picture(conn, imagePath)
            print("Poza a fost inserata in baza de date")

            # close the DB connection
            conn.close()
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return imagePath

# capture a new person
#imagePath


if __name__ == "__main__":

    p1 = multiprocessing.Process(target=text2speech,)
    p2 = multiprocessing.Process(target=captureImage)

    p2.start()
    p1.start()

    #captureImage()

    #showImageByDBIndex(34)
    #showImageByDBIndex(35)
    #showImageByDBIndex(35)

    p1.join()
    p2.join()


    print("Done!")



