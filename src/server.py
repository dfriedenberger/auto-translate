
import asyncio
import threading
import uvicorn
import logging
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from .clipboard import ClipBoardListener
from .translation import Translator

logging.basicConfig(level=logging.INFO)


class WebServer(threading.Thread):

    def __init__(self, host, port, input_language, output_language):
        super().__init__()
        self.host = host
        self.port = port
        self.is_paused = False
        self.router = APIRouter()
        self.router.add_api_route("/", self.hello_world, methods=["GET"])
        self.router.add_api_route("/health", self._health, methods=["GET"])
        self.router.add_api_websocket_route("/ws", self.websocket_endpoint)
        self.templates = Jinja2Templates(directory="./templates")

        self.translator = Translator(input_language, output_language)
        self.clip_board_listener = ClipBoardListener()
        self.clip_board_listener.print_available_formats()

    def pause(self):
        logging.info('pause')
        self.is_paused = True

    def resume(self):
        logging.info('resume')
        self.is_paused = False

    def hello_world(self, request: Request,):
        return self.templates.TemplateResponse("index.html", {"request": request, "name": "Hallo"})

    def _health(self):
        return {"Status": "UP"}

    async def websocket_endpoint(self, websocket: WebSocket):
        await websocket.accept()
        try:
            old_text = self.clip_board_listener.get_clip_board_text()
            logging.info(f"Open Connection clipboard:{old_text}")
            while True:
                text = self.clip_board_listener.get_clip_board_text()
                if old_text == text:
                    await asyncio.sleep(1.0)
                    continue
                old_text = text

                text = text.replace('\n', ' ').replace('\r', '')
                logging.info(f"Text :{text}")

                if self.is_paused:
                    logging.info("Do not translate")
                    continue

                translated = self.translator.translate(text)
                logging.info(f"Translated :{translated}")
                await websocket.send_text(translated)
        except Exception as e:
            logging.error(e)
        try:
            await websocket.close()
        except Exception as e:
            logging.error(e)

    def run(self):
        app = FastAPI(openapi_url='/openapi.json',)
        app.include_router(self.router)
        app.mount("/static", StaticFiles(directory="htdocs", html=True), name="static")

        uvicorn.run(app, host=self.host, port=self.port, ws_ping_interval=5, ws_ping_timeout=5)
