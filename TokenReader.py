import os



def token_reader(app):
    THIS_PATH = os.getcwd()
    FILE_NAME = 'tokens.txt'
    full_path = os.path.join(THIS_PATH, FILE_NAME)
    with open(full_path, 'rt', encoding='utf-8') as file:
        vk_token_name = file.readline().strip()
        ya_token_name = file.readline().strip()
        if app == 'vk':
            return vk_token_name
        elif app == 'yandex':
            return ya_token_name
