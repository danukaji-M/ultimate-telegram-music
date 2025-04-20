from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.radio_links import RADIO_STATIONS
from bot.utils.radio_browser import get_sri_lankan_radios
from userbot.streamer import Streamer
import re

@Client.on_message(filters.command("fmradio") & filters.group)
async def fmradio_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    
    if not query:
        # Show categories with inline keyboard
        buttons = [
            [InlineKeyboardButton(category, callback_data=f"radio_cat_{category}")]
            for category in RADIO_STATIONS.keys()
        ]
        await message.reply("Select a radio category:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    try:
        # Check if query is a direct URL
        if re.match(r'^https?://', query):
            stream_url = query
            station_name = "Custom Radio"
        else:
            # Search for station by name
            stream_url = None
            station_name = query.lower()
            for category, stations in RADIO_STATIONS.items():
                for station in stations:
                    if station["name"].lower() == station_name:
                        stream_url = station["url"]
                        station_name = station["name"]
                        break
                if stream_url:
                    break

        if not stream_url:
            await message.reply(f"Could not find radio station: {query}")
            return

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(message.chat.id):
            await streamer.join_vc(message.chat.id)

        # Start streaming
        await streamer.start_stream(stream_url, message.chat.id)
        await message.reply(f"📻 Now playing: {station_name}")
    except Exception as e:
        await message.reply(f"Error playing radio: {str(e)}")
        print(f"Error in /fmradio: {e}")

@Client.on_message(filters.command("allradio") & filters.group)
async def allradio_command(client: Client, message: Message):
    try:
        # Fetch Sri Lankan radio stations
        radio_stations = await get_sri_lankan_radios()
        if not radio_stations:
            await message.reply("Could not fetch radio stations. Try again later.")
            return

        # Store stations in chat data for pagination
        client.radio_stations_cache[message.chat.id] = radio_stations

        # Display first page
        page = 0
        stations_per_page = 5
        total_pages = (len(radio_stations) + stations_per_page - 1) // stations_per_page

        buttons = [
            [InlineKeyboardButton(station["name"], callback_data=f"radio_play_{page}_{i}")]
            for i, station in enumerate(radio_stations[page * stations_per_page:(page + 1) * stations_per_page])
        ]
        # Add pagination buttons
        nav_buttons = []
        if total_pages > 1:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"radio_page_{page + 1}"))
        buttons.append(nav_buttons)

        await message.reply(
            f"Sri Lankan Radio Stations (Page {page + 1}/{total_pages}):",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.reply(f"Error fetching radio stations: {str(e)}")
        print(f"Error in /allradio: {e}")