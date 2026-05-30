import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.clients import app
from database.mongo import Database
from config import Config
from utils.helpers import encode_file_id, get_file_size_str

logger = logging.getLogger(__name__)
db = Database()

# All supported media types
SUPPORTED_MEDIA = (
    filters.document
    | filters.video
    | filters.audio
    | filters.photo
    | filters.voice
    | filters.video_note
    | filters.animation
    | filters.sticker
)


@app.on_message(SUPPORTED_MEDIA & filters.private)
async def file_handler(client: Client, message: Message):
    """Receive a file, store it in the bin channel, and reply with links."""
    try:
        status_msg = await message.reply_text("⏳ Processing your file...")

        # Forward to bin channel to ensure permanent storage
        forwarded = await message.copy(Config.BIN_CHANNEL)

        # Extract file metadata
        media = (
            message.document
            or message.video
            or message.audio
            or message.photo
            or message.voice
            or message.video_note
            or message.animation
            or message.sticker
        )

        file_name = getattr(media, "file_name", None) or "file"
        file_size = getattr(media, "file_size", 0) or 0
        mime_type = getattr(media, "mime_type", "application/octet-stream") or "application/octet-stream"

        # Save to database
        file_doc = {
            "message_id": forwarded.id,
            "file_name": file_name,
            "file_size": file_size,
            "mime_type": mime_type,
            "uploader_id": message.from_user.id,
        }
        file_id = await db.save_file(file_doc)
        token = encode_file_id(file_id)

        # Generate bot username
        bot_info = await client.get_me()
        bot_username = bot_info.username

        # Build links
        store_link = f"https://t.me/{bot_username}?start=file_{token}"
        stream_link = f"{Config.FQDN.rstrip('/')}/watch/{token}"
        download_link = f"{Config.FQDN.rstrip('/')}/download/{token}"

        size_str = get_file_size_str(file_size)

        reply_text = (
            f"✅ **File Stored Successfully!**\n\n"
            f"📄 **Name:** `{file_name}`\n"
            f"📦 **Size:** {size_str}\n\n"
            f"🔗 **Your Links:**"
        )

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📨 File Link (Telegram)", url=store_link),
            ],
            [
                InlineKeyboardButton("🎬 Stream", url=stream_link),
                InlineKeyboardButton("⬇️ Download", url=download_link),
            ],
        ])

        await status_msg.delete()
        await message.reply_text(
            reply_text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

        logger.info(f"File stored: {file_name} ({size_str}) by user {message.from_user.id}")

    except Exception as e:
        logger.error(f"Error handling file from {message.from_user.id}: {e}")
        await message.reply_text("❌ Failed to store file. Please try again.")
