import discord
from discord.ext import commands
import datetime
import asyncio

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

        if member.name in self.config['intro_users']:
            # Joined a channel
            if before.channel == None and after.channel != None:
                channel = after.channel
                print(f'{member.name} joined voice channel: {channel.name}')

                if self.last_played_intro == None or abs((self.last_played_intro - datetime.datetime.now())) > datetime.timedelta(minutes=5):
                    self.last_played_intro = datetime.datetime.now()

                    vc = await channel.connect()
                    vc.play(discord.FFmpegPCMAudio(self.config['intro_mp3']))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                
                    await vc.disconnect()

        # Left a channel
        if member.name in self.config['left_users'] or len(self.config['left_users']) == 0:
            if before.channel != None and after.channel == None:
                channel = before.channel
                print(f'{member.name} left voice channel: {channel.name}')

                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(self.config['left_mp3']))
                while vc.is_playing():
                    await asyncio.sleep(1)
                
                await vc.disconnect()
    
    @commands.command()
    async def outro(self, ctx: commands.Context):
        user = ctx.message.author

        # if user.name == 'Eggkiller':
        if user.name in self.config['outro_users'] or len(self.config['outro_users']) == 0:
            channel = user.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(self.config['outro_mp3']))
            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()

async def setup(client: commands.Bot):
    await client.add_cog(IntroOutroCog(client))