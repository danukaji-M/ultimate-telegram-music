import asyncio
import os
from pyrogram import Client
from config.env import API_ID, API_HASH
from config.logging import logger

SESSION_FILE = "userbot.session"

async def generate_session() -> str:
    """Generate a new session string and save it to SESSION_FILE."""
    logger.info("No session file found. Generating a new session...")
    try:
        app = Client(
            "generate_session",
            api_id=API_ID,
            api_hash=API_HASH,
            workdir="."
        )
        async with app:
            session_string = await app.export_session_string()
            with open(SESSION_FILE, "w") as f:
                f.write(session_string)
            logger.info(f"Session generated and saved to {SESSION_FILE}")
            return session_string
    except Exception as e:
        logger.error(f"Failed to generate session: {e}")
        raise

async def get_session() -> str:
    """Retrieve session string from file or generate a new one."""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                session_string = f.read().strip()
            if session_string:
                logger.info(f"Using existing session from {SESSION_FILE}")
                return session_string
            else:
                logger.warning("Session file is empty. Generating a new session.")
        return await generate_session()
    except Exception as e:
        logger.error(f"Error reading session file: {e}")
        return await generate_session()

async def initialize_userbot() -> Client:
    """Initialize the userbot client with session string."""
    try:
        session_string = await get_session()
        userbot = Client(
            "userbot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            workdir="."
        )
        logger.info("Userbot client initialized successfully")
        return userbot
    except Exception as e:
        logger.error(f"Failed to initialize userbot client: {e}")
        raise

# Initialize userbot as None; set in main.py
userbot = None