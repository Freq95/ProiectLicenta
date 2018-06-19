from selenium import webdriver
import requests
from requests import Session
import re

ses=requests.Session()
ses.proxies={'http':'http://heed:ravi@172.31.100.29:3128','https':'https://heed:ravi@172.31.100.29:3128'}

def findId(link):
    imgId=re.search(".*fbid=([0-9]*)&",link).group(1)
    img=ses.get("https://www.facebook.com/photo/download/?fbid="+imgId).content
    fileImg=open(imgId+".jpeg","wb")
    fileImg.write(img)
    fileImg.close()
    return imgId

firstPhotoID=""
drive=webdriver.Chrome()
drive.get("https://www.facebook.com")
print("Navigate to the first photo of album using firefox that opened, then press enter ")
input()

while(True):
    link=drive.current_url
    photoID=findId(link)
    if(firstPhotoID==photoID):
        break
    if(firstPhotoID==""):
        firstPhotoID=photoID
    elem=drive.find_element_by_class_name('_n3')
    elem.click()