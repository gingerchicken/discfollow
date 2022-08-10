import discord
from discord.ext import tasks
import datetime

class FollowClient(discord.Client):
    def __init__(self, target_id):
        # Specify the target ID
        self.target_id = target_id

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
            await self.__dc(vc)
    
    def log(self, *args, **kwargs):
        print(datetime.datetime.now(), '|', *args, flush=True, **kwargs)

    async def __dc(self, vc):
        self.log('Disconnecting from', vc.channel, 'in', vc.guild, '...')
        await vc.disconnect()
    
    async def __connect(self, vc):
        # Disconnect all
        await self.__disconnect_all()

        self.log('Connecting to', vc, 'in', vc.guild, '...')

        try:
            await vc.connect()
        except discord.ClientException:
            self.log('Already connected to', vc, '...')

    async def on_voice_state_update(self, member: discord.Member, before, after):
        # Make sure that the member is not the bot itself
        if member.id == self.user.id: return

        # Make sure it is a channel change
        if before.channel == after.channel: return
        
        # Get the target
        target_user = await self.get_target()

        # Get the target channel
        target = after.channel

        # Make sure that the member is the target
        if member != target_user: return

        # Find out if the user disconnected from a voice channel
        has_disconnected = target is None
        if has_disconnected:
            self.log('Target', target_user, 'has left', before.channel, '!')

            # Disconnect from the voice channel
            await self.__disconnect_all()

            return

        # Say where they joined
        self.log('Target', target_user, 'has joined', target, 'in', target.guild, '!')

        # Disconnect from the before voice channel
        # Get all the members in the before voice channel
        if before.channel is not None:
            await self.__disconnect_all()

        # Connect to the voice channel
        await self.__connect(after.channel)
    
    async def on_exit(self):
        self.log('Exiting...')

        self.log('Disconnecting from all voice channels...')
        await self.__disconnect_all()

        self.log('Logging out...')
        await self.logout()

        self.log('Closing...')
        await self.close()
    
    @tasks.loop(seconds=1)
    async def search_for_target(self):
        # Get the target
        target_user = await self.get_target()

        # Get all out guilds
        guilds = self.guilds

        found_target = False

        # Check if we are already connected to a channel with the target
        connected = len(self.voice_clients) > 0

        # Find the target in any of the guilds
        for guild in guilds:
            # Get all the voice channels in the guild
            voice_channels = guild.voice_channels

            # Find the target in any of the voice channels
            for voice_channel in voice_channels:
                # Get all the members in the voice channel
                members = voice_channel.members

                # Find the target in any of the members
                for member in members:
                    # self.log('Searching', member, 'for', target_user, '...')

                    # Check if the member is the target
                    if member != target_user: continue

                    # Say we found the target
                    found_target = True

                    # Connect to the voice channel if we are not already connected
                    if connected: break
                    
                    # Say where we found the target
                    self.log('Found target', target_user, 'in', voice_channel, 'in', guild, '!')

                    await self.__connect(voice_channel)

                    break

        if not found_target:
            # Disconnect from all voice channels
            await self.__disconnect_all()