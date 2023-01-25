import discord
from discord.ext import commands
import logging

class HardlyKnowHerCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        # Ignore messages sent by bot
        if message.author == self.client.user:
            return

        tokens = message.content.split(' ')        
        er_tokens = [token for token in tokens if token.endswith('er')]
        if len(er_tokens) == 0:
            return
        
        logging.info(f'Found tokens: {*er_tokens,}.')
        longest_token = max(er_tokens, key=len)
        logging.info(f'Longest token: {longest_token}.')

        if len(longest_token) < 5:
            logging.info(f'Token not long enough (min 5).')
            return

        image_filename = self.config['goteem_image']
        await message.channel.send(
            content=f"{longest_token}? I hardly know 'er",
            file=discord.File(image_filename),
            delete_after=5
        )

async def setup(client: commands.Bot):
    await client.add_cog(HardlyKnowHerCog(client))