import speech_recognition as sr
import cv2
import os
#from AnotherGUI import init_gui
from AnotherGUI import *
from dummyDB import create_or_open_db, insert_picture
import multiprocessing
import win32com.client as wincl


def text2speech(case):

    if case == 0:
        p3 = multiprocessing.Process(target=speech2text)
        p3.start()
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak("Please say take a photo and look straight into the camera, after that please insert your name!")

    if case == 1:
        print("case 1")
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak("Move your head just a little bit to the left!")

    if case == 2:
        print("case 2")
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak("Move your head just a little bit to the right!!")

    #p3.join()

def speech2text():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print(audio)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))

        if r.recognize_google(audio) == "play":
            print("Correct")

        if r.recognize_google(audio) == "stop":
            print("Incorrect")

        if r.recognize_google(audio) == "take a photo":
            print("Take a photo branch")
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("test")
            photo_counter = 0
            img_counter = 0

            global case, contor_trigger, numeCandidat
            case = 1
            contor_trigger = 0

            while True:
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)
                contor_trigger = contor_trigger + 1
                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif contor_trigger == 50:
                    # no SPACE press needed
                    path = 'D:/GitLocalRepo/ProiectLicenta_git/Image_DataBase/train/'
                    os.chdir(path)

                    if case == 1:
                        # start simple GUI
                        init_gui()

                    # numele ultimului angajat introdus in lista
                    numeCandidat = lista_nume_angajati[len(lista_nume_angajati) - 1]

                    # creaza un nou director pentru noul angajat
                    if not os.path.exists(numeCandidat):
                        os.makedirs(numeCandidat)
                        path = 'D:/GitLocalRepo/ProiectLicenta_git/Image_DataBase/train/' + numeCandidat
                    else:
                        path = 'D:/GitLocalRepo/ProiectLicenta_git/Image_DataBase/train/' + numeCandidat
                        #print("Numele introdus face parte din baza noastra de date.")

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
                    text2speech(case)
                    case = case + 1
                    contor_trigger = 0
                    if case == 4:
                        break


            cam.release()
            cv2.destroyAllWindows()
            return imagePath

        if r.recognize_google(audio) == "hello":
            print("Hi")

            # start webcam
            cam = cv2.VideoCapture(0)
            while True:
                ret_val, img = cam.read()
                cv2.imshow('my webcam', img)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
            cv2.destroyAllWindows()

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}. Check network connection!".format(e))

        if r.recognize_google(audio) == "play":
            print("Correct")

        if r.recognize_google(audio) == "stop":
            print("Incorrect")

    return r.recognize_google(audio)


