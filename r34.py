import rule34
import random

r34 = rule34.Sync()
images = r34.getImages("gay mario")

def getr34img():
    links = []

    for img in images:
        links.append(img.preview_url)

    return random.choice(links)
