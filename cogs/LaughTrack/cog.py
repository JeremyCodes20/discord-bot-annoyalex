import asyncio
import os
import random
import discord
from discord.ext import commands
import logging

class LaughTrackCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def laugh(self, ctx: commands.Context):
        user = ctx.message.author
        logging.info(f'Received laugh command from user: {user.name}.')
        channel = user.voice.channel

        laughtrack_directory = './' + self.config['laughtrack_directory']
        laughtrack_filenames = os.listdir(laughtrack_directory)
        num_laughtracks = len(laughtrack_filenames)
        logging.info(f'Found {num_laughtracks} laughtracks.')
        choice = random.randint(0, num_laughtracks - 1)
        laughtrack_filename = laughtrack_filenames[choice]

        logging.info(f'Playing {laughtrack_filename} for user {user.name}.')
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(laughtrack_directory + '/' + laughtrack_filename))
        while vc.is_playing():
            await asyncio.sleep(1)
            
        logging.info(f'Finished playing {laughtrack_filename} for user {user.name}.')
        await vc.disconnect()
        
async def setup(client: commands.Bot):
    await client.add_cog(LaughTrackCog(client))