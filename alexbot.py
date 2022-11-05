import asyncio
import json
import os
import discord
from discord.ext import commands
import random

# Config
with open('config.json', 'r') as cjson:
    config = json.load(cjson)

# Setup client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=config['command_prefix'], intents=intents)
client.config = config

@client.event
async def on_ready():
    print(f'''We have logged in as {client.user}
Command prefix = \'{config['command_prefix']}\'''')

async def main():

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

    # Register cogs
    for folder in os.listdir('cogs'):
        if os.path.exists(os.path.join('cogs', folder, 'cog.py')):
            await client.load_extension(f'cogs.{folder}.cog')

    await client.start(config['client_token'])

if __name__ == '__main__':
    asyncio.run(main())