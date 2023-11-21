
import asyncio
import threading
import uvicorn

from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

from .clipboard import ClipBoardListener
from .translation import Translator

class WebServer(threading.Thread):

    def __init__(self,host,port,input_language,output_language):
        super().__init__()
        self.host = host
        self.port = port
        self.router = APIRouter()
        self.router.add_api_route("/", self.hello_world, methods=["GET"])
        self.router.add_api_route("/health", self._health, methods=["GET"])
        self.router.add_api_websocket_route("/ws", self.websocket_endpoint)
        self.templates = Jinja2Templates(directory="./templates")

        self.translator = Translator(input_language,output_language)
        self.clip_board_listener = ClipBoardListener()


    def hello_world(self,request: Request,):
        return self.templates.TemplateResponse("index.html", {"request": request, "name": "Hallo"})

    def _health(self):
        return {"Status": "UP"}

    async def websocket_endpoint(self,websocket: WebSocket):
        await websocket.accept()
        try:
            old_text = self.clip_board_listener.get_clip_board_text()
            print(old_text)
            while True:
                text = self.clip_board_listener.get_clip_board_text()
                if old_text == text:
                    await asyncio.sleep(1.0)
                    continue
                old_text = text

                text = text.replace('\n', ' ').replace('\r', '')
                print("text:",text)
                translated = self.translator.translate(text)

                print("translated:",translated)
                await websocket.send_text(translated)
        except:
            print("Exception for websocket")


    def run(self):
        app = FastAPI(openapi_url='/openapi.json',)
        app.include_router(self.router)
        app.mount("/static", StaticFiles(directory="htdocs",html = True), name="static")

        uvicorn.run(app, host=self.host, port=self.port,ws_ping_interval=5,ws_ping_timeout=5)
