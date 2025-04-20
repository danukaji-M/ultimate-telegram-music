from pyrogram import Client
from config.constants import OWNER_ID

async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    if user_id == OWNER_ID:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

async def is_banned(client: Client, user_id: int) -> bool:
    # Placeholder for banned user check (e.g., from a database)
    return False