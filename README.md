# Telegram Stream Bot

A Telegram Bot + Userbot system for streaming YouTube audio/video, playlists, and Sri Lankan radio stations into group voice chats.

## Features
- Stream YouTube songs with `/play [song name or link]`.
- Stream YouTube videos with `/vplay [video name or link]`.
- Stream YouTube playlists with `/playlist [playlist name or link]`.
- Stream Sri Lankan FM radio with `/fmradio [station name or URL]`.
- List all Sri Lankan radio stations with `/allradio` (paginated, 5 per page).
- Voice chat controls: `/join`, `/leave`, `/stop`, `/pause`, `/resume`, `/skip`.
- Inline search with `@BotName [query]` for songs, playlists, or radio stations.
- Admin-only commands: `/reload`, `/shutdown`, `/logs`.
- Deployment-ready for Heroku, Railway, or VPS.

## Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd telegram-stream-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r deployment/requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials.
4. Add a `silence.mp3` file (1-second silent MP3) to the project root.
5. Run the bot:
   ```bash
   python3 main.py
   ```
   - On first run, the userbot will prompt for a phone number and verification code to generate a session file (`userbot.session`).

## Deployment
### Heroku
1. Create a Heroku app: `heroku create your-app-name`.
2. Push code: `git push heroku main`.
3. Set environment variables: `heroku config:set KEY=VALUE`.
4. Scale worker: `heroku ps:scale worker=1`.
5. For the first run, manually generate the session locally and upload `userbot.session` to Heroku (see below).

## Environment Variables
- `API_ID`: Telegram API ID.
- `API_HASH`: Telegram API Hash.
- `BOT_TOKEN`: Bot token from @BotFather.
- `OWNER_ID`: Telegram ID of the bot owner.
- `LOG_CHANNEL`: ID of the log channel.

## Session File
- The userbot session is stored in `userbot.session`.
- On first run, the bot will prompt for a phone number and verification code to generate the session.
- For Heroku, generate the session locally, then upload `userbot.session` to the project root before deploying.

## Silence File
- A `silence.mp3` file (1-second silent MP3) is required for voice chat streaming.
- Create it using Audacity or download a silent MP3 and place it in the project root.

## Commands
- `/play [song name or link]`: Stream YouTube audio.
- `/vplay [video name or link]`: Stream YouTube video.
- `/playlist [playlist name or link]`: Stream YouTube playlist.
- `/fmradio [station name or URL]`: Stream Sri Lankan FM radio.
- `/allradio`: List all Sri Lankan radio stations (paginated, 5 per page).
- `/join`: Join voice chat.
- `/leave`: Leave voice chat.
- `/stop`: Stop streaming and leave VC.
- `/pause`: Pause stream.
- `/resume`: Resume stream.
- `/skip`: Skip to next track.
