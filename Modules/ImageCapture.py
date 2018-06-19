#from MainApp import *
import win32com.client as wincl
import multiprocessing
from speechToTextTest import speech2text


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







