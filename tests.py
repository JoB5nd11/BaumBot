import textwrap
import youtube_dl

playlists = [
    "https://www.youtube.com/watch?v=d6IhaGEuXwI&list=PLFgZ5KdvG7UShk8ijQSd84vYZ35jr8wOL"
]

for playlist in playlists:
    with youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True}) as ydl:
        playlist_dict = ydl.extract_info(playlist, download=False)
        print(playlist_dict["entries"])
        quit()
