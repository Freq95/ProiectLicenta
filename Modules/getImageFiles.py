import glob

def get_image_filename():

    # the returned value is a list that contains all the picture names from DB
    file_name_array = []
    for fileName in glob.glob('ImageDB/*.jpg'):
        fileName = fileName.replace('ImageDB', '').replace('\\', '').replace('.jpg', '').replace('.JPG', '')\
            .replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '')\
            .replace('7', '').replace('8', '').replace('9', '').replace('0', '')
        file_name_array.append(fileName)
    return file_name_array

def get_image_filename_digits():
    # the returned value is a list that contains all the picture names from DB
    file_name_array = []
    for fileName in glob.glob('ImageDB/*.jpg'):
        fileName = fileName.replace('ImageDB', '').replace('\\', '')
        file_name_array.append(fileName)
    return file_name_array