from pyradios import RadioBrowser
import asyncio

async def get_sri_lankan_radios() -> list:
    try:
        rb = RadioBrowser()
        results = rb.search(countrycode="LK", hidebroken=True)
        return [
            {
                "name": station["name"],
                "url": station["url"],
                "country": station["country"],
                "language": station["language"],
                "codec": station["codec"],
                "bitrate": station["bitrate"]
            }
            for station in results
        ]
    except Exception as e:
        print(f"Error fetching Sri Lankan radios: {e}")
        return []