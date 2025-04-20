from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.radio_links import RADIO_STATIONS
from userbot.streamer import Streamer

@Client.on_callback_query(filters.regex(r"radio_cat_(.+)"))
async def radio_category_callback(client: Client, query: CallbackQuery):
    category = query.data.split("_")[2]
    try:
        buttons = [
            [InlineKeyboardButton(station["name"], callback_data=f"radio_station_{category}_{station['name']}")]
            for station in RADIO_STATIONS.get(category, [])
        ]
        await query.message.edit_text(
            f"Select a {category} station:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await query.message.edit_text(f"Error loading stations: {str(e)}")
        print(f"Error in radio_category_callback: {e}")

@Client.on_callback_query(filters.regex(r"radio_station_(.+)_(.+)"))
async def radio_station_callback(client: Client, query: CallbackQuery):
    category, station_name = query.data.split("_")[2:4]
    try:
        stream_url = None
        for station in RADIO_STATIONS.get(category, []):
            if station["name"] == station_name:
                stream_url = station["url"]
                break

        if not stream_url:
            await query.message.edit_text(f"Station not found: {station_name}")
            return

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(query.message.chat.id):
            await streamer.join_vc(query.message.chat.id)

        # Start streaming
        await streamer.start_stream(stream_url, query.message.chat.id)
        await query.message.edit_text(f"📻 Now playing: {station_name}")
    except Exception as e:
        await query.message.edit_text(f"Error playing station: {str(e)}")
        print(f"Error in radio_station_callback: {e}")

@Client.on_callback_query(filters.regex(r"radio_page_(\d+)"))
async def radio_page_callback(client: Client, query: CallbackQuery):
    page = int(query.data.split("_")[2])
    try:
        radio_stations = client.radio_stations_cache.get(query.message.chat.id, [])
        if not radio_stations:
            await query.message.edit_text("Radio station data expired. Use /allradio again.")
            return

        stations_per_page = 5
        total_pages = (len(radio_stations) + stations_per_page - 1) // stations_per_page

        if page < 0 or page >= total_pages:
            await query.answer("No more pages!")
            return

        buttons = [
            [InlineKeyboardButton(station["name"], callback_data=f"radio_play_{page}_{i}")]
            for i, station in enumerate(radio_stations[page * stations_per_page:(page + 1) * stations_per_page])
        ]
        # Add pagination buttons
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"radio_page_{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"radio_page_{page + 1}"))
        buttons.append(nav_buttons)

        await query.message.edit_text(
            f"Sri Lankan Radio Stations (Page {page + 1}/{total_pages}):",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await query.message.edit_text(f"Error loading page: {str(e)}")
        print(f"Error in radio_page_callback: {e}")

@Client.on_callback_query(filters.regex(r"radio_play_(\d+)_(\d+)"))
async def radio_play_callback(client: Client, query: CallbackQuery):
    page, index = map(int, query.data.split("_")[2:4])
    try:
        radio_stations = client.radio_stations_cache.get(query.message.chat.id, [])
        if not radio_stations:
            await query.message.edit_text("Radio station data expired. Use /allradio again.")
            return

        station = radio_stations[page * 5 + index]
        stream_url = station["url"]
        station_name = station["name"]

        # Initialize userbot streamer
        streamer = Streamer(client)
        if not await streamer.is_in_vc(query.message.chat.id):
            await streamer.join_vc(query.message.chat.id)

        # Start streaming
        await streamer.start_stream(stream_url, query.message.chat.id)
        await query.message.edit_text(f"📻 Now playing: {station_name}")
    except Exception as e:
        await query.message.edit_text(f"Error playing station: {str(e)}")
        print(f"Error in radio_play_callback: {e}")