from aiohttp import web
from detection.detection_task import detect_cards
# from task_queue.celery import celery_app
import asyncio


class DetectionQueue:

    def __init__(self):
        pass

class DetectionHandler:

    def __init__(self):
        self._handler_routes = web.RouteTableDef()
        self._set_handlers()
    
    def _set_handlers(self):
        
        @self._handler_routes.post('/')
        async def handle_task(request:web.Request):
            try:
                print("connected !")
                res = detect_cards.delay(4)
                await asyncio.sleep(5)
                print(res.get())
            except asyncio.CancelledError as ex:
                print(ex)
                return web.HTTPInternalServerError()
            else:
                return web.Response(text="Hello you to")

    def get_handler_routes(self) -> web.RouteTableDef:
        return self._handler_routes


class DetectionServer:

    def __init__(self, host='localhost', port=8086):
        self._host = host
        self._port = port
        self._det_handler = DetectionHandler()
        self._app = web.Application() 
        self._set_routes()
    
    def _set_routes(self):
        self._app.add_routes(self._det_handler.get_handler_routes())
    
    def run(self):
        web.run_app(self._app, host=self._host, port=self._port)



if __name__ == "__main__":
    detection_server = DetectionServer()
    detection_server.run()



