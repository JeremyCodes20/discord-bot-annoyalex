import asyncio
import json
import discord
from discord.ext import commands
import random
import datetime


# Config
with open('config.json', 'r') as cjson:
    config = json.load(cjson)

# Setup client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=config['command_prefix'], intents=intents)

g_last_played_intro = None

@client.event
async def on_ready():
    print(f'''We have logged in as {client.user}
Command prefix = \'{config['command_prefix']}\'''')

@client.event
async def on_message(message: discord.message.Message):
    # Ignore messages sent by bot
    if message.author == client.user:
        return

    # Annoy Alex
    if message.author.name == config['annoy_user']:
        x = random.randint(1, 10)
        if x == 1:
            await message.channel.send(file=discord.File(config['annoy_image']))

    await client.process_commands(message)

@client.event
async def on_voice_state_update(member: discord.member.Member, before: discord.VoiceState, after: discord.VoiceState):
    # Ignore when the bot enters/leaves the chat
    if member.name == client.user.name:
        return

    if member.name in config['intro_users']:
        # Joined a channel
        if before.channel == None and after.channel != None:
            channel = after.channel
            print(f'{member.name} joined voice channel: {channel.name}')

            global g_last_played_intro
            if g_last_played_intro == None or abs((g_last_played_intro - datetime.datetime.now())) > datetime.timedelta(minutes=5):
                g_last_played_intro = datetime.datetime.now()

                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(config['intro_mp3']))
                while vc.is_playing():
                    await asyncio.sleep(1)
            
                await vc.disconnect()

    # Left a channel
    if member.name in config['left_users'] or len(config['left_users']) == 0:
        if before.channel != None and after.channel == None:
            channel = before.channel
            print(f'{member.name} left voice channel: {channel.name}')

            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(config['left_mp3']))
            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()

@client.command()
async def outro(ctx: commands.Context):
    user = ctx.message.author

    # if user.name == 'Eggkiller':
    if user.name in config['outro_users'] or len(config['outro_users']) == 0:
        channel = user.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(config['outro_mp3']))
        while vc.is_playing():
            await asyncio.sleep(1)
        
        await vc.disconnect()

client.run('MTAzODI0OTYwNzQxMjU4NDQ3MA.Gcu8UM.1XSR9nN1OTFxyWT-96nPXouqGsR7fLaxJeOqjY')