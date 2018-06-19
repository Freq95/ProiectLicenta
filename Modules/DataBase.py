import sqlite3

conn = sqlite3.connect('peopledb.sqlite')

cursor = conn.cursor()

def create_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS FaceRecognitionDB(Nume TEXT, Age REAL, Image BLOB)')

def insert(name, age, image):
    # method to add a new record
    # sqlstr = 'INSERT INTO PEOPLE(Name, Age, Image) VALUES ("' + str(name) + '", ' + str(age) + '", ' + str(image) + ')'
    sqlstr = 'INSERT INTO PEOPLE(ID, Name, Age) VALUES ("' + str(name) + '", "' + str(age) + '", ' + str(image) + ')'
    cursor.execute(sqlstr)
    connect.commit()

#create_table()
#imgPath = 'D:/__Licenta/Test/ImageDB/img1.jpg'
#img = cv2.imread(imgPath, 0)
#insert('Paul', 22, img)