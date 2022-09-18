import json
import os


class JsonWriter:
    def __init__(self, app_name):
        self.app_name = app_name


    def photo_inf_writer_vk(self, data):
        name_url_dict = {}
        name_type_list = []
        items_list = data['response']['items']
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
