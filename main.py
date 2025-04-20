import asyncio
from pyrogram import Client, idle
from config.env import API_ID, API_HASH, BOT_TOKEN
from bot.handlers import play_handler, radio_handler, inline_handler
from userbot.client import userbot

async def main():
    # Initialize bot
    bot = Client(
        "stream_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    # Start bot
    await bot.start()
    print("Bot started!")

    # Start userbot
    await userbot.start()
    print("Userbot started!")

    # Keep the app running
    await idle()

    # Stop both on shutdown
    await bot.stop()
    await userbot.stop()

if __name__ == "__main__":
    asyncio.run(main())