import requests
from uuid import uuid4
from local_data import BG_TOKEN, TOKEN, PROXY


def remove_bg(image_path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': BG_TOKEN},
    )
    if response.status_code == requests.codes.ok:
        file_name = '{}.png'.format(uuid4())
        with open(file_name, 'wb') as out:
            out.write(response.content)
            return file_name
    else:
        False


def download_file(file_path):
    proxies = { 'https' :  PROXY}
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_path), proxies=proxies)
    file_name = '{}.jpg'.format(uuid4())
    open(file_name, 'wb').write(file.content)
    return file_name
