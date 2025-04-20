import asyncio
import logging
from pyrogram import Client, idle
from config.env import API_ID, API_HASH, BOT_TOKEN
from config.logging import logger
from bot.handlers import play_handler, radio_handler, inline_handler
from userbot.client import initialize_userbot
from userbot.streamer import Streamer

async def main():
    """Main function to initialize and run the bot and userbot."""
    try:
        # Initialize bot client
        bot = Client(
            "stream_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workdir="."
        )

        # Initialize userbot client
        userbot = await initialize_userbot()

        # Initialize streamer with the userbot client
        streamer = Streamer(userbot)

        # Register handlers with bot and streamer
        play_handler.register(bot, streamer)
        radio_handler.register(bot, streamer)
        inline_handler.register(bot)

        # Start bot and userbot
        await bot.start()
        await userbot.start()
        logger.info("Bot and userbot started successfully")

        # Keep the application running
        await idle()

        # Cleanup on exit
        await bot.stop()
        await userbot.stop()
        logger.info("Bot and userbot stopped")
    except Exception as e:
        logger.error(f"Failed to run application: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())