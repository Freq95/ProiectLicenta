import requests
import random
import urllib.request


def download_web_image(url):
    name = random.randrange(1, 1000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)


token = 'EAACEdEose0cBABcvPVULbWHWAaUm5RzoajFJ7Me0OmRIEraJfgtgE498U7Grn6gyN7DVEwfAjSGQefEdMRDbu5RC17KtvcE5nwmoDvp78ZBG7JKvbMBekZAPk0AlsGzJ6ce4eQoeXudhwVtNlQGxNWjY8RmMmu4yZBlQrRGZC8TLVRgRABuOCYCSAamgup4HZAMq9qqw0nAZDZD'
me = 'https://graph.facebook.com/v3.0/me?access_token=' + token
friends = 'https://graph.facebook.com/v3.0/me/friends?access_token=' + token
search = 'https://graph.facebook.com/v3.0/search?q=mark zuukerberg&type=user&access_token=' + token
images_test = 'https://graph.facebook.com/v3.0/me/photos?access_token=' + token
picture_test = 'https://graph.facebook.com/v3.0/me/photos?access_token=' + token
images = 'https://graph.facebook.com/v3.0/me/photos?fields=link&access_token=' + token
images_1 = 'https://graph.facebook.com/v3.0/me/picture?redirect=false&access_token=' + token
images_2 = 'https://graph.facebook.com/v2.8/1482938649/photos?fields=images&access_token=' + token
get_command = "https://graph.facebook.com/v3.0/100001311647240/picture?redirect=false&access_token=EAACtdwAhfgYBAMRUQZBJWlNBpdtJgicZBMuJpZCsadg7WHqEd9fdKKKiHZBDzQi8cuatG7oZCWEuvAgOdE9BrZAeZCJ5W0z8jXfQMeq6ZAMhIVgomrhsq2HbZA62VFzHf1XnCwbJZAAUo1JPx4VakMhWAoBMgOSbiWZBVhkiWhVZC8dzDgQYqyCJJA2e6zcjkndJDwpzPZA4ZCIJrCXhDln5V0A4wOH4b6JttXq6ZCnXG79wtovuqT5ropZBZAXyZA"

me1 = requests.get(me)
f1 = requests.get(friends)
json_image = requests.get(images).json()
img2 = requests.get(images_test)
f2 = requests.get(friends)
img_1 = requests.get(images_1)
json_data = json_image['data']
get = requests.get(get_command).json()
img_2 = requests.get(images_2).json()

print(json_data[1]["link"])
print(json_data[1]["link"] + '&theater')
print('https://www.facebook.com/photo.php?fbid=1706756786044693&set=t.100001311647240&type=3&theater')

url_string_1 = json_data[1]["link"]
url_string_2 = json_data[1]["link"] + '&theater'
url_string_3 = "https://www.facebook.com/photo.php?fbid=1706756786044693&set=t.100001311647240&type=3&theater"
#download_web_image(url_string_1)
#download_web_image(url_string_2)
#download_web_image(url_string_3)
#download_web_image("https://www.facebook.com/photo.php?fbid=201724847314174&set=a.101990310620962.1073741827.100024299792818&type=3&theater")


dha = img_2['data'][0]['images'][0]['source']

import urllib.request
# data = urllib.request.urlretrieve("https://scontent.xx.fbcdn.net/v/t1.0-9/34701404_1706756792711359_5342120016852549632_n.jpg?_nc_cat=0&oh=b4834d8bad0d4e98bedd0316c65c3ebe&oe=5BA9FB9F", "000001.jpg")
# urllib.request.urlretrieve("https://scontent.xx.fbcdn.net/v/t1.0-9/34701404_1706756792711359_5342120016852549632_n.jpg?_nc_cat=0&oh=b4834d8bad0d4e98bedd0316c65c3ebe&oe=5BA9FB9F", "000005.jpg")
urllib.request.urlretrieve(dha, "Xinti.jpg")


trei = 2
