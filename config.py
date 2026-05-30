import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram API credentials
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")

    # Bot token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "filestore_bot")

    # Channels
    BIN_CHANNEL: int = int(os.getenv("BIN_CHANNEL", "0"))
    FORCE_SUB_CHANNEL: str = os.getenv("FORCE_SUB_CHANNEL", "")  # e.g. @mychannel or -100xxxxxxxxx

    # Web server
    FQDN: str = os.getenv("FQDN", "http://localhost")
    PORT: int = int(os.getenv("PORT", "8080"))

    # Admins (comma-separated user IDs)
    ADMIN_USER_IDS: list = [
        int(x.strip())
        for x in os.getenv("ADMIN_USER_IDS", "").split(",")
        if x.strip().isdigit()
    ]

    # Optional settings
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "")   # without @
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "2000"))  # 2GB default

    @classmethod
    def validate(cls):
        errors = []
        if not cls.API_ID:
            errors.append("API_ID is required")
        if not cls.API_HASH:
            errors.append("API_HASH is required")
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required")
        if not cls.BIN_CHANNEL:
            errors.append("BIN_CHANNEL is required")
        if not cls.FQDN:
            errors.append("FQDN is required")
        if errors:
            raise ValueError("Config errors:\n" + "\n".join(errors))
