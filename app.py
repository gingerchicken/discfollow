import os
import asyncio

from discfollow.bot import FollowClient

# Get the target ID from environment variables
target_id = os.environ['TARGET_ID']

# Get the token from environment variables
token = os.environ['TOKEN']

# Create the bot
bot = FollowClient(target_id)

# Login to Discord
bot.run(token)

# Make sure to close the bot in an async way
asyncio.run(bot.on_exit())