import discord
from discord.ext import commands
import datetime
import asyncio
import logging

class IntroOutroCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config
        self.last_played_intro = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.member.Member, before: discord.VoiceState, after: discord.VoiceState):
        # Ignore when the bot enters/leaves the chat
        if member.name == self.client.user.name:
            return

        # Joined a channel
        if before.channel == None and after.channel != None:
            logging.debug(f'User {member.name} joined {after.channel.name}.')
            if member.name in self.config['intro_users']:
                channel = after.channel

                logging.debug(f'User {member.name} is in the configured intro list.')
                if self.last_played_intro == None or abs((self.last_played_intro - datetime.datetime.now())) > datetime.timedelta(minutes=5):
                    self.last_played_intro = datetime.datetime.now()

                    audio_filename = self.config['intro_mp3']
                    logging.info(f'Playing {audio_filename} for user {member.name}.')
                    vc = await channel.connect()
                    vc.play(discord.FFmpegPCMAudio(self.config['intro_mp3']))
                    while vc.is_playing():
                        await asyncio.sleep(1)

                    logging.info(f'Finished playing {audio_filename} for user {member.name}.')
                    await vc.disconnect()

        # Left a channel
        if before.channel != None and after.channel == None:
            logging.debug(f'User {member.name} left {before.channel.name}.')
            if member.name in self.config['left_users'] or len(self.config['left_users']) == 0:
                channel = before.channel
                logging.debug(f'User {member.name} is in the configured left list.')

                audio_filename = self.config['left_mp3']
                logging.info(f'Playing {audio_filename} for user {member.name}.')
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(audio_filename))
                while vc.is_playing():
                    await asyncio.sleep(1)

                logging.info(f'Finished playing {audio_filename} for user {member.name}.')
                await vc.disconnect()
    
    @commands.command()
    async def outro(self, ctx: commands.Context):
        user = ctx.message.author
        logging.info(f'Received outro command from user: {user.name}.')

        if user.name in self.config['outro_users'] or len(self.config['outro_users']) == 0:
            logging.debug(f'User {user.name} is in the configured outro list.')
            channel = user.voice.channel

            audio_filename = self.config['outro_mp3']
            logging.info(f'Playing {audio_filename} for user {user.name}.')
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(audio_filename))
            while vc.is_playing():
                await asyncio.sleep(1)
            
            logging.info(f'Finished playing {audio_filename} for user {user.name}.')
            await vc.disconnect()

async def setup(client: commands.Bot):
    await client.add_cog(IntroOutroCog(client))