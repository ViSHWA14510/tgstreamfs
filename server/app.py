from aiohttp import web
from server.stream_routes import watch_handler, download_handler, health_handler, file_info_handler


def create_web_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    app.router.add_get("/file-info/{token}", file_info_handler)
    app.router.add_get("/watch/{token}", watch_handler)
    app.router.add_get("/download/{token}", download_handler)
    return app
