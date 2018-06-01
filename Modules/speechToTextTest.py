#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
import cv2



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