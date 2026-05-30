import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from config import Config

logger = logging.getLogger(__name__)


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._client = AsyncIOMotorClient(Config.DATABASE_URL)
        self._db = self._client[Config.DATABASE_NAME]
        self.files = self._db["files"]
        self.users = self._db["users"]
        self._initialized = True
        logger.info("Database connection initialized.")

    # ── File operations ──────────────────────────────────────────────────────

    async def save_file(self, file_doc: dict) -> str:
        """Insert a file record and return its string ID."""
        result = await self.files.insert_one(file_doc)
        return str(result.inserted_id)

    async def get_file(self, file_id: str) -> Optional[dict]:
        """Retrieve a file record by its string ID."""
        try:
            return await self.files.find_one({"_id": ObjectId(file_id)})
        except Exception:
            return None

    async def total_files(self) -> int:
        return await self.files.count_documents({})

    # ── User operations ──────────────────────────────────────────────────────

    async def add_user(self, user_id: int):
        """Add user if not already present."""
        await self.users.update_one(
            {"user_id": user_id},
            {"$setOnInsert": {"user_id": user_id, "banned": False}},
            upsert=True,
        )

    async def is_banned(self, user_id: int) -> bool:
        doc = await self.users.find_one({"user_id": user_id})
        return bool(doc and doc.get("banned"))

    async def ban_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": True}},
            upsert=True,
        )

    async def unban_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": False}},
        )

    async def total_users(self) -> int:
        return await self.users.count_documents({})

    async def total_banned(self) -> int:
        return await self.users.count_documents({"banned": True})

    async def get_all_users(self) -> list:
        cursor = self.users.find({"banned": {"$ne": True}}, {"user_id": 1})
        return await cursor.to_list(length=None)
