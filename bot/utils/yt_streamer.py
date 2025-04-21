import asyncio
import yt_dlp
from config.logging import logger

async def get_youtube_stream(query: str, audio_only: bool = True) -> dict:
    """Search YouTube for a video or audio stream based on the query."""
    try:
        logger.info(f"Searching YouTube for query: {query}, audio_only: {audio_only}")
        ydl_opts = {
            'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'no_warnings': True,
            'merge_output_format': 'mp4' if not audio_only else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Use ytsearch for queries that aren't URLs
            search_query = f"ytsearch:{query}" if not query.startswith(('http://', 'https://')) else query
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and info['entries']:
                # For search results
                video = info['entries'][0]
            else:
                # For direct URLs
                video = info

            if not video or 'url' not in video:
                logger.warning(f"No valid stream found for query: {query}")
                return {}

            return {
                'url': video['url'],
                'title': video.get('title', query),
                'duration': video.get('duration', 0),
            }
    except Exception as e:
        logger.error(f"Error fetching YouTube stream for query {query}: {e}")
        return {}

async def get_playlist_streams(query: str) -> list:
    """Search YouTube for a playlist and return a list of stream URLs."""
    try:
        logger.info(f"Searching YouTube playlist for query: {query}")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extract_flat': 'in_playlist',
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch:{query}" if not query.startswith(('http://', 'https://')) else query
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' not in info:
                logger.warning(f"No playlist found for query: {query}")
                return []

            streams = []
            for video in info['entries']:
                if 'url' in video:
                    streams.append({
                        'url': video['url'],
                        'title': video.get('title', 'Unknown'),
                        'duration': video.get('duration', 0),
                    })

            logger.info(f"Found {len(streams)} tracks in playlist for query: {query}")
            return streams
    except Exception as e:
        logger.error(f"Error fetching YouTube playlist for query {query}: {e}")
        return []