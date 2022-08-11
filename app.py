import os
import asyncio

from discfollow.bot import FollowClient

# Environment variables
TOKEN       = str(os.environ['TOKEN'])
TARGET_ID   = int(os.environ['TARGET_ID'])
JOIN_DELAY  = int(os.environ['JOIN_DELAY'])
LEAVE_DELAY = int(os.environ['LEAVE_DELAY'])

# Create the bot
bot = FollowClient(
    target_id=TARGET_ID,
    join_delay=JOIN_DELAY,
    leave_delay=LEAVE_DELAY
)

# Login to Discord
bot.run(TOKEN)

# Make sure to close the bot in an async way
asyncio.run(bot.close())