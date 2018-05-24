import random
import string
import os

import requests
from bs4 import BeautifulSoup


ROOT_URL = 'http://prnt.sc/'
ITERATION_COUNT = 10
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)'
}
IMG_ID = 'screenshot-image'

PRJ_DIR = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PRJ_DIR, 'media')
IMG_FORMATS = ('png', 'jpg', 'jpeg', 'gif')


def generate_url():
    return ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(6)
    )


def get_response(img_url):
    r = requests.get(ROOT_URL + img_url, headers=HEADERS)
    html_response = BeautifulSoup(r.text, 'html.parser')
    img_tag = html_response.find(class_=IMG_ID)
    if not img_tag or img_tag['src'].startswith('//'):
        return None
    else:
        save_image(img_tag, img_url)


def save_image(tag, file_name):
    img_r = requests.get(tag['src'], stream=True)
    if img_r.status_code == 200:
        img_format = tag['src'].split('.')[-1]
        if img_format not in IMG_FORMATS:
            img_format = 'jpg'
        path = os.path.join(MEDIA_ROOT, '{name}.{format}'.format(
            name=file_name,
            format=tag['src'].split('.')[-1]
        ))
        with open(path, 'wb') as f:
            for chunk in img_r:
                f.write(chunk)


def main():
    for i in range(ITERATION_COUNT):
        get_response(generate_url())


if __name__ == '__main__':
    if not os.path.isdir(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    main()