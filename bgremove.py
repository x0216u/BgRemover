import requests
from local_data import BG_TOKEN

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('putin.jpg', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': BG_TOKEN},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
