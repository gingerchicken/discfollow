import discord
from discord.ext import tasks

import datetime
import asyncio

class FollowClient(discord.Client):
    __is_connecting   = False
    __is_disconncting = False

    def __init__(self, target_id, join_delay : int = 0, leave_delay : int = 0, play_audio : bool = False):
        # Specify the target ID
        self.target_id  = target_id

        # Delays
        self.join_delay = join_delay
        self.leave_delay = leave_delay

        # Play audio
        self.play_audio = play_audio

        # Super
        super().__init__()

    async def get_target(self):
        """Gets the target as a Discord user"""

        return self.get_user(int(self.target_id))

    async def on_ready(self):
        # Print who we are
        self.log('Logged in as', self.user, '!')

        # Find the target
        target_user = await self.get_target()

        # Make sure you're not None
        if target_user is None:
            # Print an error
            raise ValueError('Target user is None (the client couldn\'t find the target user)', target_user, self.target_id)

        # Print who we are following
        self.log('Targetting user', await self.get_target(), '!')

        # Start looking
        self.search_for_target.start()

        # Start playing music
        self.play_music.start()

    async def __disconnect_all(self):
        """Disconnects all voice clients"""

        for vc in self.voice_clients:
            await vc.disconnect()
    
    def log(self, *args, **kwargs):
        """Logs a message to the console in a pretty way"""

        print(datetime.datetime.now(), '|', *args, flush=True, **kwargs)

    async def __dc(self, vc):
        """Disconnects from a VC"""

        if self.__is_disconncting: return

        self.log('Disconnecting from', vc, 'in', vc.guild, f'(in {self.leave_delay} seconds)', '...')

        await self.__leave_wait()

        # Make sure that we have a client to disconnect from
        if vc.guild.voice_client is None: return

        # Disconnect the voice channel
        await vc.guild.voice_client.disconnect()

    async def __join_wait(self):
        """Waits the specified amount of seconds before joining"""

        if self.join_delay == 0: return

        self.__is_connecting = True
        await asyncio.sleep(self.join_delay)
        self.__is_connecting = False

    async def __leave_wait(self):
        """Waits the specified amount of seconds before leaving"""

        if self.leave_delay == 0: return

        self.__is_disconncting = True
        await asyncio.sleep(self.leave_delay)
        self.__is_disconncting = False

    async def __connect(self, vc):
        """Connects/moves to a VC"""

        if self.__is_connecting: return

        # Check if we have a client in that guild
        if vc.guild.voice_client is not None:
            self.log('Moving to', vc, '(from ' + str(vc.guild.voice_client.channel) + ')', 'in', vc.guild, f'(in {self.join_delay} seconds)', '...')

            await self.__join_wait()

            # Disconnect it from the voice channel
            await vc.guild.voice_client.disconnect()
            # TODO use move_to() instead of disconnect()
        else:
            self.log('Connecting to', vc, 'in', vc.guild, f'(in {self.join_delay} seconds)', '...')

            await self.__join_wait()

        try:
            await vc.connect()
        except discord.ClientException:
            self.log('Already connected to', vc)

    async def on_voice_state_update(self, member: discord.Member, before, after):
        """Handles VC state changes"""

        # Make sure that the member is not the bot itself
        if member.id == self.user.id: return

        # Make sure it is a channel change
        if before.channel == after.channel: return
        
        # Get the target
        target_user = await self.get_target()

        # Make sure that the member is the target
        if member != target_user: return

        # Get the target channel
        target_chan = after.channel if after.channel is not None else before.channel

        # Get the target channel's guild
        target_guild = target_chan.guild

        # Check if it was a disconnect
        if after.channel is None:
            # Get the before channel's guild as the target guild
            target_guild = before.channel.guild

            # Disconnect the voice channel
            await self.__dc(before.channel)

            return

        # Connect to the target channel
        await self.__connect(target_chan)
    
    async def on_exit(self):
        self.log('Disconnecting from all voice channels...')
        await self.__disconnect_all()

        self.log('Closing...')
        await self.close()
    
    @tasks.loop(seconds=15)
    async def search_for_target(self):
        """Looks for the target in all Discord servers"""

        # Get the target
        target_user = await self.get_target()

        # Get all out guilds
        guilds = self.guilds

        for guild in guilds:
            # Get the voice channels in the guild
            for voice_channel in guild.voice_channels:
                # Check if the voice channel contains our target
                if target_user not in voice_channel.members: continue

                # Check if we are already connected to the voice channel
                if self.user in voice_channel.members: continue

                # Connect to the voice channel
                await self.__connect(voice_channel)

                # Next guild
                break
    
    @tasks.loop(seconds=1)
    async def play_music(self):
        """Plays music in all voice channels"""
        if not self.play_audio: return

        for client in self.voice_clients:
            # Make sure the client is connected
            if not client.is_connected(): continue

            # Make sure that the client is not playing anything
            if client.is_playing(): continue

            # Play music in the voice channel
            client.play(discord.FFmpegPCMAudio('audio'))