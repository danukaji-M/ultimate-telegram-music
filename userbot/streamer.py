import asyncio
import os
from pyrogram import Client
from pytgcalls import PyTgCalls
from config.logging import logger

class Streamer:
    """A class to manage streaming audio/video in Telegram group calls using PyTgCalls."""

    def __init__(self, client: Client):
        """Initialize the Streamer with a Pyrogram client."""
        try:
            logger.info(f"Initializing Streamer with client: {client}")
            if client is None:
                raise ValueError("Client cannot be None")
            self.client = client
            self.tgcalls = PyTgCalls(client)
            self.active_streams = {}  # {chat_id: {"stream": url, "paused": bool, "queue": [urls]}}
        except Exception as e:
            logger.error(f"Failed to initialize Streamer: {e}")
            raise

    async def is_in_vc(self, chat_id: int) -> bool:
        """Check if the bot is in a voice chat for the given chat_id."""
        return chat_id in self.active_streams

    async def join_vc(self, chat_id: int) -> None:
        """
        Join a voice chat in the specified chat.
        Args:
            chat_id: The ID of the chat to join.
        Raises:
            ValueError: If chat_id is invalid.
            FileNotFoundError: If silence.mp3 is missing.
            Exception: If joining the voice chat fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")

        try:
            await self.tgcalls.start()
            if not os.path.exists("silence.mp3"):
                raise FileNotFoundError("silence.mp3 not found in project root")
            await self.tgcalls.join_group_call(
                chat_id,
                "silence.mp3"  # Direct file path for initial silent stream
            )
            self.active_streams[chat_id] = {"stream": None, "paused": False, "queue": []}
            logger.info(f"Joined voice chat in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to join voice chat in chat {chat_id}: {e}")
            raise

    async def leave_vc(self, chat_id: int) -> None:
        """
        Leave the voice chat in the specified chat.
        Args:
            chat_id: The ID of the chat to leave.
        Raises:
            ValueError: If chat_id is invalid.
            Exception: If leaving the voice chat fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")

        if chat_id not in self.active_streams:
            logger.warning(f"No active stream in chat {chat_id} to leave")
            return

        try:
            await self.tgcalls.leave_group_call(chat_id)
            del self.active_streams[chat_id]
            logger.info(f"Left voice chat in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to leave voice chat in chat {chat_id}: {e}")
            raise

    async def start_stream(self, stream_url: str, chat_id: int) -> None:
        """
        Start streaming a URL in the specified chat.
        Args:
            stream_url: The URL or file path of the stream to play.
            chat_id: The ID of the chat to stream in.
        Raises:
            ValueError: If stream_url or chat_id is invalid.
            Exception: If starting the stream fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if not stream_url or not isinstance(stream_url, str):
            raise ValueError("Invalid stream_url: must be a non-empty string")
        if chat_id not in self.active_streams:
            raise ValueError(f"No active voice chat in chat {chat_id}")

        try:
            await self.tgcalls.play(chat_id, stream_url)
            self.active_streams[chat_id]["stream"] = stream_url
            self.active_streams[chat_id]["paused"] = False
            logger.info(f"Started streaming {stream_url} in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to start stream {stream_url} in chat {chat_id}: {e}")
            raise

    async def stop_stream(self, chat_id: int) -> None:
        """
        Stop the current stream in the specified chat.
        Args:
            chat_id: The ID of the chat to stop streaming in.
        Raises:
            ValueError: If chat_id is invalid.
            FileNotFoundError: If silence.mp3 is missing.
            Exception: If stopping the stream fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if chat_id not in self.active_streams:
            logger.warning(f"No active stream in chat {chat_id} to stop")
            return

        try:
            self.active_streams[chat_id]["stream"] = None
            self.active_streams[chat_id]["queue"] = []
            if not os.path.exists("silence.mp3"):
                raise FileNotFoundError("silence.mp3 not found in project root")
            await self.tgcalls.play(chat_id, "silence.mp3")
            logger.info(f"Stopped streaming in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to stop stream in chat {chat_id}: {e}")
            raise

    async def pause_stream(self, chat_id: int) -> None:
        """
        Pause the current stream in the specified chat.
        Args:
            chat_id: The ID of the chat to pause streaming in.
        Raises:
            ValueError: If chat_id is invalid.
            Exception: If pausing the stream fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if chat_id not in self.active_streams:
            logger.warning(f"No active stream in chat {chat_id} to pause")
            return

        try:
            await self.tgcalls.pause(chat_id)
            self.active_streams[chat_id]["paused"] = True
            logger.info(f"Paused stream in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to pause stream in chat {chat_id}: {e}")
            raise

    async def resume_stream(self, chat_id: int) -> None:
        """
        Resume the paused stream in the specified chat.
        Args:
            chat_id: The ID of the chat to resume streaming in.
        Raises:
            ValueError: If chat_id is invalid.
            Exception: If resuming the stream fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if chat_id not in self.active_streams:
            logger.warning(f"No active stream in chat {chat_id} to resume")
            return

        try:
            await self.tgcalls.resume(chat_id)
            self.active_streams[chat_id]["paused"] = False
            logger.info(f"Resumed stream in chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to resume stream in chat {chat_id}: {e}")
            raise

    async def skip_stream(self, chat_id: int) -> str | None:
        """
        Skip to the next stream in the queue for the specified chat.
        Args:
            chat_id: The ID of the chat to skip the stream in.
        Returns:
            The URL of the next stream, or None if the queue is empty.
        Raises:
            ValueError: If chat_id is invalid.
            Exception: If skipping the stream fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if chat_id not in self.active_streams or not self.active_streams[chat_id]["queue"]:
            logger.warning(f"No queue or active stream in chat {chat_id} to skip")
            return None

        try:
            next_url = self.active_streams[chat_id]["queue"].pop(0)
            await self.start_stream(next_url, chat_id)
            logger.info(f"Skipped to next stream {next_url} in chat {chat_id}")
            return next_url
        except Exception as e:
            logger.error(f"Failed to skip stream in chat {chat_id}: {e}")
            raise

    async def add_to_queue(self, urls: list, chat_id: int) -> None:
        """
        Add URLs to the stream queue for the specified chat.
        Args:
            urls: List of stream URLs to add.
            chat_id: The ID of the chat to add the queue to.
        Raises:
            ValueError: If urls or chat_id is invalid.
            Exception: If adding to queue fails.
        """
        if not isinstance(chat_id, int) or chat_id >= 0:
            raise ValueError("Invalid chat_id: must be a negative integer")
        if not isinstance(urls, list) or not urls:
            raise ValueError("Invalid urls: must be a non-empty list")
        if chat_id not in self.active_streams:
            logger.warning(f"No active stream in chat {chat_id} to add to queue")
            return

        try:
            valid_urls = [url for url in urls if isinstance(url, str) and url]
            if valid_urls:
                self.active_streams[chat_id]["queue"].extend(valid_urls)
                logger.info(f"Added {len(valid_urls)} track(s) to queue in chat {chat_id}")
            else:
                logger.warning("No valid URLs provided to add to queue")
        except Exception as e:
            logger.error(f"Failed to add URLs to queue in chat {chat_id}: {e}")
            raise