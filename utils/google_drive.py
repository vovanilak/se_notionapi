from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import os 

class GoogleApi:
    def __init__(self, service_path, root_folder_id):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.metadata'
        ]
        self.SERVICE_ACCOUNT_FILE = service_path
        self.credentials = service_account.Credentials.from_service_account_file(
                self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.root_folder_id = root_folder_id

    def dir_list(self):
        results = self.service.files().list(pageSize=10,
                                    fields="nextPageToken, files(id, name, mimeType)").execute()
        return results


    def load_to(self, folder_id, file_path, name):
        file_metadata = {
                        'name': name,
                        'mimeType': 'image/png',
                        'parents': [folder_id]
                    }
        media = MediaFileUpload(file_path, resumable=True)
        r = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return r['id']
        
    def load_img(self, file_path, name):
        file_metadata = {
                        'name': name,
                    }
        media = MediaFileUpload(file_path, resumable=True)
        r = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return r['id']

    def give_perm(self, file_id):
        response_permission = self.service.permissions().create(
            body={'role':'reader', 'type': 'anyone'}, 
            fileId=file_id).execute()
        response_share_link = self.service.files().get(
            fileId=file_id,
            fields='webViewLink').execute()
        url = response_share_link.get('webViewLink')
        ind = url.rfind('/')
        return url[:ind] 

    def create_folder(self, folder_name, parent_folder_id=None):
        parent_folder_id = self.root_folder_id
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        return folder['id']


    def del_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()


    def folder_here(self, folder_name):
        results = self.service.files().list(pageSize=100,
                                    fields="files(id, name, mimeType)").execute()
        for file in results.get('files', []):
            if file.get('name') == folder_name:
                return file.get('id')


    def create_n_load(self, folder_name, img_path, img_name):
        folder_id = self.folder_here(folder_name)
        if not folder_id:
            folder_id = self.create_folder(folder_name)
        file_id = self.load_to(folder_id, img_path, img_name)
        link = self.give_perm(file_id)
        return link + '/preview'


if __name__ == '__main__':
    os.chdir('notionapi')
    api = GoogleApi('my_google_key.json', '19i_mtgS6DTCMhtzPpt3wKdnN0vH_U8iW')
    #api = GoogleApi('se_google_key.json', '1wbmhJP3JEsL2_n2bgXaD4yl7PAbx6k_R')
    #here = api.folder_here('Симонов Никита Алексеевич')
    here = api.create_n_load('Симонов Никита Алексеевич', '1715758693.8517.png', '1715758693.8517.png')
    #lol = api.create_n_load('test', '1715758693.8517.png', '1715758693.8517.png')
    #folder_id = google.create_folder('test3', 'null')
    #fill = api.load_img('1715758693.8517.png', '1715758693.8517.png')
    #fill = api.load_to('19i_mtgS6DTCMhtzPpt3wKdnN0vH_U8iW', '1715758693.8517.png', '1715758693.8517.png')
    #perm = api.give_perm(fill)
    #fill = api.load_to('1mnyu7zvD1yNgAtZDWmKeeSMdmXRYuOYu', '1715758693.8517.png', '1715758693.8517.png')
    #1715758693.8517.png
    print(here)