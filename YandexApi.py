import requests
from main import VKApi
from tqdm import tqdm
from time import sleep


TOKEN = ''


class YaUploader:
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {TOKEN}'}
        self.folder_name = f"{input('Придумайте название для папки: ')}/"

    def create_folder(self):
        requests.put(YaUploader.base_url, headers=self.headers, params={'path': self.folder_name})

    def upload_to_disk(self):
        self.create_folder()
        data = VKApi()
        data.get_json()
        for file_name, file_url in tqdm(data.get_name_and_links().items(), desc='Photo uploaded'):
            disk_path = self.folder_name + str(file_name)
            upload_link_url = YaUploader.base_url + 'upload'
            params = {'path': disk_path,
                      'url': file_url,
                      'overwrite': 'true'}
            requests.post(upload_link_url, headers=self.headers, params=params)
            sleep(0.05)


if __name__ == '__main__':

    uploader = YaUploader()
    # uploader.create_folder()
    uploader.upload_to_disk()
