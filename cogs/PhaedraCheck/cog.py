import datetime
import discord
from discord.ext import commands, tasks
import logging
import requests
import re

class PhaedraCheckCog(commands.Cog):
    fortnite_url = 'https://fortnite.gg/shop'

    def __init__(self, client):
        self.client = client
        self.config = client.config
        
        # Start looping task
        self.check_store.start()

    def cog_unload(self):
        self.check_store.cancel()

    @tasks.loop(time=datetime.time(hour=0, minute=1))
    async def check_store(self):
        try:
            page = requests.get(self.fortnite_url)
            html = page.text
        except Exception as e:
            logging.error(e)
            raise Exception(f'Could not get HTML from {self.fortnite_url}.')

        # Search for Phaedra
        if re.search('phaedra', html, re.IGNORECASE):
            logging.info(f'Found Phaedra at {self.fortnite_url}.')
            channel: discord.TextChannel = self.client.get_channel(self.config['phaedra_alert_channel_id'])
            if channel is None:
                logging.error("Failed to retrieve the designated Phaedra alert channel.")
                return
            try:
                await channel.send(content='MOMMY IS IN THE SHOP, THIS IS NOT A DRILL', \
                    file=discord.File(self.config['phaedra_image']))
                logging.info('Successfully sent Phaedra alert.')
            except Exception as e:
                logging.error(e)
                raise Exception("Phaedra is in the shop, but the message failed to send.", e)
        else:
            logging.info('Phaedra is not in the shop today :(')

async def setup(client: commands.Bot):
    await client.add_cog(PhaedraCheckCog(client))