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
    return await context.author.voice.channel.connect()

async def check_and_leave(voice_channel):
    if voice_channel != None:
        await voice_channel.disconnect()
