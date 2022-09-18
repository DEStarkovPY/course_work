from tkinter import Y
import requests




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
