import discord
import random
import math

async def check_and_join(voice_channel, context, on_join=False):
    #If the author is not in any voice channel
    if not context.author.voice:
        await context.send('I cannot join, because you are not in any voice channel')
        return voice_channel #Do not return Null, because bot could be in channel but author not

    #If the bot is already in the channel
    if(voice_channel and context.author.voice.channel == voice_channel.channel):
        if on_join: #Otherwhise another call would be marked as responded
            await context.send('I already joined the "{}" channel'.format(voice_channel.channel.name))
        return voice_channel

    #Else leave current channel if possible and return connect() to new one
    await check_and_leave(voice_channel)
    if on_join: #Otherwhise another call would be marked as responded
        await context.send('I am joining: "{}"'.format(context.author.voice.channel.name))
    voice_channel = await context.author.voice.channel.connect()
    # voice_channel.play(discord.FFmpegPCMAudio('misc/smol.mp3'))
    return voice_channel

async def check_and_leave(voice_channel):
    if voice_channel != None:
        await voice_channel.disconnect()

def generate_teams(members, teams=2, fair=True):
    members.append('Test Member 1')
    members.append('Test Member 2')
    members.append('Test Member 3')
    members.append('Test Member 4')
    members.append('Test Member 5')

    random.shuffle(members)
    final_teams = [[] for _ in range(teams)]
    res_string = ""

    if fair:
        for i, member in enumerate(members):
            final_teams[i % teams].append(member)

    else:
        #fill one member in each team
        for i in range(teams):
            if len(members) > 0:
                final_teams[i].append(members.pop())
        #distr rest
        for member in members:
            final_teams[random.randint(0, teams - 1)].append(member)

    for i, team in enumerate(final_teams):
        res_string += f'**Team {i + 1}:** {", ".join(team)}\n'

    return str(res_string)
