import cv2
import os
from dummyDB import *

def captureImage():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0



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
        elif k%256 == 32:
            # SPACE pressed
            path = 'D:/__Licenta/Test/ImageDB'
            numeCandidat = input("Introduceti numele persoanei: ")
            img_name = (numeCandidat + "{}.jpg").format(img_counter)
            cv2.imwrite(os.path.join(path, img_name), frame)
            imagePath = path + '/' + img_name
            print("{} salvata!".format(img_name))

            insert_picture(conn, imagePath)
            print("Poza a fost inserata in baza de date")
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return imagePath

# capture a new person
#imagePath

# insert a person picture in DB // create connection with DB
conn = create_or_open_db('picture_db.sqlite')

captureImage()

#showImageByDBIndex(34)
#showImageByDBIndex(35)
#showImageByDBIndex(35)
# close the DB connection

conn.close()