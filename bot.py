import asyncio
import logging
from aiohttp import web
from bot.clients import app as pyrogram_app
from server.app import create_web_app
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    # Start Pyrogram client
    await pyrogram_app.start()
    logger.info("Pyrogram client started.")

    # Create and start web server
    web_app = create_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
    await site.start()
    logger.info(f"Web server started on port {Config.PORT}")

    logger.info("Bot is running. Press Ctrl+C to stop.")
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")
    finally:
        await pyrogram_app.stop()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
