import rule34
import random
import nest_asyncio
nest_asyncio.apply()

r34 = rule34.Sync()

def getr34img(search, gay, hentai, animated, drawing, comic):

    tags = []
    if gay == True:
        tags.append("gay")

    if hentai == True:
        tags.append("hentai")

    if animated == True:
        tags.append("animated")

    if drawing == True:
        tags.append("drawing")

    if comic == True:
        tags.append("comic")

    if len(tags)>0:
        images = r34.getImages(search, tags)
    else:
        images = r34.getImages(search)

    links = []

    if not images:
        return "No images found"

    for img in images:
        links.append(img.preview_url)

    returnlink = random.choice(links)
    print(returnlink)

    return returnlink
