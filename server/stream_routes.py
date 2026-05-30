import logging
import mimetypes
from aiohttp import web
from bot.clients import app as pyrogram_app
from database.mongo import Database
from config import Config
from utils.helpers import decode_file_id

logger = logging.getLogger(__name__)
db = Database()

CHUNK_SIZE = 1024 * 1024  # 1 MB chunks


async def health_handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "bot": "FileStoreBot"})


async def _stream_file(request: web.Request, token: str, disposition: str) -> web.StreamResponse:
    """Core streaming logic shared by watch and download endpoints."""
    try:
        file_id = decode_file_id(token)
    except Exception:
        raise web.HTTPBadRequest(text="Invalid token.")

    record = await db.get_file(file_id)
    if not record:
        raise web.HTTPNotFound(text="File not found.")

    message_id = record["message_id"]
    file_name = record.get("file_name", "file")
    file_size = record.get("file_size", 0)
    mime_type = record.get("mime_type") or mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    # Handle HTTP Range requests (for seeking in video players)
    range_header = request.headers.get("Range")
    start = 0
    end = file_size - 1 if file_size else None

    if range_header and file_size:
        try:
            range_val = range_header.replace("bytes=", "")
            range_start, range_end = range_val.split("-")
            start = int(range_start) if range_start else 0
            end = int(range_end) if range_end else file_size - 1
        except Exception:
            raise web.HTTPRequestRangeNotSatisfiable()

    status = 206 if range_header else 200
    headers = {
        "Content-Type": mime_type,
        "Content-Disposition": f'{disposition}; filename="{file_name}"',
        "Accept-Ranges": "bytes",
        "Cache-Control": "no-cache",
    }
    if file_size:
        content_length = (end - start + 1) if range_header else file_size
        headers["Content-Length"] = str(content_length)
        if range_header:
            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"

    response = web.StreamResponse(status=status, headers=headers)
    await response.prepare(request)

    try:
        # Stream the file from Telegram in chunks via Pyrogram
        async for chunk in pyrogram_app.stream_media(
            await pyrogram_app.get_messages(Config.BIN_CHANNEL, message_id),
            offset=start,
            limit=((end - start + 1) if end else None),
        ):
            await response.write(chunk)
    except Exception as e:
        logger.error(f"Streaming error for token {token}: {e}")

    await response.write_eof()
    return response


async def file_info_handler(request: web.Request) -> web.Response:
    """Return JSON metadata for a file (used by Vercel frontend)."""
    token = request.match_info["token"]
    try:
        file_id = decode_file_id(token)
    except Exception:
        raise web.HTTPBadRequest(text="Invalid token.")

    record = await db.get_file(file_id)
    if not record:
        raise web.HTTPNotFound(text="File not found.")

    return web.json_response({
        "file_name": record.get("file_name", "file"),
        "file_size": record.get("file_size", 0),
        "mime_type": record.get("mime_type", "application/octet-stream"),
    })


async def watch_handler(request: web.Request) -> web.StreamResponse:
    """Stream endpoint — inline display for video/audio players."""
    token = request.match_info["token"]
    return await _stream_file(request, token, disposition="inline")


async def download_handler(request: web.Request) -> web.StreamResponse:
    """Download endpoint — forces browser download."""
    token = request.match_info["token"]
    return await _stream_file(request, token, disposition="attachment")
