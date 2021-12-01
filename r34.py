import rule34
import random

def getr34img(search):

    r34 = rule34.Sync()
    images = r34.getImages(search)

    links = []

    for img in images:
        links.append(img.preview_url)

    return random.choice(links)
