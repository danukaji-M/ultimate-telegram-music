from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from bot.utils.yt_streamer import get_youtube_stream
from bot.utils.radio_browser import get_sri_lankan_radios

@Client.on_inline_query()
async def inline_query(client: Client, query: InlineQuery):
    search_query = query.query.strip()
    if not search_query:
        await query.answer(results=[])
        return

    try:
        results = []

        # Search YouTube for songs
        stream_url = await get_youtube_stream(search_query, audio_only=True)
        if stream_url:
            results.append(
                InlineQueryResultArticle(
                    title=f"Song: {search_query}",
                    input_message_content=InputTextMessageContent(f"/play {search_query}"),
                    description="Play this song in voice chat",
                    thumb_url="https://i.imgur.com/0B3zV.png"
                )
            )

        # Search YouTube for playlists
        playlist_urls = await get_playlist_streams(search_query)
        if playlist_urls:
            results.append(
                InlineQueryResultArticle(
                    title=f"Playlist: {search_query}",
                    input_message_content=InputTextMessageContent(f"/playlist {search_query}"),
                    description=f"Play this playlist ({len(playlist_urls)} tracks)",
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
    except Exception as e:
        print(f"Error in inline query: {e}")
        await query.answer(results=[])