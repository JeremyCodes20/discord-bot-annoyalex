import random
import discord
from discord.ext import commands
import logging

class AnnoyAlexCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        # Ignore messages sent by bot
        if message.author == self.client.user:
            return

        # Annoy Alex
        if message.author.name == self.config['annoy_user']:
            logging.debug(f'User {message.author.name} sent a message.')
            x = random.randint(1, 10)
            if x == 1:
                image_filename = self.config['annoy_image']
                logging.debug(f'Sending image: {image_filename}')
                await message.channel.send(file=discord.File(image_filename))

        # await self.client.process_commands(message)

async def setup(client: commands.Bot):
    await client.add_cog(AnnoyAlexCog(client))