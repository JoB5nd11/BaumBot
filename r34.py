import rule34
import random
import nest_asyncio
nest_asyncio.apply()

r34 = rule34.Sync()

def getr34img(search):
    images = r34.getImages(search)

    links = []

    for img in images:
        links.append(img.preview_url)

    return random.choice(links)
