from pyrogram import Client
from config.env import API_ID, API_HASH
import os
import asyncio

SESSION_FILE = "userbot.session"

async def generate_session():
    """Generate a new session string and save it to SESSION_FILE."""
    print("No session file found. Generating a new session...")
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
        print(f"Session generated and saved to {SESSION_FILE}")
        return session_string

async def get_session():
    """Retrieve session string from file or generate a new one."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session_string = f.read().strip()
        print(f"Using existing session from {SESSION_FILE}")
        return session_string
    else:
        return await generate_session()

# Initialize userbot client
userbot = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=asyncio.run(get_session()),
    workdir="."
)