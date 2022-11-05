import random
import discord
from discord.ext import commands

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
            x = random.randint(1, 10)
            if x == 1:
                await message.channel.send(file=discord.File(self.config['annoy_image']))

        # await self.client.process_commands(message)

async def setup(client: commands.Bot):
    await client.add_cog(AnnoyAlexCog(client))