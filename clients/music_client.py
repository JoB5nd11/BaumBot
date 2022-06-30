import discord
import youtube_dl


class MusicClient:
    def __init__(self):
        self.ydl_opts = ydl_opts = {
        	'format': 'bestaudio/best',
        	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        	'restrictfilenames': True,
        	'noplaylist': False,
        	'nocheckcertificate': True,
        	'ignoreerrors': False,
        	'logtostderr': False,
        	'quiet': True,
        	'no_warnings': True,
        	'default_search': 'auto',
            'dump_single_json': True,
            'extract_flat': True,
        	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
        }
        self.youtube = youtube_dl.YoutubeDL(ydl_opts)
        self.queue = []
        self.current_song = ""
        self._current_url = ""

    def play(self, voice_channel, url):
        #TODO Differenciate between youtube and spotify
        if "youtu.be" in url:
            url = "https://www.youtube.com/watch?v=" + url.split("/")[-1]

        #its a radio and not a playlist
        if "&list=" in url and "&start_radio" in url:
            video_id = url.split('watch?v=')[1].split('&list=')[0]
            url = "https://www.youtube.com/watch?v=" + video_id

        #its a playlist
        if "&list=" in url and not "&start_radio" in url:
            playlist_id = url.split('list=')[1]
            url = "https://www.youtube.com/playlist?list=" + playlist_id

        if "playlist" in url:
            try:
                playlists_dict = self.youtube.extract_info(url, download=False)
                for entrie in playlists_dict['entries']:
                    self.queue.append("https://www.youtube.com/watch?v=" + entrie['url'])

                self._play_next_song(voice_channel)
                return f'Added {len(playlists_dict["entries"])} songs the the queue...'
            except:
                return f'I tried to add a playlist but something went wrong :( \nThe link was {url}'

        #single video no playlist or else
        info = self.youtube.extract_info(url, download=False)
        get_url = info['url']
        try:
            voice_channel.play(discord.FFmpegPCMAudio(get_url), after=lambda x=0: self._play_next_song(voice_channel))
            self.current_song = info['title']
            self._current_url = url
            return 'Now playing: "' + info['title'] + '"'

        except:
            self.queue.append(url)
            return 'Added "' + info['title'] + '" to queue'

    def pause(self, voice_channel):
        if voice_channel.is_playing:
            voice_channel.pause() #Check things <- wat?

    def resume(self, voice_channel):
        if voice_channel.is_paused:
            voice_channel.resume()

    def stop(self, voice_channel):
        if voice_channel.is_playing:
            voice_channel.stop() #What about the queue

    #OPTIMIZE!
    def print_queue(self):
        result = ""
        for i, url in enumerate(self.queue):
            with self.youtube as ydl:
                info = ydl.extract_info(url, download=False)
                result += str(i + 1) + ":\t" + info['title'] + "\n"

        if result == "":
            result = "no songs in queue"

        return result

    def clear_queue(self):
        length = len(self.queue)
        self.queue = []
        return "Cleared {} songs".format(length)

    def next_song(self, voice_channel):
        voice_channel.stop()
        self._play_next_song(voice_channel)
        return "Jumped to next song"

    def repeat_current_song(self, count):
        new_queue = []
        for c in range(count):
            new_queue.append(self._current_url)

        new_queue += self.queue
        self.queue = new_queue

        return "Current song now {} times in queue".format(count)

    def _play_next_song(self, voice_channel):
        self.current_song = "Not playing anything"
        if len(self.queue) > 0:
            url = self.queue.pop(0)

            with self.youtube as ydl:
                info = ydl.extract_info(url, download=False)
                get_url = info['url']

            self.current_song = info['title']
            self._current_url = url
            voice_channel.play(discord.FFmpegPCMAudio(get_url), after=lambda x=0: self._play_next_song(voice_channel))


if __name__ == '__main__':
    mc = MusicClient()
    with mc.youtube as ydl:
        playlists_dict = ydl.extract_info("https://www.youtube.com/playlist?list=PLFgZ5KdvG7UShk8ijQSd84vYZ35jr8wOL", download=False)
        for entrie in playlists_dict['entries']:
            print(entrie['url'])
