from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from bot.utils.yt_streamer import get_youtube_stream, get_playlist_streams
from bot.utils.radio_browser import get_sri_lankan_radios
from config.logging import logger
from userbot.streamer import Streamer

def register(app: Client, streamer: Streamer = None):
    """Register inline query handlers."""
    
    @app.on_inline_query()
    async def inline_query(client: Client, query: InlineQuery):
        """Handle inline queries for song, playlist, and radio search."""
        search_query = query.query.strip()
        if not search_query:
            await query.answer(results=[])
            logger.info("Empty inline query received")
            return

        try:
            logger.info(f"Processing inline query: {search_query}")
            results = []

            # Search YouTube for songs
            stream_data = await get_youtube_stream(search_query, audio_only=True)
            if stream_data and stream_data.get('url'):
                results.append(
                    InlineQueryResultArticle(
                        title=f"Song: {stream_data.get('title', search_query)}",
                        input_message_content=InputTextMessageContent(f"/play {search_query}"),
                        description="Play this song in voice chat",
                        thumb_url="https://i.imgur.com/0B3zV.png"
                    )
                )

            # Search YouTube for playlists
            playlist_streams = await get_playlist_streams(search_query)
            if playlist_streams:
                results.append(
                    InlineQueryResultArticle(
                        title=f"Playlist: {search_query}",
                        input_message_content=InputTextMessageContent(f"/playlist {search_query}"),
                        description=f"Play this playlist ({len(playlist_streams)} tracks)",
                        thumb_url="https://i.imgur.com/0B3zV.png"
                    )
                )

            # Search radio stations
            radio_stations = await get_sri_lankan_radios()
            for station in radio_stations[:5]:  # Limit to 5 radio results
                if search_query.lower() in station["name"].lower():
                    results.append(
                        InlineQueryResultArticle(
                            title=f"Radio: {station['name']}",
                            input_message_content=InputTextMessageContent(f"/fmradio {station['name']}"),
                            description=f"{station['language']} - {station['bitrate']} kbps",
                            thumb_url="https://i.imgur.com/0B3zV.png"
                        )
                    )

            await query.answer(results=results)
            logger.info(f"Answered inline query with {len(results)} results")
        except Exception as e:
            logger.error(f"Error in inline query: {e}")
            await query.answer(results=[])