from pyrogram import Client
import asyncio
import pytgcalls
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

class Streamer:
    def __init__(self, client: Client):
        self.client = client
        self.tgcalls = PyTgCalls(client)
        self.active_streams = {}  # {chat_id: {"stream": url, "paused": bool, "queue": [urls]}}

    async def is_in_vc(self, chat_id: int) -> bool:
        return chat_id in self.active_streams

    async def join_vc(self, chat_id: int):
        try:
            await self.tgcalls.start()
            await self.tgcalls.join_group_call(
                chat_id,
                AudioPiped("silence.mp3"),
                stream_type=StreamType().pulse_stream
            )
            self.active_streams[chat_id] = {"stream": None, "paused": False, "queue": []}
            print(f"Joined VC in chat {chat_id}")
        except Exception as e:
            print(f"Error joining VC: {e}")
            raise

    async def leave_vc(self, chat_id: int):
        try:
            if chat_id in self.active_streams:
                await self.tgcalls.leave_group_call(chat_id)
                del self.active_streams[chat_id]
                print(f"Left VC in chat {chat_id}")
        except Exception as e:
            print(f"Error leaving VC: {e}")
            raise

    async def start_stream(self, stream_url: str, chat_id: int):
        if chat_id not in self.active_streams:
            return

        try:
            stream_type = AudioVideoPiped if stream_url.endswith(('.mp4', '.mkv')) else AudioPiped
            await self.tgcalls.change_stream(
                chat_id,
                stream_type(stream_url),
                stream_type=StreamType().pulse_stream
            )
            self.active_streams[chat_id]["stream"] = stream_url
            self.active_streams[chat_id]["paused"] = False
            print(f"Started streaming {stream_url} in chat {chat_id}")
        except Exception as e:
            print(f"Error starting stream: {e}")
            raise

    async def stop_stream(self, chat_id: int):
        if chat_id in self.active_streams:
            try:
                self.active_streams[chat_id]["stream"] = None
                self.active_streams[chat_id]["queue"] = []
                await self.tgcalls.change_stream(
                    chat_id,
                    AudioPiped("silence.mp3"),
                    stream_type=StreamType().pulse_stream
                )
                print(f"Stopped streaming in chat {chat_id}")
            except Exception as e:
                print(f"Error stopping stream: {e}")
                raise

    async def pause_stream(self, chat_id: int):
        if chat_id in self.active_streams:
            try:
                await self.tgcalls.pause_stream(chat_id)
                self.active_streams[chat_id]["paused"] = True
                print(f"Paused streaming in chat {chat_id}")
            except Exception as e:
                print(f"Error pausing stream: {e}")
                raise

    async def resume_stream(self, chat_id: int):
        if chat_id in self.active_streams:
            try:
                await self.tgcalls.resume_stream(chat_id)
                self.active_streams[chat_id]["paused"] = False
                print(f"Resumed streaming in chat {chat_id}")
            except Exception as e:
                print(f"Error resuming stream: {e}")
                raise

    async def skip_stream(self, chat_id: int) -> str:
        if chat_id in self.active_streams and self.active_streams[chat_id]["queue"]:
            try:
                next_url = self.active_streams[chat_id]["queue"].pop(0)
                await self.start_stream(next_url, chat_id)
                return next_url
            except Exception as e:
                print(f"Error skipping stream: {e}")
                raise
        return None

    async def add_to_queue(self, urls: list, chat_id: int):
        if chat_id in self.active_streams:
            self.active_streams[chat_id]["queue"].extend(urls[1:])
            print(f"Added {len(urls[1:])} tracks to queue in chat {chat_id}")