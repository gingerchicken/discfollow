import os
import asyncio

from discfollow.bot import FollowClient

# Environment variables
TOKEN       = str(os.environ['TOKEN'])
TARGET_ID   = int(os.environ['TARGET_ID'])
JOIN_DELAY  = int(os.environ['JOIN_DELAY'])
LEAVE_DELAY = int(os.environ['LEAVE_DELAY'])
PLAY_AUDIO  = os.environ['PLAY_AUDIO'].lower() == 'true'

# Create the bot
bot = FollowClient(
    target_id=TARGET_ID,
    join_delay=JOIN_DELAY,
    leave_delay=LEAVE_DELAY,
    play_audio=PLAY_AUDIO
)

# Enable logging
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(handler)

# Login to Discord
bot.run(TOKEN)

# Make sure to close the bot in an async way
asyncio.run(bot.close())