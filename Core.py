#!/usr/bin/env python3
import datetime
import asyncio
from discord.ext import commands
import discord

Version = '0.1'

***REMOVED***

client = commands.Bot(command_prefix= ('!','!!'))
# client.remove_command('help')

# Dictionary of all existing players with server id as key
players = {}

# Dictionary of all player invoking channels per server with id as key
channels = {}

# TODO: add player queues, add catgirls, use cogs
# TODO: add youtube search

@client.event
async def on_ready():
    """
    Posts current time and a \'Bot Ready\' message to bot-status in my test
    server when bot starts
    """
    # Print startup message to speciified channel with startup time
    current_time = datetime.datetime.now().strftime('%A %B %d %Y %X')
    await client.send_message(discord.Object(id='269203549186031617'),
        '**{} : Bot Ready**, version = {}'.format(current_time, Version))

    # Rich presence times out after a while so updates every 12 hours
    while True:
        await client.change_presence(game=discord.Game(
            name='!communist_propaganda'))
        await asyncio.sleep(12 * 3600)

@client.event
async def on_voice_state_update(before, after):
    """Checks for empty voice channel and leaves (and pauses players)
    if found"""
    voice_client = client.voice_client_in(after.server)
    if voice_client:
        # if bot is in voice channel in server
        if not tuple(filter(lambda z: not z,
            [x.bot for x in voice_client.channel.voice_members])):
            # and if only bots are in voice channel (rather there are not
            # any members who aren't bots)
            channel = channels[id]
            await client.send_message(channel,
            'Pausing **{}**'.format(player.title))
            try:
                # Bot trys to pauses music stream
                id = after.server.id
                player = players[id]
                players[id].pause()
            except KeyError:
                pass

            await voice_client.disconnect()

@client.command(name='ssf')
async def stupid_sexy_flanders():
    """Posts flanders picture to channel"""
    ssfurl = 'https://cdn.discordapp.com/attachments/268166253288488960/478362864340434966/Stupid_Sexy_Flanders_Tapped_Out.png'
    emb = discord.Embed().set_image(url=ssfurl)
    await client.say(embed=emb)

@client.command(pass_context=True)
async def clear(ctx, amount=5):
    """
    clears \'amount\' messages from channel (includes invoking message as 1 of
    them)
    """
    server = ctx.message.server
    if server.name == 'Test':
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        length = len(messages)
        await client.delete_messages(messages)
        await client.say('**Deleted {} messages**'.format(length))

# @client.command(pass_context=True)
# async def help(ctx, pm=False):
#     emb = discord.Embed(
#         title = 'Help',
#         colour = discord.Colour.pink()
#     )
#
#     emb.add_field(name='!ssf', value='Returns StupidSexyFlanders Picture',
#         inline=False)
#     emb.add_field(name='clear', value='Clears number of messages, default 5',
#         inline=False)
#     if pm == True:
#         await client.send_message(ctx.message.author, embed=emb)
#     else:
#         await client.say(embed=emb)

@client.command(pass_context=True)
async def join(ctx):
    """Bot joins user voice channel"""
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server
    try:
        # Try to join channel
        await client.join_voice_channel(channel)
    except discord.errors.InvalidArgument:
        # Except if user is not in a voice channel
        await client.say(
        '**{}** is not in a voice channel.'.format(ctx.message.author.name))
    except discord.errors.ClientException:
        # Except bot is already in a voice channel
        voice_client = client.voice_client_in(server)
        if voice_client.channel == channel:
            # Bot is in same channel as user
            await client.say('I\'m already in that channel')
        else:
            # Bot changes channel to user
            await voice_client.disconnect()
            await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    """Bot leaves voice channel in server"""
    server = ctx.message.server
    try:
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()
    except AttributeError:
        await client.say('I am not in a voice channel comrade.')

@client.command(pass_context=True)
async def play(ctx, url):
    """Bot plays from youtube url"""
    id = ctx.message.server.id
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server

    try:
        # Try to join channel
        await client.join_voice_channel(channel)
    except discord.errors.InvalidArgument:
        # Except if user is not in a voice channel
        await client.say(ctx.message.author.name +
            ' is not in a voice channel.')
        return
    except discord.errors.ClientException:
        # Except bot is already in a voice channel
        voice_client = client.voice_client_in(server)
        if voice_client.channel == channel:
            # Bot is in same channel as user
            pass
        else:
            # Bot changes channel to user
            await voice_client.disconnect()
            await client.join_voice_channel(channel)

    try:
        # First stops any existing players
        player_title = players[id].title
        players[id].stop()
        await client.say('Now stopping **{}**'.format(player_title))
    except KeyError:
        # If nothing was playing does nothing
        pass

    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    channels[server.id] = ctx.message.channel
    player.start()

    await client.delete_message(ctx.message)
    await client.say('Now Playing **{}**'.format(player.title))

@client.command(pass_context=True)
async def pause(ctx):
    """Bot pauses music stream"""
    try:
        id = ctx.message.server.id
        player = players[id]
        await client.say('Pausing ' + player.title)
        players[id].pause()
    except KeyError:
        pass

@client.command(pass_context=True)
async def stop(ctx):
    """Bot stops music stream"""
    id = ctx.message.server.id
    player = players[id]
    await client.say('Stopping ' + player.title)
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    """Bot resumes music stream"""
    id = ctx.message.server.id
    player = players[id]
    await client.say('Resuming ' + player.title)
    players[id].resume()

@client.command(pass_context=True, name='commie')
async def communist_propaganda(ctx):
    """Bot plays communist music"""
    id = ctx.message.server.id
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server

    try:
        # Try to join channel
        await client.join_voice_channel(channel)
    except discord.errors.InvalidArgument:
        # Except if user is not in a voice channel
        await client.say(ctx.message.author.name +
            ' is not in a voice channel.')
        return
    except discord.errors.ClientException:
        # Except bot is already in a voice channel
        voice_client = client.voice_client_in(server)
        if voice_client.channel == channel:
            # Bot is in same channel as user
            pass
        else:
            # Bot changes channel to user
            await voice_client.disconnect()
            await client.join_voice_channel(channel)

    try:
        # First stops any existing players
        player_title = players[id].title
        players[id].stop()
        await client.say('Now stopping **{}**'.format(player_title))
    except KeyError:
        # If nothing was playing does nothing
        pass

    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(
    'https://www.youtube.com/watch?v=TaNtIYZj0m0')
    players[server.id] = player
    channels[server.id] = ctx.message.channel
    player.start()

    await client.delete_message(ctx.message)
    await client.say('Now Playing **{}**'.format(player.title))

async def bot_update():
    """
    Looping Function to update on current bot status by printing and sending to
    bot-status in my test server, a list of servers the bot is currently
    connected to along with the time and date.
    """
    await client.wait_until_ready()
    while not client.is_closed:
        servs= ''
        print("Current servers:")
        for server in client.servers:
            print(server.id + ' : ' + server.name)
            servs = servs + server.id + ' : ' + server.name + '\n'

        current_time = datetime.datetime.now().strftime('%A %B %d %Y %X')
        print(current_time)

        emb = discord.Embed(
            title = 'Bot Update',
            colour = discord.Colour.green()
        )
        emb.add_field(name='Time:', value=current_time, inline=False)
        emb.add_field(name='Current Servers:', value=servs, inline=False)
        await client.send_message(discord.Object(id='478584604362539008'),
            embed=emb)

        await asyncio.sleep(6000)

client.loop.create_task(bot_update())
client.run(TOKEN)
