import discord
import os
import platform
import requests
import json
import random
import asyncio
import nacl
import pandas as pd

import youtube_dl
import randomreddit
import all_commands

client = discord.Client()
vc = None # current voice channel

music_queue = []
sad_words = ["traurig", "deprimiert", "unglücklich", "wütend", "niedergeschlagen", "depressiv"]
starter_encouragements = ["Heul net rum!", "Heul leise!", "Is mir egal!"]
ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

def get_random_insult(username):
	file = open('insults.txt', 'r', encoding='utf-8')
	lines = file.readlines()
	all_insults = []
	for line in lines:
		elements = line.split('[name]')
		all_insults.append(elements[0] + username + elements[1])
	final_answer = random.choice(all_insults)
	final_answer = final_answer.replace('  ', ' ')
	return final_answer



def get_quote():
	response = requests.get('https://zenquotes.io/api/random')
	json_data = json.loads(response.text)
	#quote = translator.translate(json_data[0]['q']) + '\n\t-' + json_data[0]['a']
	quote = json_data[0]['q'] + '\n\t-' + json_data[0]['a']
	return quote

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	global vc

	if message.author == client.user:
		return

	if message.content.startswith('/help'): #v
		await message.channel.send(all_commands.print_all_commands())

	elif message.content.startswith('/hallo'): #v
		await message.channel.send('Hallo :)')

	elif message.content.startswith('/inspire'): #v
		await message.channel.send(get_quote())

	elif any(word in message.content for word in sad_words):
		await message.channel.send(random.choice(starter_encouragements))

	elif message.content.startswith('/insult'): #v
		username = message.content.split('/insult', 1)[1]
		await message.channel.send(get_random_insult(username))

	elif message.content.startswith('/randomreddit'): #v
		await message.channel.send(randomreddit.get_subreddit())

	elif message.content.startswith('/Sieg'): #v
		await message.channel.send('𝕳𝖊𝖎𝖑')

	elif message.content.startswith('#join'): #v
		vc = await message.author.voice.channel.connect()

	elif message.content.startswith('/leave'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		await vc.disconnect()
		vc = None

	elif message.content.startswith('/heehee'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('HeeHee.mp3'))

	elif message.content.startswith('/rrr'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('rrr.mp3'))

	elif message.content.startswith('/hoyaa'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('hoyaa.mp3'))

	elif("lmao" in message.content or "Lmao" in message.content or "LMAO" in message.content):
		await message.channel.send('lmao')


	elif message.content.startswith('/speakas'): #v
		name = message.content.split('/speakas ', 1)[1]
		if not vc:
			vc = await message.author.voice.channel.connect()

		if name == "Johannes" or name == "johannes":
			vc.play(discord.FFmpegPCMAudio('johannes.mp3'))


	elif message.content.startswith('/play'): #v
		if not vc:
			vc = await message.author.voice.channel.connect()

		video_link = message.content.split('/play', 1)[1]

		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(video_link, download=False)
				url = info['entries'][0]['url']
				vc.play(discord.FFmpegPCMAudio(url))
		except:
			music_queue.append(video_link)

		"""
		Allgemeine Queue implementieren
		-> D.h. jedes Video kommt in die Queue
		-> Thread schaut ob die Queue gefüllt ist und ob gerade ein song spielt, sonst nächster song in der queue

		+ next song command
		+ empty queue command
		+ now! command
		+ repeat_current [number]
		"""

	elif message.content.startswith('/stop'): #v
		try:
			vc.stop()
		except:
			pass

	elif message.content.startswith('/Yamete'):
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('Yamete.mp3'))

	elif message.content.startswith('/Moan'):
		if not vc:
			vc = await message.author.voice.channel.connect()
		vc.play(discord.FFmpegPCMAudio('moan.mp3'))

client.run('') #change new token
