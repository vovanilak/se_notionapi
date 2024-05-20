import os
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Настройки Google Drive API
SERVICE_ACCOUNT_FILE = 'my_google_key.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Настройки Notion API
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_PAGE_ID = 'd760cecda12a4b138c0c209209b743fb'

# Функция для получения изображений из Google Drive
def get_images_from_drive(folder_id):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    query = f"'{folder_id}' in parents and mimeType contains 'image/'"
    results = service.files().list(q=query).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return []

    images = []
    for item in items:
        file_id = item['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        fh.seek(0)
        images.append((item['name'], fh))

    return images

# Функция для загрузки изображений в Notion
def upload_images_to_notion(image_url):
    notion = Client(auth=NOTION_TOKEN)
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        },
        data=json.dumps({
            "parent": {"type": "page_id", "page_id": NOTION_PAGE_ID},
            "properties": {
                "title": [
                    {
                        "text": {
                            "content": "00"
                        }
                    }
                ]
            },
            "children": [{
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": image_url  # URL загруженного изображения
                    }
                }
            }]
        })
    )

    if response.status_code == 200:
        print(f"Image uploaded successfully to Notion.")
    else:
        print(f"Failed to upload image to Notion. Response: {response.content}")

# Основная функция
def main():
    #folder_id = 'your_google_drive_folder_id'
    #images = get_images_from_drive(folder_id)
    url = 'https://drive.google.com/file/d/1fzNvirJivoe98I7_lgrx4LE4MINgR9ND/view'
    upload_images_to_notion(url)

if __name__ == "__main__":
    main()
