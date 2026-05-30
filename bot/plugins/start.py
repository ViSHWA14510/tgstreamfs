import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from bot.clients import app
from database.mongo import Database
from config import Config
from utils.helpers import decode_file_id

logger = logging.getLogger(__name__)
db = Database()


async def is_subscribed(client: Client, user_id: int) -> bool:
    """Check if user is subscribed to the force sub channel."""
    if not Config.FORCE_SUB_CHANNEL:
        return True
    try:
        member = await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user_id)
        return member.status.value not in ("left", "banned", "kicked")
    except UserNotParticipant:
        return False
    except Exception as e:
        logger.warning(f"Force sub check failed: {e}")
        return True  # Fail open if channel can't be checked


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    args = message.command
    user_id = message.from_user.id

    # No argument → welcome message
    if len(args) == 1:
        bot_info = await client.get_me()
        await message.reply_text(
            f"👋 Hello **{message.from_user.first_name}**!\n\n"
            f"I'm **{bot_info.first_name}**, a File Store & Stream Bot.\n\n"
            f"📤 Send me any file and I'll give you:\n"
            f"• 🔗 A shareable Telegram link\n"
            f"• 🎬 A stream link\n"
            f"• ⬇️ A download link\n\n"
            f"Managed by: @{(await client.get_me()).username}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 Updates Channel", url="https://t.me/your_channel")
            ]])
        )
        return

    # File Store link: /start file_<encoded_id>
    token = args[1]
    if not token.startswith("file_"):
        await message.reply_text("❌ Invalid link.")
        return

    # Force subscribe check
    if not await is_subscribed(client, user_id):
        channel = Config.FORCE_SUB_CHANNEL
        join_url = f"https://t.me/{channel.lstrip('@')}" if isinstance(channel, str) else f"https://t.me/c/{str(channel).replace('-100', '')}"
        await message.reply_text(
            "🔒 **Access Restricted!**\n\n"
            "You must join our channel to use this bot and access files.\n"
            "Click **Join Channel** below, then click **✅ Try Again**.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=join_url)],
                [InlineKeyboardButton("✅ Try Again", callback_data=f"check_sub_{token}")]
            ])
        )
        return

    await send_file_to_user(client, message, token, user_id)


@app.on_callback_query(filters.regex(r"^check_sub_(.+)$"))
async def check_sub_callback(client: Client, callback: CallbackQuery):
    token = callback.matches[0].group(1)
    user_id = callback.from_user.id

    if not await is_subscribed(client, user_id):
        await callback.answer("❌ You haven't joined yet! Please join and try again.", show_alert=True)
        return

    await callback.answer("✅ Verified! Sending your file...", show_alert=False)
    await send_file_to_user(client, callback.message, token, user_id, edit=True)


async def send_file_to_user(client: Client, message, token: str, user_id: int, edit: bool = False):
    """Fetch and forward file from bin channel to user."""
    try:
        file_id = decode_file_id(token)
        record = await db.get_file(file_id)
        if not record:
            text = "❌ File not found or has been deleted."
            if edit:
                await message.edit_text(text)
            else:
                await message.reply_text(text)
            return

        msg_id = record["message_id"]

        if edit:
            await message.delete()

        await client.copy_message(
            chat_id=user_id,
            from_chat_id=Config.BIN_CHANNEL,
            message_id=msg_id,
        )
    except Exception as e:
        logger.error(f"Error sending file to user {user_id}: {e}")
        text = "⚠️ An error occurred while fetching your file. Please try again."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
