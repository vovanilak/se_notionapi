import requests
import os

def post_uguu(img_path):
    url = 'https://uguu.se/upload'
    with open(img_path, 'rb') as file:
        response = requests.post(url, files={"files[]": file})
    res = response.json()
    os.remove(f"{img_path}")
    return res['files'][0]['url']

if __name__ == '__main__':
    print(post_uguu('../img.png'))
    