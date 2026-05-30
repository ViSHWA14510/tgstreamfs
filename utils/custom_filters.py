from pyrogram import filters
from config import Config
from database.mongo import Database

db = Database()


def is_admin(_, __, message):
    """Filter: only allow configured admin user IDs."""
    return message.from_user and message.from_user.id in Config.ADMIN_USER_IDS


admin_filter = filters.create(is_admin)


def is_not_banned(_, __, message):
    """This is a sync wrapper; use with caution — prefer async checks in handlers."""
    # For async ban checks, handle inside the handler directly.
    return True  # Placeholder; real check is async in handlers


not_banned_filter = filters.create(is_not_banned)
