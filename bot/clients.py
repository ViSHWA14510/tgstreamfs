from pyrogram import Client
from config import Config

# Single bot client
app = Client(
    name="FileStoreBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={"root": "bot/plugins"},
    sleep_threshold=60,
)
