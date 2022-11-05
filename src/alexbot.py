import asyncio
import discord
from discord.ext import commands
import random
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

g_last_played_intro = None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.message.Message):
    # Ignore messages sent by bot
    if message.author == client.user:
        return

    # Annoy Alex
    if message.author.name == 'AlexW':
        x = random.randint(1, 10)
        if x == 1:
            await message.channel.send(file=discord.File('img/20151230_055139000_iOS.jpg'))

    await bot.process_commands(message)

@client.event
async def on_voice_state_update(member: discord.member.Member, before: discord.VoiceState, after: discord.VoiceState):
    # Ignore when the bot enters/leaves the chat
    if member.name == client.user.name:
        return

    if member.name == 'Eggkiller':
        # Joined a channel
        if before.channel == None and after.channel != None:
            channel = after.channel
            print(f'{member.name} joined voice channel: {channel.name}')

            global g_last_played_intro
            if g_last_played_intro == None or abs((g_last_played_intro - datetime.datetime.now())) > datetime.timedelta(minutes=5):
                g_last_played_intro = datetime.datetime.now()

                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio('audio/intro_edited_volume_fixed.mp3'))
                while vc.is_playing():
                    await asyncio.sleep(1)
            
                await vc.disconnect()

    # Left a channel
    if before.channel != None and after.channel == None:
        channel = before.channel
        print(f'{member.name} left voice channel: {channel.name}')

        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('audio/RobloxDeathSound.mp3'))
        while vc.is_playing():
            await asyncio.sleep(1)
        
        await vc.disconnect()

@bot.command()
async def outro(ctx: commands.Context):
    print("Command received")
    user = ctx.message.author

    # if user.name == 'Eggkiller':
    channel = user.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('audio/outro.mp3'))
    while vc.is_playing():
        await asyncio.sleep(1)
    
    await vc.disconnect()

client.run('MTAzODI0OTYwNzQxMjU4NDQ3MA.Gcu8UM.1XSR9nN1OTFxyWT-96nPXouqGsR7fLaxJeOqjY')