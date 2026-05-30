import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.clients import app
from database.mongo import Database
from config import Config
from utils.custom_filters import admin_filter

logger = logging.getLogger(__name__)
db = Database()


@app.on_message(filters.command("stats") & admin_filter)
async def stats_handler(client: Client, message: Message):
    """Show bot statistics."""
    try:
        total_users = await db.total_users()
        total_files = await db.total_files()
        banned_users = await db.total_banned()

        bot_info = await client.get_me()
        stats_text = (
            f"📊 **Bot Statistics**\n\n"
            f"🤖 **Bot:** @{bot_info.username}\n"
            f"👥 **Total Users:** {total_users}\n"
            f"📁 **Total Files Stored:** {total_files}\n"
            f"🚫 **Banned Users:** {banned_users}\n"
        )
        await message.reply_text(stats_text)
    except Exception as e:
        logger.error(f"Stats error: {e}")
        await message.reply_text("❌ Failed to fetch stats.")


@app.on_message(filters.command("broadcast") & admin_filter)
async def broadcast_handler(client: Client, message: Message):
    """Broadcast a message to all users."""
    if not message.reply_to_message:
        await message.reply_text(
            "📢 **Usage:** Reply to a message with /broadcast to send it to all users."
        )
        return

    status_msg = await message.reply_text("📤 Broadcasting...")
    broadcast_msg = message.reply_to_message

    all_users = await db.get_all_users()
    success, failed = 0, 0

    for user in all_users:
        try:
            await broadcast_msg.copy(int(user["user_id"]))
            success += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"✔️ Sent: {success}\n"
        f"❌ Failed: {failed}"
    )


@app.on_message(filters.command("ban") & admin_filter)
async def ban_handler(client: Client, message: Message):
    """Ban a user."""
    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("🚫 **Usage:** `/ban <user_id>`")
        return

    user_id = int(args[1])
    await db.ban_user(user_id)
    await message.reply_text(f"🚫 User `{user_id}` has been **banned**.")


@app.on_message(filters.command("unban") & admin_filter)
async def unban_handler(client: Client, message: Message):
    """Unban a user."""
    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("✅ **Usage:** `/unban <user_id>`")
        return

    user_id = int(args[1])
    await db.unban_user(user_id)
    await message.reply_text(f"✅ User `{user_id}` has been **unbanned**.")


@app.on_message(filters.command("ban_check") & admin_filter)
async def ban_check_handler(client: Client, message: Message):
    """Check if a user is banned."""
    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("🔍 **Usage:** `/ban_check <user_id>`")
        return

    user_id = int(args[1])
    is_banned = await db.is_banned(user_id)
    status = "🚫 **Banned**" if is_banned else "✅ **Not Banned**"
    await message.reply_text(f"User `{user_id}`: {status}")
