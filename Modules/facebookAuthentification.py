import requests

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    #print file.text #to test what the FB api responded with    
    result = file.json()
    #print file.text #to test the TOKEN
    return result


token = get_fb_token("100001311647240", "andreeutza")
print(token)
