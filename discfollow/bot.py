import discord
from discord.ext import tasks

import datetime
import asyncio

class FollowClient(discord.Client):
    __is_connecting   = False
    __is_disconncting = False

    def __init__(self, target_id, join_delay : int = 0, leave_delay : int = 0):
        # Specify the target ID
        self.target_id  = target_id

        # Delays
        self.join_delay = join_delay
        self.leave_delay = leave_delay

        # Super
        super().__init__()

    async def get_target(self):
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

    async def __disconnect_all(self):
        for vc in self.voice_clients:
            await vc.disconnect()
    
    def log(self, *args, **kwargs):
        print(datetime.datetime.now(), '|', *args, flush=True, **kwargs)

    async def __dc(self, vc):
        if self.__is_disconncting: return

        self.log('Disconnecting from', vc, 'in', vc.guild, f'(in {self.leave_delay} seconds)', '...')

        # Wait the leave delay
        self.__is_disconncting = True
        await asyncio.sleep(self.leave_delay)
        self.__is_disconncting = False

        # Make sure that we have a client to disconnect from
        if vc.guild.voice_client is None: return

        # Disconnect the voice channel
        await vc.guild.voice_client.disconnect()

    async def __connect(self, vc):
        if self.__is_connecting: return

        async def wait():
            # Wait the join delay
            self.__is_connecting = True
            await asyncio.sleep(self.join_delay)
            self.__is_connecting = False

        # Check if we have a client in that guild
        if vc.guild.voice_client is not None:
            self.log('Moving to', vc, '(from ' + str(vc.guild.voice_client.channel) + ')', 'in', vc.guild, f'(in {self.join_delay} seconds)', '...')

            await wait()

            # Disconnect it from the voice channel
            await vc.guild.voice_client.disconnect()
        else:
            self.log('Connecting to', vc, 'in', vc.guild, f'(in {self.join_delay} seconds)', '...')
            
            await wait()

        try:
            await vc.connect()
        except discord.ClientException:
            self.log('Already connected to', vc)

    async def on_voice_state_update(self, member: discord.Member, before, after):
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
    
    @tasks.loop(seconds=1)
    async def search_for_target(self):
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