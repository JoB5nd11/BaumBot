import rule34
import random


def getr34img():
    r34 = rule34.Sync()
    images = r34.getImages("gay mario")
    links = []

    for img in images:
        links.append(img.preview_url)

    return random.choose(links)
