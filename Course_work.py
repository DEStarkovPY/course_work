from tkinter import Y
import requests
import json
import os
from pprint import pprint


class VkWorker:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {'access_token': token,
                       'v': version
        }

    def profile_photo_get(self):
        method_url = self.base_url + 'photos.get'
        this_method_params = {'album_id': 'profile',
                              'extended': '1',
                              'count': '1000'
        }
        this_method_params.update(self.params)
        ans = (requests.get(method_url, params=this_method_params)).json()
        return ans


    def profile_photo_url_loader(self):
        name_url_dict = {}
        items_list = self.profile_photo_get()['response']['items']
        for item in items_list:
            if 'likes' in item:
                photo_name = item['likes']['count']
            if 'date' in item:
                photo_date = item['date']
            if 'sizes' in item:
                sizes_list = item['sizes']
                height_list = []
                [height_list.append(height['height']) for height in sizes_list]
                max_height = max(height_list)
                for params in sizes_list:
                    if params['height'] == max_height:
                        if photo_name not in name_url_dict.keys():
                            name_url_dict[photo_name] = params['url']
                        elif photo_name in name_url_dict.keys():
                            name_url_dict[photo_date] =params['url']
        return name_url_dict


    def photo_inf_writer(self):
        name_url_dict = {}
        name_type_list = []
        items_list = self.profile_photo_get()['response']['items']
        for item in items_list:
            if 'likes' in item:
                photo_name = item['likes']['count']
            if 'date' in item:
                photo_date = item['date']
            if 'sizes' in item:
                sizes_list = item['sizes']
                height_list = []
                [height_list.append(height['height']) for height in sizes_list]
                max_height = max(height_list)
                for params in sizes_list:
                    if params['height'] == max_height:
                        if photo_name not in name_url_dict.keys():
                            name_url_dict[photo_name] = params['url']
                            params_dict = {}
                            params_dict['file_name'] = f'{photo_name}.jpg'
                            params_dict['size'] = params['type']
                            name_type_list.append(params_dict)

                        elif photo_name in name_url_dict.keys():
                            name_url_dict[photo_date] =params['url']
                            params_dict = {}
                            params_dict['file_name'] = f'{photo_date}.jpg'
                            params_dict['size'] = params['type']
                            name_type_list.append(params_dict)
        FILE_NAME = 'photo_inf.json'
        THIS_PATH = os.getcwd()
        file_path = os.path.join(THIS_PATH, FILE_NAME)
        with open(file_path, 'w', encoding = 'utf-8') as file:
            json.dump(name_type_list, file, ensure_ascii = False, indent = 2)
        return file_path


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
        folder_name = 'VkYaTransfer'
        my_params = {'path': folder_name}
        requests.put(method_url, headers=my_headers, params=my_params)
        return folder_name


    def ya_photo_uploader(self, name_url_dict):
        method_url = self.base_url + 'upload'
        self.headers = self.get_headers()
        for name, url in name_url_dict.items():
            method_params = {'path': f'{MyYaDisk.empty_folder_creater()}/{name}',
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





if __name__ == '__main__':
    vk_token = ""
    ya_token =''
    MyVkPhotos = VkWorker(vk_token)
    MyYaDisk = YaWorker(ya_token)


    MyYaDisk.empty_folder_creater()
    MyYaDisk.photo_inf_uploader(f'{MyYaDisk.empty_folder_creater()}/photo_inf.json', MyVkPhotos.photo_inf_writer())
    MyYaDisk.ya_photo_uploader(MyVkPhotos.profile_photo_url_loader())
