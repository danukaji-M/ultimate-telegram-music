import yt_dlp
import asyncio

async def get_youtube_stream(query: str, audio_only: bool = True) -> str:
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in query or "youtu.be" in query:
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return info['url']
    except Exception as e:
        print(f"Error fetching YouTube stream: {e}")
        return None

async def get_playlist_streams(query: str) -> list:
    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in query and "list=" in query:
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{query} playlist", download=False)
            if 'entries' not in info:
                return []
            return [entry['url'] for entry in info['entries']]
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []