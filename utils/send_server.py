def post_uguu(img_name):
    import requests
    url = 'https://uguu.se/upload'
    response = requests.post(url, files={"files[]": open(img_path, 'rb')})
    res = response.json()
    os.remove(f"{image_folder}/{img_name}.png")
    return res['files'][0]['url']