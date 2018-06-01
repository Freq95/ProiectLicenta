# import the necessary packages
from __future__ import print_function
from Camera_InputText import *
from imutils.video import VideoStream
import argparse
import time
import cv2

# construct the argument parse and parse the arguments
vs = cv2.VideoCapture(0)

# start the app
pba = PhotoBoothApp(vs, 'D:/__Licenta/Test/ImageDB')
pba.root.mainloop()