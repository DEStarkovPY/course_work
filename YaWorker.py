from tkinter import Y
import requests


class YaWorker:
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return{
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }


    def empty_folder_creater(self):
        method_url = self.base_url[:-1]
        my_headers = self.get_headers()
        global your_folder_name
        your_folder_name = input(str('Введите имя папки, в которой будут храниться файлы (В случае, если данная папка уже существует, код даст ошибку): '))
        my_params = {'path': your_folder_name}
        ans = requests.put(method_url, headers=my_headers, params=my_params)
        ans.raise_for_status()
        return your_folder_name


    def ya_photo_uploader(self, name_url_dict):
        method_url = self.base_url + 'upload'
        self.headers = self.get_headers()
        for name, url in name_url_dict.items():
            method_params = {'path': f'{your_folder_name}/{name}',
                             'url': f'{url}',
                             'disable_redirects': 'false'
            }
            request = requests.post(method_url, params=method_params, headers=self.headers)
        if request.status_code == 202:
            return print('Done')
        else:
            return print('Error')


    def get_upload_link(self, disk_file_path):
        method_url = self.base_url + 'upload'
        my_headers = self.get_headers()
        my_params = {'path': disk_file_path,
                     'overwrite': 'true'
        }
        responce = requests.get(method_url, headers=my_headers, params=my_params)
        return responce.json()


    def photo_inf_uploader(self, disk_file_path, file_name):
        href = self.get_upload_link(disk_file_path=disk_file_path).get('href', '')
        responce = requests.put(href, data=open(file_name, 'rb'))
        responce.raise_for_status()
        if responce.status_code == 201:
            print('Done')
