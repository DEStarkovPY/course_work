from VkWorker import VkWorker
from YaWorker import YaWorker
from Jsonwriter import JsonWriter
from TokenReader import token_reader
if __name__ == '__main__':
    vk_token = token_reader('vk')
    ya_token = token_reader('yandex')
    MyVkPhotos = VkWorker(vk_token)
    MyYaDisk = YaWorker(ya_token)
    MyJsonWriter = JsonWriter('VkWriter')
    MyYaDisk.photo_inf_uploader(f'{MyYaDisk.empty_folder_creater()}/photo_inf.json',
                                MyJsonWriter.photo_inf_writer_vk(MyVkPhotos.profile_photo_get()))
    MyYaDisk.ya_photo_uploader(MyVkPhotos.profile_photo_url_loader())
