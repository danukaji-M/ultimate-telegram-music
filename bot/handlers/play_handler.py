from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.yt_streamer import get_youtube_stream, get_playlist_streams
from userbot.streamer import Streamer
from config.constants import OWNER_ID
import asyncio

@Client.on_message(filters.command("play") & filters.group)
async def play_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide a song name or YouTube link!")
        return

    try:
        # Get stream URL (audio only)
        stream_url = await get_youtube_stream(query, audio_only=True)
        if not stream_url:
            await message.reply("Could not find the song!")
            return

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(message.chat.id):
            await streamer.join_vc(message.chat.id)

        # Start streaming
        await streamer.start_stream(stream_url, message.chat.id)
        await message.reply(f"🎵 Now playing: {query}")
    except Exception as e:
        await message.reply(f"Error playing song: {str(e)}")
        print(f"Error in /play: {e}")

@Client.on_message(filters.command("vplay") & filters.group)
async def vplay_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide a video name or YouTube link!")
        return

    try:
        # Get stream URL (video + audio)
        stream_url = await get_youtube_stream(query, audio_only=False)
        if not stream_url:
            await message.reply("Could not find the video!")
            return

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(message.chat.id):
            await streamer.join_vc(message.chat.id)

        # Start streaming
        await streamer.start_stream(stream_url, message.chat.id)
        await message.reply(f"🎥 Now playing video: {query}")
    except Exception as e:
        await message.reply(f"Error playing video: {str(e)}")
        print(f"Error in /vplay: {e}")

@Client.on_message(filters.command("playlist") & filters.group)
async def playlist_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide a playlist name or YouTube playlist link!")
        return

    try:
        # Get playlist stream URLs
        playlist_urls = await get_playlist_streams(query)
        if not playlist_urls:
            await message.reply("Could not find the playlist!")
            return

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(message.chat.id):
            await streamer.join_vc(message.chat.id)

        # Add playlist to queue and start streaming
        await streamer.add_to_queue(playlist_urls, message.chat.id)
        await streamer.start_stream(playlist_urls[0], message.chat.id)
        await message.reply(f"🎶 Started playing playlist: {query} ({len(playlist_urls)} tracks)")
    except Exception as e:
        await message.reply(f"Error playing playlist: {str(e)}")
        print(f"Error in /playlist: {e}")

@Client.on_message(filters.command("stop") & filters.group)
async def stop_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if await streamer.is_in_vc(message.chat.id):
            await streamer.stop_stream(message.chat.id)
            await streamer.leave_vc(message.chat.id)
            await message.reply("⏹ Stopped streaming and left VC.")
        else:
            await message.reply("Not in a voice chat!")
    except Exception as e:
        await message.reply(f"Error stopping stream: {str(e)}")
        print(f"Error in /stop: {e}")

@Client.on_message(filters.command("join") & filters.group)
async def join_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if not await streamer.is_in_vc(message.chat.id):
            await streamer.join_vc(message.chat.id)
            await message.reply("✅ Joined voice chat!")
        else:
            await message.reply("Already in voice chat!")
    except Exception as e:
        await message.reply(f"Error joining VC: {str(e)}")
        print(f"Error in /join: {e}")

@Client.on_message(filters.command("leave") & filters.group)
async def leave_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if await streamer.is_in_vc(message.chat.id):
            await streamer.leave_vc(message.chat.id)
            await message.reply("👋 Left voice chat!")
        else:
            await message.reply("Not in a voice chat!")
    except Exception as e:
        await message.reply(f"Error leaving VC: {str(e)}")
        print(f"Error in /leave: {e}")

@Client.on_message(filters.command("pause") & filters.group)
async def pause_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if await streamer.is_in_vc(message.chat.id):
            await streamer.pause_stream(message.chat.id)
            await message.reply("⏸ Stream paused.")
        else:
            await message.reply("Not in a voice chat!")
    except Exception as e:
        await message.reply(f"Error pausing stream: {str(e)}")
        print(f"Error in /pause: {e}")

@Client.on_message(filters.command("resume") & filters.group)
async def resume_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if await streamer.is_in_vc(message.chat.id):
            await streamer.resume_stream(message.chat.id)
            await message.reply("▶️ Stream resumed.")
        else:
            await message.reply("Not in a voice chat!")
    except Exception as e:
        await message.reply(f"Error resuming stream: {str(e)}")
        print(f"Error in /resume: {e}")

@Client.on_message(filters.command("skip") & filters.group)
async def skip_command(client: Client, message: Message):
    try:
        streamer = Streamer(client)
        if await streamer.is_in_vc(message.chat.id):
            next_track = await streamer.skip_stream(message.chat.id)
            if next_track:
                await message.reply(f"⏭ Skipped to next track.")
            else:
                await message.reply("No more tracks in queue!")
        else:
            await message.reply("Not in a voice chat!")
    except Exception as e:
        await message.reply(f"Error skipping track: {str(e)}")
        print(f"Error in /skip: {e}")