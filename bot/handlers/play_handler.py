from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.yt_streamer import get_youtube_stream, get_playlist_streams
from userbot.streamer import Streamer
from config.constants import OWNER_ID
from config.logging import logger

def register(app: Client, streamer: Streamer):
    """Register play-related command handlers."""
    
    @app.on_message(filters.command("play") & filters.group)
    async def play_command(client: Client, message: Message):
        """Handle /play command to stream audio in a group voice chat."""
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a song name or YouTube link!")
            return

        try:
            logger.info(f"Processing /play for query: {query} in chat {message.chat.id}")
            # Get stream URL (audio only)
            stream_url = await get_youtube_stream(query, audio_only=True)
            if not stream_url:
                await message.reply("Could not find the song!")
                return

            # Check if in voice chat
            if not await streamer.is_in_vc(message.chat.id):
                await streamer.join_vc(message.chat.id)
                logger.info(f"Joined voice chat for chat {message.chat.id}")

            # Start streaming
            await streamer.start_stream(stream_url, message.chat.id)
            await message.reply(f"🎵 Now playing: {query}")
            logger.info(f"Started streaming {query} in chat {message.chat.id}")
        except Exception as e:
            logger.error(f"Error in /play for chat {message.chat.id}: {e}")
            await message.reply(f"Error playing song: {str(e)}")

    @app.on_message(filters.command("vplay") & filters.group)
    async def vplay_command(client: Client, message: Message):
        """Handle /vplay command to stream video in a group voice chat."""
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a video name or YouTube link!")
            return

        try:
            logger.info(f"Processing /vplay for query: {query} in chat {message.chat.id}")
            # Get stream URL (video + audio)
            stream_url = await get_youtube_stream(query, audio_only=False)
            if not stream_url:
                await message.reply("Could not find the video!")
                return

            # Check if in voice chat
            if not await streamer.is_in_vc(message.chat.id):
                await streamer.join_vc(message.chat.id)
                logger.info(f"Joined voice chat for chat {message.chat.id}")

            # Start streaming
            await streamer.start_stream(stream_url, message.chat.id)
            await message.reply(f"🎥 Now playing video: {query}")
            logger.info(f"Started streaming video {query} in chat {message.chat.id}")
        except Exception as e:
            logger.error(f"Error in /vplay for chat {message.chat.id}: {e}")
            await message.reply(f"Error playing video: {str(e)}")

    @app.on_message(filters.command("playlist") & filters.group)
    async def playlist_command(client: Client, message: Message):
        """Handle /playlist command to stream a YouTube playlist."""
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a playlist name or YouTube playlist link!")
            return

        try:
            logger.info(f"Processing /playlist for query: {query} in chat {message.chat.id}")
            # Get playlist stream URLs
            playlist_urls = await get_playlist_streams(query)
            if not playlist_urls:
                await message.reply("Could not find the playlist!")
                return

            # Check if in voice chat
            if not await streamer.is_in_vc(message.chat.id):
                await streamer.join_vc(message.chat.id)
                logger.info(f"Joined voice chat for chat {message.chat.id}")

            # Add playlist to queue and start streaming
            await streamer.add_to_queue(playlist_urls, message.chat.id)
            await streamer.start_stream(playlist_urls[0], message.chat.id)
            await message.reply(f"🎶 Started playing playlist: {query} ({len(playlist_urls)} tracks)")
            logger.info(f"Started playlist {query} with {len(playlist_urls)} tracks in chat {message.chat.id}")
        except Exception as e:
            logger.error(f"Error in /playlist for chat {message.chat.id}: {e}")
            await message.reply(f"Error playing playlist: {str(e)}")

    @app.on_message(filters.command("stop") & filters.group)
    async def stop_command(client: Client, message: Message):
        """Handle /stop command to stop streaming and leave voice chat."""
        try:
            logger.info(f"Processing /stop in chat {message.chat.id}")
            if await streamer.is_in_vc(message.chat.id):
                await streamer.stop_stream(message.chat.id)
                await streamer.leave_vc(message.chat.id)
                await message.reply("⏹ Stopped streaming and left VC.")
                logger.info(f"Stopped streaming and left VC in chat {message.chat.id}")
            else:
                await message.reply("Not in a voice chat!")
        except Exception as e:
            logger.error(f"Error in /stop for chat {message.chat.id}: {e}")
            await message.reply(f"Error stopping stream: {str(e)}")

    @app.on_message(filters.command("join") & filters.group)
    async def join_command(client: Client, message: Message):
        """Handle /join command to join a voice chat."""
        try:
            logger.info(f"Processing /join in chat {message.chat.id}")
            if not await streamer.is_in_vc(message.chat.id):
                await streamer.join_vc(message.chat.id)
                await message.reply("✅ Joined voice chat!")
                logger.info(f"Joined voice chat in chat {message.chat.id}")
            else:
                await message.reply("Already in voice chat!")
        except Exception as e:
            logger.error(f"Error in /join for chat {message.chat.id}: {e}")
            await message.reply(f"Error joining VC: {str(e)}")

    @app.on_message(filters.command("leave") & filters.group)
    async def leave_command(client: Client, message: Message):
        """Handle /leave command to leave a voice chat."""
        try:
            logger.info(f"Processing /leave in chat {message.chat.id}")
            if await streamer.is_in_vc(message.chat.id):
                await streamer.leave_vc(message.chat.id)
                await message.reply("👋 Left voice chat!")
                logger.info(f"Left voice chat in chat {message.chat.id}")
            else:
                await message.reply("Not in a voice chat!")
        except Exception as e:
            logger.error(f"Error in /leave for chat {message.chat.id}: {e}")
            await message.reply(f"Error leaving VC: {str(e)}")

    @app.on_message(filters.command("pause") & filters.group)
    async def pause_command(client: Client, message: Message):
        """Handle /pause command to pause the stream."""
        try:
            logger.info(f"Processing /pause in chat {message.chat.id}")
            if await streamer.is_in_vc(message.chat.id):
                await streamer.pause_stream(message.chat.id)
                await message.reply("⏸ Stream paused.")
                logger.info(f"Paused stream in chat {message.chat.id}")
            else:
                await message.reply("Not in a voice chat!")
        except Exception as e:
            logger.error(f"Error in /pause for chat {message.chat.id}: {e}")
            await message.reply(f"Error pausing stream: {str(e)}")

    @app.on_message(filters.command("resume") & filters.group)
    async def resume_command(client: Client, message: Message):
        """Handle /resume command to resume the stream."""
        try:
            logger.info(f"Processing /resume in chat {message.chat.id}")
            if await streamer.is_in_vc(message.chat.id):
                await streamer.resume_stream(message.chat.id)
                await message.reply("▶️ Stream resumed.")
                logger.info(f"Resumed stream in chat {message.chat.id}")
            else:
                await message.reply("Not in a voice chat!")
        except Exception as e:
            logger.error(f"Error in /resume for chat {message.chat.id}: {e}")
            await message.reply(f"Error resuming stream: {str(e)}")

    @app.on_message(filters.command("skip") & filters.group)
    async def skip_command(client: Client, message: Message):
        """Handle /skip command to skip to the next track."""
        try:
            logger.info(f"Processing /skip in chat {message.chat.id}")
            if await streamer.is_in_vc(message.chat.id):
                next_track = await streamer.skip_stream(message.chat.id)
                if next_track:
                    await message.reply(f"⏭ Skipped to next track.")
                    logger.info(f"Skipped to next track in chat {message.chat.id}")
                else:
                    await message.reply("No more tracks in queue!")
            else:
                await message.reply("Not in a voice chat!")
        except Exception as e:
            logger.error(f"Error in /skip for chat {message.chat.id}: {e}")
            await message.reply(f"Error skipping track: {str(e)}")