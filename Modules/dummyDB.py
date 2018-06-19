import sqlite3
import os
from PIL import Image

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print('Creating schema')
        sql = '''create table if not exists PICTURES(ID INTEGER PRIMARY KEY AUTOINCREMENT, PICTURE BLOB, TYPE TEXT, FILE_NAME TEXT);'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
    else:
        print('Schema exists\n')
    return conn

def insert_picture(conn, picture_file):
    with open(picture_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(picture_file)
        afile, ext = os.path.splitext(base)
        sql = '''INSERT INTO PICTURES (PICTURE, TYPE, FILE_NAME) VALUES(?, ?, ?);'''
        conn.execute(sql,[sqlite3.Binary(ablob), ext, afile])
        conn.commit()


def extract_picture(cursor, picture_id):
    sql = "SELECT PICTURE, TYPE, FILE_NAME FROM PICTURES WHERE id = :id"
    param = {'id': picture_id}
    cursor.execute(sql, param)
    ablob, ext, afile = cursor.fetchone()
    filename = afile + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    return filename


def showImageByDBIndex(index):
    conn = create_or_open_db('picture_db.sqlite')
    cur = conn.cursor()
    filename = extract_picture(cur, index)
    cur.close()
    conn.close()
    im = Image.open('D:/__Licenta/Test/ImageDB/'+filename)
    im.show()

# show every picture from DB
#showImageByDBIndex(14)

# insert a pic in DB
#conn = create_or_open_db('picture_db.sqlite')
#picture_file = "D:/__Licenta/Test/ImageDB/p2.jpg"
#insert_picture(conn, picture_file)
#conn.close()